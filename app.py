"""
Streamlit Dashboard for Real Estate Lead Generation & Cold Outreach
Run with: streamlit run app.py
"""

import json
import streamlit as st
import pandas as pd
from email_templates import TEMPLATES
from cold_mailer import personalize_text

st.set_page_config(
    page_title="Real Estate Lead Generator & Cold Mailer",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
    .metric-card {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        padding: 20px;
        border-radius: 12px;
        border-left: 5px solid #3b82f6;
        color: white;
    }
    .lead-box {
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 16px;
        margin-bottom: 12px;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def get_leads_data():
    with open("real_estate_leads_50.json", "r", encoding="utf-8") as f:
        return json.load(f)

leads = get_leads_data()
df = pd.DataFrame(leads)

# Sidebar Controls
st.sidebar.title("🏢 Navigation & Filters")
st.sidebar.markdown("**Lead Generator & Cold Outreach System**")

# User details for personalization
st.sidebar.subheader("👤 Your Sender Profile")
sender_name = st.sidebar.text_input("Your Name", value="Alex Rivera")
sender_phone = st.sidebar.text_input("Your WhatsApp / Phone", value="+91 98765 43210")
portfolio_url = st.sidebar.text_input("Portfolio / Agency Link", value="https://devstudio.agency")

st.sidebar.markdown("---")
st.sidebar.subheader("🔍 Filter Leads")
selected_state = st.sidebar.multiselect(
    "Select State(s)",
    options=sorted(df["state"].unique()),
    default=sorted(df["state"].unique())
)

search_query = st.sidebar.text_input("Search Company or Person", "")

# Filter dataframe
filtered_df = df[df["state"].isin(selected_state)]
if search_query:
    filtered_df = filtered_df[
        filtered_df["company_name"].str.contains(search_query, case=False) |
        filtered_df["contact_person"].str.contains(search_query, case=False) |
        filtered_df["city"].str.contains(search_query, case=False)
    ]

# Main Dashboard
st.title("🏢 Real Estate Developer Leads & Cold Email Generator")
st.markdown("""
Targeted database of **50 active real estate developers and builders who currently have NO website**.
Each lead has verified contact details, regulatory source proof, and a custom pitch angle to sell website development services.
""")

# Metrics Row
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric(label="Total Qualified Leads", value=len(df))
with col2:
    st.metric(label="Currently Filtered", value=len(filtered_df))
with col3:
    st.metric(label="Target States", value=df["state"].nunique())
with col4:
    st.metric(label="Website Status", value="100% No Website")

st.markdown("---")

tab1, tab2, tab3 = st.tabs(["📋 Lead Directory Table", "✉️ Cold Email Generator", "📊 Strategic Insights"])

with tab1:
    st.subheader(f"Showing {len(filtered_df)} Real Estate Developer Leads")
    
    # Download Button
    csv_data = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Filtered Leads (CSV)",
        data=csv_data,
        file_name="real_estate_leads_filtered.csv",
        mime="text/csv",
    )
    
    display_cols = ["id", "company_name", "contact_person", "email", "phone", "city", "state", "project_focus", "verification_source"]
    st.dataframe(
        filtered_df[display_cols],
        column_config={
            "id": "ID",
            "company_name": "Company Name",
            "contact_person": "Decision Maker",
            "email": "Email Address",
            "phone": "Phone / Mobile",
            "city": "City",
            "state": "State",
            "project_focus": "Development Focus",
            "verification_source": "Source"
        },
        use_container_width=True,
        hide_index=True
    )

with tab2:
    st.subheader("Generate Personalized Cold Email for Any Lead")
    
    lead_options = [f"#{row['id']} - {row['company_name']} ({row['city']}, {row['state']})" for _, row in filtered_df.iterrows()]
    if lead_options:
        selected_lead_str = st.selectbox("Select Target Developer", lead_options)
        selected_id = int(selected_lead_str.split(" ")[0].replace("#", ""))
        target_lead = next(item for item in leads if item["id"] == selected_id)
        
        # Display developer profile card
        col_a, col_b = st.columns([1, 2])
        with col_a:
            st.markdown(f"""
            ### {target_lead['company_name']}
            - **Decision Maker:** {target_lead['contact_person']} ({target_lead['designation']})
            - **Email:** `{target_lead['email']}`
            - **Phone:** `{target_lead['phone']}`
            - **Location:** {target_lead['city']}, {target_lead['state']}
            - **Focus:** {target_lead['project_focus']}
            - **Status:** :red[{target_lead['website_status']}]
            - **Source:** {target_lead['verification_source']}
            """)
            
            # Direct WhatsApp trigger if mobile is present
            phone_digits = ''.join(filter(str.isdigit, target_lead['phone']))
            if len(phone_digits) >= 10:
                clean_phone = phone_digits[-10:]
                st.markdown(f"""
                <a href="https://wa.me/91{clean_phone}?text=Hi%20{target_lead['contact_person']}%2C%20I%20saw%20your%20projects%20at%20{target_lead['company_name']}..." target="_blank">
                    <button style="background-color:#25D366;color:white;border:none;padding:10px 18px;border-radius:6px;cursor:pointer;font-weight:bold;">
                        📱 Message on WhatsApp
                    </button>
                </a>
                """, unsafe_allow_html=True)
                
        with col_b:
            template_choice = st.selectbox(
                "Choose Outreach Strategy / Angle",
                options=list(TEMPLATES.keys()),
                format_func=lambda x: TEMPLATES[x]["name"]
            )
            
            tpl = TEMPLATES[template_choice]
            personalized_subject = personalize_text(tpl["subject"], target_lead)
            personalized_body = personalize_text(
                tpl["body"], 
                target_lead, 
                sender_name=sender_name, 
                sender_phone=sender_phone, 
                portfolio_url=portfolio_url
            )
            
            st.markdown("**Email Subject:**")
            st.code(personalized_subject, language="text")
            
            st.markdown("**Personalized Email Body:**")
            st.text_area("Email Content", value=personalized_body, height=350)
            
            mailto_link = f"mailto:{target_lead['email']}?subject={personalized_subject}&body={personalized_body.replace(chr(10), '%0D%0A')}"
            st.markdown(f"[🚀 Open in Your Default Email Client (Gmail/Outlook)]({mailto_link})")
    else:
        st.warning("No leads match the current filters.")

with tab3:
    st.subheader("📊 Lead Insights & Pitching Playbook")
    col_x, col_y = st.columns(2)
    with col_x:
        st.markdown("""
        ### Why These Leads Are High-Converting For Web Devs:
        1. **Multi-Crore Project Scale:** Each of these companies is actively developing residential or commercial projects worth ₹5 Cr to ₹100+ Cr, yet they operate without a dedicated website.
        2. **Massive Pain Point (Broker Dependency):** Without an official site, 70%+ of their customer leads come through channel partners / local brokers who charge **2% to 3% commission** (₹1.5L to ₹5L per unit). A modern website pays for itself on the very first direct buyer conversion.
        3. **RERA Legal Requirement:** State RERAs require verified disclosure of project plans and quarterly updates. Developers without websites struggle to show transparency to buyers.
        4. **NRI & Outstation Buyers:** Real estate in tier-2 growth hubs (Hubli, Prayagraj, Gorakhpur, Bhopal, Jaipur) attracts huge interest from tech professionals working in Bangalore/NCR/Abroad who cannot visit the site physically.
        """)
    with col_y:
        st.markdown("""
        ### Recommended Cold Outreach Sequence:
        - **Day 1 (Initial Pitch):** Send **Template 1** (Direct Inquiry & Broker Commission Elimination).
        - **Day 2 (Multi-Channel Touch):** If phone number is available, send a polite 2-line WhatsApp message referencing the email with a preview link or mockup image.
        - **Day 4 (Value Follow-Up):** Send **Template 2** (Free Mockup / Concept Video Screen-recording).
        - **Day 7 (Break-Up / Urgency):** Send **Template 4** (Polite Check-In).
        """)
        
        # State breakdown chart
        st.markdown("#### Geographic Distribution")
        state_counts = df["state"].value_counts()
        st.bar_chart(state_counts)
