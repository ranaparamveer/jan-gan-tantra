# Tech Stack Decision Document

## Overview
This document explains the technology choices for Jan-Gan-Tantra, prioritizing **open-source**, **self-hostable**, and **cost-effective** solutions suitable for civic infrastructure.

---

## Frontend: Next.js 15

### Why Next.js?
- **SEO Critical**: Civic content must be discoverable via Google
- **PWA Support**: Works offline for users with poor connectivity
- **Server Components**: Reduces JavaScript bundle size for low-end phones
- **App Router**: Modern routing with built-in layouts

### Alternatives Considered
- **Vite + React**: Lacks built-in SSR/SEO
- **SvelteKit**: Smaller ecosystem, harder to find contributors
- **Remix**: Similar to Next.js but smaller community

### Decision: Next.js 15 with App Router

---

## Backend: Django 5.1

### Why Django?
- **Batteries Included**: Admin panel, ORM, authentication out-of-the-box
- **GIS Support**: GeoDjango for PostGIS integration (critical for heatmaps)
- **REST Framework**: Mature ecosystem for API development
- **Python Ecosystem**: Easy integration with AI libraries (Whisper, Llama)

### Alternatives Considered
- **FastAPI**: Faster but lacks admin panel and GIS support
- **Express.js**: Would require more boilerplate for complex data models
- **Rails**: Ruby has weaker AI/ML ecosystem

### Decision: Django 5.1 + Django REST Framework

---

## Database: PostgreSQL 16 + PostGIS + pgvector

### Why PostgreSQL?
- **PostGIS Extension**: Industry standard for geospatial data
- **pgvector Extension**: Vector embeddings for semantic search
- **JSONB Support**: Flexible schema for government hierarchy data
- **Reliability**: Battle-tested for civic infrastructure

### Alternatives Considered
- **MongoDB**: No native geospatial indexing like PostGIS
- **MySQL**: Weaker GIS support, no vector search
- **SQLite**: Not suitable for production geospatial queries

### Decision: PostgreSQL 16 with PostGIS + pgvector

---

## Search: MeiliSearch

### Why MeiliSearch?
- **Typo Tolerance**: Critical for Indian language searches
- **Multi-Language**: Built-in support for Hindi, Tamil, etc.
- **Fast Setup**: Easier than Elasticsearch
- **Low Resource**: Runs on cheap VPS

### Alternatives Considered
- **Elasticsearch**: Overkill, resource-intensive
- **Typesense**: Similar to MeiliSearch but smaller community
- **PostgreSQL Full-Text**: Lacks typo tolerance and ranking

### Decision: MeiliSearch

---

## Maps: Leaflet + OpenStreetMap

### Why Leaflet?
- **Free**: No API costs (unlike Google Maps)
- **Customizable**: Full control over styling
- **Lightweight**: Works on low-end devices
- **OSM Data**: Community-maintained, no vendor lock-in

### Alternatives Considered
- **Google Maps**: $200/month for expected traffic
- **Mapbox**: Free tier too limited
- **MapLibre**: Similar to Leaflet, less mature

### Decision: Leaflet with OpenStreetMap tiles

---

## AI Stack

### Translation: Bhashini API

**Why?**
- Government-backed initiative for Indian languages
- Free for non-commercial use
- Supports 22+ Indian languages

**Fallback**: Meta's NLLB (self-hosted)

---

### Voice Input: OpenAI Whisper

**Why?**
- Best accuracy for Indian accents
- Open-source (can self-host)
- Supports Hindi, Tamil, Bengali natively

**Deployment**: Self-hosted via `faster-whisper` (optimized)

---

### LLM: Llama 3 8B via Ollama

**Why?**
- Runs on consumer GPU (RTX 3060)
- Privacy-focused (no data sent to OpenAI)
- Good at Indian English and code-switching

**Use Cases**:
- Simplifying government jargon
- Drafting complaint letters
- Summarizing long PDFs

**Fallback**: Gemini Flash (for complex queries)

---

### Semantic Search: pgvector

**Why?**
- Integrated with PostgreSQL (no extra service)
- Fast vector similarity search
- Works with any embedding model

**Embedding Model**: `sentence-transformers/paraphrase-multilingual-mpnet-base-v2`

---

## Deployment

### Development: Docker Compose

**Why?**
- Single command to start all services
- Consistent across team members
- Easy to add new services (Redis, Celery)

---

### Production: Coolify

**Why?**
- Open-source Heroku alternative
- Self-hosted on any VPS
- Built-in SSL, backups, monitoring
- Cost: ~$10/month (DigitalOcean droplet)

**Alternatives Considered**:
- **Vercel + Railway**: $50+/month for expected scale
- **AWS ECS**: Too complex for small team
- **Bare Metal**: Requires DevOps expertise

---

## Cost Breakdown (Monthly)

| Service | Cost | Notes |
|---------|------|-------|
| VPS (8GB RAM) | $10 | DigitalOcean/Hetzner |
| Domain | $1 | .org domain |
| Backups | $2 | S3-compatible storage |
| **Total** | **$13** | Scales to 10K users |

**AI Costs**:
- Bhashini: Free (government API)
- Whisper: Self-hosted (no cost)
- Llama 3: Self-hosted (no cost)

---

## Scalability Plan

### 10K Users
- Current stack handles this easily
- Single VPS with 8GB RAM

### 100K Users
- Add Redis caching
- Separate database server
- CDN for static assets (Cloudflare free tier)
- Cost: ~$50/month

### 1M Users
- Kubernetes cluster
- Read replicas for database
- Managed MeiliSearch
- Cost: ~$500/month

---

## Security Considerations

1. **Data Privacy**
   - No user tracking
   - Optional anonymous submissions
   - Self-hosted AI (no data sent to third parties)

2. **DDOS Protection**
   - Cloudflare free tier
   - Rate limiting on API

3. **Data Integrity**
   - Daily backups to S3
   - Point-in-time recovery (PostgreSQL)

---

## Open Source Licenses

| Component | License | Compatibility |
|-----------|---------|---------------|
| Next.js | MIT | ✅ |
| Django | BSD | ✅ |
| PostgreSQL | PostgreSQL License | ✅ |
| MeiliSearch | MIT | ✅ |
| Leaflet | BSD | ✅ |
| Whisper | MIT | ✅ |
| Llama 3 | Llama 3 License | ✅ (non-commercial) |

**Project License**: AGPL-3.0 (ensures all forks remain open-source)

---

## Decision Log

| Date | Decision | Rationale |
|------|----------|-----------|
| 2025-12-31 | Next.js over Vite | SEO + PWA critical |
| 2025-12-31 | Django over FastAPI | GIS support needed |
| 2025-12-31 | MeiliSearch over Elasticsearch | Easier setup, lower cost |
| 2025-12-31 | Llama 3 over GPT-4 | Privacy + cost |

---

**Last Updated**: 2025-12-31  
**Maintainer**: Jan-Gan-Tantra Core Team
