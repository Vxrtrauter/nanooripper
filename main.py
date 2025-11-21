import requests
import json
import webview
from http.cookies import SimpleCookie
import time

COOKIE_FILE = "session_cookies.json"

def load_cookies():
    try:
        with open(COOKIE_FILE, 'r') as f:
            cookies = json.load(f)
            print(f"Loaded cookies from file: {list(cookies.keys())}")
            return cookies
    except:
        return {}

def save_cookies(cookies_dict):
    with open(COOKIE_FILE, "w") as f:
        json.dump(cookies_dict, f, indent=2)
    print(f"Cookies saved to {COOKIE_FILE}")

def validate_cookies(cookies):
    if not cookies or "session" not in cookies:
        print("No session cookie found")
        return False
    session = requests.Session()
    for name, value in cookies.items():
        session.cookies.set(name, value, domain="www.nanoo.tv", path="/")
    try:
        print("Validating cookies...")
        response = session.get("https://www.nanoo.tv/", timeout=10)
        if response.status_code == 200 and "nanoo.tv" in response.text:
            print("Validation successful!")
            return True
        print("Validation failed")
        return False
    except Exception as e:
        print(f"Validation error: {e}")
        return False

def get_authenticated_cookies():
    print("Launching Microsoft login window...")
    cookies_collected = []
    login_complete = [False]
    
    def on_loaded():
        time.sleep(1.5)
        current_url = window.get_current_url()
        print(f"Current URL: {current_url}")
        if current_url and current_url.startswith('https://www.nanoo.tv/') and '/sso/' not in current_url and not login_complete[0]:
            print("Login detected, extracting cookies...")
            login_complete[0] = True
            nonlocal cookies_collected
            cookies_collected = window.get_cookies()
            print(f"Extracted {len(cookies_collected)} cookies")
            time.sleep(1)
            window.destroy()

    window = webview.create_window("Microsoft Login", "https://www.nanoo.tv/sso/waad", width=1000, height=700)
    window.events.loaded += on_loaded
    webview.start()
    
    print(f"Webview closed. Processing {len(cookies_collected)} cookies...")
    cookies_dict = {}
    for cookie in cookies_collected:
        if isinstance(cookie, SimpleCookie):
            for key, morsel in cookie.items():
                cookies_dict[key] = morsel.value
                print(f"Extracted cookie: {key} = {morsel.value[:20]}...")
    
    if cookies_dict:
        save_cookies(cookies_dict)
        return cookies_dict
    else:
        print("No cookies extracted!")
        return {}

if __name__ == "__main__":
    cookies = load_cookies()
    
    if not validate_cookies(cookies):
        print("\nCookies invalid or expired. Logging in...")
        cookies = get_authenticated_cookies()
        if not cookies or "session" not in cookies:
            print("Failed to get valid cookies!")
            exit(1)
    else:
        print("Using existing valid cookies\n")

    session = requests.Session()
    for name, value in cookies.items():
        session.cookies.set(name, value, domain="www.nanoo.tv", path="/")

    url = input("Input URL: ").strip()
    video_id = url.strip("/").split("/")[-1]
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:136.0) Gecko/20100101 Firefox/136.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Referer": "https://www.nanoo.tv/"
    }
    
    print("Visiting video page to authorize session...")
    page_response = session.get(url, headers=headers, timeout=10)
    print(f"Page visit status: {page_response.status_code}")
    
    session_cookie = cookies.get("session")
    api_url = f"https://www.nanoo.tv/api/v1/recordings/{video_id}|{session_cookie}/media"
    
    headers["Accept"] = "*/*"
    headers["Referer"] = url
    
    response = session.get(api_url, headers=headers, timeout=10)
    data = response.json()
    
    mp4_url = None
    if 'data' in data and 'video' in data['data']:
        for video in data['data']['video']:
            if video.get('default'):
                mp4_url = video['encodings'][0]['src']
                break
    
    if not mp4_url:
        print("Error: No video found")
        print(data.get('data', {}).get('title', ''))
        exit(1)

    print(mp4_url)
