# 🚀 Production Deployment Guide

Complete guide for deploying AI Accountant API to production.

---

## 📋 Prerequisites

- Docker & Docker Compose installed
- Domain name (optional, for HTTPS)
- OpenAI API key
- Server with at least 2GB RAM

---

## 🔧 Quick Start (Docker)

### 1. Clone & Configure

```bash
cd /path/to/midas

# Copy environment template
cp env.production.example .env

# Edit configuration
nano .env
```

### 2. Required Environment Variables

**⚠️ MUST CHANGE THESE:**

```bash
# Generate secure secret key
SECRET_KEY=$(python -c "import secrets; print(secrets.token_urlsafe(32))")

# Database password
POSTGRES_PASSWORD=your_secure_db_password

# OpenAI API key
OPENAI_API_KEY=sk-your-real-openai-key

# Your domain
CORS_ORIGINS=https://yourdomain.com,https://app.yourdomain.com
```

### 3. Deploy

```bash
# Option A: Using deploy script
./scripts/deploy.sh

# Option B: Manual Docker Compose
docker-compose up -d
```

### 4. Verify

```bash
# Check services
docker-compose ps

# View logs
docker-compose logs -f api

# Test API
curl http://localhost:8000/health
```

API will be available at: **http://localhost:8000**

---

## 🌐 Production Deployment Options

### Option 1: Docker Compose (Recommended)

**Pros:** Simple, includes PostgreSQL, easy to manage
**Best for:** Small-medium deployments, VPS hosting

```bash
# Start with Nginx reverse proxy
docker-compose --profile production up -d

# Without Nginx (if using external reverse proxy)
docker-compose up -d
```

### Option 2: Cloud Platforms

#### Heroku

```bash
# Install Heroku CLI
heroku create midas-api

# Add PostgreSQL
heroku addons:create heroku-postgresql:mini

# Set environment variables
heroku config:set SECRET_KEY=your-secret-key
heroku config:set OPENAI_API_KEY=sk-...
heroku config:set CORS_ORIGINS=https://yourfrontend.com

# Deploy
git push heroku main
```

#### Railway.app

1. Connect GitHub repository
2. Add PostgreSQL database
3. Set environment variables in dashboard
4. Deploy automatically

#### DigitalOcean App Platform

1. Create new app from GitHub
2. Add managed PostgreSQL database
3. Configure environment variables
4. Deploy

#### Render

1. Create new Web Service
2. Add PostgreSQL database
3. Set environment variables
4. Auto-deploy on git push

---

## 🔐 Security Checklist

### Before Production:

- [ ] ✅ Generate secure `SECRET_KEY` (32+ characters)
- [ ] ✅ Use strong `POSTGRES_PASSWORD`
- [ ] ✅ Set correct `CORS_ORIGINS` (your frontend domain)
- [ ] ✅ Never commit `.env` file
- [ ] ✅ Enable HTTPS (SSL/TLS)
- [ ] ✅ Set up firewall rules
- [ ] ✅ Enable database backups
- [ ] ✅ Monitor API logs

### Generate Secure Secrets:

```bash
# SECRET_KEY
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Database password
python -c "import secrets; print(secrets.token_urlsafe(24))"
```

---

## 📁 File Structure

```
midas/
├── .env                    # Your production config (CREATE THIS!)
├── env.production.example  # Template
├── docker-compose.yml      # Docker orchestration
├── Dockerfile             # API container
├── nginx.conf             # Reverse proxy (optional)
├── schema.sql             # Database schema
└── scripts/
    └── deploy.sh          # Deployment script
```

---

## 🗄️ Database Setup

### Auto-initialization (Docker)

Database schema is automatically applied on first run.

### Manual Setup (Non-Docker)

```bash
# Create database
createdb midas_db

# Apply schema
psql -U postgres -d midas_db -f schema.sql

# (Optional) Add sample data
python scripts/generate_sample_data.py
psql -U postgres -d midas_db -f sample_data.sql
```

---

## 🌍 Domain & HTTPS Setup

### Using Nginx (Included)

1. **Get SSL Certificate** (Let's Encrypt):

```bash
# Install certbot
sudo apt-get install certbot

# Get certificate
sudo certbot certonly --standalone -d yourdomain.com

# Certificates will be in /etc/letsencrypt/live/yourdomain.com/
```

2. **Update nginx.conf**:

```nginx
server {
    listen 443 ssl http2;
    server_name yourdomain.com;
    
    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
    
    # ... rest of config
}
```

3. **Mount certificates in docker-compose.yml**:

```yaml
nginx:
  volumes:
    - /etc/letsencrypt:/etc/nginx/ssl:ro
```

4. **Restart Nginx**:

```bash
docker-compose restart nginx
```

### Using External Reverse Proxy (Caddy/Traefik)

If using external proxy, just run API without Nginx:

```bash
docker-compose up -d db api
```

**Caddy example**:
```caddy
yourdomain.com {
    reverse_proxy localhost:8000
}
```

---

## 📊 Monitoring

### View Logs

```bash
# All services
docker-compose logs -f

# API only
docker-compose logs -f api

# Database only
docker-compose logs -f db

# Last 100 lines
docker-compose logs --tail=100 api
```

### Health Checks

```bash
# API health
curl http://localhost:8000/health

# Database health
docker-compose exec db pg_isready -U postgres
```

### Container Status

```bash
# List containers
docker-compose ps

# Resource usage
docker stats
```

---

## 🔄 Updates & Maintenance

### Update Application

```bash
# Pull latest changes
git pull

# Rebuild and restart
docker-compose up -d --build

# Or using script
./scripts/deploy.sh
```

### Database Backup

```bash
# Backup
docker-compose exec db pg_dump -U postgres midas_db > backup.sql

# Restore
docker-compose exec -T db psql -U postgres midas_db < backup.sql
```

### Clean Up

```bash
# Stop services
docker-compose down

# Remove volumes (CAUTION: deletes database!)
docker-compose down -v

# Remove images
docker-compose down --rmi all
```

---

## 🐛 Troubleshooting

### API won't start

```bash
# Check logs
docker-compose logs api

# Common issues:
# 1. Missing environment variables
# 2. Database not ready (wait 10s and retry)
# 3. Port 8000 already in use
```

### Database connection failed

```bash
# Check database is running
docker-compose ps db

# Check DATABASE_URL format
# Should be: postgresql+asyncpg://user:pass@db:5432/dbname

# Test connection
docker-compose exec db psql -U postgres -d midas_db -c "SELECT 1;"
```

### OpenAI API errors

```bash
# Verify API key is set
docker-compose exec api env | grep OPENAI

# Test AI endpoint
curl -X POST http://localhost:8000/ai/parse-transaction \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "text=test"
```

---

## 📈 Scaling

### Increase Workers

Edit `docker-compose.yml`:

```yaml
api:
  command: uvicorn api.main:app --host 0.0.0.0 --workers 4
```

### Database Connection Pooling

Already configured in `api/database.py`:
- Pool size: 10
- Max overflow: 20

### Load Balancing

Use Nginx upstream with multiple API instances:

```nginx
upstream api {
    server api1:8000;
    server api2:8000;
    server api3:8000;
}
```

---

## 💰 Cost Estimates

### Cloud Hosting (Monthly)

- **Heroku**: $7 (Hobby tier) + $9 (PostgreSQL) = **$16/mo**
- **Railway**: $5-20 depending on usage
- **DigitalOcean**: $12 (Droplet) + $15 (Database) = **$27/mo**
- **Render**: $7 (Web Service) + $7 (PostgreSQL) = **$14/mo**
- **VPS (DigitalOcean/Linode)**: $6-12/mo (self-managed)

### OpenAI Costs

- Text parsing: ~$0.0001 per request
- Voice (Whisper): ~$0.006 per minute
- Expected: **$5-20/mo** for moderate usage

---

## 📞 Support & Next Steps

### After Deployment:

1. ✅ Test all endpoints at `/docs`
2. ✅ Create first user via `/auth/register`
3. ✅ Add sample data (optional)
4. ✅ Connect frontend application
5. ✅ Set up monitoring/alerts
6. ✅ Configure backups

### Frontend Integration:

```javascript
// Example: Connect React/Vue app
const API_URL = 'https://api.yourdomain.com';

// Register user
fetch(`${API_URL}/auth/register`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    username: 'user',
    email: 'user@example.com',
    password: 'password123'
  })
});
```

---

## ✅ Deployment Checklist

- [ ] Copy `env.production.example` to `.env`
- [ ] Generate secure `SECRET_KEY`
- [ ] Set `POSTGRES_PASSWORD`
- [ ] Add `OPENAI_API_KEY`
- [ ] Configure `CORS_ORIGINS`
- [ ] Run `docker-compose up -d`
- [ ] Verify health: `curl localhost:8000/health`
- [ ] Test registration: `/docs`
- [ ] Set up HTTPS (production)
- [ ] Configure backups
- [ ] Set up monitoring

---

**🎉 You're all set! Your AI Accountant API is production-ready!**

For questions or issues, check logs with `docker-compose logs -f`
