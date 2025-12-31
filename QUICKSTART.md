# Jan-Gan-Tantra: Quick Reference

## 🚀 Start the Platform

```bash
./start.sh
```

## 🔗 Access URLs

- **Frontend**: http://localhost:3000
- **API**: http://localhost:8000
- **Swagger Docs**: http://localhost:8000/swagger/
- **Django Admin**: http://localhost:8000/admin
- **MeiliSearch**: http://localhost:7700

## 🧪 Test Everything

```bash
./test.sh
```

## 📦 Key Commands

### Backend (Django)
```bash
# Run migrations
docker-compose exec api python manage.py migrate

# Create superuser
docker-compose exec api python manage.py createsuperuser

# Shell
docker-compose exec api python manage.py shell

# Logs
docker-compose logs -f api
```

### Frontend (Next.js)
```bash
cd apps/web
npm run dev          # Development
npm run build        # Production build
npm run start        # Production server
```

### Database
```bash
# Access PostgreSQL
docker-compose exec db psql -U jgt_user jan_gan_tantra

# Backup
docker-compose exec db pg_dump -U jgt_user jan_gan_tantra > backup.sql

# Restore
docker-compose exec -T db psql -U jgt_user jan_gan_tantra < backup.sql
```

## 🔧 Common Issues

### Port Already in Use
```bash
# Find process
lsof -i :8000

# Kill process
kill -9 <PID>
```

### Reset Everything
```bash
docker-compose down -v
docker-compose up -d
docker-compose exec api python manage.py migrate
```

### Frontend Build Errors
```bash
cd apps/web
rm -rf node_modules .next
npm install
```

## 📝 API Examples

### Translation
```bash
curl -X POST http://localhost:8000/api/ai/translate/ \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello", "source_lang": "en", "target_lang": "hi"}'
```

### Voice to Text
```bash
curl -X POST http://localhost:8000/api/ai/voice-to-text/ \
  -F "audio_file=@recording.wav" \
  -F "language=hi"
```

### Simplify Jargon
```bash
curl -X POST http://localhost:8000/api/ai/simplify-jargon/ \
  -H "Content-Type: application/json" \
  -d '{"text": "As per Section 4(1)(d)...", "language": "en"}'
```

### Report Issue
```bash
curl -X POST http://localhost:8000/api/issues/issues/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Broken street light",
    "description": "Street light not working for 2 weeks",
    "category": 1,
    "location": {"type": "Point", "coordinates": [77.2090, 28.6139]}
  }'
```

## 🌐 Environment Variables

Required in `.env`:
```bash
# AI Services
BHASHINI_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here

# Django
DJANGO_SECRET_KEY=change-in-production
DEBUG=True

# Database (auto-configured in Docker)
DATABASE_URL=postgresql://jgt_user:jgt_dev_password@db:5432/jan_gan_tantra
```

## 📚 Documentation

- [SETUP.md](SETUP.md) - Complete setup guide
- [API_GUIDE.md](docs/API_GUIDE.md) - API documentation
- [PROJECT_COMPLETION.md](docs/PROJECT_COMPLETION.md) - Project report
- [CONTRIBUTING.md](CONTRIBUTING.md) - How to contribute

## 🆘 Get Help

- **Swagger UI**: http://localhost:8000/swagger/ (interactive API testing)
- **Django Admin**: http://localhost:8000/admin (content management)
- **Logs**: `docker-compose logs -f`
- **Issues**: https://github.com/ranaparamveer/jan-gan-tantra/issues

---

**Built with ❤️ for India** 🇮🇳
