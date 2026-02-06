# Termux Linux Desktop (Debian Edition)

This tool turns your Android device into a functional Linux Desktop using Debian XFCE. It is designed to be extremely simple: one script handles the installation, configuration, and launching of the desktop.

## Features
- **One-Click Setup**: Automatically installs Debian, XFCE4, Firefox, and Audio drivers.
- **Smart Detection**: Skips installation if packages already exist.
- **Lightweight**: Uses Debian stable and XFCE for performance on mobile devices.
- **Browser Included**: Firefox ESR comes pre-installed.

## Requirements

### 1. Termux App
You must be running this inside the Termux app.

### 2. Termux:X11 App (Required for Display)
You must install the **Termux:X11** companion app (APK) to view the desktop.
- Download the artifact (APK) from the [Termux:X11 GitHub Actions](https://github.com/termux/termux-x11/actions).
- Install the APK on your Android device.

### Storage & Data Usage
Please ensure you have enough internet data and storage before running.

| Component | Download Size | Installed Size |
|-----------|---------------|----------------|
| Debian Core | ~200 MB | ~600 MB |
| XFCE4 & Firefox | ~500 MB | ~1.5 GB |
| **Total Recommended** | **~1 GB Data** | **~3 GB Storage** |

## How to Install & Use

1. Open Termux.
2. Clone this repository (or download the files):
   ```bash
   git clone https://github.com/TechWithout Drama/twd-desktop.git
   cd twd-desktop
