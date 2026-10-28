import json
import urllib.request

API_KEY = os.environ.get("STITCH_API_KEY", "")
MCP_URL = "https://stitch.googleapis.com/mcp"

payload = {
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/list"
}

req = urllib.request.Request(
    MCP_URL,
    data=json.dumps(payload).encode("utf-8"),
    headers={
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream",
        "X-Goog-Api-Key": API_KEY
    }
)

with urllib.request.urlopen(req) as resp:
    raw = resp.read().decode("utf-8")
    if raw.startswith("event:") or "data:" in raw:
        for line in raw.split("\n"):
            if line.startswith("data:"):
                res = json.loads(line[5:].strip())
                break
    else:
        res = json.loads(raw)

with open("stitch_output/tools.json", "w", encoding="utf-8") as f:
    json.dump(res, f, indent=2)

print("Tools schema saved to stitch_output/tools.json!")

