#!/usr/bin/env python3

# Required parameters:
# @raycast.schemaVersion 1
# @raycast.title Stream TV
# @raycast.mode compact
# @raycast.packageName Live TV Streams
# @raycast.icon 📺

# Optional parameters:
# @raycast.argument1 { "type": "text", "placeholder": "Search (e.g., CNN, BBC, NBA)", "optional": true }

# Documentation:
# @raycast.description Find and play live TV streams in QuickTime Player
# @raycast.author amelkamu

import sys
import os
import json
import urllib.request
import re
import subprocess
from typing import List, Dict, Tuple

# --- Configuration ---

# Remote M3U playlist URL (set to "" to disable)
PLAYLIST_URL = "https://tvpass.org/playlist/m3u"

# Sports leagues to prioritize in search results
SPORTS_LEAGUES = ["NBA", "NFL", "NHL", "NCAAF", "NCAAB", "MLB", "MLS", "UFC"]

# --- End Configuration ---

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CHANNELS_FILE = os.path.join(SCRIPT_DIR, "channels.json")


def load_custom_channels() -> List[Dict[str, str]]:
    """Load channels from channels.json."""
    if not os.path.exists(CHANNELS_FILE):
        return []
    try:
        with open(CHANNELS_FILE, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(f"Warning: Could not load {CHANNELS_FILE}: {e}")
        return []


def fetch_playlist() -> str:
    """Fetch the M3U playlist from the URL."""
    if not PLAYLIST_URL:
        return ""
    try:
        with urllib.request.urlopen(PLAYLIST_URL, timeout=10) as response:
            return response.read().decode('utf-8')
    except Exception as e:
        print(f"Warning: Could not fetch remote playlist: {e}")
        return ""


def parse_m3u(content: str) -> List[Dict[str, str]]:
    """Parse M3U playlist and extract channel information."""
    channels = []
    if not content:
        return channels

    lines = content.strip().split('\n')

    i = 0
    while i < len(lines):
        if lines[i].startswith('#EXTINF:'):
            metadata = lines[i]

            group_match = re.search(r'group-title="([^"]*)"', metadata)
            group = group_match.group(1) if group_match else "Other"

            name_match = re.search(r',(.+)$', metadata)
            name = name_match.group(1) if name_match else "Unknown"

            if i + 1 < len(lines) and not lines[i + 1].startswith('#'):
                url = lines[i + 1].strip()
                channels.append({
                    'name': name,
                    'group': group,
                    'url': url
                })
                i += 2
            else:
                i += 1
        else:
            i += 1

    return channels


def rank_channels(channels: List[Dict[str, str]], search_term: str = "") -> List[Tuple[Dict[str, str], int]]:
    """Rank channels based on sports priority and search term match."""
    ranked = []
    search_lower = search_term.lower()

    for channel in channels:
        score = 0
        name_lower = channel['name'].lower()
        group_lower = channel['group'].lower()

        if search_lower:
            if search_lower in name_lower:
                score += 1000
                if name_lower.startswith(search_lower):
                    score += 500
            if search_lower in group_lower:
                score += 800

        if channel['group'] in SPORTS_LEAGUES:
            score += 100
            if search_lower and group_lower == search_lower:
                score += 500

        if score > 0 or not search_term:
            ranked.append((channel, score))

    ranked.sort(key=lambda x: x[1], reverse=True)
    return ranked


def open_in_quicktime(stream_url: str):
    """Open stream in QuickTime Player."""
    try:
        subprocess.Popen([
            'open',
            '-a', 'QuickTime Player',
            stream_url
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception as e:
        print(f"Error opening QuickTime: {e}")
        sys.exit(1)


def main():
    search_term = sys.argv[1] if len(sys.argv) > 1 else ""

    # Load channels from both sources
    channels = load_custom_channels()

    if PLAYLIST_URL:
        remote_content = fetch_playlist()
        channels.extend(parse_m3u(remote_content))

    if not channels:
        print("No channels found. Add channels to channels.json or set a PLAYLIST_URL.")
        sys.exit(1)

    # Rank and search
    ranked = rank_channels(channels, search_term)

    if not ranked:
        print(f"No channels matching '{search_term}'")
        sys.exit(1)

    if search_term:
        best_match = ranked[0][0]
        print(f"Opening: {best_match['name']}")
        open_in_quicktime(best_match['url'])
    else:
        by_group = {}
        for channel, score in ranked:
            group = channel['group']
            if group not in by_group:
                by_group[group] = []
            by_group[group].append(channel)

        for league in SPORTS_LEAGUES:
            if league in by_group:
                print(f"\n{league}:")
                for channel in by_group[league][:10]:
                    print(f"  {channel['name']}")

        print(f"\n{len(channels)} channels available. Search to play one.")


if __name__ == "__main__":
    main()
