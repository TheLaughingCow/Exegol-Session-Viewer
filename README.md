 
# Exegol Session Viewer (ESV)

![image](https://github.com/user-attachments/assets/ff03d2c2-e9a9-40ad-bb45-44243ae4326a)

**ESV** is a minimal interface to explore, filter, and replay session logs generated inside Exegol containers.

It supports:
- Filtering by container name and date/time
- Playback via embedded Asciinema player
- Raw `.cast` extract and download
- Support for compressed `.asciinema.gz` files

---

## Features

- Automatic scan of Exegol workspace logs
- Grouping by container
- Time-based filtering
- Start/End offset for extracts
- Downloadable `.cast` files

---

## Installation
Oneliner :
```bash
git clone https://github.com/TheLaughingCow/Exegol-Session-Viewer.git && cd Exegol-Session-Viewer && bash install.sh
```
Git :
```bash
git clone https://github.com/TheLaughingCow/Exegol-Session-Viewer.git
cd Exegol-Session-Viewer
./install.sh
```

## Screenshoots:
![image](https://github.com/user-attachments/assets/6bb6c9af-14d0-49dd-9b9a-f393831b1536)
![image](https://github.com/user-attachments/assets/fdc4dabd-0294-4cf6-825c-bcd7c55126d8)


Then open your browser at: [http://localhost:5005](http://localhost:5005)
---

## ⚠️ Security Warning

**This tool is meant to be used locally only.**  
Do **not expose** the web interface to the internet or untrusted networks.

There is **no authentication or access control**, and exposing this service may lead to **serious security issues*.
---
 
## Requirements

- Python 3.8+
- Flask

Everything is handled automatically by the installer.

## TODO

- Export sessions to `.mp4`

---

## Credits

Made for [Exegol](https://exegol.com) with love <3
