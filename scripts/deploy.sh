#!/bin/bash
# Production deployment script

set -e

echo "🚀 Starting Midas API deployment..."

# Check if .env exists
if [ ! -f .env ]; then
    echo "❌ Error: .env file not found!"
    echo "📝 Please copy env.production.example to .env and configure it:"
    echo "   cp env.production.example .env"
    echo "   nano .env"
    exit 1
fi

# Load environment variables
source .env

# Validate required variables
required_vars=("SECRET_KEY" "POSTGRES_PASSWORD" "OPENAI_API_KEY")
for var in "${required_vars[@]}"; do
    if [ -z "${!var}" ]; then
        echo "❌ Error: $var is not set in .env"
        exit 1
    fi
done

# Check SECRET_KEY is not default
if [ "$SECRET_KEY" = "generate-secure-32-char-secret-key-here" ]; then
    echo "❌ Error: Please generate a secure SECRET_KEY!"
    echo "💡 Run: python -c \"import secrets; print(secrets.token_urlsafe(32))\""
    exit 1
fi

echo "✅ Environment variables validated"

# Build Docker images
echo "🔨 Building Docker images..."
docker-compose build

# Start services
echo "🐳 Starting services..."
docker-compose up -d

# Wait for database to be ready
echo "⏳ Waiting for database..."
sleep 5

# Check if services are healthy
echo "🏥 Checking service health..."
docker-compose ps

# Show logs
echo ""
echo "📋 Service logs (press Ctrl+C to stop):"
echo "   To view logs: docker-compose logs -f"
echo "   To stop: docker-compose down"
echo ""
echo "✅ Deployment complete!"
echo "🌐 API available at: http://localhost:${API_PORT:-8000}"
echo "📚 API docs: http://localhost:${API_PORT:-8000}/docs"
