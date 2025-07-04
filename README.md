 
# Exegol Session Viewer (ESW)

![image](https://github.com/user-attachments/assets/ff03d2c2-e9a9-40ad-bb45-44243ae4326a)

**ESW** is a minimal interface to explore, filter, and replay session logs generated inside Exegol containers.

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

```bash
git clone https://github.com/yourname/exegol-replay.git
cd exegol-replay
./install.sh
```

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
