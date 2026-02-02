from .core import System

class DistroManager:
    def list_distros(self):
        print("\n--- Available Distributions ---")
        # Hardcoded specific list as requested + Debian default
        distros = [
            "debian", "ubuntu", "archlinux", "alpine", "void", 
            "fedora", "manjaro", "opensuse"
        ]
        
        for i, d in enumerate(distros, 1):
            marker = " (Recommended)" if d == "debian" else ""
            print(f" {i}. {d:<12}{marker}")
        return distros

    def install(self, alias):
        print(f"\n[*] Installing {alias} via proot-distro...")
        System.run(["proot-distro", "install", alias])

    def setup_desktop_base(self, alias):
        print(f"\n[*] Installing XFCE4 Base in {alias}...")
        
        # Command mimics reference: update + install xfce4 stack
        pkgs = "xfce4 xfce4-terminal dbus-x11 pulseaudio pavucontrol xfce4-goodies"
        
        cmd = ""
        if alias in ["debian", "ubuntu"]:
            cmd = f"apt update && apt install -y {pkgs}"
        elif alias == "archlinux":
            cmd = f"pacman -Syu --noconfirm {pkgs}"
        else:
            print("[!] Automatic setup limited to Debian/Ubuntu/Arch.")
            return

        System.run(["proot-distro", "login", alias, "--", "bash", "-c", cmd])
        
        print("[*] Installing Termux PulseAudio...")
        System.run("pkg install -y pulseaudio", shell=True)

    def remove(self, alias):
        System.run(["proot-distro", "remove", alias])
