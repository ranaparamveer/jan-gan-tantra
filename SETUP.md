# Jan-Gan-Tantra: Complete Setup Guide

## Quick Start (5 minutes)

### Prerequisites
- Docker & Docker Compose installed
- Git installed

### Steps

1. **Clone and setup**
```bash
git clone https://github.com/ranaparamveer/jan-gan-tantra.git
cd jan-gan-tantra
cp .env.example .env
```

2. **Start all services**
```bash
./start.sh
```

3. **Access the platform**
- Frontend: http://localhost:3000
- API: http://localhost:8000
- Swagger Docs: http://localhost:8000/swagger/
- Django Admin: http://localhost:8000/admin

---

## Detailed Setup

### Option 1: Docker (Recommended)

#### 1. Environment Configuration

Edit `.env` file:
```bash
# Required for AI features
BHASHINI_API_KEY=your_bhashini_key_here
OPENAI_API_KEY=your_openai_key_here

# Database (auto-configured in Docker)
DATABASE_URL=postgresql://jgt_user:jgt_dev_password@db:5432/jan_gan_tantra

# Django
DJANGO_SECRET_KEY=change-this-in-production
DEBUG=True
```

#### 2. Start Services

```bash
docker-compose up -d
```

#### 3. Run Migrations

```bash
docker-compose exec api python manage.py makemigrations
docker-compose exec api python manage.py migrate
```

#### 4. Create Superuser

```bash
docker-compose exec api python manage.py createsuperuser
```

#### 5. (Optional) Load Sample Data

```bash
docker-compose exec api python manage.py loaddata fixtures/sample_data.json
```

---

### Option 2: Local Development

#### Backend Setup

1. **Install Python 3.12+**

2. **Setup PostgreSQL with PostGIS**
```bash
# Ubuntu/Debian
sudo apt-get install postgresql-16 postgis

# macOS
brew install postgresql@16 postgis

# Create database
createdb jan_gan_tantra
psql jan_gan_tantra -c "CREATE EXTENSION postgis;"
psql jan_gan_tantra -c "CREATE EXTENSION vector;"
```

3. **Install Python dependencies**
```bash
cd apps/api
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

4. **Run migrations**
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

5. **Start Django**
```bash
python manage.py runserver
```

#### Frontend Setup

1. **Install Node.js 20+**

2. **Install dependencies**
```bash
cd apps/web
npm install
```

3. **Start Next.js**
```bash
npm run dev
```

#### Additional Services

**MeiliSearch** (for search):
```bash
docker run -d -p 7700:7700 \
  -e MEILI_ENV=development \
  -e MEILI_MASTER_KEY=dev_master_key \
  getmeili/meilisearch:v1.6
```

**Redis** (for Celery):
```bash
docker run -d -p 6379:6379 redis:7-alpine
```

**Ollama** (for LLM, optional):
```bash
curl https://ollama.ai/install.sh | sh
ollama pull llama3
ollama serve
```

---

## API Keys Setup

### 1. Bhashini (Translation)

1. Visit https://bhashini.gov.in/
2. Register for API access
3. Get your API key
4. Add to `.env`: `BHASHINI_API_KEY=your_key`

### 2. OpenAI (Voice & LLM fallback)

1. Visit https://platform.openai.com/
2. Create API key
3. Add to `.env`: `OPENAI_API_KEY=your_key`

**Note**: OpenAI is optional if you use Ollama for LLM

---

## Testing the Setup

### 1. Test Backend API

```bash
curl http://localhost:8000/api/wiki/categories/
```

Expected: JSON list of categories

### 2. Test AI Services

**Translation**:
```bash
curl -X POST http://localhost:8000/api/ai/translate/ \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello", "source_lang": "en", "target_lang": "hi"}'
```

**Jargon Simplification**:
```bash
curl -X POST http://localhost:8000/api/ai/simplify-jargon/ \
  -H "Content-Type: application/json" \
  -d '{"text": "As per Section 4(1)(d)...", "language": "en"}'
```

### 3. Test Frontend

Visit http://localhost:3000 and:
- Try voice search (click microphone icon)
- Search for "garbage collection"
- View issues on the map

---

## Production Deployment

### Using Coolify (Recommended)

1. **Install Coolify** on your VPS:
```bash
curl -fsSL https://cdn.coollabs.io/coolify/install.sh | bash
```

2. **Configure Environment**:
- Set production `DJANGO_SECRET_KEY`
- Set `DEBUG=False`
- Configure production database
- Add domain name

3. **Deploy**:
- Connect Git repository
- Coolify auto-deploys on push

### Manual Deployment

1. **Build Docker images**:
```bash
docker-compose -f docker-compose.prod.yml build
```

2. **Run migrations**:
```bash
docker-compose -f docker-compose.prod.yml run api python manage.py migrate
```

3. **Collect static files**:
```bash
docker-compose -f docker-compose.prod.yml run api python manage.py collectstatic --noinput
```

4. **Start services**:
```bash
docker-compose -f docker-compose.prod.yml up -d
```

---

## Troubleshooting

### Database Connection Errors

**Error**: `could not connect to server`

**Solution**:
```bash
# Check if PostgreSQL is running
docker-compose ps

# Restart database
docker-compose restart db

# Check logs
docker-compose logs db
```

### Frontend Build Errors

**Error**: `Module not found`

**Solution**:
```bash
cd apps/web
rm -rf node_modules .next
npm install
npm run dev
```

### AI Service Errors

**Error**: `Translation failed`

**Solution**:
- Check if `BHASHINI_API_KEY` is set
- Verify API key is valid
- Check internet connection

**Error**: `Ollama connection refused`

**Solution**:
```bash
# Start Ollama
ollama serve

# Pull model
ollama pull llama3
```

### Port Already in Use

**Error**: `port 8000 already allocated`

**Solution**:
```bash
# Find process using port
lsof -i :8000

# Kill process
kill -9 <PID>

# Or change port in docker-compose.yml
```

---

## Performance Optimization

### For 10K+ Users

1. **Enable Redis Caching**:
```python
# settings.py
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://redis:6379/1',
    }
}
```

2. **Setup CDN** for static files (Cloudflare)

3. **Database Optimization**:
```sql
-- Add indexes
CREATE INDEX idx_issues_location ON issues USING GIST (location);
CREATE INDEX idx_issues_status ON issues (status);
```

4. **Enable Gunicorn** (production):
```bash
gunicorn core.wsgi:application --workers 4 --bind 0.0.0.0:8000
```

---

## Monitoring

### Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f api
docker-compose logs -f web
```

### Health Checks

```bash
# API health
curl http://localhost:8000/api/wiki/categories/

# Database health
docker-compose exec db pg_isready

# Redis health
docker-compose exec redis redis-cli ping
```

---

## Backup & Restore

### Backup Database

```bash
docker-compose exec db pg_dump -U jgt_user jan_gan_tantra > backup.sql
```

### Restore Database

```bash
docker-compose exec -T db psql -U jgt_user jan_gan_tantra < backup.sql
```

---

## Next Steps

1. **Add Sample Data**: Create solutions, categories, government hierarchy
2. **Configure Domain**: Point your domain to the server
3. **Setup SSL**: Use Let's Encrypt (Coolify does this automatically)
4. **Monitor Usage**: Setup analytics (optional)
5. **Community**: Invite users to test and provide feedback

---

## Support

- **Documentation**: See `/docs` folder
- **API Docs**: http://localhost:8000/swagger/
- **Issues**: https://github.com/ranaparamveer/jan-gan-tantra/issues

---

**Built with ❤️ for the people of India**
