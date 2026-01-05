# 📊 KPI Sales Dashboard – Google Sheets Sync

Un **dashboard professionnel** générant des KPI en temps quasi-réel à partir de Google Sheets, prêt à mettre en avant pour tes clients Upwork.

## 🎯 Qu'est-ce que c'est ?

Ce projet démontre une **solution production-ready** pour transformer des données brutes Google Sheets en un dashboard visuel avec :
- **4 KPI cards** : Revenu total, Nombre de deals, Deals gagnés, Taux de conversion
- **4 graphiques interactifs** : Revenu par canal, Distribution des statuts, Revenu par commercial, Tendance journalière
- **Filtres dynamiques** : Par canal, commercial, statut
- **Tableau de données** : Vue brute des dernières 20 lignes
- **Synchronisation automatique** : Rafraîchissement toutes les 5 minutes

## 📁 Structure

```
.
├── kpi-dashboard.html          # Dashboard HTML (prêt à utiliser)
├── api_integration.py          # Script Python pour lire/écrire Google Sheets
├── requirements.txt            # Dépendances Python
├── README.md                   # Ce fichier (français)
├── README_EN.md                # English version
└── config.example.json         # Configuration exemple
```

## 🚀 Démarrage rapide

### Option 1 : Voir le dashboard (sans code)
1. Ouvre `kpi-dashboard.html` dans un navigateur
2. Le dashboard charge avec des **données fictives** (démo)
3. Joue avec les filtres et graphiques

### Option 2 : Connecter à ton Google Sheet (recommandé pour démo Upwork)

#### Étape 1 : Préparer Google Sheets API
```bash
# 1. Va sur Google Cloud Console
# https://console.cloud.google.com/

# 2. Crée un projet et active Google Sheets API

# 3. Crée des "Credentials" :
#    - Type : "Service Account"
#    - Télécharge le fichier JSON

# 4. Partage ton Google Sheet avec l'email du service account
#    (format : xxx@xxx.iam.gserviceaccount.com)
```

#### Étape 2 : Configurer le Python script
```bash
# 1. Clone ou crée le dossier du projet
mkdir kpi-dashboard
cd kpi-dashboard

# 2. Installe les dépendances
pip install -r requirements.txt

# 3. Copie le fichier credentials JSON téléchargé
cp /chemin/vers/credentials.json ./google-credentials.json

# 4. Configure config.json
cp config.example.json config.json

# Édite config.json :
{
  "sheet_id": "15gK_hwPkhL7UIVAJxvZPU_1MR24yxV_nWKpYXg9DN1w",
  "range": "Raw_Data!A:F",
  "credentials_path": "./google-credentials.json"
}
```

#### Étape 3 : Lancer le dashboard
```bash
# Donne au dashboard accès à tes données Google Sheets
python api_integration.py

# Ouvre kpi-dashboard.html dans ton navigateur
# → Le dashboard récupère maintenant les **vraies données** de Google Sheets
```

## 🎨 Fonctionnalités

### KPI Cards
- **Total Revenue** : Somme de tous les montants
- **Total Deals** : Nombre de lignes
- **Deals Won** : Décompte des lignes avec "Gagné"
- **Conversion Rate** : (Deals Won / Total) × 100

### Graphiques
1. **Revenu par Canal** (bar chart) : Voir où vient ton revenue (SEO, Ads, Referral, Email)
2. **Distribution des Statuts** (doughnut chart) : Quel % de Gagné, Perdu, Opportunité, Lead
3. **Revenu par Commercial** (bar horizontal) : Performance de chaque membre de l'équipe
4. **Tendance Revenue** (line chart) : Évolution journalière (revenue gagnée)

### Filtres
- Filtre par **Canal** (SEO, Ads, Referral, Email)
- Filtre par **Commercial** (Alice, Bob, Carlos, etc.)
- Filtre par **Statut** (Gagné, Perdu, Opportunité, Lead)
- Bouton **Refresh** pour forcer une synchronisation immédiate

## 📊 Format de données attendu

Ton Google Sheet doit avoir cette structure (onglet `Raw_Data`) :

| Date | Client | Canal | Commercial | Montant | Statut |
|------|--------|-------|------------|---------|--------|
| 2025-01-01 | Client A | SEO | Alice | 1200 | Gagné |
| 2025-01-02 | Client B | Ads | Bob | 850 | Lead |
| ... | ... | ... | ... | ... | ... |

**Colonnes requises** :
- `Date` : format YYYY-MM-DD
- `Client` : nom du client (string)
- `Canal` : SEO / Ads / Referral / Email
- `Commercial` : nom du commercial
- `Montant` : montant numérique (euros)
- `Statut` : Gagné / Perdu / Opportunité / Lead

## 💻 Architecture technique

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
    Chart.js (graphiques)
```

### Sécurité
- **Credentials** : Stockés en variables d'environnement (`GOOGLE_CREDENTIALS_PATH`)
- **Tokens** : Service Account (pas de token refresh nécessaire)
- **API Keys** : Ne jamais committer en Git (ajouter à `.gitignore`)

## 🔧 Personnalisation

### Ajouter un nouveau KPI
Édite `kpi-dashboard.html` et ajoute une carte :
```html
<div class="kpi-card success">
    <div class="kpi-label">Ton KPI</div>
    <div class="kpi-value" id="tonKpi">0</div>
    <div class="kpi-change positive">↑ Real-time</div>
</div>
```

Puis dans le JavaScript, calcule-le :
```javascript
function updateKPICards(data) {
    const tonKpi = data.filter(row => /* ta logique */).length;
    document.getElementById('tonKpi').textContent = tonKpi;
}
```

### Changer les couleurs
Les couleurs sont en CSS (haut du fichier HTML) :
```css
header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}
```

### Ajouter une colonne de données
1. Ajoute une colonne dans ton Google Sheet
2. Mets à jour la plage API (`range: "Raw_Data!A:G"`)
3. Ajoute un filtre ou un graphique

## 🌐 Déployer sur le web

### Option A : Netlify (gratuit, recommandé)
```bash
# 1. Crée un repo GitHub avec tes fichiers
# 2. Connecte Netlify à GitHub
# 3. Ajoute les variables d'environnement en settings Netlify
# 4. Déploie automatiquement

# Ton dashboard est accessible via : https://ton-url.netlify.app
```

### Option B : Vercel
```bash
npm install -g vercel
vercel --env GOOGLE_API_KEY=xxx
```

### Option C : Serveur personnel (Docker)
```bash
docker build -t kpi-dashboard .
docker run -e GOOGLE_CREDENTIALS_PATH=/secrets/creds.json \
           -v /chemin/vers/creds.json:/secrets/creds.json \
           -p 8000:8000 kpi-dashboard
```

## 📈 SLA & Performance

| Métrique | Valeur |
|----------|--------|
| Refresh automatique | 5 min |
| Temps de sync | < 30 sec |
| Uptime cible | 95%+ |
| Rate limit Google Sheets API | 300 req/min |

## 🚨 Troubleshooting

### "Error: 401 Unauthorized"
→ Vérifier que le service account est **partagé** sur le Google Sheet

### "Error: 403 Forbidden"
→ Vérifier que Google Sheets API est **activée** dans Google Cloud Console

### Dashboard affiche "Loading data..." indéfiniment
→ Vérifier que `GOOGLE_API_KEY` est correct en variables d'environnement

## 📞 Support client Upwork

Quand un client demande "Peux-tu créer un KPI dashboard Google Sheets ?" :

1. **Montre ce projet** comme démo de ce que tu peux faire
2. **Explique le processus** :
   - "Je construis un dashboard personnalisé pour tes KPI"
   - "Données en direct depuis Google Sheets"
   - "Rafraîchissement auto toutes les 30 min"
   - "Filtres + 4-5 graphiques clés"
3. **Adapte les KPI** à son besoin spécifique (ventes, marketing, RH, ops)
4. **Propose des options** :
   - Excel Online en plus
   - Alertes par email
   - Authentification multi-user

## 📚 Ressources

- [Google Sheets API Docs](https://developers.google.com/sheets/api)
- [Chart.js Docs](https://www.chartjs.org/)
- [OAuth 2.0 Guide](https://developers.google.com/identity/protocols/oauth2)

## 📝 Licence

Libre de réutilisation. À adapter pour chaque client.

---

**Créé pour te demarquer sur Upwork en montrant une expertise complète :** 
✅ Google Sheets + API + Python + Frontend + Design

