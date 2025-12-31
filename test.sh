#!/bin/bash

# Jan-Gan-Tantra - Quick Test Script
# Tests all major components of the platform

echo "🧪 Testing Jan-Gan-Tantra Platform..."
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

API_URL="http://localhost:8000"

# Test 1: Backend API
echo "1️⃣  Testing Backend API..."
response=$(curl -s -o /dev/null -w "%{http_code}" $API_URL/api/wiki/categories/)
if [ "$response" = "200" ]; then
    echo -e "${GREEN}✓ Backend API is running${NC}"
else
    echo -e "${RED}✗ Backend API failed (HTTP $response)${NC}"
fi

# Test 2: Swagger Documentation
echo "2️⃣  Testing Swagger Documentation..."
response=$(curl -s -o /dev/null -w "%{http_code}" $API_URL/swagger/)
if [ "$response" = "200" ]; then
    echo -e "${GREEN}✓ Swagger docs are accessible${NC}"
else
    echo -e "${RED}✗ Swagger docs failed (HTTP $response)${NC}"
fi

# Test 3: Translation API
echo "3️⃣  Testing Translation API..."
response=$(curl -s -X POST $API_URL/api/ai/translate/ \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello", "source_lang": "en", "target_lang": "hi"}' \
  -w "%{http_code}" -o /dev/null)
if [ "$response" = "200" ]; then
    echo -e "${GREEN}✓ Translation API is working${NC}"
else
    echo -e "${RED}✗ Translation API failed (HTTP $response)${NC}"
fi

# Test 4: Database Connection
echo "4️⃣  Testing Database Connection..."
if docker-compose exec -T db pg_isready > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Database is connected${NC}"
else
    echo -e "${RED}✗ Database connection failed${NC}"
fi

# Test 5: Redis Connection
echo "5️⃣  Testing Redis Connection..."
if docker-compose exec -T redis redis-cli ping > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Redis is connected${NC}"
else
    echo -e "${RED}✗ Redis connection failed${NC}"
fi

# Test 6: MeiliSearch
echo "6️⃣  Testing MeiliSearch..."
response=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:7700/health)
if [ "$response" = "200" ]; then
    echo -e "${GREEN}✓ MeiliSearch is running${NC}"
else
    echo -e "${RED}✗ MeiliSearch failed (HTTP $response)${NC}"
fi

# Test 7: Frontend
echo "7️⃣  Testing Frontend..."
response=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:3000)
if [ "$response" = "200" ]; then
    echo -e "${GREEN}✓ Frontend is running${NC}"
else
    echo -e "${RED}✗ Frontend failed (HTTP $response)${NC}"
fi

echo ""
echo "✅ Testing complete!"
echo ""
echo "📊 Access Points:"
echo "   Frontend: http://localhost:3000"
echo "   API: http://localhost:8000"
echo "   Swagger: http://localhost:8000/swagger/"
echo "   Admin: http://localhost:8000/admin"
