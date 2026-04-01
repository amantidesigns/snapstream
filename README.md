# SnapStream

![SnapStream](social-preview.png)

Live TV in Picture-in-Picture, right from Raycast. Breaking news, live sports, or any channel — floating over your workspace in three keystrokes.

![Raycast](https://img.shields.io/badge/Raycast-Extension-FF6363)
![macOS](https://img.shields.io/badge/macOS-13%2B-000000)

## Why

When something major is happening in the world, you don't want to go hunt for an article or open a browser tab. You want to hit Cmd+Space, type three letters, and have CNN live in the corner of your screen while you keep working.

Same for sports — type "Wolves" and the game is floating over your code in Picture-in-Picture. Open as many streams as you want. They all float independently.

SnapStream is for people who spend long hours at their desk and want instant awareness of what's happening without breaking focus.

## How it works

1. Open Raycast and type **SnapStream**
2. Enter a search term (e.g., `CNN`, `BBC`, `Wolves`)
3. The best matching channel opens live in QuickTime Player
4. QuickTime automatically enters Picture-in-Picture — the stream floats over your work

No browser. No app switching. No tab management.

## Install

```bash
git clone https://github.com/amantidesigns/snapstream.git
cd snapstream
./install.sh
```

Then in Raycast:
1. Open **Raycast Settings** (Cmd+,)
2. Go to **Extensions** > **Script Commands**
3. Make sure `~/.raycast/scripts` is listed as a script directory

Type "SnapStream" in Raycast to start watching.

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

To extract `.m3u8` URLs from an M3U playlist file, open it in a text editor — each channel has a `#EXTINF:` metadata line followed by the stream URL on the next line.

### Converting an M3U playlist

If you have an `.m3u` or `.m3u8` playlist file, convert it to `channels.json`:

```bash
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

By default, SnapStream also fetches channels from a remote M3U playlist for live sports. You can change or disable this by editing the `PLAYLIST_URL` variable at the top of `stream-tv.py`:

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

SnapStream is currently a Raycast Script Command. The plan is to evolve it into a full Raycast Extension with:

- Interactive channel browser with search and categories
- Favorites and recently watched
- Multiple playlist sources
- Submission to the Raycast Extension Store

See the [milestones](../../milestones) for detailed plans.

## License

MIT
