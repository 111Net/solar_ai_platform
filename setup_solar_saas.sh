#!/bin/bash
# ===========================
# Extended Solar AI SaaS Setup
# Fully automated: Git + backend + frontend + Docker + AI modules + CI/CD
# WARNING: Resets Git history and overwrites remote repo!
# ===========================

# --- CONFIGURE THESE ---
GITHUB_URL="git@github.com:111Net/solar_ai_platform.git"  # Replace with your repo
SERVER_IP="192.168.111.129"   # Replace with deployment server IP
DOCKER_USERNAME="aakinyanju@gmail.com"
DOCKER_PASSWORD="2780@inas"
# ===========================

echo "?? Starting extended Solar AI SaaS setup..."

# 1?? Ensure main branch
git checkout main || git checkout -b main

# 2?? Stage current changes
git add -A
git commit -m "Master commit: initialize full Solar AI SaaS platform structure" || echo "No changes to commit"

# 3?? Reset Git history
echo "?? Resetting Git history..."
rm -rf .git
git init
git branch -M main
git add -A
git commit -m "Initial commit: production-ready Solar AI SaaS"

# 4?? Add GitHub remote and push
git remote add origin $GITHUB_URL
git push -u origin main --force

# 5?? Create backend/frontend structure
echo "?? Creating project structure..."
mkdir -p backend/app/routers backend/app/models backend/app/services backend/app/utils frontend/src/{components,pages,services,hooks}

# 6?? Create initial files
touch backend/requirements.txt backend/Dockerfile backend/app/main.py backend/app/services/ai_engine.py
touch frontend/package.json frontend/Dockerfile frontend/src/App.jsx

# 7?? Populate backend/requirements.txt
cat <<EOL > backend/requirements.txt
fastapi
uvicorn[standard]
pydantic
requests
python-multipart
jinja2
aiofiles
redis
psycopg2-binary
EOL

# 8?? Populate backend/Dockerfile
cat <<EOL > backend/Dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app ./app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
EOL

# 9?? Create initial AI engine stub
cat <<EOL > backend/app/services/ai_engine.py
def optimize_solar(roof_area, location, energy_consumption, tariff):
    """
    Stub for AI solar optimization.
    Returns a dummy result.
    """
    return {
        "panels_needed": int(roof_area / 1.6),
        "expected_kwh_per_year": int(energy_consumption * 1.1),
        "roi_years": 5
    }
EOL

# 10?? Populate frontend/package.json
cat <<EOL > frontend/package.json
{
  "name": "solar-ai-frontend",
  "version": "0.1.0",
  "private": true,
  "dependencies": {
    "react": "^19.2.4",
    "react-dom": "^19.2.4",
    "react-scripts": "5.0.1",
    "recharts": "^2.7.0",
    "axios": "^1.5.0"
  },
  "scripts": {
    "start": "react-scripts start",
    "build": "react-scripts build"
  }
}
EOL

# 11?? Populate frontend/Dockerfile
cat <<EOL > frontend/Dockerfile
FROM node:20
WORKDIR /app
COPY package.json package-lock.json* ./
RUN npm install
COPY . .
RUN npm run build
CMD ["npx", "serve", "-s", "build", "-l", "3000"]
EOL

# 12?? Create App.jsx stub
cat <<EOL > frontend/src/App.jsx
import React from 'react';

function App() {
  return (
    <div>
      <h1>Solar AI SaaS Dashboard</h1>
      <p>Frontend ready and connected to backend.</p>
    </div>
  );
}

export default App;
EOL

# 13?? Create docker-compose.yml
cat <<EOL > docker-compose.yml
version: "3.9"
services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgres://saas:secret@db:5432/solar
      - REDIS_URL=redis://redis:6379
    depends_on:
      - db
      - redis

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"

  db:
    image: postgres:16
    environment:
      POSTGRES_USER: saas
      POSTGRES_PASSWORD: secret
      POSTGRES_DB: solar
    volumes:
      - db_data:/var/lib/postgresql/data

  redis:
    image: redis:7
    ports:
      - "6379:6379"

volumes:
  db_data:
EOL

# 14?? Create CI/CD workflow
mkdir -p .github/workflows
cat <<EOL > .github/workflows/deploy.yml
name: CI/CD Pipeline

on:
  push:
    branches: [main]

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Setup Docker
        uses: docker/setup-buildx-action@v2

      - name: Build Docker images
        run: docker-compose -f docker-compose.yml build --no-cache

      - name: Push images
        run: |
          echo "$DOCKER_PASSWORD" | docker login -u "$DOCKER_USERNAME" --password-stdin
          docker-compose -f docker-compose.yml push

      - name: Deploy to server
        run: ssh ubuntu@$SERVER_IP "cd ~/solar_ai_platform && docker-compose pull && docker-compose up -d"
EOL

# 15?? Install backend dependencies locally
echo "?? Installing FastAPI dependencies locally..."
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r backend/requirements.txt
deactivate

# 16?? Install frontend dependencies locally
echo "?? Installing React frontend dependencies..."
cd frontend
npm install
cd ..

# 17?? Final Git commit
git add -A
git commit -m "Setup backend, frontend, AI engine, Docker, and CI/CD"
git push origin main --force

echo "? Extended Solar AI SaaS setup complete!"
echo "Run 'docker-compose up -d' to start backend + frontend + Postgres + Redis"