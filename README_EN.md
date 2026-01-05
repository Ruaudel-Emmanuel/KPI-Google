# 📊 KPI Sales Dashboard – Google Sheets Sync

A **professional, production-ready dashboard** that transforms raw Google Sheets data into real-time KPI visualizations. Perfect to showcase your skills on Upwork.

## 🎯 What is it?

This project demonstrates a **complete, scalable solution** for building KPI dashboards from Google Sheets data:
- **4 KPI Cards** : Total Revenue, Total Deals, Deals Won, Conversion Rate
- **4 Interactive Charts** : Revenue by Channel, Deal Status Distribution, Revenue by Sales Rep, Daily Trend
- **Dynamic Filters** : By Channel, Sales Rep, Status
- **Data Table** : Raw data view (last 20 rows)
- **Auto-Sync** : Automatic refresh every 5 minutes

## 📁 Project Structure

```
.
├── kpi-dashboard.html          # Dashboard (ready to use)
├── api_integration.py          # Python script for Google Sheets API
├── requirements.txt            # Python dependencies
├── README.md                   # French documentation
├── README_EN.md                # This file (English)
└── config.example.json         # Configuration example
```

## 🚀 Quick Start

### Option 1 : View the Dashboard (No Coding Required)
1. Open `kpi-dashboard.html` in your browser
2. Dashboard loads with **mock data** for demo purposes
3. Play with filters and explore all charts

### Option 2 : Connect to Your Google Sheet (Recommended for Upwork Demo)

#### Step 1 : Setup Google Sheets API
```bash
# 1. Visit Google Cloud Console
# https://console.cloud.google.com/

# 2. Create a project and enable Google Sheets API

# 3. Create Credentials:
#    - Type: "Service Account"
#    - Download JSON file

# 4. Share your Google Sheet with the service account email
#    (format: xxx@xxx.iam.gserviceaccount.com)
```

#### Step 2 : Configure Python Integration
```bash
# 1. Create project folder
mkdir kpi-dashboard
cd kpi-dashboard

# 2. Install dependencies
pip install -r requirements.txt

# 3. Add your Google credentials
cp /path/to/credentials.json ./google-credentials.json

# 4. Create config.json
cp config.example.json config.json

# Edit config.json:
{
  "sheet_id": "15gK_hwPkhL7UIVAJxvZPU_1MR24yxV_nWKpYXg9DN1w",
  "range": "Raw_Data!A:F",
  "credentials_path": "./google-credentials.json"
}
```

#### Step 3 : Launch the Dashboard
```bash
# Run the Python integration script
python api_integration.py

# Open kpi-dashboard.html in your browser
# → Dashboard now pulls **live data** from your Google Sheet
```

## 🎨 Features Overview

### KPI Cards
- **Total Revenue** : Sum of all deal amounts
- **Total Deals** : Count of all transactions
- **Deals Won** : Count of rows with "Gagné" (Won) status
- **Conversion Rate** : (Deals Won / Total Deals) × 100

### Interactive Charts
1. **Revenue by Channel** (bar chart) : See performance by SEO, Ads, Referral, Email
2. **Deal Status Distribution** (doughnut chart) : Visual breakdown of Won, Lost, Opportunity, Lead
3. **Revenue by Sales Rep** (horizontal bar) : Compare team member performance
4. **Revenue Trend** (line chart) : Daily revenue evolution (won deals only)

### Filters
- **Channel** : SEO, Ads, Referral, Email
- **Sales Rep** : Filter by team member name
- **Status** : Gagné, Perdu, Opportunité, Lead
- **Refresh Button** : Manual sync trigger

## 📊 Expected Data Format

Your Google Sheet should have this structure (in a sheet named `Raw_Data`):

| Date | Client | Canal | Commercial | Montant | Statut |
|------|--------|-------|------------|---------|--------|
| 2025-01-01 | Client A | SEO | Alice | 1200 | Gagné |
| 2025-01-02 | Client B | Ads | Bob | 850 | Lead |
| ... | ... | ... | ... | ... | ... |

**Required Columns** :
- `Date` : YYYY-MM-DD format
- `Client` : Client name (string)
- `Canal` : SEO / Ads / Referral / Email
- `Commercial` : Sales rep name
- `Montant` : Numeric amount (currency)
- `Statut` : Gagné / Perdu / Opportunité / Lead

## 💻 Technical Architecture

```
Google Sheets (Raw_Data)
        ↓
  Google Sheets API v4
        ↓
Python FastAPI (api_integration.py)
        ↓
    JSON response
        ↓
  Dashboard HTML (kpi-dashboard.html)
        ↓
    Chart.js (interactive visualization)
```

### Security Best Practices
- **Credentials** : Stored as environment variables (`GOOGLE_CREDENTIALS_PATH`)
- **Tokens** : Service Account authentication (no refresh needed)
- **API Keys** : Never commit to Git (add to `.gitignore`)
- **HTTPS** : Required for production deployment

## 🔧 Customization

### Add a New KPI Card
Edit `kpi-dashboard.html` and add a card:
```html
<div class="kpi-card success">
    <div class="kpi-label">Your KPI Name</div>
    <div class="kpi-value" id="yourKpi">0</div>
    <div class="kpi-change positive">↑ Real-time</div>
</div>
```

Then update the JavaScript calculation:
```javascript
function updateKPICards(data) {
    const yourKpi = data.filter(row => /* your logic */).length;
    document.getElementById('yourKpi').textContent = yourKpi;
}
```

### Customize Colors
Edit the CSS color variables (top of HTML file):
```css
header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}
```

### Add a New Data Column
1. Add a column to your Google Sheet
2. Update the API range (`range: "Raw_Data!A:G"`)
3. Add new filters or charts based on the data

## 🌐 Deploy to Production

### Option A : Netlify (Free, Recommended)
```bash
# 1. Push files to GitHub
# 2. Connect GitHub repo to Netlify
# 3. Add environment variables in Netlify settings
# 4. Auto-deploy on push

# Your dashboard is live at: https://your-url.netlify.app
```

### Option B : Vercel
```bash
npm install -g vercel
vercel --env GOOGLE_API_KEY=xxx
```

### Option C : Docker (Self-Hosted)
```bash
docker build -t kpi-dashboard .
docker run -e GOOGLE_CREDENTIALS_PATH=/secrets/creds.json \
           -v /path/to/creds.json:/secrets/creds.json \
           -p 8000:8000 kpi-dashboard
```

## 📈 SLA & Performance

| Metric | Value |
|--------|-------|
| Auto-refresh interval | 5 minutes |
| Sync time | < 30 seconds |
| Target uptime | 95%+ |
| Google Sheets API limit | 300 req/min |

## 🚨 Troubleshooting

### "Error: 401 Unauthorized"
→ Ensure service account email is **shared** on your Google Sheet

### "Error: 403 Forbidden"
→ Verify Google Sheets API is **enabled** in Google Cloud Console

### Dashboard shows "Loading data..." indefinitely
→ Check that `GOOGLE_API_KEY` environment variable is correct

### Charts not updating
→ Browser cache issue. Try Ctrl+Shift+Del to clear cache and refresh.

## 📞 How to Pitch This on Upwork

When a client asks "Can you build a Google Sheets KPI dashboard?":

1. **Share this project** as your portfolio demo
2. **Explain the process** :
   - "I build custom dashboards from your Google Sheets data"
   - "Real-time metrics and interactive charts"
   - "Auto-refresh every 30 minutes"
   - "4-5 key KPI visualizations based on your needs"
3. **Adapt to their requirements** : Sales, Marketing, Operations, HR, Finance
4. **Propose upsells** :
   - Excel Online integration (Microsoft Graph)
   - Email alerts & anomaly detection
   - Multi-user authentication (RBAC)
   - Custom data transformations

## 📚 Resources

- [Google Sheets API Documentation](https://developers.google.com/sheets/api)
- [Chart.js Official Docs](https://www.chartjs.org/)
- [OAuth 2.0 Authorization Guide](https://developers.google.com/identity/protocols/oauth2)
- [Google Cloud Console](https://console.cloud.google.com/)

## 📝 License

Open source. Feel free to adapt and reuse for client projects.

---

**Why this project makes you stand out on Upwork:**
✅ End-to-end solution (Google Sheets API + Python + Frontend)
✅ Production-ready code with security best practices
✅ Professional UI/UX with responsive design
✅ Demonstrates full-stack skills
✅ Easy to customize for different client needs

**Next Steps:**
1. Connect your real Google Sheet data
2. Take screenshots and add to your Upwork portfolio
3. Use as reference when pitching KPI dashboard projects
4. Adapt colors/layout for each client

