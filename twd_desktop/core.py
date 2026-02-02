import os
import sys
import subprocess
import shutil
import platform

class System:
    @staticmethod
    def check_environment():
        if "com.termux" not in os.environ.get("PREFIX", ""):
            print("[!] Error: This tool must run inside Termux.")
            sys.exit(1)
        
        if not shutil.which("proot-distro"):
            print("[!] Error: 'proot-distro' not found.")
            print("    Run: pkg install proot-distro")
            sys.exit(1)

    @staticmethod
    def get_arch():
        return platform.machine()

    @staticmethod
    def run(cmd, shell=False, check=True, show_cmd=True, capture=False):
        if show_cmd and not capture:
            cmd_str = cmd if isinstance(cmd, str) else " ".join(cmd)
            print(f"    [CMD] {cmd_str}")
        
        try:
            if capture:
                return subprocess.check_output(cmd, shell=shell, text=True).strip()
            return subprocess.run(cmd, shell=shell, check=check)
        except subprocess.CalledProcessError as e:
            if not capture:
                print(f"[!] Command failed: {e}")
            raise e

    @staticmethod
    def download_file(url, dest):
        print(f"[*] Downloading: {os.path.basename(dest)}")
        # Using curl for reliability in Termux
        cmd = f"curl -L -o {dest} {url}"
        subprocess.run(cmd, shell=True, check=True)

    @staticmethod
    def extract_tar(tar_path, dest_dir):
        print(f"[*] Extracting: {os.path.basename(tar_path)}")
        os.makedirs(dest_dir, exist_ok=True)
        # Handle various compression types via tar auto-detect
        cmd = f"tar -xf {tar_path} -C {dest_dir}"
        subprocess.run(cmd, shell=True, check=True)
