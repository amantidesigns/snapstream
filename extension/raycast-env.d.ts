/// <reference types="@raycast/api">

/* 🚧 🚧 🚧
 * This file is auto-generated from the extension's manifest.
 * Do not modify manually. Instead, update the `package.json` file.
 * 🚧 🚧 🚧 */

/* eslint-disable @typescript-eslint/ban-types */

type ExtensionPreferences = {
  /** Remote M3U Playlist URL - URL to a remote M3U playlist for additional channels (leave empty to disable) */
  "playlistUrl": string,
  /** undefined - Automatically enter Picture-in-Picture mode after opening a stream */
  "autoPip": boolean,
  /** PiP Delay (seconds) - Seconds to wait before triggering PiP (increase if streams take longer to load) */
  "pipDelay": string
}

/** Preferences accessible in all the extension's commands */
declare type Preferences = ExtensionPreferences

declare namespace Preferences {
  /** Preferences accessible in the `search-channels` command */
  export type SearchChannels = ExtensionPreferences & {}
  /** Preferences accessible in the `import-channels` command */
  export type ImportChannels = ExtensionPreferences & {}
}

declare namespace Arguments {
  /** Arguments passed to the `search-channels` command */
  export type SearchChannels = {}
  /** Arguments passed to the `import-channels` command */
  export type ImportChannels = {}
}

