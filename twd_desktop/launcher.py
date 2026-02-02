import os
import time
import subprocess
from .core import System

class Launcher:
    def __init__(self, alias):
        self.alias = alias
        self.log_file = os.path.join(os.environ["HOME"], "twd_desktop.log")

    def start(self):
        print("\n[*] Initializing Desktop Session...")
        
        # Cleanup
        System.run("rm -rf $PREFIX/tmp/.X11-unix", shell=True, show_cmd=False)
        System.run("killall termux-x11 pulseaudio 2>/dev/null || true", shell=True, show_cmd=False)

        # Start Audio
        print("[*] Starting Audio Server...")
        audio_cmd = "pulseaudio --start --load='module-native-protocol-tcp auth-ip-acl=127.0.0.1 auth-anonymous=1' --exit-idle-time=-1"
        System.run(audio_cmd, shell=True, show_cmd=False)

        # Start X11
        print("[*] Starting X11 Server...")
        System.run("termux-x11 :0 >/dev/null &", shell=True)
        time.sleep(1)

        # Start Android App
        System.run("am start --user 0 -n com.termux.x11/com.termux.x11.MainActivity", shell=True)

        # Proot Command
        # This mirrors the startup command structure of the reference
        start_cmd = (
            "export DISPLAY=:0; "
            "export PULSE_SERVER=127.0.0.1; "
            "dbus-launch --exit-with-session startxfce4"
        )

        full_proot_cmd = [
            "proot-distro", "login", self.alias, "--shared-tmp", "--", "bash", "-c", start_cmd
        ]

        print(f"[*] Launching XFCE4 in background...")
        print(f"[*] Logs are being written to: {self.log_file}")
        
        # Launch in background, redirecting output to log file
        with open(self.log_file, "w") as log:
            subprocess.Popen(full_proot_cmd, stdout=log, stderr=log)

        print("[+] Desktop started successfully.")
        print("[*] You may now use this terminal for other commands.")
        print("[*] To view logs in real-time, run: tail -f ~/twd_desktop.log")

    def stop(self):
        print("\n[*] Stopping services...")
        System.run("killall termux-x11 pulseaudio 2>/dev/null || true", shell=True)
        System.run(f"pkill -f 'proot-distro login {self.alias}' || true", shell=True)
        print("[+] Desktop stopped.")
