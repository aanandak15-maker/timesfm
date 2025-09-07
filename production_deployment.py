"""
Production Deployment Configuration for AgriForecast.ai
Docker, hosting, and performance optimization setup
"""

import os
import json
import subprocess
from typing import Dict, List, Optional
import streamlit as st
from datetime import datetime

class ProductionConfig:
    """Production deployment configuration"""
    
    def __init__(self):
        self.app_name = "agriforecast-ai"
        self.version = "1.0.0"
        self.environment = "production"
        
    def generate_dockerfile(self) -> str:
        """Generate optimized Dockerfile for production"""
        dockerfile_content = """
# Multi-stage build for AgriForecast.ai Production
FROM python:3.9-slim as builder

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    build-essential \\
    curl \\
    software-properties-common \\
    git \\
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Production stage
FROM python:3.9-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0
ENV STREAMLIT_SERVER_HEADLESS=true
ENV STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

# Create non-root user
RUN groupadd -r agriforecast && useradd -r -g agriforecast agriforecast

# Set working directory
WORKDIR /app

# Copy Python packages from builder
COPY --from=builder /usr/local/lib/python3.9/site-packages/ /usr/local/lib/python3.9/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p /app/cache /app/logs /app/data && \\
    chown -R agriforecast:agriforecast /app

# Switch to non-root user
USER agriforecast

# Expose port
EXPOSE 8501

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \\
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

# Start application
CMD ["streamlit", "run", "agriforecast_modern.py", "--server.port=8501", "--server.address=0.0.0.0"]
"""
        return dockerfile_content
    
    def generate_docker_compose(self) -> str:
        """Generate Docker Compose for full stack deployment"""
        compose_content = """
version: '3.8'

services:
  # Frontend Streamlit App
  frontend:
    build: .
    container_name: agriforecast-frontend
    ports:
      - "8501:8501"
    environment:
      - FASTAPI_BACKEND_URL=http://backend:8000
      - ENVIRONMENT=production
      - REDIS_URL=redis://redis:6379
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
    depends_on:
      - backend
      - redis
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8501/_stcore/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  # FastAPI Backend
  backend:
    build:
      context: .
      dockerfile: Dockerfile.backend
    container_name: agriforecast-backend
    ports:
      - "8000:8000"
    environment:
      - ENVIRONMENT=production
      - DATABASE_URL=postgresql://postgres:password@postgres:5432/agriforecast
      - REDIS_URL=redis://redis:6379
    volumes:
      - ./models:/app/models
      - ./data:/app/data
    depends_on:
      - postgres
      - redis
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  # PostgreSQL Database
  postgres:
    image: postgres:13
    container_name: agriforecast-db
    environment:
      - POSTGRES_DB=agriforecast
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql
    ports:
      - "5432:5432"
    restart: unless-stopped

  # Redis for caching
  redis:
    image: redis:7-alpine
    container_name: agriforecast-redis
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    restart: unless-stopped

  # Nginx Reverse Proxy
  nginx:
    image: nginx:alpine
    container_name: agriforecast-nginx
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - frontend
      - backend
    restart: unless-stopped

volumes:
  postgres_data:
  redis_data:
"""
        return compose_content
    
    def generate_nginx_config(self) -> str:
        """Generate Nginx configuration for production"""
        nginx_config = """
events {
    worker_connections 1024;
}

http {
    upstream frontend {
        server frontend:8501;
    }
    
    upstream backend {
        server backend:8000;
    }
    
    # Rate limiting
    limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
    limit_req_zone $binary_remote_addr zone=app:10m rate=30r/s;
    
    server {
        listen 80;
        server_name agriforecast.ai www.agriforecast.ai;
        
        # Redirect HTTP to HTTPS
        return 301 https://$server_name$request_uri;
    }
    
    server {
        listen 443 ssl http2;
        server_name agriforecast.ai www.agriforecast.ai;
        
        # SSL Configuration
        ssl_certificate /etc/nginx/ssl/cert.pem;
        ssl_certificate_key /etc/nginx/ssl/key.pem;
        ssl_protocols TLSv1.2 TLSv1.3;
        ssl_ciphers HIGH:!aNULL:!MD5;
        
        # Security headers
        add_header X-Frame-Options DENY;
        add_header X-Content-Type-Options nosniff;
        add_header X-XSS-Protection "1; mode=block";
        add_header Strict-Transport-Security "max-age=31536000; includeSubDomains";
        
        # Gzip compression
        gzip on;
        gzip_types text/plain text/css application/json application/javascript text/xml application/xml;
        
        # Frontend (Streamlit)
        location / {
            limit_req zone=app burst=20 nodelay;
            
            proxy_pass http://frontend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            
            # WebSocket support for Streamlit
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
            proxy_read_timeout 86400;
        }
        
        # Backend API
        location /api/ {
            limit_req zone=api burst=10 nodelay;
            
            proxy_pass http://backend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
        
        # Static files caching
        location ~* \\.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
            expires 1y;
            add_header Cache-Control "public, immutable";
        }
        
        # Health check
        location /health {
            access_log off;
            return 200 "healthy\\n";
            add_header Content-Type text/plain;
        }
    }
}
"""
        return nginx_config
    
    def generate_requirements_txt(self) -> str:
        """Generate production requirements.txt"""
        requirements = """
# Core Framework
streamlit==1.28.0
fastapi==0.104.0
uvicorn[standard]==0.24.0

# Database
sqlalchemy==2.0.0
psycopg2-binary==2.9.7
alembic==1.12.0

# Data Processing
pandas==2.1.0
numpy==1.24.0
plotly==5.17.0

# Machine Learning
scikit-learn==1.3.0
torch==2.0.0
transformers==4.33.0

# Caching & Performance
redis==4.6.0
streamlit-cache==0.1.0

# Monitoring & Logging
structlog==23.1.0
prometheus-client==0.17.0

# Security
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4

# HTTP & API
httpx==0.24.0
aiohttp==3.8.5
requests==2.31.0

# Configuration
python-dotenv==1.0.0
pydantic==2.3.0
pydantic-settings==2.0.0

# Production
gunicorn==21.2.0
gevent==23.7.0
"""
        return requirements

    def generate_kubernetes_deployment(self) -> str:
        """Generate Kubernetes deployment configuration"""
        k8s_config = """
apiVersion: apps/v1
kind: Deployment
metadata:
  name: agriforecast-frontend
  labels:
    app: agriforecast-frontend
spec:
  replicas: 3
  selector:
    matchLabels:
      app: agriforecast-frontend
  template:
    metadata:
      labels:
        app: agriforecast-frontend
    spec:
      containers:
      - name: frontend
        image: agriforecast/frontend:latest
        ports:
        - containerPort: 8501
        env:
        - name: FASTAPI_BACKEND_URL
          value: "http://agriforecast-backend:8000"
        - name: ENVIRONMENT
          value: "production"
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "1Gi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /_stcore/health
            port: 8501
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /_stcore/health
            port: 8501
          initialDelaySeconds: 5
          periodSeconds: 5

---
apiVersion: v1
kind: Service
metadata:
  name: agriforecast-frontend
spec:
  selector:
    app: agriforecast-frontend
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8501
  type: LoadBalancer

---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: agriforecast-backend
  labels:
    app: agriforecast-backend
spec:
  replicas: 2
  selector:
    matchLabels:
      app: agriforecast-backend
  template:
    metadata:
      labels:
        app: agriforecast-backend
    spec:
      containers:
      - name: backend
        image: agriforecast/backend:latest
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: db-secret
              key: url
        resources:
          requests:
            memory: "1Gi"
            cpu: "500m"
          limits:
            memory: "2Gi"
            cpu: "1000m"

---
apiVersion: v1
kind: Service
metadata:
  name: agriforecast-backend
spec:
  selector:
    app: agriforecast-backend
  ports:
  - protocol: TCP
    port: 8000
    targetPort: 8000
"""
        return k8s_config

class PerformanceOptimizer:
    """Production performance optimization"""
    
    def __init__(self):
        self.optimizations = []
    
    def optimize_streamlit_config(self) -> str:
        """Generate optimized Streamlit configuration"""
        config = """
[global]
developmentMode = false
showWarningOnDirectExecution = false

[server]
port = 8501
enableCORS = false
enableXsrfProtection = true
maxUploadSize = 200
maxMessageSize = 200
enableWebsocketCompression = true
headless = true

[browser]
gatherUsageStats = false
serverAddress = "0.0.0.0"

[client]
caching = true
displayEnabled = true

[runner]
magicEnabled = true
installTracer = false
fixMatplotlib = true
postScriptGC = true
fastReruns = true

[theme]
primaryColor = "#4CAF50"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
font = "sans serif"
"""
        return config
    
    def generate_monitoring_config(self) -> Dict:
        """Generate monitoring and logging configuration"""
        return {
            'prometheus': {
                'enabled': True,
                'port': 9090,
                'metrics': [
                    'request_duration_seconds',
                    'request_count',
                    'active_users',
                    'prediction_latency',
                    'cache_hit_rate'
                ]
            },
            'logging': {
                'level': 'INFO',
                'format': 'json',
                'handlers': ['console', 'file'],
                'file_rotation': '1GB',
                'retention_days': 30
            },
            'alerts': {
                'high_cpu': 80,
                'high_memory': 85,
                'low_disk_space': 90,
                'api_error_rate': 5
            }
        }
    
    def generate_security_config(self) -> Dict:
        """Generate security configuration"""
        return {
            'authentication': {
                'jwt_secret': 'CHANGE_THIS_IN_PRODUCTION',
                'token_expiry': 86400,
                'refresh_token_expiry': 604800
            },
            'rate_limiting': {
                'api_requests_per_minute': 100,
                'login_attempts_per_hour': 10,
                'upload_requests_per_hour': 50
            },
            'cors': {
                'allowed_origins': ['https://agriforecast.ai'],
                'allowed_methods': ['GET', 'POST', 'PUT', 'DELETE'],
                'allowed_headers': ['Content-Type', 'Authorization']
            },
            'ssl': {
                'enforce_https': True,
                'hsts_max_age': 31536000,
                'certificate_path': '/etc/ssl/certs/cert.pem',
                'private_key_path': '/etc/ssl/private/key.pem'
            }
        }

class DeploymentManager:
    """Manages production deployment process"""
    
    def __init__(self):
        self.config = ProductionConfig()
        self.optimizer = PerformanceOptimizer()
    
    def generate_deployment_files(self, output_dir: str = "deployment"):
        """Generate all deployment files"""
        os.makedirs(output_dir, exist_ok=True)
        
        # Docker files
        with open(f"{output_dir}/Dockerfile", "w") as f:
            f.write(self.config.generate_dockerfile())
        
        with open(f"{output_dir}/docker-compose.yml", "w") as f:
            f.write(self.config.generate_docker_compose())
        
        with open(f"{output_dir}/nginx.conf", "w") as f:
            f.write(self.config.generate_nginx_config())
        
        # Kubernetes
        with open(f"{output_dir}/k8s-deployment.yaml", "w") as f:
            f.write(self.config.generate_kubernetes_deployment())
        
        # Configuration files
        with open(f"{output_dir}/requirements.txt", "w") as f:
            f.write(self.config.generate_requirements_txt())
        
        with open(f"{output_dir}/.streamlit/config.toml", "w") as f:
            os.makedirs(f"{output_dir}/.streamlit", exist_ok=True)
            f.write(self.optimizer.optimize_streamlit_config())
        
        # Configuration JSONs
        with open(f"{output_dir}/monitoring.json", "w") as f:
            json.dump(self.optimizer.generate_monitoring_config(), f, indent=2)
        
        with open(f"{output_dir}/security.json", "w") as f:
            json.dump(self.optimizer.generate_security_config(), f, indent=2)
        
        return output_dir
    
    def create_deployment_script(self, output_dir: str = "deployment") -> str:
        """Create deployment script"""
        script_content = """#!/bin/bash

echo "🚀 AgriForecast.ai Production Deployment"
echo "========================================"

# Set variables
APP_NAME="agriforecast-ai"
VERSION="1.0.0"
REGISTRY="your-registry.com"

# Build and tag images
echo "📦 Building Docker images..."
docker build -t $REGISTRY/$APP_NAME-frontend:$VERSION .
docker build -f Dockerfile.backend -t $REGISTRY/$APP_NAME-backend:$VERSION .

# Push to registry
echo "📤 Pushing to registry..."
docker push $REGISTRY/$APP_NAME-frontend:$VERSION
docker push $REGISTRY/$APP_NAME-backend:$VERSION

# Deploy with Docker Compose
echo "🚀 Deploying with Docker Compose..."
docker-compose down
docker-compose pull
docker-compose up -d

# Wait for services
echo "⏳ Waiting for services to start..."
sleep 30

# Health checks
echo "🏥 Running health checks..."
curl -f http://localhost:8501/_stcore/health || echo "❌ Frontend health check failed"
curl -f http://localhost:8000/health || echo "❌ Backend health check failed"

echo "✅ Deployment complete!"
echo "🌐 Frontend: http://localhost:8501"
echo "🔗 Backend: http://localhost:8000"
echo "📊 Monitoring: http://localhost:9090"
"""
        
        script_path = f"{output_dir}/deploy.sh"
        with open(script_path, "w") as f:
            f.write(script_content)
        
        # Make executable
        os.chmod(script_path, 0o755)
        
        return script_path

# Streamlit integration
def render_deployment_dashboard():
    """Render production deployment dashboard"""
    st.title("🚀 Production Deployment Center")
    
    deployment_manager = DeploymentManager()
    
    # Deployment options
    st.subheader("📦 Deployment Options")
    
    deployment_type = st.selectbox(
        "Choose Deployment Type",
        ["Docker Compose", "Kubernetes", "Cloud Provider", "VPS/Dedicated Server"]
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🔧 Configuration")
        
        # Environment settings
        env = st.selectbox("Environment", ["production", "staging", "development"])
        ssl_enabled = st.checkbox("Enable SSL/HTTPS", value=True)
        monitoring_enabled = st.checkbox("Enable Monitoring", value=True)
        auto_scaling = st.checkbox("Enable Auto-scaling", value=True if deployment_type == "Kubernetes" else False)
        
        # Resource settings
        st.write("**Resource Allocation:**")
        frontend_replicas = st.number_input("Frontend Replicas", min_value=1, max_value=10, value=3)
        backend_replicas = st.number_input("Backend Replicas", min_value=1, max_value=5, value=2)
        
    with col2:
        st.subheader("📊 Estimated Resources")
        
        # Calculate resource requirements
        total_cpu = (frontend_replicas * 0.5) + (backend_replicas * 1.0)
        total_memory = (frontend_replicas * 1) + (backend_replicas * 2)
        
        st.metric("Total CPU", f"{total_cpu} cores")
        st.metric("Total Memory", f"{total_memory} GB")
        st.metric("Storage", "50 GB minimum")
        
        # Cost estimation
        if deployment_type == "Cloud Provider":
            estimated_cost = total_cpu * 30 + total_memory * 15  # Rough AWS pricing
            st.metric("Est. Monthly Cost", f"${estimated_cost:.0f}")
    
    # Generate deployment files
    st.subheader("📁 Generate Deployment Files")
    
    if st.button("🏗️ Generate Deployment Configuration"):
        with st.spinner("Generating deployment files..."):
            output_dir = deployment_manager.generate_deployment_files()
            script_path = deployment_manager.create_deployment_script(output_dir)
            
            st.success(f"✅ Deployment files generated in: {output_dir}")
            
            # Show generated files
            st.write("**Generated Files:**")
            generated_files = [
                "Dockerfile",
                "docker-compose.yml", 
                "nginx.conf",
                "k8s-deployment.yaml",
                "requirements.txt",
                ".streamlit/config.toml",
                "monitoring.json",
                "security.json",
                "deploy.sh"
            ]
            
            for file in generated_files:
                st.write(f"• {file}")
    
    # Deployment commands
    st.subheader("🚀 Deployment Commands")
    
    if deployment_type == "Docker Compose":
        st.code("""
# Clone repository
git clone https://github.com/your-repo/agriforecast-ai.git
cd agriforecast-ai

# Build and deploy
chmod +x deployment/deploy.sh
./deployment/deploy.sh

# Check status
docker-compose ps
docker-compose logs -f
        """, language="bash")
    
    elif deployment_type == "Kubernetes":
        st.code("""
# Apply Kubernetes manifests
kubectl apply -f deployment/k8s-deployment.yaml

# Check deployment status
kubectl get deployments
kubectl get pods
kubectl get services

# Port forwarding for testing
kubectl port-forward service/agriforecast-frontend 8501:80
        """, language="bash")
    
    # Monitoring and maintenance
    st.subheader("📊 Production Monitoring")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.write("**Health Checks**")
        st.write("• Frontend: /_stcore/health")
        st.write("• Backend: /health")
        st.write("• Database: Custom query")
    
    with col2:
        st.write("**Monitoring URLs**")
        st.write("• Prometheus: :9090")
        st.write("• Grafana: :3000") 
        st.write("• Logs: /var/log/agriforecast")
    
    with col3:
        st.write("**Backup Strategy**")
        st.write("• Database: Daily")
        st.write("• Models: Weekly")
        st.write("• Configs: Version control")
    
    # Security checklist
    with st.expander("🔒 Production Security Checklist"):
        security_items = [
            "SSL/TLS certificates configured",
            "Environment variables secured",
            "Database credentials encrypted", 
            "API rate limiting enabled",
            "CORS properly configured",
            "Security headers implemented",
            "Regular security updates",
            "Backup encryption enabled",
            "Access logs monitored",
            "Firewall rules configured"
        ]
        
        for item in security_items:
            st.checkbox(item, key=f"security_{item}")

# Demo function
def demo_production_deployment():
    """Demo the production deployment dashboard"""
    render_deployment_dashboard()

if __name__ == "__main__":
    demo_production_deployment()
