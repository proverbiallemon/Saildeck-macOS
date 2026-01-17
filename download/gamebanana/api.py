import requests

SOH_GAME_ID = "16121"
API_V11_BASE = "https://gamebanana.com/apiv11"
HEADERS = {"User-Agent": "Saildeck/1.0 (Ship of Harkinian Mod Manager)"}


def fetch_soh_mods(page=1, per_page=15, sort="new", search=None):
    """Fetch Ship of Harkinian mods from GameBanana V11 API.

    Args:
        page: Page number (1-indexed)
        per_page: Number of mods per page
        sort: Sort order - 'new', 'updated'
        search: Search string (optional)

    Returns:
        Tuple of (mods list, total count, has more pages)
    """
    try:
        if search:
            # Use search endpoint for search queries
            return _search_mods(search, page, per_page)
        else:
            # Use subfeed for browsing
            return _browse_mods(page, per_page, sort)

    except Exception as e:
        print(f"[API] Error fetching mods: {e}")
        return [], 0, False


def _browse_mods(page, per_page, sort):
    """Browse mods without search."""
    url = f"{API_V11_BASE}/Game/{SOH_GAME_ID}/Subfeed"
    params = {
        "_nPage": str(page),
        "_nPerpage": str(per_page),
        "_sSort": sort,
        "_aFilters[Generic_Category]": "Mod"
    }

    response = requests.get(url, params=params, headers=HEADERS, timeout=15)
    response.raise_for_status()
    data = response.json()

    metadata = data.get("_aMetadata", {})
    total_count = metadata.get("_nRecordCount", 0)
    is_complete = metadata.get("_bIsComplete", True)

    mods = []
    for record in data.get("_aRecords", []):
        mod = _parse_mod_record(record)
        mods.append(mod)

    return mods, total_count, not is_complete


def _search_mods(search_term, page, per_page):
    """Search mods by term."""
    url = f"{API_V11_BASE}/Util/Search/Results"
    params = {
        "_sSearchString": search_term,
        "_nPage": str(page),
        "_nPerpage": str(per_page),
        "_idGameRow": SOH_GAME_ID
    }

    response = requests.get(url, params=params, headers=HEADERS, timeout=15)
    response.raise_for_status()
    data = response.json()

    metadata = data.get("_aMetadata", {})
    total_count = metadata.get("_nRecordCount", 0)
    is_complete = metadata.get("_bIsComplete", True)

    mods = []
    for record in data.get("_aRecords", []):
        # Search results have same structure as browse
        mod = _parse_mod_record(record)
        mods.append(mod)

    return mods, total_count, not is_complete


def _parse_mod_record(record):
    """Parse a mod record from the V11 API response."""
    mod_id = record.get("_idRow")

    # Get preview image
    image_url = None
    preview_media = record.get("_aPreviewMedia", {})
    images = preview_media.get("_aImages", [])
    if images:
        img = images[0]
        base_url = img.get("_sBaseUrl", "")
        file_220 = img.get("_sFile220", "")
        if base_url and file_220:
            image_url = f"{base_url}/{file_220}"

    # Get submitter/author
    submitter = record.get("_aSubmitter", {})
    author = submitter.get("_sName", "Unknown")

    # Get category
    category = record.get("_aRootCategory", {})
    category_name = category.get("_sName", "Unknown")

    return {
        "mod_id": mod_id,
        "name": record.get("_sName", f"Mod #{mod_id}"),
        "author": author,
        "image_url": image_url,
        "category": category_name,
        "view_count": record.get("_nViewCount", 0),
        "like_count": record.get("_nLikeCount", 0),
        "url": record.get("_sProfileUrl", f"https://gamebanana.com/mods/{mod_id}"),
        "date_added": record.get("_tsDateAdded"),
        "date_updated": record.get("_tsDateUpdated"),
        "has_files": record.get("_bHasFiles", False),
        "files": []  # Files loaded on-demand when downloading
    }


def get_mod_files(mod_id):
    """Fetch download files for a specific mod.

    Args:
        mod_id: The GameBanana mod ID

    Returns:
        List of file dicts with download info
    """
    try:
        url = f"{API_V11_BASE}/Mod/{mod_id}/Files"
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        data = response.json()

        files = []
        if isinstance(data, list):
            for file_info in data:
                files.append({
                    "file_id": file_info.get("_idRow"),
                    "filename": file_info.get("_sFile", ""),
                    "filesize": file_info.get("_nFilesize", 0),
                    "download_url": file_info.get("_sDownloadUrl", ""),
                    "download_count": file_info.get("_nDownloadCount", 0),
                    "md5": file_info.get("_sMd5Checksum", ""),
                    "analysis_result": file_info.get("_sAnalysisResult", ""),
                })

        return files

    except Exception as e:
        print(f"[API] Error fetching files for mod {mod_id}: {e}")
        return []
