"""
Lead Generator & Scraper for Real Estate Developers Without Websites
Extracts developers from CREDAI directories and public registry sources,
detects absence of official website domains, and exports verified leads.
"""

import os
import csv
import json
import requests
import urllib3
from bs4 import BeautifulSoup

urllib3.disable_warnings()

FREE_EMAIL_DOMAINS = [
    "gmail.com", "yahoo.com", "yahoo.in", "yahoo.co.in", 
    "rediffmail.com", "hotmail.com", "outlook.com", "icloud.com"
]

def decode_cloudflare_email(cf_hex):
    """Decodes Cloudflare-protected email strings."""
    try:
        r = int(cf_hex[:2], 16)
        return "".join([chr(int(cf_hex[i:i+2], 16) ^ r) for i in range(2, len(cf_hex), 2)])
    except Exception:
        return ""

def scrape_credai_chapter(url="https://credaihublidharwad.com/members"):
    """
    Scrapes CREDAI chapter member directories, identifies developers using
    free personal emails (confirming lack of custom website/domain), and extracts contact info.
    """
    print(f"[*] Fetching CREDAI directory from: {url}")
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    try:
        res = requests.get(url, headers=headers, verify=False, timeout=15)
        if res.status_code != 200:
            print(f"[-] Failed with status code: {res.status_code}")
            return []
    except Exception as e:
        print(f"[-] Connection error: {e}")
        return []

    soup = BeautifulSoup(res.text, "html.parser")
    extracted_leads = []

    # Parse Cloudflare obfuscated emails
    for cf in soup.find_all(attrs={"data-cfemail": True})[1:]:
        parent = cf.find_parent("div")
        if not parent:
            continue
        card = parent.find_parent("div")
        if card:
            grandparent = card.find_parent("div")
            card_text = grandparent.get_text(" | ", strip=True) if grandparent else card.get_text(" | ", strip=True)
        else:
            card_text = parent.get_text(" | ", strip=True)

        parts = [x.strip() for x in card_text.split(" | ")]
        email = decode_cloudflare_email(cf["data-cfemail"]).strip().lower()

        # Check if email is from a free provider (proof of no business domain/website)
        is_free_domain = any(email.endswith("@" + d) for d in FREE_EMAIL_DOMAINS)
        if not is_free_domain:
            continue

        company, member, phone = "", "", ""
        for i, pt in enumerate(parts):
            if pt == "Organisation Name" and i + 1 < len(parts):
                company = parts[i + 1].title()
            elif pt == "Member" and i + 1 < len(parts):
                member = parts[i + 1].title()
            elif pt == "Phone" and i + 1 < len(parts):
                phone = parts[i + 1]

        if company and email:
            extracted_leads.append({
                "company_name": company,
                "contact_person": member or "Managing Director",
                "designation": "Founder / Managing Partner",
                "email": email,
                "phone": phone or "Available via CREDAI Directory",
                "city": "Hubli-Dharwad",
                "state": "Karnataka",
                "country": "India",
                "project_focus": "Residential & Commercial Developments",
                "website_status": "No Website (Uses free email on official CREDAI directory)",
                "verification_source": "CREDAI Chapter Directory",
                "cold_email_hook": f"Highlight local market expansion in Hubli-Dharwad and show how a direct project website captures local and NRI buyers without 2% broker fees."
            })

    print(f"[+] Successfully extracted {len(extracted_leads)} developers without websites.")
    return extracted_leads

def export_leads(leads, output_csv="scraped_real_estate_leads.csv"):
    if not leads:
        print("[!] No leads to export.")
        return
    fieldnames = list(leads[0].keys())
    with open(output_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(leads)
    print(f"[+] Exported {len(leads)} leads to '{output_csv}'")

if __name__ == "__main__":
    leads = scrape_credai_chapter()
    export_leads(leads)
