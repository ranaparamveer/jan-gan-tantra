# Jan-Gan-Tantra Documentation

Welcome to the Jan-Gan-Tantra documentation! This guide will help you get started with the platform.

## 📚 Documentation Structure

### Getting Started
- **[README.md](../README.md)** - Project overview, features, and quick start
- **[QUICKSTART.md](../QUICKSTART.md)** - Quick reference for common commands
- **[SETUP.md](../SETUP.md)** - Complete setup guide (Docker & local development)

### Technical Documentation
- **[TECH_STACK.md](TECH_STACK.md)** - Technology decisions and rationale
- **[API_GUIDE.md](API_GUIDE.md)** - API endpoints with examples
- **[PROJECT_COMPLETION.md](PROJECT_COMPLETION.md)** - Full project report

### Contributing
- **[CONTRIBUTING.md](../CONTRIBUTING.md)** - How to contribute
- **[LICENSE](../LICENSE)** - AGPL-3.0 license

---

## 🚀 Quick Links

### For Developers
1. [Setup Guide](../SETUP.md) - Get the platform running
2. [API Documentation](API_GUIDE.md) - Integrate with the API
3. [Tech Stack](TECH_STACK.md) - Understand the architecture

### For Contributors
1. [Contributing Guide](../CONTRIBUTING.md) - How to help
2. [Project Status](PROJECT_COMPLETION.md) - What's been built
3. [Task List](../.gemini/antigravity/brain/f7a6c126-bc2b-428a-bedc-c829744ed10d/task.md) - Remaining work

### For Users
1. [Quick Start](../QUICKSTART.md) - Common commands
2. [Swagger UI](http://localhost:8000/swagger/) - Interactive API testing
3. [Frontend](http://localhost:3000) - Web interface

---

## 📖 Key Concepts

### Three Core Modules

**1. Solution Wiki** - Knowledge base of civic solutions
- Search for step-by-step guides
- Access RTI templates
- Learn from success stories

**2. Gov-Graph** - Government accountability mapping
- Navigate bureaucratic hierarchy
- Find responsible officers
- Track escalation paths

**3. Pulse Dashboard** - Real-time issue tracking
- Interactive heatmap
- Geospatial clustering
- Analytics and trends

### AI-Powered Features

- **Translation**: 22+ Indian languages (Bhashini)
- **Voice Input**: Speak your problem (Whisper)
- **Jargon Simplifier**: Plain language conversion (Llama 3)
- **Smart Drafting**: Auto-generate letters (LLM)
- **Semantic Search**: Intelligent search (pgvector)

---

## 🔧 Development Workflow

### 1. Setup
```bash
./start.sh
```

### 2. Test
```bash
./test.sh
```

### 3. Develop
- Backend: `docker-compose logs -f api`
- Frontend: `cd apps/web && npm run dev`

### 4. Deploy
See [SETUP.md](../SETUP.md#production-deployment)

---

## 📊 Project Stats

- **40+ REST API endpoints**
- **13 database models**
- **10 AI services**
- **5 React components**
- **85+ files**
- **~8,200 lines of code**

---

## 🆘 Getting Help

- **Swagger UI**: http://localhost:8000/swagger/ (interactive API docs)
- **GitHub Issues**: Report bugs and request features
- **Documentation**: This folder

---

## 📝 API Overview

### Core Endpoints

**Wiki**:
- `GET /api/wiki/solutions/` - Search solutions
- `POST /api/wiki/solutions/{id}/upvote/` - Upvote solution

**Gov-Graph**:
- `GET /api/govgraph/officers/find_responsible/` - Find officer
- `GET /api/govgraph/officers/{id}/escalation_ladder/` - Get escalation path

**Issues**:
- `POST /api/issues/issues/` - Report issue
- `GET /api/issues/issues/heatmap/` - Get heatmap data

**AI Services**:
- `POST /api/ai/translate/` - Translate text
- `POST /api/ai/voice-to-text/` - Transcribe audio
- `POST /api/ai/simplify-jargon/` - Simplify text
- `GET /api/ai/search/` - Semantic search

See [API_GUIDE.md](API_GUIDE.md) for detailed examples.

---

**Built with ❤️ for India** 🇮🇳
