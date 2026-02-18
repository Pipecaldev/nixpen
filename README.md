# NixPen

NixPen is a free and open-source screen annotation tool built specifically for Linux desktops.

It allows you to draw, highlight and annotate directly over your screen with a lightweight and distraction-free experience.

## ✨ Features

*   **✏️ Freehand drawing (Pen)**
*   **🧹 Eraser**
*   **� Geometric shapes (Line, Arrow, Rectangle, Ellipse)**
*   **📝 Text tool**
*   **🔦 Spotlight mode**
*   **⬜ Whiteboard (White / Black background)**
*   **↩ Undo / Redo system**
*   **🎨 Quick color switching**
*   **📏 Adjustable brush size**
*   **⌨ Full keyboard shortcut support**
*   **� Toggle drawing mode instantly**

## 🎯 Philosophy

NixPen was created to provide a modern, lightweight and reliable screen annotation experience for Linux.

While similar tools exist on other platforms, Linux lacked a simple, polished and actively maintained alternative focused on speed and usability.

NixPen aims to be:
*   Minimal
*   Fast
*   Stable
*   Focused
*   Native to the Linux ecosystem

## � Compatibility

NixPen works on modern Linux distributions including:
*   Ubuntu / Debian-based systems
*   Fedora / RHEL-based systems
*   Arch-based systems
*   KDE Plasma
*   GNOME
*   X11
*   Wayland (via XWayland compatibility layer)

## 📦 Installation (AppImage)

The easiest way to run NixPen on most Linux distributions.

1.  **Download** the latest `NixPen-x86_64.AppImage` from the [Releases](https://github.com/Pipecaldev/nixpen/releases) page.
2.  **Make it executable**:
    ```bash
    chmod +x NixPen-x86_64.AppImage
    ```
3.  **Run**:
    ```bash
    ./NixPen-x86_64.AppImage
    ```

### Optional: System Integration
For better desktop integration (application menu, icons, auto-updates), we recommend using **[AppImageLauncher](https://github.com/TheAssassin/AppImageLauncher)**. It will automatically detect and integrate your AppImages.

Alternatively, you can use our built-in script to integrate manually:
1.  Download `install_system.sh` from the repository (or extract from source).
2.  Make sure `NixPen-x86_64.AppImage` is in the same folder.
3.  Run:
    ```bash
    chmod +x install_system.sh
    ./install_system.sh
    ```
    This will move the AppImage to `~/Applications/`, create a desktop entry, and install the icon.

### Flatpak (Coming Soon)
### Arch (AUR) (Planned)

## ⌨ Keyboard Shortcuts

Full shortcut list available inside the app:
**Help → Keyboard Shortcuts**


## 🎛 Configuring NixPen with OpenDeck (Linux / X11)

NixPen can be integrated with OpenDeck (Stream Deck on Linux) using `xdotool` to send keyboard shortcuts directly to the application window.

This setup allows full control of tools, colors, and actions without requiring the window to be manually focused.

### 📦 Requirements

Install `xdotool`:

```bash
sudo apt install xdotool
```

### ⚙️ OpenDeck Setup

Inside OpenDeck:
1.  Select the desired button.
2.  Add the **Run Command** action.
3.  Copy and paste the corresponding command from the tables below.

> All commands activate the NixPen window before sending the shortcut.

### 🛠 Tools (Ctrl + Shift)

| Action | Shortcut | Command |
| :--- | :--- | :--- |
| **Pencil** | `Ctrl+Shift+P` | `bash -lc 'xdotool search --onlyvisible --class "NixPen" windowactivate --sync key ctrl+shift+p'` |
| **Eraser** | `Ctrl+Shift+E` | `bash -lc 'xdotool search --onlyvisible --class "NixPen" windowactivate --sync key ctrl+shift+e'` |
| **Line** | `Ctrl+Shift+L` | `bash -lc 'xdotool search --onlyvisible --class "NixPen" windowactivate --sync key ctrl+shift+l'` |
| **Arrow** | `Ctrl+Shift+A` | `bash -lc 'xdotool search --onlyvisible --class "NixPen" windowactivate --sync key ctrl+shift+a'` |
| **Rectangle** | `Ctrl+Shift+R` | `bash -lc 'xdotool search --onlyvisible --class "NixPen" windowactivate --sync key ctrl+shift+r'` |
| **Ellipse** | `Ctrl+Shift+M` | `bash -lc 'xdotool search --onlyvisible --class "NixPen" windowactivate --sync key ctrl+shift+m'` |
| **Text** | `Ctrl+Shift+T` | `bash -lc 'xdotool search --onlyvisible --class "NixPen" windowactivate --sync key ctrl+shift+t'` |
| **Focus** | `Ctrl+Shift+S` | `bash -lc 'xdotool search --onlyvisible --class "NixPen" windowactivate --sync key ctrl+shift+s'` |

### 🎮 Control

| Action | Shortcut | Command |
| :--- | :--- | :--- |
| **Toggle Drawing** | `Ctrl+Shift+D` | `bash -lc 'xdotool search --onlyvisible --class "NixPen" windowactivate --sync key ctrl+shift+d'` |
| **Clear Screen** | `Ctrl+Shift+C` | `bash -lc 'xdotool search --onlyvisible --class "NixPen" windowactivate --sync key ctrl+shift+c'` |
| **Whiteboard** | `Ctrl+Shift+W` | `bash -lc 'xdotool search --onlyvisible --class "NixPen" windowactivate --sync key ctrl+shift+w'` |
| **Blackboard** | `Ctrl+Shift+B` | `bash -lc 'xdotool search --onlyvisible --class "NixPen" windowactivate --sync key ctrl+shift+b'` |
| **Show Help** | `Ctrl+Shift+H` | `bash -lc 'xdotool search --onlyvisible --class "NixPen" windowactivate --sync key ctrl+shift+h'` |

### ↩ Actions

| Action | Shortcut | Command |
| :--- | :--- | :--- |
| **Undo** | `Ctrl+Z` | `bash -lc 'xdotool search --onlyvisible --class "NixPen" windowactivate --sync key ctrl+z'` |
| **Redo** | `Ctrl+Y` | `bash -lc 'xdotool search --onlyvisible --class "NixPen" windowactivate --sync key ctrl+y'` |

### 🎨 Colors (Stable Implementation)

For colors, explicit keydown/keyup is used to avoid modifier state conflicts.

| Color | Shortcut | Command |
| :--- | :--- | :--- |
| **Red** | `Ctrl+1` | `bash -lc 'xdotool search --onlyvisible --class "NixPen" windowactivate --sync keydown ctrl key 1 keyup ctrl'` |
| **Blue** | `Ctrl+2` | `bash -lc 'xdotool search --onlyvisible --class "NixPen" windowactivate --sync keydown ctrl key 2 keyup ctrl'` |
| **Green** | `Ctrl+3` | `bash -lc 'xdotool search --onlyvisible --class "NixPen" windowactivate --sync keydown ctrl key 3 keyup ctrl'` |
| **Yellow** | `Ctrl+4` | `bash -lc 'xdotool search --onlyvisible --class "NixPen" windowactivate --sync keydown ctrl key 4 keyup ctrl'` |
| **Black** | `Ctrl+5` | `bash -lc 'xdotool search --onlyvisible --class "NixPen" windowactivate --sync keydown ctrl key 5 keyup ctrl'` |
| **White** | `Ctrl+6` | `bash -lc 'xdotool search --onlyvisible --class "NixPen" windowactivate --sync keydown ctrl key 6 keyup ctrl'` |
| **Orange** | `Ctrl+7` | `bash -lc 'xdotool search --onlyvisible --class "NixPen" windowactivate --sync keydown ctrl key 7 keyup ctrl'` |
| **Purple** | `Ctrl+8` | `bash -lc 'xdotool search --onlyvisible --class "NixPen" windowactivate --sync keydown ctrl key 8 keyup ctrl'` |

### 🧠 Technical Notes

*   This integration is designed for **X11** environments.
*   **Wayland** may restrict keyboard injection.
*   `--sync` ensures the window receives focus before sending input.
*   Explicit `keydown/keyup` prevents modifier state conflicts.

## 🛣 Roadmap

*   Improve Wayland behavior
*   Performance optimizations
*   UI refinements
*   Packaging for more distributions
*   Localization support

## 🤝 Contributing

Contributions are welcome.

You can help by:
*   Reporting bugs
*   Suggesting improvements
*   Submitting pull requests
*   Improving documentation

Please open an issue before large feature proposals.

## � License

NixPen is licensed under the **GNU General Public License v3 (GPLv3)**.

You are free to use, modify and distribute this software under the terms of the license.

## 👤 Maintainer

Maintained by
**Felipe Calderón**
GitHub: [https://github.com/Pipecaldev](https://github.com/Pipecaldev)

NixPen is currently maintained by a single developer.
Community contributions are encouraged.

## 💛 Support

If you find NixPen useful, you may support development through donations (optional).
