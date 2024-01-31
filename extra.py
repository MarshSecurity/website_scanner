from urllib.parse import urlparse, urlunsplit , urljoin
import requests
import os
from bs4 import BeautifulSoup
from datetime import datetime
from colorama import Fore
from concurrent.futures import ThreadPoolExecutor
import socket

marshsecurity = f"""

 ███▄ ▄███▓ ▄▄▄       ██▀███    ██████  ██░ ██   ██████ ▓█████  ▄████▄   █    ██  ██▀███   ██▓▄▄▄█████▓▓██   ██▓
▓██▒▀█▀ ██▒▒████▄    ▓██ ▒ ██▒▒██    ▒ ▓██░ ██▒▒██    ▒ ▓█   ▀ ▒██▀ ▀█   ██  ▓██▒▓██ ▒ ██▒▓██▒▓  ██▒ ▓▒ ▒██  ██▒
▓██    ▓██░▒██  ▀█▄  ▓██ ░▄█ ▒░ ▓██▄   ▒██▀▀██░░ ▓██▄   ▒███   ▒▓█    ▄ ▓██  ▒██░▓██ ░▄█ ▒▒██▒▒ ▓██░ ▒░  ▒██ ██░
▒██    ▒██ ░██▄▄▄▄██ ▒██▀▀█▄    ▒   ██▒░▓█ ░██   ▒   ██▒▒▓█  ▄ ▒▓▓▄ ▄██▒▓▓█  ░██░▒██▀▀█▄  ░██░░ ▓██▓ ░   ░ ▐██▓░
▒██▒   ░██▒ ▓█   ▓██▒░██▓ ▒██▒▒██████▒▒░▓█▒░██▓▒██████▒▒░▒████▒▒ ▓███▀ ░▒▒█████▓ ░██▓ ▒██▒░██░  ▒██▒ ░   ░ ██▒▓░
░ ▒░   ░  ░ ▒▒   ▓▒█░░ ▒▓ ░▒▓░▒ ▒▓▒ ▒ ░ ▒ ░░▒░▒▒ ▒▓▒ ▒ ░░░ ▒░ ░░ ░▒ ▒  ░░▒▓▒ ▒ ▒ ░ ▒▓ ░▒▓░░▓    ▒ ░░      ██▒▒▒ 
░  ░      ░  ▒   ▒▒ ░  ░▒ ░ ▒░░ ░▒  ░ ░ ▒ ░▒░ ░░ ░▒  ░ ░ ░ ░  ░  ░  ▒   ░░▒░ ░ ░   ░▒ ░ ▒░ ▒ ░    ░     ▓██ ░▒░ 
░      ░     ░   ▒     ░░   ░ ░  ░  ░   ░  ░░ ░░  ░  ░     ░   ░         ░░░ ░ ░   ░░   ░  ▒ ░  ░       ▒ ▒ ░░  
       ░         ░  ░   ░           ░   ░  ░  ░      ░     ░  ░░ ░         ░        ░      ░            ░ ░     
                                                               ░                                        ░ ░     
Scanner tool by @MarshSecurity
"""



def print_border(text):
    border_top = "╔" + "═" * len(text) + "╗"
    border_bottom = "╚" + "═" * len(text) + "╝"
    content_line = "║ " + text + "║"

    print(border_top)
    print(content_line)
    print(border_bottom)

def change_url(input_url):
    if '://' not in input_url:
        new_scheme = "https://"
        processed_url = f"{new_scheme}{input_url.lstrip('/')}"
    else:
        processed_url = input_url
    return processed_url
def change_for_ip(input_url):
    if '://' in input_url:
        input_url = input_url.split('://')[1]

    return input_url.lstrip('/')

def get_ip_addresses(url):
    try:
        ip_addresses = socket.gethostbyname_ex(url)[2]
        return ip_addresses
    except socket.gaierror:
        print(f"Unable to resolve IP addresses for {url}")
        return None

def get_server_info(url):
    try:
        response = requests.head(url, allow_redirects=True)
        server_info = response.headers.get("Server")
        return server_info
    except requests.RequestException as e:
        print(f"Error: {e}")
        return None

def create_links_folder():
    folder_name = "info"
    current_dir = os.path.dirname(os.path.abspath(__file__))
    folder_path = os.path.join(current_dir, folder_name)

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

def get_links(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    links = [link.get('href') for link in soup.find_all('a', href=True)]
    return links

def save_info_to_file(url, links, subdomains, admin_panels, include_subdomains=True, include_admin_panels=True):
    folder_name = "info"
    current_dir = os.path.dirname(os.path.abspath(__file__))
    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    file_name_prefix = url.replace('://', '').replace('/', '_')
    file_name = f"{file_name_prefix}_{current_time}.txt"
    file_path = os.path.join(current_dir, folder_name, file_name)

    with open(file_path, 'w') as file:
        if include_admin_panels:
            file.write(f"Admin Panels for {url}:\n")
            for admin_panel in admin_panels:
                file.write(f"{admin_panel}\n")

        if include_subdomains:
            file.write(f"\nSubdomains for {url}:\n")
            for subdomain in subdomains:
                file.write(f"{subdomain}\n")

        file.write(f"\nUshbu saytda ishlatilgan barcha LINKlar {url}:\n")
        for link in links:
            if not link.startswith(('http:', 'https:')):
                link = urljoin(url, link)
            file.write(f"{link}\n")



def find_admin_panels(target_url, admin_file):
    found_admin_panels = []

    with open(admin_file, 'r') as file:
        admin_links = [line.strip() for line in file]
    target_url = change_for_ip(target_url)
    def check_admin_panel(admin_link):
        full_url = f"https://{target_url}/{admin_link}"
        try:
            response = requests.get(full_url)
            if response.status_code == 200 or response.status_code == 302:
                print(Fore.YELLOW + f'[+] {full_url} - > FOUND' + Fore.RESET)
                found_admin_panels.append(full_url)
            else:
                print(Fore.RED + f"[-] {full_url} - > ERROR (HTTP {response.status_code})" + Fore.RESET)
        except requests.RequestException as e:
            print(f"Error connecting to {full_url}: {e}")

    with ThreadPoolExecutor() as executor:
        executor.map(check_admin_panel, admin_links)

    return found_admin_panels

def domain_scanner(domain_name, sub_domnames):
    found_subdomains = []
    domain_name = change_for_ip(domain_name)
    def check_subdomain(subdomain):
        url = f"https://{subdomain}.{domain_name}"
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200 or response.status_code == 302:
                print(Fore.YELLOW + f'[+] {url} - > FOUND' + Fore.RESET)
                found_subdomains.append(url)
        except requests.ConnectionError:
            print(Fore.RED + f'[-] {url} - > ERROR' + Fore.RESET)
        except requests.Timeout:
            print(Fore.BLUE + f'[-] {url} - > TIMED OUT' + Fore.RESET)

    with ThreadPoolExecutor() as executor:
        executor.map(check_subdomain, sub_domnames)

    return found_subdomains



#bymarshsecurity