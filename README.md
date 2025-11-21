# nanoo.tv Video Link Extractor (NanooRipper)

A lightweight Python script that extracts direct MP4 download links from nanoo.tv videos using Microsoft SSO authentication.

## Features

- 🔐 Automated Microsoft SSO login via webview
- 💾 Cookie persistence (no repeated logins)
- 🎥 Extracts signed MP4 stream URLs
- ⚡ Lightweight - no browser automation frameworks needed
- 🔄 Automatic session validation


## Installation

1. Clone this repository:
```bash
git clone <your-repo-url>
cd nanooripper
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the script:
```bash
python main.py
```

**First run:** A Microsoft login window will appear. Sign in with your credentials.

**Subsequent runs:** Your session will be validated automatically. If expired, the login window appears again.

When prompted, paste the nanoo.tv video URL (e.g., `https://www.nanoo.tv/link/v/970559`)

The script will output the direct MP4 download link.

## Notes

- MP4 links expire after ~24 hours (check the `e=` parameter)
- The script requires valid nanoo.tv school/institution access
- Repository is partly coded with AI (Including this README)


***

**Disclaimer:** This tool is for personal educational use only. Respect nanoo.tv's terms of service and copyright laws.
