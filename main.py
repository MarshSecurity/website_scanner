import argparse
from extra import *
import requests
from colorama import Fore

print(Fore.RED + marshsecurity + Fore.RESET)

parser = argparse.ArgumentParser(description="Process a website URL.")
parser.add_argument('-u', '--url', help='Website URL', required=True)
args = parser.parse_args()
website_url = args.url
changed_url = change_url(website_url)
print_border(Fore.BLUE + f"TARGET SET - >  {website_url}" + Fore.RESET)

website_url = args.url
changed_url_for_ip = change_for_ip(website_url)
ip_addresses = get_ip_addresses(changed_url_for_ip)
if ip_addresses:
    print_border(Fore.YELLOW + f"IP addresses for {website_url}  -->   " + Fore.RESET +  f"{' | '.join(ip_addresses)}")


def check_cloudflare_waf(url):
    try:
        response = requests.get(url)
        if "cloudflare" in response.headers.get("server", "").lower():
            cloudflare = "YES"
        else:
            cloudflare = "NO"
        print_border(Fore.YELLOW + "CLOURFLARE: " + Fore.RESET + cloudflare)

        if "waf" in response.text.lower():
            waf = "YES"
        else:
            waf = "NO"
        print_border(Fore.YELLOW + "WAF : " + Fore.RESET + waf)

    except requests.RequestException as e:
        print(f"Error: {e}")

check_cloudflare_waf(changed_url)

server_info = get_server_info(changed_url)

if server_info:
    print_border(Fore.YELLOW + f"SERVER: " + Fore.RESET +  f"{server_info}")
else:
    print(f"Unable to retrieve server information for {website_url}")

target_url = website_url
admin_file = 'extra/admin.txt'
subdomains_file = 'extra/sub.txt'

def admin_finder():
    print(Fore.YELLOW + "\nADMIN PANEL QIDIRLMOQDA ... TOPILGAN LINKLAR INFO PAPKASIGA SAQLANADI....\n" + Fore.RESET)
    found_admin_panels = find_admin_panels(target_url, admin_file)
    print(Fore.BLUE + "Topilgan Admin panellar : " + Fore.RESET)
    for admin_panel in found_admin_panels:
        print(f"[+] {admin_panel}")
    try:
        links = get_links(changed_url)
        save_info_to_file(changed_url, links, [], found_admin_panels, include_subdomains=False)
        print_border(Fore.YELLOW + f"TOPILGAN BARCHA ADMIN PANEL VA LINKLAR 'INFO' NOMLI PAPKAGA SAQLANDI" + Fore.RESET)
    except Exception as e:
        print(f"Error: {e}")


def sub_finder():
    print(Fore.YELLOW + "\nSUBDOMAIN  QIDIRLMOQDA ... TOPILGAN SUBDOMAINLAR INFO PAPKASIGA SAQLANADI....\n" + Fore.RESET)
    dom_name = website_url
    with open(subdomains_file, 'r') as file:
        sub_dom = file.read().splitlines()

    sub_domains = domain_scanner(dom_name, sub_dom)

    try:
        links = get_links(changed_url)
        save_info_to_file(changed_url, links, sub_domains, [], include_admin_panels=False)
        print_border(Fore.YELLOW + f"TOPILGAN BARCHA SUBDOMAINLAR VA LINKLAR  'INFO' NOMLI PAPKAGA SAQLANDI" + Fore.RESET)
    except Exception as e:
        print(f"Error: {e}")


create_links_folder()



choice_text = f"""
[*] 1. Agar siz {website_url} ning admin panelini qidirmoqchi bo'lsangiz 1 yozing ..
[*] 2. Agar siz {website_url} ning subdomain larini qidirmoqchi bo'lsangiz 2 yozing ..
[*] 3. Agar siz {website_url} ning admin panelini ham va subdomainini ham qidirmoqchi bo'lsangiz 3 yozing ..
[*] 4. Agar siz dasturni to'xtatoqchi bo'lsangiz ENTER ni bosing ..
"""
print(Fore.BLUE + choice_text + Fore.RESET)
choice = input(Fore.YELLOW + "Qaysi birini tanlaysiz ? ( dasturni to'xtatish uchun ENTER ni bosing)  --->   " + Fore.RESET)

if choice == "1":
    admin_finder()
elif choice == "2":
    sub_finder()
elif choice == "3":
    admin_finder()
    sub_finder()
   

else:
     exit()

#bymarshsecurity
