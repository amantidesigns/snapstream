# Stream TV for Raycast

A Raycast script command that lets you search and watch live TV channels directly from your Mac. Type a channel name, hit Enter, and it opens in QuickTime Player — no app switching, no browser tabs.

![Raycast](https://img.shields.io/badge/Raycast-Script%20Command-FF6363)
![macOS](https://img.shields.io/badge/macOS-13%2B-000000)
![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB)

## How it works

1. Open Raycast and type **Stream TV**
2. Enter a search term (e.g., `CNN`, `BBC`, `NBA`)
3. The best matching channel opens live in QuickTime Player
4. Open as many channels as you want simultaneously

The script searches your local channel list (`channels.json`) and optionally pulls from a remote M3U playlist for live sports and additional channels.

## Install

```bash
git clone https://github.com/amelkamu/raycast-stream-tv.git
cd raycast-stream-tv
./install.sh
```

Then in Raycast:
1. Open **Raycast Settings** (Cmd+,)
2. Go to **Extensions** > **Script Commands**
3. Make sure `~/.raycast/scripts` is listed as a script directory

That's it. Type "Stream TV" in Raycast to start.

## Add your own channels

Your channels live in `~/.raycast/scripts/channels.json`. Edit this file to add, remove, or change channels.

Each channel is a JSON object with three fields:

```json
{
  "name": "Channel Name",
  "group": "Category",
  "url": "https://example.com/stream.m3u8"
}
```

| Field   | Description                                      |
|---------|--------------------------------------------------|
| `name`  | What you search for (e.g., "BBC News", "ESPN")   |
| `group` | Category for organization (e.g., "News", "Sports") |
| `url`   | Direct HLS stream URL (`.m3u8`)                  |

### Example: adding a channel

```json
[
  {
    "name": "France 24 English",
    "group": "News",
    "url": "https://stream.france24.com/f24_en/smil:f24_en.smil/playlist.m3u8"
  }
]
```

## Where to find channels

You need `.m3u8` stream URLs. Here are some places to find them:

| Source | What's there | Link |
|--------|-------------|------|
| **iptv-org/iptv** | 8,000+ channels organized by country/category | [github.com/iptv-org/iptv](https://github.com/iptv-org/iptv) |
| **Free-TV/IPTV** | Curated free legal streams | [github.com/Free-TV/IPTV](https://github.com/Free-TV/IPTV) |
| **Pluto TV** | Free ad-supported channels (US) | [pluto.tv](https://pluto.tv) |
| **TVPASS** | Live sports and TV streams | [tvpass.org](https://tvpass.org) |

To extract `.m3u8` URLs from an M3U playlist file, open it in a text editor -- each channel has a `#EXTINF:` metadata line followed by the stream URL on the next line.

### Using an M3U playlist file directly

If you have an `.m3u` or `.m3u8` playlist file, you can convert it to `channels.json` format:

```bash
# Quick conversion (requires python3)
python3 -c "
import re, json, sys
channels = []
with open(sys.argv[1]) as f:
    lines = f.read().strip().split('\n')
i = 0
while i < len(lines):
    if lines[i].startswith('#EXTINF:'):
        g = re.search(r'group-title=\"([^\"]*)\"', lines[i])
        n = re.search(r',(.+)$', lines[i])
        if i+1 < len(lines) and not lines[i+1].startswith('#'):
            channels.append({'name': n.group(1) if n else 'Unknown', 'group': g.group(1) if g else 'Other', 'url': lines[i+1].strip()})
            i += 2; continue
    i += 1
print(json.dumps(channels, indent=2))
" your-playlist.m3u > channels.json
```

## Remote playlist

By default, the script also fetches channels from a remote M3U playlist (currently [tvpass.org](https://tvpass.org)) for live sports. You can change or disable this by editing the `PLAYLIST_URL` variable at the top of `stream-tv.py`:

```python
# Change to your preferred playlist
PLAYLIST_URL = "https://your-playlist-url.com/playlist.m3u"

# Or disable remote fetching entirely
PLAYLIST_URL = ""
```

## Configuration

All configuration is at the top of `stream-tv.py`:

| Variable | Default | Description |
|----------|---------|-------------|
| `PLAYLIST_URL` | `https://tvpass.org/playlist/m3u` | Remote M3U playlist URL (set to `""` to disable) |
| `SPORTS_LEAGUES` | NBA, NFL, NHL, etc. | League names that get priority in search results |

## Requirements

- macOS 13+
- Python 3.9+ (included with macOS)
- [Raycast](https://raycast.com)
- QuickTime Player (included with macOS)

## Roadmap

This is currently a Raycast Script Command. The plan is to evolve it into a full Raycast Extension with:

- Interactive channel browser with search and categories
- User preferences (choose your player, configure playlists in Raycast settings)
- Favorites and recently watched
- Submission to the Raycast Extension Store

See the [GitHub milestones](../../milestones) for detailed plans.

## License

MIT
