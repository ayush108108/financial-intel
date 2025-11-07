# Deployment Guide - Financial Intelligence Platform

This guide covers deploying Financial Intelligence to production environments including Docker, DigitalOcean, AWS, and self-hosted options.

---

## Table of Contents
- [Prerequisites](#prerequisites)
- [Local Deployment](#local-deployment)
- [Docker Deployment](#docker-deployment)
- [DigitalOcean Deployment](#digitalocean-deployment)
- [AWS Deployment](#aws-deployment)
- [Self-Hosted (VPS)](#self-hosted-vps)
- [Database Setup](#database-setup)
- [Monitoring & Maintenance](#monitoring--maintenance)
- [Troubleshooting](#troubleshooting)

---

## Prerequisites

- **Docker** (18.09+) and **Docker Compose** (1.24+)
- **PostgreSQL** (14+) or **Supabase** account
- **Domain name** (optional, for production)
- **SSL certificate** (for production)

---

## Local Deployment

### Quick Start (Docker)

```bash
# 1. Clone repository
git clone https://github.com/ayush108108/financial-intel.git
cd financial-intel

# 2. Configure environment
cp .env.example .env
# Edit .env with your Supabase credentials

# 3. Start all services
docker-compose up -d

# 4. Initialize database
docker-compose exec backend python -m backend.api.db.init

# 5. Run first pipeline
docker-compose exec backend python scripts/pipelines/daily_eod_pipeline.py
```

**Access Points:**
- API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Frontend: http://localhost:80
- Database: localhost:5432

### Manual Setup (No Docker)

```bash
# 1. Clone and install
git clone https://github.com/ayush108108/financial-intel.git
cd financial-intel
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 2. Configure
cp .env.example .env
# Edit .env

# 3. Start API server
cd backend
python run.py &

# 4. Start frontend (in another terminal)
cd frontend-v2
npm install
npm run dev &

# 5. Run pipeline manually
python ../scripts/pipelines/daily_eod_pipeline.py
```

---

## Docker Deployment

### Using docker-compose.yml

The repository includes a production-ready `docker-compose.yml`:

```bash
# Build and start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Full cleanup (includes volumes!)
docker-compose down -v
```

**Services:**
- `backend`: FastAPI API server
- `frontend`: Vue 3 + Nginx frontend
- `postgres`: PostgreSQL database (optional, if using local DB)
- `nginx`: Reverse proxy

### Build Custom Images

```bash
# Build backend image
cd backend
docker build -t financial-intel-backend:latest .

# Build frontend image
cd ../frontend-v2
docker build -t financial-intel-frontend:latest .
```

### Push to Docker Registry

```bash
# Tag images
docker tag financial-intel-backend:latest yourregistry/financial-intel-backend:latest
docker tag financial-intel-frontend:latest yourregistry/financial-intel-frontend:latest

# Push to Docker Hub or private registry
docker push yourregistry/financial-intel-backend:latest
docker push yourregistry/financial-intel-frontend:latest
```

---

## DigitalOcean Deployment

### Option 1: App Platform (Recommended)

**DigitalOcean App Platform** is the easiest way to deploy.

1. **Create Supabase Database**
   - Sign up at https://supabase.com (free tier)
   - Create new project
   - Note your connection credentials

2. **Push Code to GitHub**
   ```bash
   git remote add origin https://github.com/yourusername/financial-intel.git
   git push -u origin main
   ```

3. **Create App on DigitalOcean**
   - Go to DigitalOcean Console → App Platform
   - Click "Create App"
   - Select GitHub repository
   - Configure components:
     - **Backend** (`backend/`)
       - Runtime: Python/FastAPI
       - Build command: `pip install -r requirements.txt`
       - Run command: `python run.py`
       - HTTP port: 8000
       - Add env vars from `.env.example`
     
     - **Frontend** (`frontend-v2/`)
       - Runtime: Node.js
       - Build command: `npm install && npm run build`
       - HTTP port: 80
       - Set `VITE_API_URL=https://api.yourapp.com`

   - Configure environment variables in DO Console

4. **Schedule Pipeline Runs**
   - Use DO Functions or cron jobs to run `daily_eod_pipeline.py`
   - Or use GitHub Actions (see CI/CD section)

### Option 2: Droplet + Docker

1. **Create Droplet**
   ```bash
   # Ubuntu 22.04 LTS, 4GB RAM, $24/month recommended
   # SSH into droplet
   ssh root@your_droplet_ip
   ```

2. **Install Docker & Docker Compose**
   ```bash
   apt update && apt upgrade -y
   apt install -y docker.io docker-compose
   usermod -aG docker $USER
   ```

3. **Clone and Deploy**
   ```bash
   cd /opt
   git clone https://github.com/ayush108108/financial-intel.git
   cd financial-intel
   
   # Configure environment
   cp .env.example .env
   nano .env  # Edit with your credentials
   
   # Start services
   docker-compose up -d
   ```

4. **Setup Reverse Proxy (Nginx)**
   ```bash
   apt install -y nginx certbot python3-certbot-nginx
   
   # Configure Nginx (create /etc/nginx/sites-available/financial-intel)
   sudo nano /etc/nginx/sites-available/financial-intel
   ```

   **Nginx Config:**
   ```nginx
   upstream backend {
       server 127.0.0.1:8000;
   }
   
   upstream frontend {
       server 127.0.0.1:3000;
   }
   
   server {
       listen 80;
       server_name api.yourapp.com;
       
       location / {
           proxy_pass http://backend;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   
   server {
       listen 80;
       server_name yourapp.com;
       
       location / {
           proxy_pass http://frontend;
           proxy_set_header Host $host;
       }
   }
   ```

5. **Enable SSL**
   ```bash
   sudo certbot --nginx -d api.yourapp.com -d yourapp.com
   ```

---

## AWS Deployment

### Option 1: AWS ECS (Elastic Container Service)

1. **Push Images to ECR**
   ```bash
   # Create ECR repository
   aws ecr create-repository --repository-name financial-intel-backend
   aws ecr create-repository --repository-name financial-intel-frontend
   
   # Build and push
   docker build -t financial-intel-backend:latest backend/
   docker tag financial-intel-backend:latest \
     123456789.dkr.ecr.us-east-1.amazonaws.com/financial-intel-backend:latest
   docker push 123456789.dkr.ecr.us-east-1.amazonaws.com/financial-intel-backend:latest
   ```

2. **Create RDS Database**
   - Go to RDS Console → Create Database
   - Engine: PostgreSQL 14
   - Multi-AZ deployment for HA
   - Note connection string

3. **Create ECS Cluster**
   - Create Fargate cluster
   - Create task definition for backend and frontend
   - Configure environment variables
   - Set up load balancer

### Option 2: AWS Lambda (Serverless Pipeline)

```python
# lambda_function.py
import json
from scripts.pipelines.daily_eod_pipeline import run_daily_pipeline

def lambda_handler(event, context):
    try:
        result = run_daily_pipeline()
        return {
            'statusCode': 200,
            'body': json.dumps(result)
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
```

Deploy with AWS CloudFormation or AWS SAM CLI.

---

## Self-Hosted (VPS)

### Hetzner / Linode / Vultr Setup

1. **Create VPS**
   - OS: Ubuntu 22.04 LTS
   - Specs: 4GB RAM, 2vCPU, 100GB SSD (minimum)
   - SSH key-based auth

2. **Setup Server**
   ```bash
   ssh root@your_vps_ip
   
   # System updates
   apt update && apt upgrade -y
   apt install -y curl wget git htop
   
   # Install Docker
   curl -fsSL https://get.docker.com -o get-docker.sh
   sh get-docker.sh
   docker run hello-world
   
   # Install Docker Compose
   curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" \
     -o /usr/local/bin/docker-compose
   chmod +x /usr/local/bin/docker-compose
   ```

3. **Deploy Application**
   ```bash
   # Create app directory
   mkdir -p /srv/financial-intel
   cd /srv/financial-intel
   
   # Clone repository
   git clone https://github.com/ayush108108/financial-intel.git .
   
   # Configure
   cp .env.example .env
   nano .env  # Edit configuration
   
   # Start services
   docker-compose up -d
   ```

4. **Setup SSL with Let's Encrypt**
   ```bash
   apt install -y nginx certbot python3-certbot-nginx
   certbot certonly --standalone -d api.yourapp.com -d yourapp.com
   ```

---

## Database Setup

### Supabase (Recommended for Cloud)

1. Sign up at https://supabase.com
2. Create new project
3. Run SQL migrations:
   ```bash
   # From Supabase dashboard → SQL Editor
   psql -h your_host -U postgres -d your_db -f scripts/db/schema.sql
   ```

### Self-Hosted PostgreSQL

```bash
# Using Docker
docker run -d \
  --name financial-intel-db \
  -e POSTGRES_DB=financial_intel \
  -e POSTGRES_PASSWORD=your_secure_password \
  -v postgres_data:/var/lib/postgresql/data \
  -p 5432:5432 \
  postgres:14

# Initialize schema
docker exec financial-intel-db psql -U postgres -d financial_intel \
  -f /scripts/db/schema.sql
```

---

## Monitoring & Maintenance

### Health Checks

```bash
# Check API health
curl http://localhost:8000/health

# Check database connection
curl http://localhost:8000/api/health/db

# Check pipeline status
docker-compose logs backend | grep "Tier"
```

### Automated Backups

```bash
# Daily backup script
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
pg_dump financial_intel | gzip > /backups/backup_$DATE.sql.gz

# Keep only last 7 days
find /backups -name "backup_*.sql.gz" -mtime +7 -delete
```

### Log Rotation

```bash
# Logrotate configuration
cat > /etc/logrotate.d/financial-intel <<EOF
/var/log/financial-intel/*.log {
    daily
    rotate 7
    compress
    delaycompress
    notifempty
    create 0640 root root
}
EOF
```

### Monitoring Tools

- **Uptime**: Use UptimeRobot or Pingdom for HTTP checks
- **Logs**: Send to ELK Stack, Datadog, or Splunk
- **Metrics**: Collect with Prometheus, ship to Grafana
- **Alerts**: Configure Slack/email notifications

---

## Troubleshooting

### Issue: "Cannot connect to database"

```bash
# Check Supabase credentials
export SUPABASE_URL="your_url"
export SUPABASE_SERVICE_KEY="your_key"
psql postgresql://postgres.xxxxx:password@xxxxx.pooler.supabase.com:6543/postgres

# If local DB:
docker-compose logs postgres
```

### Issue: "API returning 502 Bad Gateway"

```bash
# Check backend logs
docker-compose logs backend

# Restart backend
docker-compose restart backend

# Check port conflict
lsof -i :8000
```

### Issue: "Pipeline not running on schedule"

```bash
# Check GitHub Actions logs
git log --oneline

# Verify cron configuration
docker-compose exec backend crontab -l

# Manually run pipeline
docker-compose exec backend python scripts/pipelines/daily_eod_pipeline.py
```

### Issue: "Out of memory"

```bash
# Increase Docker memory limit in docker-compose.yml
services:
  backend:
    mem_limit: 2g  # Increase from default

# Or restart with higher limit
docker run --memory=4g ...
```

---

## Production Checklist

- [ ] Environment variables configured (no hardcoded secrets)
- [ ] SSL certificates installed and auto-renewed
- [ ] Database backups automated (daily)
- [ ] Monitoring and alerts configured
- [ ] Log aggregation enabled
- [ ] Rate limiting configured
- [ ] CORS policies restricted
- [ ] Health checks running
- [ ] Performance benchmarks established
- [ ] Disaster recovery plan documented

---

## Support

- **Issues**: https://github.com/ayush108108/financial-intel/issues
- **Discussions**: https://github.com/ayush108108/financial-intel/discussions
- **Email**: ayush@example.com

---

For more details on specific infrastructure providers, see provider-specific guides in `docs/deployment/`.
