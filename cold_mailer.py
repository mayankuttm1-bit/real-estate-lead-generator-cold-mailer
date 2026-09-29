"""
Cold Mailer Automation Script for Real Estate Developer Outreach
Supports dry-run previews, templating, rate limiting, and SMTP delivery.
"""

import os
import json
import time
import argparse
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email_templates import TEMPLATES

LOG_FILE = "campaign_delivery_log.json"

def load_leads(filepath="real_estate_leads_50.json"):
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

def load_logs():
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_log(lead_id, status, recipient):
    logs = load_logs()
    logs[str(lead_id)] = {
        "recipient": recipient,
        "status": status,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    }
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(logs, f, indent=2)

def personalize_text(text, lead, sender_name="Web Developer", sender_phone="+91-XXXXX-XXXXX", portfolio_url="https://yourportfolio.com"):
    replacements = {
        "{{contact_person}}": lead.get("contact_person", "Sir/Madam"),
        "{{company_name}}": lead.get("company_name", "your firm"),
        "{{city}}": lead.get("city", "your area"),
        "{{state}}": lead.get("state", ""),
        "{{project_focus}}": lead.get("project_focus", "projects"),
        "{{cold_email_hook}}": lead.get("cold_email_hook", ""),
        "[Your Name]": sender_name,
        "[Your Phone / WhatsApp]": sender_phone,
        "[Your Phone Number / WhatsApp]": sender_phone,
        "[Your Brand / Portfolio URL]": portfolio_url
    }
    for tag, val in replacements.items():
        text = text.replace(tag, str(val))
    return text

def preview_campaign(leads, template_key="template_1_direct_inquiries", limit=3, sender_name="Alex"):
    template = TEMPLATES[template_key]
    print("\n" + "="*80)
    print(f" CAMPAIGN PREVIEW: {template['name']}")
    print("="*80 + "\n")
    
    for lead in leads[:limit]:
        subject = personalize_text(template["subject"], lead)
        body = personalize_text(template["body"], lead, sender_name=sender_name)
        print(f"--- [Lead #{lead['id']}] {lead['company_name']} ({lead['city']}, {lead['state']}) ---")
        print(f"To: {lead['contact_person']} <{lead['email']}>")
        print(f"Phone: {lead['phone']}")
        print(f"Subject: {subject}")
        print("\n" + body)
        print("-" * 80 + "\n")

def send_cold_emails(leads, template_key="template_1_direct_inquiries", dry_run=True, delay_seconds=20, sender_name="Alex", sender_email="", sender_pass="", smtp_host="smtp.gmail.com", smtp_port=587):
    template = TEMPLATES[template_key]
    logs = load_logs()
    
    print(f"[*] Starting campaign run with template: {template_key}")
    print(f"[*] Mode: {'DRY RUN (No emails sent)' if dry_run else 'LIVE SENDING'}")
    print(f"[*] Target leads count: {len(leads)}")
    
    server = None
    if not dry_run:
        if not sender_email or not sender_pass:
            print("[!] Error: Sender email and password required for live mode.")
            return
        server = smtplib.SMTP(smtp_host, smtp_port)
        server.starttls()
        server.login(sender_email, sender_pass)
        print("[+] Connected to SMTP server successfully.")

    try:
        for lead in leads:
            lead_id = str(lead["id"])
            if lead_id in logs and logs[lead_id]["status"] == "SENT":
                print(f"[~] Skipping Lead #{lead_id} ({lead['company_name']}) - already contacted.")
                continue

            subject = personalize_text(template["subject"], lead)
            body = personalize_text(template["body"], lead, sender_name=sender_name)
            to_email = lead["email"]

            if dry_run:
                print(f"[DRY-RUN] Would send to: {lead['contact_person']} <{to_email}> | Subject: '{subject}'")
                save_log(lead_id, "PREVIEWED", to_email)
            else:
                msg = MIMEMultipart()
                msg["From"] = f"{sender_name} <{sender_email}>"
                msg["To"] = to_email
                msg["Subject"] = subject
                msg.attach(MIMEText(body, "plain"))

                try:
                    server.sendmail(sender_email, to_email, msg.as_string())
                    print(f"[+] Successfully sent to Lead #{lead_id}: {lead['company_name']} ({to_email})")
                    save_log(lead_id, "SENT", to_email)
                    time.sleep(delay_seconds)
                except Exception as e:
                    print(f"[-] Failed sending to Lead #{lead_id} ({to_email}): {e}")
                    save_log(lead_id, f"FAILED: {e}", to_email)
    finally:
        if server:
            server.quit()
            print("[*] Closed SMTP connection.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Cold mailer tool for real estate leads")
    parser.add_argument("--preview", action="store_true", help="Preview first few emails")
    parser.add_argument("--limit", type=int, default=3, help="Number of leads to preview")
    parser.add_argument("--template", type=str, default="template_1_direct_inquiries", choices=list(TEMPLATES.keys()))
    parser.add_argument("--send", action="store_true", help="Execute sending (requires SMTP credentials)")
    parser.add_argument("--dry-run", action="store_true", default=True, help="Simulate run without sending")
    parser.add_argument("--name", type=str, default="Your Name", help="Your sender name")
    
    args = parser.parse_args()
    leads = load_leads()
    
    if args.preview:
        preview_campaign(leads, template_key=args.template, limit=args.limit, sender_name=args.name)
    else:
        send_cold_emails(leads, template_key=args.template, dry_run=args.dry_run, sender_name=args.name)
