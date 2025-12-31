# Local Testing Guide (Without Docker)

Since Docker isn't installed, here's how to test locally:

## Backend Testing

### 1. Setup Virtual Environment
```bash
cd apps/api
python3.12 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 2. Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Setup PostgreSQL (if available)
```bash
# If PostgreSQL is installed locally
createdb jan_gan_tantra
psql jan_gan_tantra -c "CREATE EXTENSION postgis;"
psql jan_gan_tantra -c "CREATE EXTENSION vector;"
```

### 4. Configure Environment
```bash
cp ../../.env.example ../../.env
# Edit .env with local database URL
```

### 5. Run Migrations
```bash
export DATABASE_URL="postgresql://user:pass@localhost:5432/jan_gan_tantra"
export DJANGO_SECRET_KEY="test-secret-key"
export DEBUG=True

python manage.py makemigrations
python manage.py migrate
```

### 6. Run Tests
```bash
python manage.py test
```

### 7. Start Server
```bash
python manage.py runserver
```

## Frontend Testing

### 1. Install Dependencies
```bash
cd apps/web
npm install
```

### 2. Run Linting
```bash
npm run lint
```

### 3. Type Check
```bash
npx tsc --noEmit
```

### 4. Build
```bash
npm run build
```

### 5. Start Dev Server
```bash
npm run dev
```

## Pre-commit Hooks Testing

### 1. Install pre-commit
```bash
pip install pre-commit
```

### 2. Install hooks
```bash
cd /path/to/jan-gan-tantra
pre-commit install
```

### 3. Run all checks
```bash
pre-commit run --all-files
```

## Quick Validation (No Database Required)

### Backend
```bash
cd apps/api
python -c "import django; print(f'Django {django.VERSION}')"
python manage.py check --deploy
```

### Frontend
```bash
cd apps/web
npm run lint
npx tsc --noEmit
```

## Docker Testing (When Available)

```bash
# Install Docker first
sudo apt install docker.io docker-compose

# Then run
./start.sh
./test.sh
```

## CI Simulation

Run the same commands as CI:

### Backend
```bash
cd apps/api
pip install -r requirements.txt
python manage.py migrate
python manage.py test
flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
```

### Frontend
```bash
cd apps/web
npm audit --audit-level=high
npm install
npm run lint
npm run build
npx tsc --noEmit
```

## Results

✅ **What Works Without Docker**:
- Dependency installation
- Linting and type checking
- Build process
- Pre-commit hooks
- Code quality checks

❌ **What Needs Docker**:
- Full database integration
- PostGIS features
- Redis/Celery
- MeiliSearch
- Complete end-to-end testing

## Recommendation

For full testing, install Docker:
```bash
# Ubuntu/Debian
sudo apt install docker.io docker-compose
sudo usermod -aG docker $USER
# Log out and back in

# Then
./start.sh
```
