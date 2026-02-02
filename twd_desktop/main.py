import sys
import os
from .core import System
from .distro import DistroManager
from .installer import StyleManager, AppStoreInstaller
from .launcher import Launcher

def menu():
    print("\n------------------------------")
    print("         TWD-DESKTOP          ")
    print("------------------------------")
    print("1. Install Distro & Desktop")
    print("2. Apply Style (Theme/Icons)")
    print("3. Start Desktop")
    print("4. Stop Desktop")
    print("5. Install Termux-AppStore")
    print("6. Uninstall Distro")
    print("0. Exit")
    return input("\nOption: ").strip()

def main():
    System.check_environment()
    dm = DistroManager()
    
    # State file
    cfg = os.path.expanduser("~/.twd_config")
    distro = "debian" # Default
    if os.path.exists(cfg):
        with open(cfg) as f: distro = f.read().strip()

    while True:
        opt = menu()
        
        if opt == "1":
            d_list = dm.list_distros()
            try:
                idx = int(input("\nSelect distro number: ")) - 1
                distro = d_list[idx]
                
                dm.install(distro)
                if input("Install XFCE4? [y/N]: ").lower() == "y":
                    dm.setup_desktop_base(distro)
                
                # Save selection
                with open(cfg, "w") as f: f.write(distro)
            except (ValueError, IndexError):
                print("[!] Invalid selection.")

        elif opt == "2":
            print("\nSelect Style (fetches from repository):")
            print("1. Minimalist Setup 1 (Arc/Papirus)")
            print("2. Modern Style (Greybird/Elementary)")
            print("3. Minimalist Setup 2 (Adwaita)")
            
            sid = input("Selection: ")
            sm = StyleManager(distro)
            sm.install_dependencies(sid) # Apt installs
            sm.apply_style(sid)          # Asset downloads

        elif opt == "3":
            Launcher(distro).start()

        elif opt == "4":
            Launcher(distro).stop()

        elif opt == "5":
            AppStoreInstaller.install()

        elif opt == "6":
            if input(f"Delete {distro}? [y/N]: ").lower() == "y":
                dm.remove(distro)

        elif opt == "0":
            sys.exit(0)

if __name__ == "__main__":
    main()
