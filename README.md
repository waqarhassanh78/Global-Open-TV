# 📺 Waqar Hassan Global Open TV (CLI Player)

A lightweight, fully open-source terminal-based IPTV player. This tool taps into the community-driven `iptv-org` database to stream thousands of live public television broadcasts directly through your command line using VLC media player.

## ✨ Features
- **Global IPTV Database:** Dynamically fetches and filters live channels from the `iptv-org` network.
- **VLC Integration:** Streams video in a detached window while maintaining terminal control, utilizing custom caching and auto-reconnect flags for unstable networks.
- **Cyberpunk UI:** Built with `rich` for a clean, secure terminal dashboard experience.
- **Cross-Platform:** Runs natively on Linux, Windows, and macOS.

## 🛠️ Prerequisites
- **Python 3.x**
- **VLC Media Player:** The script requires the system-level VLC engine to decode and display the video.
  - *Debian / Ubuntu / Kali Linux:* `sudo apt install vlc`
  - *Windows / macOS:* Download from [VideoLAN](https://www.videolan.org/)

## 🚀 Installation & Setup 

*(Note for Linux users: This setup utilizes a Virtual Environment to comply with PEP 668 restrictions.)*

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/waqarhassanh78/global-tv.git](https://github.com/waqarhassanh78/global-tv.git)
   cd global-tv ```
   Initialize the virtual environment:

```Bash
sudo apt install python3-venv -y
python3 -m venv venv
source venv/bin/activate
```
**Install the required dependencies:**

```Bash
pip install python-vlc rich requests
```
**🕹️ Usage**
Activate your environment and launch the terminal dashboard:

```Bash
source venv/bin/activate
python3 tv.py
```
**📜 Available Commands:**
search <keyword> : Scans the database (up to 70 results) for networks or countries (e.g., search news, search uk, search sports).

play <id> : Launches the video broadcast in a new VLC window.

stop : Terminates the current broadcast.

exit : Closes the interface securely.

Developed by Waqar Hassan | BS Cyber Security
