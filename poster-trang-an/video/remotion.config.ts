import {Config} from '@remotion/cli/config';

// Use the Chromium headless shell that ships with this environment
// instead of downloading one.
Config.setBrowserExecutable('/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell');
Config.setVideoImageFormat('jpeg');
Config.setOverwriteOutput(true);
