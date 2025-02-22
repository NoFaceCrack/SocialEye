import instaloader
import json
import os
from collections import Counter
import time
import importlib.util
import sys
import re
import requests
from bs4 import BeautifulSoup
from googlesearch import search

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')


def set_terminal_size(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    max_width = max(len(line) for line in lines)
    height = len(lines)
    os.system(f'mode con: cols={max_width+2} lines={height+2}' if os.name == 'nt' else f'printf "\\e[8;{height+2};{max_width+2}t"')


def print_banner_slowly(file_path, duration=10):
    with open(file_path, 'r') as file:
        banner = file.read()
    delay = duration / len(banner)
    for char in banner:
        print(char, end='', flush=True)
        time.sleep(delay)


def check_libraries(libraries):
    missing_libs = []
    for lib in libraries:
        if importlib.util.find_spec(lib) is None:
            missing_libs.append(lib)
    if missing_libs:
        print("\n\nSome libraries are missing:")
        for lib in missing_libs:
            print(f"- {lib}")
        print('\nRun the following command to install them:')
        print('python3 setup.py')
    else:
        print("\n\nAll libraries are installed. OK ✅")


if __name__ == "__main__":
    clear_terminal()
    set_terminal_size('output2.txt')
    print_banner_slowly('output2.txt', duration=10)
    check_libraries(['json', 'instaloader', 'os', 'time', 'collections'])
    print("\nTool starting...")
    

 

def animated_bar():
    for i in range(101):
        time.sleep(0.50)
        sys.stdout.write('\r\033[91m[{0}] {1}%\033[0m'.format('#' * (i // 2) + '-' * (50 - i // 2), i))
        sys.stdout.flush()
        
animated_bar()
print("\n\033[91mCompleted...........!\033[0m")

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')
clear_terminal()


def banner():
    print("\033[31m███████╗ ██████╗  ██████╗██╗ █████╗ ██╗     ███████╗██╗   ██╗███████╗")
    print("██╔════╝██╔═══██╗██╔════╝██║██╔══██╗██║     ██╔════╝╚██╗ ██╔╝██╔════╝")
    print("███████╗██║   ██║██║     ██║███████║██║     █████╗   ╚████╔╝ █████╗  ")
    print("╚════██║██║   ██║██║     ██║██╔══██║██║     ██╔══╝    ╚██╔╝  ██╔══╝  ")
    print("███████║╚██████╔╝╚██████╗██║██║  ██║███████╗███████╗   ██║   ███████╗")
    print("╚══════╝ ╚═════╝  ╚═════╝╚═╝╚═╝  ╚═╝╚══════╝╚══════╝   ╚═╝   ╚══════╝")
    print("                                     █▓▒▒░░░Created By Naresh ░░░▒▒▓█\033[0m")

banner()

DOWNLOAD_FOLDER = "Download"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

def scrape_instagram(username):
    """Scrapes Instagram profile data"""
    L = instaloader.Instaloader()

    try:
        profile = instaloader.Profile.from_username(L.context, username)

        data = {
            "Username": profile.username,
            "Full Name": profile.full_name,
            "Bio": profile.biography,
            "Followers": profile.followers,
            "Following": profile.followees,
            "Posts Count": profile.mediacount,
            "Profile Pic URL": profile.profile_pic_url,
            "External URL": profile.external_url
        }

        print("\n📌 Instagram Account Information:")
        for key, value in data.items():
            print(f"{key}: {value}")

        return profile, data

    except Exception as e:
        print("❌ Error:", e)
        return None, None

def location_finder():
    post_url = input("🔗 Enter Instagram Post URL: ")

    post_match = re.search(r"instagram\.com/p/([^/]+)/", post_url)
    if not post_match:
        print("❌ Invalid Instagram URL!")
        return None
    post_id = post_match.group(1)

    save_folder = "post_analysis"
    os.makedirs(save_folder, exist_ok=True)

    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(post_url, headers=headers)
    if response.status_code != 200:
        print("❌ Failed to fetch the post.")
        return None

    soup = BeautifulSoup(response.text, "html.parser")

    caption = soup.find("meta", {"property": "og:title"})
    location = soup.find("a", {"class": "x1i10hfl"})
    likes = soup.find("meta", {"property": "og:description"})

    post_data = {
        "Post ID": post_id,
        "Caption": caption["content"] if caption else "N/A",
        "Location": location.text if location else "N/A",
        "Likes & Comments": likes["content"] if likes else "N/A",
        "URL": post_url
    }

    json_path = os.path.join(save_folder, f"{post_id}.json")
    with open(json_path, "w", encoding="utf-8") as json_file:
        json.dump(post_data, json_file, indent=4, ensure_ascii=False)

    print("\n📌 Instagram Post Details:")
    for key, value in post_data.items():
        print(f"🔹 {key}: {value}")

    return post_data

import requests
import time
import logging
import argparse
from googlesearch import search
from bs4 import BeautifulSoup

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def dark_web_search(username):
    dark_web_sites = [
        "https://ahmia.fi/search/?q=",
        "https://onion.live/search/?q=",
        "https://darksearch.io/search?q="
    ]
    
    logging.info("Starting dark web search...")
    results = []
    headers = {"User-Agent": "Mozilla/5.0"}
    
    for site in dark_web_sites:
        url = site + username
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                links = [a['href'] for a in soup.find_all('a', href=True)]
                results.extend(links)
                logging.info(f"✅ Found results on {site}")
            else:
                logging.warning(f"❌ No data found on {site}")
        except requests.exceptions.RequestException as e:
            logging.error(f"⚠️ Could not connect to {site}: {e}")
    
    return results

def google_dork_search(username):
    google_dorks = [
        f"site:pastebin.com {username}",
        f"site:github.com {username}",
        f"site:reddit.com {username}",
        f"site:instagram.com {username}"
    ]
    
    logging.info("Starting Google Dorking...")
    results = []
    
    for dork in google_dorks:
        try:
            for result in search(dork, num=5, stop=5, pause=2, user_agent="Mozilla/5.0"):
                results.append(result)
                logging.info(result)
        except Exception as e:
            logging.error(f"Error while searching with dork '{dork}': {e}")
    
    return results

def save_results(username, dark_web_results, google_results):
    filename = f"osint_results_{username}.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"Results for username: {username}\n\n")
        
        f.write("[+] Dark Web Results:\n")
        if dark_web_results:
            for result in dark_web_results:
                f.write(result + "\n")
        else:
            f.write("No dark web results found.\n")
        
        f.write("\n[+] Google Dorking Results:\n")
        if google_results:
            for result in google_results:
                f.write(result + "\n")
        else:
            f.write("No Google Dorking results found.\n")
    
    logging.info(f"Results saved in {filename}")

def osint_search(username):
    dark_web_results = dark_web_search(username)
    google_results = google_dork_search(username)
    save_results(username, dark_web_results, google_results)

def run_osint():
    username = input("Enter username to search: ")
    osint_search(username)



def check_username(username):
    websites = {
        "Instagram": f"https://www.instagram.com/{username}",
        "Twitter": f"https://www.twitter.com/{username}",
        "Facebook": f"https://www.facebook.com/{username}",
        "GitHub": f"https://www.github.com/{username}",
        "Reddit": f"https://www.reddit.com/user/{username}",
        "TikTok": f"https://www.tiktok.com/@{username}"
    }

    results = {}

    for site, url in websites.items():
        try:
            response = requests.get(url)
            if response.status_code == 200:
                results[site] = f"Found ✅ ({url})"
            else:
                results[site] = "Not Found ❌"
        except requests.exceptions.RequestException:
            results[site] = "Error checking ❌"

    return results

def call():
    username = input("Enter Instagram Username: ")
    print("Checking username, this may take some time...")
    loading_animation()
    result = check_username(username)

    for site, status in result.items():
        print(f"{site}: {status}")

    save = input("\nDo you want to save the results in JSON format? (yes/no): ")
    if save.lower() == "yes":
        with open(f"{username}_lookup.json", "w") as file:
            json.dump(result, file, indent=4)
        print(f"Results saved as {username}_lookup.json")

def download_posts_reels(username):
    L = instaloader.Instaloader(download_pictures=True, download_videos=True)

    try:
        print(f"\n📥 Downloading posts and reels of {username}...")
        L.download_profile(username, profile_pic_only=False)
        print("✅ Download complete.")
    
    except Exception as e:
        print("❌ Error downloading posts & reels:", e)

def save_to_json(username, data):
    filename = os.path.join(DOWNLOAD_FOLDER, f"{username}.json")
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)

    print(f"\n✅ Data saved successfully in {filename} 📂")

def about_me():
    print("""
    ===============================
          🔥 About Naresh (Me) 🔥
    ===============================

    👨‍💻 *Cyber Security Enthusiast & Ethical Hacker*
    🚀 Advanced Pentesting | OSINT | Exploit Development  
    🎯 Passionate about Cybersecurity & Ethical Hacking  
    🛠️ Expert in Python, Linux, Networking & Automation  

    📌 *What I Do?*  
    - WiFi & Network Security Testing  
    - OSINT (Open Source Intelligence) Mastery  
    - Custom Exploit & Payload Development  
    - Social Media Intelligence Gathering  
    - Tool Development & Automation  

    🏆 *My Mission:*  
    "To explore the depths of cybersecurity, master ethical hacking,  
    and build tools that make the digital world more secure."  

    🔗 Follow me on Instagram: https://www.instagram.com/ismart_nrh?igsh=MjJoejQ0ZjlwNmVv 

    ===============================
    """)

while True:
    print("\n█ Select An Option █             # SocialEye Is Powerful OSINT Framework | Use It Your Own Risk ")
    print("1️⃣ Instagram Account Information  # Public Information About Target Username")
    print("2️⃣ Post Analysis & Read           # Post Analysis (Information | Scraping | Extract | Tracking)")
    print("3️⃣ Search Leak Data On Dark Web   # If User Data Leak On Dark Web And Google Dork... ")
    print("4️⃣ Username Website Lookup        # Check Social Media Target Where Registered Online Website")
    print("5️⃣ Download Posts && Reels        # Download Public Account Reels and post (Private Account Not Supported")
    print("6️⃣ About Me 😊                    # About Me Function Showcases The Devloper's Skills , Expertise And Vision")   
    print("7️⃣ Exit                           # In Case You Want Exit ") 

    choice = input("\n📌 Enter Your Choice (1-7): ")

    if choice == "7":
        exit_choice = input("⚠️ Do You Really Want To Exit? (yes/no): ").strip().lower()
        if exit_choice == "yes":
            print("Bye 👋 Exiting...")
            break
        else:
            continue
    
    if choice == "6":
        about_me()

    if choice == "2":
        location_finder()

    if choice == "3":
        run_osint()

    if choice == "4":
        call()

    if choice == "":
        print("Select One Option Between ❌ ")
        os.system("clear")
        print(banner())
    else:
        username = input("🔍 Enter Instagram Username: @")

    if choice == "1":
        scrape_instagram(username)
    elif choice == "5":
        download_posts_reels(username)
    else:
        print("❌ Invalid option, try again.")
