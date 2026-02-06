import os
import sys
import subprocess
import shutil
import time

# Configuration
DISTRO = "debian"
TERMUX_DEPS = ["proot-distro", "pulseaudio", "termux-x11-nightly"]
GUEST_DEPS = ["xfce4", "xfce4-goodies", "dbus-x11", "pulseaudio", "firefox-esr"]

class TWD:
    def __init__(self):
        self.prefix = os.environ.get("PREFIX", "")
        self.home = os.environ.get("HOME", "")
        
    def run(self, cmd, shell=True, check=True):
        """Runs a command and handles errors."""
        try:
            subprocess.run(cmd, shell=shell, check=check)
        except subprocess.CalledProcessError as e:
            print(f"Error executing: {cmd}")
            print(f"Details: {e}")
            sys.exit(1)

    def is_installed_termux(self, pkg_name):
        """Checks if a Termux package is installed."""
        try:
            # dpkg -s returns 0 if installed, 1 if not
            subprocess.check_output(f"dpkg -s {pkg_name}", shell=True, stderr=subprocess.DEVNULL)
            return True
        except subprocess.CalledProcessError:
            return False

    def check_android_app(self):
        """Checks if Termux:X11 Android app is installed."""
        try:
            output = subprocess.check_output("cmd package list packages com.termux.x11", shell=True, text=True)
            if "com.termux.x11" in output:
                return True
        except:
            pass
        return False

    def setup_termux_env(self):
        """Installs necessary packages on the Termux host."""
        print("[*] Checking Termux environment...")
        
        # 1. Update and enable repos
        if not self.is_installed_termux("x11-repo"):
            print(" -> Enabling X11 repository...")
            self.run("pkg update -y && pkg install -y x11-repo")
        
        # 2. Install dependencies
        to_install = []
        for pkg in TERMUX_DEPS:
            if not self.is_installed_termux(pkg):
                to_install.append(pkg)
        
        if to_install:
            print(f" -> Installing Termux packages: {', '.join(to_install)}")
            self.run(f"pkg install -y {' '.join(to_install)}")
        else:
            print(" -> Termux packages already installed.")

    def setup_distro(self):
        """Installs Debian via proot-distro."""
        print(f"[*] Checking {DISTRO} installation...")
        
        # Check if distro exists in proot-distro list
        installed_list = subprocess.check_output("proot-distro list --installed", shell=True, text=True)
        
        if DISTRO not in installed_list:
            print(f" -> Installing {DISTRO} (This requires internet)...")
            self.run(f"proot-distro install {DISTRO}")
        else:
            print(f" -> {DISTRO} is already installed.")

    def setup_guest_env(self):
        """Installs Desktop environment inside Debian."""
        print("[*] Checking Debian packages (XFCE4, Firefox)...")
        
        # Check if xfce4-session is already inside
        check_cmd = f"proot-distro login {DISTRO} -- command -v xfce4-session"
        try:
            subprocess.check_call(check_cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print(" -> XFCE4 and components appear to be installed.")
        except subprocess.CalledProcessError:
            print(" -> Installing XFCE4, Firefox, and Audio (This may take a while)...")
            
            install_cmd = (
                f"proot-distro login {DISTRO} -- bash -c '"
                "apt update && "
                f"apt install -y {' '.join(GUEST_DEPS)}"
                "'"
            )
            self.run(install_cmd)
            print(" -> Guest setup complete.")

    def start_desktop(self):
        # 1. Check for Android App
        if not self.check_android_app():
            print("\n[!] WARNING: 'Termux:X11' Android App not detected.")
            print("    Please install the APK from GitHub Actions or F-Droid.")
            input("    Press Enter to continue anyway (or Ctrl+C to exit)...")

        print("\n[*] Starting Desktop...")

        # 2. Cleanup previous sessions
        self.stop_desktop(silent=True)

        # 3. Start X11 Server (Termux side)
        print(" -> Starting X11 Server...")
        self.run("termux-x11 :0 -xstartup 'dbus-launch --exit-with-session xfce4-session' >/dev/null 2>&1 &", shell=True, check=False)
        
        # 4. Wait a moment
        time.sleep(1)

        # 5. Launch Android App
        print(" -> Launching App Display...")
        self.run("am start --user 0 -n com.termux.x11/com.termux.x11.MainActivity", shell=True, check=False)

        # 6. Login and Start XFCE (The xstartup arg in step 3 often handles it, but running proot keeps session alive)
        print(" -> Logging into Debian...")
        print("[*] Desktop is running. Check the Termux:X11 app.")
        print("[*] Press Ctrl+C here to stop the desktop.")
        
        try:
            # We run a shell to keep the script running and the session active
            cmd = (
                f"proot-distro login {DISTRO} --shared-tmp -- bash -c "
                "'export DISPLAY=:0; export PULSE_SERVER=127.0.0.1; "
                "dbus-launch --exit-with-session xfce4-session'"
            )
            subprocess.run(cmd, shell=True)
        except KeyboardInterrupt:
            self.stop_desktop()

    def stop_desktop(self, silent=False):
        if not silent:
            print("\n[*] Stopping services...")
        self.run("killall -9 termux-x11 pulseaudio 2>/dev/null || true", shell=True, check=False)
        self.run(f"pkill -f 'proot-distro login {DISTRO}' || true", shell=True, check=False)
        if not silent:
            print("[+] Desktop stopped.")

    def main_menu(self):
        while True:
            os.system("clear")
            print("========================================")
            print("     LINUX DESKTOP INSTALLER     ")
            print("========================================")
            print("1. Start Desktop (Auto-Install & Run)")
            print("2. Stop Desktop (Kill processes)")
            print("3. Exit")
            print("========================================")
            
            choice = input("Select option [1-3]: ").strip()
            
            if choice == "1":
                # Auto-setup run sequence
                self.setup_termux_env()
                self.setup_distro()
                self.setup_guest_env()
                self.start_desktop()
                input("\nPress Enter to return to menu...")
            elif choice == "2":
                self.stop_desktop()
                input("\nPress Enter to return to menu...")
            elif choice == "3":
                sys.exit(0)

if __name__ == "__main__":
    app = TWD()
    # If the user just runs the script, we show the menu.
    # The setup checks happen automatically when they select "Start".
    try:
        app.main_menu()
    except KeyboardInterrupt:
        print("\nExiting...")
