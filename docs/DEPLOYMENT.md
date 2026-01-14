# Deployment Guide

## Deployment Options

### Option 1: Local Docker (Recommended)

See Commit 12 for Docker setup.

### Option 2: Cloud VM (AWS/GCP/Azure)

#### Requirements
- VM with 8GB+ RAM
- Ubuntu 20.04 or later
- Python 3.9+

#### Steps

1. **Provision VM**
```bash
   # Example: AWS EC2 t3.large or GCP n1-standard-2
```

2. **Install Dependencies**
```bash
   sudo apt update
   sudo apt install -y python3-pip python3-venv git
```

3. **Clone and Setup**
```bash
   git clone https://github.com/yourusername/shopassist-rag.git
   cd shopassist-rag
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
```

4. **Configure Environment**
```bash
   cp .env.example .env
   nano .env  # Add API keys
```

5. **Setup Data** (one-time)
```bash
   python scripts/download_data.py
   python scripts/generate_policies.py
   python scripts/process_data.py
   python scripts/build_vector_store.py
```

6. **Run Application**
```bash
   # Option A: API
   nohup python src/api.py > api.log 2>&1 &
   
   # Option B: Streamlit
   nohup streamlit run app.py --server.port 8501 --server.address 0.0.0.0 > app.log 2>&1 &
```

7. **Configure Firewall**
```bash
   # Allow API port
   sudo ufw allow 8000
   # Allow Streamlit port
   sudo ufw allow 8501
```

### Option 3: Serverless (Modal, RunPod)

**Coming Soon**: Serverless deployment guide for cost-effective hosting.

### Option 4: Container Services (ECS, Cloud Run, App Engine)

**Coming Soon**: Container orchestration deployment guide.

## Production Considerations

### Security
- [ ] Add API authentication (API keys, OAuth)
- [ ] Implement rate limiting
- [ ] Configure CORS properly
- [ ] Use HTTPS/SSL certificates
- [ ] Secure environment variables
- [ ] Set up firewall rules

### Monitoring
- [ ] Set up logging (CloudWatch, Stackdriver)
- [ ] Add error tracking (Sentry)
- [ ] Monitor API usage
- [ ] Track costs (OpenAI API)
- [ ] Set up alerts

### Performance
- [ ] Use distributed cache (Redis)
- [ ] Implement load balancing
- [ ] Add CDN for static assets
- [ ] Optimize vector store queries
- [ ] Consider GPU for faster inference

### Scaling
- [ ] Horizontal scaling (multiple instances)
- [ ] Database for caching (instead of files)
- [ ] Message queue for async processing
- [ ] Separate embedding/LLM services
- [ ] Auto-scaling policies

## Cost Optimization

### Reduce OpenAI Costs
- Use caching aggressively
- Implement query deduplication
- Use smaller embedding models when possible
- Batch embeddings efficiently
- Set reasonable rate limits

### Infrastructure Costs
- Use spot instances when possible
- Right-size your VMs
- Implement auto-scaling
- Use serverless for variable traffic
- Monitor and optimize resource usage

## Maintenance

### Regular Tasks
- Monitor API costs
- Check error logs
- Update dependencies
- Backup vector store
- Clear old cache files

### Updates
```bash
git pull origin main
pip install -r requirements.txt
# Restart services
```

## Support

For deployment issues:
1. Check logs: `api.log`, `app.log`
2. Verify environment variables
3. Test with curl/Postman
4. Check firewall settings
5. Review cloud provider docs