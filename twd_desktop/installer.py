import os
from .core import System

class StyleManager:
    # Repository constants from reference
    REPO_RAW = "https://raw.githubusercontent.com/sabamdarif/termux-desktop/setup-files/setup-files/xfce"
    
    # Mapping user friendly names to folder names in the reference repo
    STYLES = {
        "1": {"name": "Minimalist Setup 1", "folder": "look_2"}, # Mapped to look_2 based on description
        "2": {"name": "Modern Style",       "folder": "look_5"}, # Mapped to look_5
        "3": {"name": "Minimalist Setup 2", "folder": "look_6"}, # Mapped to look_6
    }

    def __init__(self, distro_alias):
        self.alias = distro_alias
        self.home = os.environ["HOME"]

    def install_dependencies(self, style_id):
        """Installs dependencies required by specific styles."""
        # Generic dependencies often used by these custom styles
        pkgs = "gtk2-engines-murrine gnome-themes-extra"
        System.run(["proot-distro", "login", self.alias, "--", "apt", "install", "-y", pkgs], show_cmd=True)

    def apply_style(self, style_key):
        if style_key not in self.STYLES:
            print("[!] Invalid style selection.")
            return

        style_data = self.STYLES[style_key]
        folder = style_data["folder"]
        
        print(f"\n[*] Applying: {style_data['name']} (Source: {folder})")
        
        # 1. Prepare Local Directories
        dirs = {
            "theme": os.path.join(self.home, ".themes"),
            "icon": os.path.join(self.home, ".icons"),
            "config": os.path.join(self.home, ".config"),
            "wall": os.path.join(os.environ["PREFIX"], "share/backgrounds")
        }
        for d in dirs.values():
            os.makedirs(d, exist_ok=True)

        # 2. Download and Extract Components
        components = ["theme", "icon", "config", "wallpaper"]
        
        for comp in components:
            url = f"{self.REPO_RAW}/{folder}/{comp}.tar.gz"
            tmp_file = os.path.join(self.home, f"tmp_{comp}.tar.gz")
            
            try:
                System.download_file(url, tmp_file)
                
                # Determine destination
                dest = dirs["wall"] if comp == "wallpaper" else dirs[comp]
                
                # Config often extracts into .config, handle separately if needed
                # The reference script extracts config directly into home or .config
                if comp == "config":
                    # Extract config relative to home usually, but we target .config safely
                    System.extract_tar(tmp_file, dirs["config"]) 
                else:
                    System.extract_tar(tmp_file, dest)
                
            except Exception as e:
                print(f"[!] Failed to fetch {comp}: {e}")
            finally:
                if os.path.exists(tmp_file):
                    os.remove(tmp_file)

        # 3. Update GTK Cache (Proot)
        print("[*] Updating GTK Icon Cache in Distro...")
        System.run(["proot-distro", "login", self.alias, "--", "gtk-update-icon-cache", "-f", "-t", "/usr/share/icons/hicolor"], show_cmd=False)
        
        print("[+] Style applied successfully.")

class AppStoreInstaller:
    @staticmethod
    def install():
        print("\n[*] Installing Termux-AppStore...")
        
        # URL from reference repo logic
        url = "https://raw.githubusercontent.com/sabamdarif/Termux-AppStore/refs/heads/src/appstore"
        dest = "appstore_installer"
        
        try:
            System.download_file(url, dest)
            System.run(f"chmod +x {dest}", shell=True)
            
            # Run installer
            print("[*] Running AppStore installer script...")
            System.run(f"./{dest} --install v0.5.4.1", shell=True)
            
            print("[+] Termux-AppStore installed.")
        except Exception as e:
            print(f"[!] AppStore installation failed: {e}")
        finally:
            if os.path.exists(dest):
                os.remove(dest)
