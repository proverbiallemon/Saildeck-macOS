# Saildeck French to English Translations

This document lists all French strings that were translated to English during the macOS port.

## mod_manager.py

| French | English |
|--------|---------|
| Bascule l'état du mod entre activé/désactivé | Toggle mod state between enabled/disabled |
| Ignorer les autres fichiers | Ignore other files |
| Force l'état du mod (activé ou désactivé) selon `enable` | Force the mod state (enabled or disabled) based on `enable` |
| Remonte jusqu'au dossier "mods" | Traverse up to the "mods" folder |
| Active ou désactive tous les mods dans un dossier (récursivement) | Enable or disable all mods in a folder (recursively) |
| Le chemin spécifié n'est pas un dossier | The specified path is not a folder |
| Aucun mod trouvable à activer/désactiver dans ce dossier | No mods found to enable/disable in this folder |
| Déterminer si au moins un est désactivé | Determine if at least one is disabled |
| Si on veut activer tous les désactivés | If we want to enable all disabled mods |

## delete.py

| French | English |
|--------|---------|
| Supprime le mod ou dossier donné, avec confirmation | Delete the given mod or folder, with confirmation |
| fonction à appeler pour rafraîchir l'UI après suppression | function to call to refresh the UI after deletion |
| fonction pour mettre à jour le status | function to update the status |
| Le chemin n'existe pas | Path does not exist |
| Suppression annulée | Deletion cancelled |

## export_modpacks.py

| French | English |
|--------|---------|
| exe packagé | Packaged exe |
| mode script python | Python script mode |
| Trier les chemins relatifs complets (dossiers + fichiers) par ordre alphabétique | Sort relative paths (folders + files) alphabetically |
| Mise à jour status | Update status |
| Importé | Imported |
| Import terminé dans | Import complete in |
| Import réussi | Import successful |
| importé avec succès | imported successfully |

## save_modpacks.py

| French | English |
|--------|---------|
| Fonction pour obtenir le bon chemin (VSC ou exe PyInstaller) | Get the correct path (VSCode or PyInstaller exe) |
| dossier du .exe | Folder of the .exe |
| dossier du script | Folder of the script |

## launch.py

| French | English |
|--------|---------|
| Vérifie si l'utilisateur souhaite que AltAssets soit forcé | Check if the user wants AltAssets to be force-enabled |
| Aucun fichier de configuration trouvé, AltAssets activé par défaut | No config file found, AltAssets enabled by default |
| AltAssets auto-activation : activé/désactivé | AltAssets auto-activation: enabled/disabled |
| Erreur lors de la lecture de | Error reading |
| Retourne True si un .otr ou .o2r actif est trouvé n'importe où dans /mods | Return True if an active .otr or .o2r is found anywhere in /mods |
| Recherche récursive de mods actifs dans | Recursively searching for active mods in |
| Dossier des mods introuvable | Mods folder not found |
| Mod actif détecté | Active mod detected |
| Aucun fichier .otr ou .o2r actif détecté dans les sous-dossiers | No active .otr or .o2r files detected in subfolders |
| Active AltAssets dans CVars > gSettings uniquement | Enable AltAssets in CVars > gSettings only |
| Activation de AltAssets dans gSettings | Enabling AltAssets in gSettings |
| Fichier shipofharkinian.json introuvable | shipofharkinian.json not found |
| CVars > gSettings non trouvé | CVars > gSettings not found |
| AltAssets (gSettings) activé | AltAssets (gSettings) enabled |
| AltAssets (gSettings) est déjà activé | AltAssets (gSettings) is already enabled |
| Erreur lors de la mise à jour de AltAssets | Error updating AltAssets |

## utils.py

| French | English |
|--------|---------|
| Liste récursivement tous les fichiers | Recursively list all files |
| Charge un fichier JSON. Retourne `default` si erreur | Load a JSON file. Returns `default` on error |
| Écrit un dictionnaire dans un fichier JSON | Write a dictionary to a JSON file |
| SETTINGS.JSON SPECIFIQUES | SETTINGS FUNCTIONS |
| Charge les paramètres depuis 'settings.json' | Load settings from saildeck.data |
| Sauvegarde les paramètres dans 'settings.json' | Save settings to saildeck.data |
| Retourne le chemin du jeu depuis les paramètres (ou None si non défini) | Return the game path from settings (or None if not set) |
| Définit et sauvegarde le chemin du jeu dans les paramètres | Set and save the game path in settings |
| Crée le fichier saildeck.data s'il n'existe pas | Create saildeck.data file if it doesn't exist |

## about.py

| French | English |
|--------|---------|
| Rend la fenêtre modale | Make the window modal |
| Définir l'icône | Set the icon |
| Erreur chargement icon.ico | Error loading icon.ico |
| Logo Saildeck via Canvas (pas de fond parasite) | Saildeck logo via Canvas (no background artifacts) |
| Erreur chargement logo_name.png | Error loading logo_name.png |
| Texte centré | Centered text |
| Lien GitHub cliquable | Clickable GitHub link |
| Remerciement personnalisé | Custom thanks |
| Bouton Fermer | Close button |
| Logo Blepy en bas à droite | Blepy logo in bottom right |
| Petit format | Small size |
| éviter le garbage collector | Prevent garbage collection |
| Erreur chargement blepy_logo.png | Error loading blepy_logo.png |

## check_version.py

| French | English |
|--------|---------|
| Lance simplement le nouvel exécutable sans tenter de supprimer l'ancien | Simply launch the new executable without trying to delete the old one |

## gui.py

| French | English |
|--------|---------|
| Erreur chargement logo_small.png | Error loading logo_small.png |
| Erreur lors du rechargement du thème | Error reloading theme |
| Nom | Name |
| stop propagation de l'événement (évite comportement par défaut) | Stop event propagation (prevent default behavior) |
| Gestion des mods (provenant de GameBanana...) | Mod management (from GameBanana...) |
| Fonctionnalité en cours de développement | Feature under development |

## main.py

| French | English |
|--------|---------|
| Vérification de mise à jour (plus de parent/root) | Check for updates |
| Lecture du chemin du jeu | Read game path |
| Lancement de l'application principale | Launch main application |

## settings_window.py

| French | English |
|--------|---------|
| Impossible de charger l'icône | Unable to load icon |
