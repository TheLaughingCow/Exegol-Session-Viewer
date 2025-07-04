#!/usr/bin/env python3
import os
import sys
import subprocess
import tempfile
import shutil
import gzip
import json
import re
from flask import Flask, render_template_string, request, send_file, send_from_directory
from glob import glob
from datetime import datetime
from collections import defaultdict

venv_path = os.path.expanduser("~/.venv/exegol-replay")
expected_python = os.path.join(venv_path, "bin", "python3")

if sys.executable != expected_python and not os.environ.get("IN_VENV"):
    if not os.path.exists(venv_path):
        print("[+] Creating virtual environment for Exegol Replay...")
        subprocess.check_call([sys.executable, "-m", "venv", venv_path])
        subprocess.check_call([os.path.join(venv_path, "bin", "pip"), "install", "flask"])
    os.environ["IN_VENV"] = "1"
    os.execv(expected_python, [expected_python] + sys.argv)

app = Flask(__name__, static_folder='.')

ANSI_ESCAPE = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')

@app.route("/logo.png")
def logo():
    return send_from_directory('.', 'logo.png')

@app.route("/")
def index():
    base = os.path.expanduser("~/.exegol/workspaces")
    selected = request.args.get("container")
    start = request.args.get("start")
    end = request.args.get("end")
    files, containers = [], set()
    for path in glob(base + "/*/logs/*.asciinema*"):
        container = path.split(os.sep)[-3]
        containers.add(container)
        try:
            open_func = gzip.open if path.endswith(".gz") else open
            with open_func(path, 'rt', errors='ignore') as f:
                line = f.readline()
                header = json.loads(line) if line.startswith('{') else {}
                ts = header.get('timestamp', os.path.getmtime(path))
        except:
            ts = os.path.getmtime(path)
        files.append((container, datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S'), path))
    containers = sorted(containers)
    result = []
    if start and end:
        dt_start = datetime.fromisoformat(start)
        dt_end = datetime.fromisoformat(end)
        for c, dts, p in files:
            dt = datetime.strptime(dts, '%Y-%m-%d %H:%M:%S')
            if (not selected or c == selected) and dt_start <= dt <= dt_end:
                result.append((c, dts, p))
    else:
        result = files if not selected else [f for f in files if f[0] == selected]
    grouped = defaultdict(list)
    for c, d, p in sorted(result, key=lambda x: (x[0], x[1]), reverse=True):
        grouped[c].append((d, p))
    return render_template_string("""
<!doctype html><html><head>
<title>Exegol Sessions Viewer</title>
<style>
  body { font-family: sans-serif; background: #111; color: #eee; padding: 20px; }
  .logo { text-align: center; margin-bottom: 10px; }
  .logo img { height: 80px; }
  .content { max-width: 960px; margin: auto; }
  h2 { text-align: center; }
  form { display: flex; justify-content: center; flex-wrap: wrap; gap: 10px; margin-bottom: 20px; }
  select, input, button { padding: 6px; border-radius: 5px; border: none; }
  .container-group { background: #222; margin-bottom: 20px; border-radius: 8px; box-shadow: 0 0 8px #333; }
  .container-title { background: #333; padding: 10px; font-weight: bold; }
  table { width: 100%; border-collapse: collapse; }
  th, td { padding: 8px; border-bottom: 1px solid #444; }
  .view-cell { text-align: right; white-space: nowrap; }
  a.view-link, a.download-link { background: #0099cc; color: #fff; padding: 6px 10px; border-radius: 5px; text-decoration: none; margin-left: 5px; }
  a.view-link:hover, a.download-link:hover { background: #0077aa; }
  footer { text-align: center; margin-top: 40px; font-size: 0.9em; color: #777; }
  footer a { color: #aaa; text-decoration: none; font-weight: bold; }
</style></head><body>
<div class="logo"><a href="https://github.com/Frozenka/Exegol-Session-Viewer" target="_blank"><img src="/logo.png" alt="logo"></a></div>
<div class="content">
<form method="get">
  <label>Container:
    <select name="container">
      <option value="">All</option>
      {% for c in containers %}
        <option value="{{c}}" {% if c==selected %}selected{% endif %}>{{c}}</option>
      {% endfor %}
    </select>
  </label>
  <label>Start:
    <input type="datetime-local" name="start" value="{{start or ''}}">
  </label>
  <label>End:
    <input type="datetime-local" name="end" value="{{end or ''}}">
  </label>
  <button type="submit">Search</button>
</form>

{% for container, sessions in grouped.items() %}
<div class="container-group">
  <div class="container-title">{{ container }}</div>
  <table>
    <tr><th>Date</th><th class="view-cell">Action</th></tr>
    {% for date, path in sessions %}
    <tr>
      <td>{{ date }}</td>
      <td class="view-cell">
        <a class="view-link" href="/view?file={{ path }}">▶ View</a>
        <a class="download-link" href="/view?file={{ path }}&download=1">⬇ Download</a>
      </td>
    </tr>
    {% endfor %}
  </table>
</div>
{% endfor %}
<footer>Made for <a href="https://exegol.com" target="_blank">Exegol</a> with ❤️</footer>
</div></body></html>""", grouped=grouped, containers=containers, selected=selected, start=start, end=end)

@app.route("/view")
def view():
    path = request.args.get("file")
    download_only = request.args.get("download")
    cast_path = convert_to_cast(path)
    container = path.split("/")[-3]
    cast_name = os.path.basename(cast_path)
    if download_only:
        return send_file(cast_path, as_attachment=True, download_name=cast_name)
    title = f"Replay {container} from " + os.path.basename(path).split("_shell")[0].replace("_", " ")
    return f"""<!doctype html><html><head>
<title>Replay</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/asciinema-player@3.0.1/dist/bundle/asciinema-player.css" />
</head><body style="font-family:sans-serif;background:#111;color:#eee;text-align:center">
<div class="logo" style="margin:15px;"><a href="https://github.com/Frozenka/Exegol-Session-Viewer" target="_blank"><img src="/logo.png" style="height:80px;"></a></div>
<h2>{title}</h2>
<div id="player" style="width:80%;max-width:960px;margin:auto;"></div>
<div style="margin-top:1em;">
  <label>Start (s): <input id="start" type="number" step="0.1" style="width:80px;"></label>
  <label>End (s): <input id="end" type="number" step="0.1" style="width:80px;"></label>
  <button onclick="downloadExtract()">🎯 Download extract</button>
</div>
<script src="https://cdn.jsdelivr.net/npm/asciinema-player@3.0.1/dist/bundle/asciinema-player.min.js"></script>
<script>
AsciinemaPlayer.create("/raw?file={cast_path}", document.getElementById("player"), {{
  cols: 100, rows: 30, autoplay: true, preload: true, theme: "asciinema"
}});
function downloadExtract() {{
  const s = document.getElementById('start').value;
  const e = document.getElementById('end').value;
  let url = `/extract?file={cast_path}`;
  if (s && e && parseFloat(e) > parseFloat(s)) {{
    url += `&start=${{s}}&end=${{e}}`;
  }}
  alert(`🎉 The cast file will be downloaded after clicking OK.\\n\\nTo replay it:\\n\\nasciinema play ./` + "{cast_name}" + `\\n\\nMake sure asciinema is installed. This is a .cast recording file.`);
  window.open(url);
}}
</script>
<footer style="margin-top:30px;font-size:0.9em;color:#777;">Made for <a href="https://exegol.com" target="_blank" style="color:#aaa;font-weight:bold;">Exegol</a> with ❤️</footer>
</body></html>"""

@app.route("/raw")
def raw():
    return send_file(request.args.get("file"), mimetype="application/json")

@app.route("/extract")
def extract():
    path = request.args.get("file")
    start = float(request.args.get("start", "0"))
    end = float(request.args.get("end", "999999"))
    with open(path) as f:
        lines = f.readlines()
    header = lines[0]
    body = [json.loads(l) for l in lines[1:] if l.strip() and l.startswith("[")]
    filtered = [e for e in body if start <= e[0] <= end]
    outname = os.path.basename(path).replace(".asciinema.gz", ".cast").replace(".asciinema", ".cast")
    outpath = os.path.join(tempfile.gettempdir(), outname)
    with open(outpath, 'w') as w:
        w.write(header)
        for line in filtered:
            w.write(json.dumps(line) + "\n")
    return send_file(outpath, as_attachment=True, download_name=outname)

def convert_to_cast(path):
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".cast", mode="w", encoding="utf-8")
    opener = gzip.open if path.endswith(".gz") else open
    with opener(path, 'rt', encoding='utf-8', errors='ignore') as f_in:
        lines = f_in.readlines()
    header = {
        "version": 2,
        "width": 100,
        "height": 30,
        "timestamp": int(os.path.getmtime(path)),
        "env": {"TERM": "xterm", "SHELL": "/bin/bash"}
    }
    try:
        maybe_header = json.loads(lines[0])
        if isinstance(maybe_header, dict) and "version" in maybe_header:
            header.update(maybe_header)
            lines = lines[1:]
    except:
        pass
    tmp.write(json.dumps(header) + "\n")
    for line in lines:
        if line.strip().startswith("["):
            try:
                evt = json.loads(line)
                if isinstance(evt, list) and evt[1] == "o":
                    clean_output = ANSI_ESCAPE.sub('', evt[2])
                    if clean_output.strip():
                        tmp.write(json.dumps([evt[0], "o", clean_output]) + "\n")
            except:
                continue
    tmp.close()
    return tmp.name

if __name__ == "__main__":
    app.run(debug=True, port=5005)
