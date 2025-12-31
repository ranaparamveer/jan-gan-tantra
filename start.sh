#!/bin/bash

echo "🚀 Jan-Gan-Tantra Quick Start"
echo "=============================="
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "📝 Creating .env file from example..."
    cp .env.example .env
    echo "✅ .env created. Please update with your API keys."
    echo ""
fi

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker and try again."
    exit 1
fi

echo "🐳 Starting Docker services..."
docker compose up -d --build

echo ""
echo "⏳ Waiting for services to be healthy..."
sleep 10
docker compose exec api python manage.py makemigrations wiki govgraph issues ai
docker compose exec api python manage.py migrate
docker compose exec api python manage.py seed_data
docker compose exec api python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@example.com', 'admin'); user = User.objects.get(username='admin'); user.set_password('admin'); user.save()"

echo ""
echo "⏳ Waiting for services to be healthy..."
sleep 10

echo ""
echo "✅ Services started!"
echo ""
echo "📍 Access points:"
echo "   Frontend:  http://localhost:3000"
echo "   API:       http://localhost:8000"
echo "   Admin:     http://localhost:8000/admin"
echo "   Search:    http://localhost:7700"
echo ""
echo "📚 Next steps:"
echo "   1. Run migrations: docker-compose exec api python manage.py migrate"
echo "   2. Create superuser: docker-compose exec api python manage.py createsuperuser"
echo "   3. Visit http://localhost:3000"
echo ""
echo "🛑 To stop: docker compose down"
