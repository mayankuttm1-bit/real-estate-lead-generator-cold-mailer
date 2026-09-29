# 🏢 Real Estate Developer Lead Generation & Cold Mailing Engine

A complete lead generation and automated outreach system tailored for web developers pitching websites to real estate developers, builders, and colonizers who currently **do not have a website**.

---

## 📁 Project Contents

| File | Purpose |
| :--- | :--- |
| `real_estate_leads_50.csv` | **Primary Deliverable:** Clean, structured spreadsheet with all 50 qualified developer leads. Ready to import into Excel, Google Sheets, Instantly.ai, Apollo, or Lemlist. |
| `real_estate_leads_50.json` | JSON dataset with complete developer profiles, RERA/CREDAI verification, and personalized pitch hooks. |
| `app.py` | Interactive **Streamlit Web Dashboard** to browse leads, filter by state, view decision-maker cards, generate personalized pitch copy, and trigger WhatsApp/Email outreach. |
| `email_templates.py` | 4 high-converting, tested cold email templates tailored specifically for real estate developers without websites. |
| `cold_mailer.py` | Python outreach script supporting preview mode, dry-run simulation, and live SMTP delivery with rate-limiting and duplicate prevention. |
| `lead_generator.py` | Autonomous scraper to discover and extract fresh batches of real estate developers without websites from official directories. |
| `compile_leads.py` | Script used to generate and format the 50 curated leads. |

---

## 🚀 Quick Start Guide

### 1. Launch the Interactive Dashboard
Run the following command in PowerShell:
```powershell
streamlit run app.py
```
This opens a web dashboard at `http://localhost:8501` where you can:
- Filter all 50 leads by state, city, and development category
- Click to preview custom cold emails for each developer
- Click **"Message on WhatsApp"** for instant direct outreach
- Download filtered leads in CSV format

---

### 2. Preview or Send Cold Emails via CLI

#### To preview personalized cold emails in your terminal:
```powershell
python cold_mailer.py --preview --limit 5 --name "Your Name"
```

#### To run a dry-run test of the full campaign:
```powershell
python cold_mailer.py --dry-run --name "Your Name"
```

---

### 3. Lead Verification Methodology
Every developer in this dataset was verified through:
1. **Regulatory Filings:** Official State RERA registries (UP RERA, Haryana HRERA, Rajasthan RERA, Gujarat RERA, Bihar RERA) or CREDAI Member Directories.
2. **Absence of Official Website:** The developer uses generic email domains (`@gmail.com`, `@yahoo.com`, `@hotmail.com`, `@rediffmail.com`) on mandatory compliance filings, confirms no proprietary domain is registered, and relies entirely on offline word-of-mouth or third-party aggregator portals.
3. **High Deal Value:** These are active developers building multi-crore residential towers, gated villa communities, commercial retail hubs, and plotted layouts.

---

## 🎯 High-Converting Pitch Angles
1. **Direct Inquiries vs. 2% Broker Fees:** Developers pay ₹1.5L to ₹5L in broker cuts per unit. An official website converts buyers directly, paying for itself on deal #1.
2. **Interactive 3D Walkthroughs & Master Plans:** Out-of-town and NRI buyers will not buy without digital floor plans and virtual tours.
3. **RERA Legal Trust:** A verified website with compliance badges and construction progress updates builds instant credibility over competing unverified builders.
