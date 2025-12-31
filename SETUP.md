# Jan-Gan-Tantra Development Setup

## Quick Start with Docker

1. **Copy environment variables**
   ```bash
   cp .env.example .env
   ```

2. **Start all services**
   ```bash
   docker-compose up -d
   ```

3. **Access the application**
   - Frontend: http://localhost:3000
   - API: http://localhost:8000
   - Django Admin: http://localhost:8000/admin
   - MeiliSearch: http://localhost:7700

## Local Development (Without Docker)

### Backend Setup

1. **Install Python dependencies**
   ```bash
   cd apps/api
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Setup PostgreSQL**
   - Install PostgreSQL 16 with PostGIS extension
   - Create database:
     ```bash
     createdb jan_gan_tantra
     psql jan_gan_tantra -c "CREATE EXTENSION postgis;"
     psql jan_gan_tantra -c "CREATE EXTENSION vector;"
     ```

3. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

5. **Start development server**
   ```bash
   python manage.py runserver
   ```

### Frontend Setup

1. **Install Node dependencies**
   ```bash
   cd apps/web
   npm install
   ```

2. **Start development server**
   ```bash
   npm run dev
   ```

## Project Structure

```
jan-gan-tantra/
├── apps/
│   ├── web/              # Next.js frontend
│   │   ├── app/          # App Router pages
│   │   ├── components/   # React components
│   │   └── lib/          # Utilities
│   ├── api/              # Django backend
│   │   ├── core/         # Django settings
│   │   ├── wiki/         # Solution Wiki app
│   │   ├── govgraph/     # Gov-Graph app
│   │   ├── issues/       # Issues tracking app
│   │   └── ai/           # AI services app
│   └── worker/           # Celery background tasks
├── infrastructure/
│   ├── docker/           # Dockerfiles
│   └── scripts/          # Deployment scripts
└── docs/                 # Documentation
```

## Next Steps

1. **Populate seed data**
   ```bash
   cd apps/api
   python manage.py loaddata fixtures/initial_data.json
   ```

2. **Configure AI services**
   - Get Bhashini API key from https://bhashini.gov.in/
   - (Optional) Get OpenAI API key for Whisper ASR

3. **Start building features**
   - See `docs/TECH_STACK.md` for architecture details
   - See task.md for implementation roadmap

## Troubleshooting

### Database connection errors
- Ensure PostgreSQL is running
- Check DATABASE_URL in .env file
- Verify PostGIS extension is installed

### Frontend build errors
- Clear Next.js cache: `rm -rf apps/web/.next`
- Reinstall dependencies: `npm ci`

### Docker issues
- Reset containers: `docker-compose down -v && docker-compose up -d`
- Check logs: `docker-compose logs -f`

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

AGPL-3.0 - See [LICENSE](LICENSE) for details.
