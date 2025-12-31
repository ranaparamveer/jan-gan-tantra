# Jan-Gan-Tantra (People's System)

**A civic-tech platform empowering Indian citizens to navigate bureaucracy, hold authorities accountable, and solve civic problems collectively.**

---

## 🎯 Vision

Jan-Gan-Tantra transforms the citizen-government relationship by providing:
- **Actionable Knowledge**: Search engine for civic solutions, not just problems
- **Accountability Mapping**: Visual hierarchy of who is responsible for what
- **Collective Action**: Cluster analysis to identify systemic issues

---

## 🏗️ Architecture

### Three Core Modules

1. **Solution Wiki** (Knowledge Layer)
   - Searchable "How-To" guides for civic issues
   - RTI templates and complaint letter generators
   - Crowdsourced "Success Paths" from citizens

2. **Gov-Graph** (Accountability Layer)
   - Hierarchical mapping of Indian bureaucracy
   - Designation-to-officer mapping with contact details
   - Visual escalation ladder for complaints

3. **Pulse Dashboard** (Visual Layer)
   - Geospatial heatmaps of unresolved issues
   - Cluster detection for systemic problems
   - Accountability scorecards for departments

---

## 🛠️ Tech Stack

| Component | Technology | Why? |
|-----------|-----------|------|
| Frontend | Next.js 15 | SEO-friendly, PWA support, fast |
| Backend | Django 5.1 | Complex data relationships, GIS support |
| Database | PostgreSQL 16 + PostGIS | Geospatial queries, vector search |
| Search | MeiliSearch | Typo-tolerant, multi-language |
| Maps | Leaflet + OpenStreetMap | Free, customizable |
| AI Translation | Bhashini API | Indian language support |
| Voice Input | OpenAI Whisper | Accurate for Indian accents |
| LLM | Llama 3 8B (Ollama) | Self-hosted, privacy-focused |
| Deployment | Docker + Coolify | Self-hostable, low cost |

---

## 🚀 Getting Started

### Prerequisites
- Docker & Docker Compose
- Node.js 20+
- Python 3.12+

### Quick Start

```bash
# Clone repository
git clone https://github.com/ranaparamveer/jan-gan-tantra.git
cd jan-gan-tantra

# Setup environment
cp .env.example .env
# Edit .env and add your API keys (Bhashini, OpenAI)

# Start all services
./start.sh

# Access the platform
# Frontend: http://localhost:3000
# API: http://localhost:8000
# Swagger: http://localhost:8000/swagger/
```

For detailed setup instructions, see [SETUP.md](SETUP.md).

### Development Setup

```bash
# Backend
cd apps/api
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver

# Frontend
cd apps/web
npm install
npm run dev
```

---

## 📱 Key Features

### 🔍 Solution Wiki
- **500+ Civic Solutions**: Step-by-step guides for common problems
- **Smart Templates**: AI-generated RTI applications and complaint letters
- **Success Stories**: Crowdsourced resolution paths
- **22+ Languages**: Full multi-language support via Bhashini

### 🏛️ Gov-Graph
- **Government Hierarchy**: Complete org chart (national to municipal)
- **Officer Finder**: Locate the right official for any issue
- **Escalation Ladders**: Know who to contact next
- **Accountability Scorecards**: A+ to F grading for departments
- **Directory Scraper**: Auto-populate from NIC/municipal websites

### 📍 Pulse Dashboard
- **Interactive Heatmap**: Real-time civic issues on maps
- **Geospatial Clustering**: Group nearby similar issues
- **Issue Tracking**: Report, upvote, monitor resolution
- **Analytics**: Statistics on types, rates, hotspots

### 🤖 AI Services (10 Endpoints)
- **Translation** (Bhashini): 22+ Indian languages
- **Voice Input** (Whisper): Speak in any language
- **Jargon Simplifier**: Convert legalese to plain language
- **Smart Drafting**: Auto-generate formal letters
- **Document Summarizer**: Condense long PDFs
- **RTI Generator**: Create RTI applications
- **Semantic Search**: AI-powered intelligent search
- **Similar Solutions**: Find related guides
- **Issue Clustering**: Group similar problems

### 📱 User Experience
- **Voice-Enabled Search**: Speak or type
- **PWA Support**: Install on mobile
- **Responsive Design**: Desktop, tablet, mobile
- **Offline Capable**: Works without internet

---

## 🗺️ Status

✅ **Phase 1**: Foundation & Architecture (100%)  
✅ **Phase 2**: Core Modules - Wiki, Gov-Graph, Dashboard (100%)  
✅ **Phase 3**: AI Integration - Translation, Voice, LLM, Semantic Search (100%)  
✅ **Phase 4**: Frontend - Search, Map, Solutions Browser (95%)  
⏳ **Phase 5**: Data Seeding & Testing (20%)  
⏳ **Phase 6**: Public Beta Launch (Planned)

**Current Stats**:
- 40+ REST API endpoints
- 13 database models
- 10 AI services
- 5 React components
- 85+ files, ~8,200 lines of code

**Ready for**: Beta testing and deployment

---

## 🤝 Contributing

We welcome contributions! This is an open-source project built for public good.

### Areas We Need Help
- **Data Collection**: Scraping government directories (NIC, state portals)
- **Translation**: Improving Bhashini prompts for regional languages
- **UI/UX**: Mobile-first design for low-literacy users
- **Legal**: Reviewing RTI templates for accuracy

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## 📄 License

**AGPL-3.0** - This project must remain open-source. Any modifications or hosted versions must also be open-sourced.

---

## 🙏 Acknowledgments

- Inspired by civic-tech movements like [I Paid A Bribe](https://ipaidabribe.com/)
- Built on open-source tools from the global commons
- Powered by the Indian developer community

---

## 📞 Contact

- **Issues**: [GitHub Issues](https://github.com/yourusername/jan-gan-tantra/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/jan-gan-tantra/discussions)
- **Email**: contact@jan-gan-tantra.org

---

**"Empowering citizens, one solution at a time."**
