# CyBurn Digital SIRS Engine

## Enterprise Semantic Compression for Air-Gapped RAG Pipelines

[![Docker Pulls](https://img.shields.io/badge/docker-ghcr.io%2Fthedevilhimselfcodes%2Fsirs--engine-blue)](https://github.com/thedevilhimselfcodes/sirs-engine/pkgs/container/sirs-engine)
[![Version](https://img.shields.io/badge/version-1.6.0-green)](https://github.com/thedevilhimselfcodes/sirs-engine)
[![License](https://img.shields.io/badge/license-Commercial-red)](https://cyburndigital.com)

---

## 🚨 The Problem

Enterprise RAG (Retrieval-Augmented Generation) pipelines face a critical bottleneck:

- **Storage Explosion**: High-dimensional embeddings (768-1024D) consume massive database resources
- **Performance Degradation**: Vector similarity searches become slower as data grows
- **Air-Gapped Constraints**: Many enterprises cannot use cloud-based embedding services
- **Cost Proliferation**: Storing and processing full-dimensional vectors at scale is prohibitively expensive

Traditional solutions either sacrifice semantic quality for compression or require constant internet connectivity. Enterprises need a solution that **preserves semantic fidelity** while **dramatically reducing storage requirements** in **air-gapped environments**.

---

## 💡 The Solution: SIRS Engine

**SIRS (Semantic Intelligent Reduction System)** is CyBurn Digital's enterprise-grade vector compression middleware that:

- **Reduces Vector Dimensions by 70-90%** without significant semantic loss
- **Preserves 95%+ Explained Variance** through sophisticated SVD-based calibration
- **Operates Completely Offline** - No cloud APIs, no external dependencies
- **Provides Sub-10ms Compression** for production throughput
- **Delivers Enterprise Security** with cryptographic license enforcement

### How It Works

1. **Calibration Phase**: The engine analyzes your domain corpus using SVD (Singular Value Decomposition) to discover optimal semantic subspaces
2. **Dual-Map Compression**: 
   - **Primary Map** (256-768D): Preserves dominant semantic structure
   - **Residual Map** (32-256D): Captures subtle semantic nuances
3. **Out-of-Distribution Detection**: Automatically clips anomalous vectors to prevent semantic drift
4. **Seamless Reconstruction**: Full 1024D vectors can be restored for downstream processing

### Key Advantages

| Metric | Traditional RAG | SIRS Engine |
|--------|----------------|-------------|
| Storage per Document | 1024D × 4 bytes = 4KB | 256D × 2 bytes = 512B |
| Compression Ratio | 1:1 | 8:1 |
| Semantic Retention | 100% | 95%+ |
| Search Speed | Baseline | 3-5x faster |
| Cloud Dependency | Often Required | **None** |

---

## 🚀 Quick Start Guide

### 1. Prerequisites

- Docker installed on your system
- Valid CyBurn Digital commercial license key
- GPU recommended for optimal performance (CPU supported)

### 2. Pull the Docker Image

```bash
docker pull ghcr.io/thedevilhimselfcodes/sirs-engine:latest
```

### 3. Obtain Your License Key
Contact our sales team to obtain your commercial license:

Email: vindana@cyburndigital.com

WhatsApp: +94 76 388 5727

### 4. Run the Container
```bash
docker run -d \
  -p 8000:8000 \
  -e CYBURN_LICENSE_KEY='your_license_token_here' \
  --name sirs-engine \
  ghcr.io/thedevilhimselfcodes/sirs-engine:latest
```
### 5. Verify Installation
```bash
curl http://localhost:8000/api/v1/health
Expected response:

json
{
  "status": "active",
  "device": "cuda",
  "engine_calibrated": false,
  "active_dimensions": null
}
```
### 6. Calibrate the Engine
Your first step is to calibrate the engine with your domain corpus:

```bash
curl -X POST http://localhost:8000/api/v1/calibrate \
  -H "Content-Type: application/json" \
  -d '{
    "domain_corpus_text": "Your enterprise documents, technical manuals, knowledge base articles..."
  }'
```
Minimum Requirement: At least 256 text chunks for mathematically sound calibration.

### 7. Start Compressing
```bash
curl -X POST http://localhost:8000/api/v1/compress \
  -H "Content-Type: application/json" \
  -d '{"text": "Your document content here..."}'
```
Response:

```json
{
  "status": "success",
  "num_chunks": 4,
  "dimensions": 288,
  "chunk_positions": [0, 224, 448, 672],
  "vectors": [[0.123, -0.456, ...], ...]
}
```
### 8. Reconstruct When Needed
```bash
curl -X POST http://localhost:8000/api/v1/reconstruct \
  -H "Content-Type: application/json" \
  -d '{
    "compressed_payload": {
      "vectors": [[0.123, -0.456, ...], ...]
    }
  }'
```
### 📚 API Reference
Health Check
http
GET /api/v1/health
Response:

```json
{
  "status": "active",
  "device": "cuda",
  "engine_calibrated": true,
  "active_dimensions": 288
}
```
### Calibrate Engine
http
POST /api/v1/calibrate
Request Body:

```json
{
  "domain_corpus_text": "string (minimum 256 chunks recommended)"
}
```
Response:

```json
{
  "status": "success",
  "message": "Engine calibrated. Compliance report saved to disk.",
  "optimization_metrics": {
    "primary_dimensions": 256,
    "residual_dimensions": 32,
    "total_dimensions": 288
  },
  "validation_proof": {
    "mse": 0.000234,
    "explained_variance": 0.958,
    "compression_ratio": 7.11
  }
}
```
### Notes:

Calibration typically takes 1-5 minutes depending on corpus size

Matrices are automatically saved to ./sirs_primary.pt and ./sirs_residual.pt

Requires a minimum of 256 unique text chunks for statistical significance

### Compress Text
http
POST /api/v1/compress
Request Body:

```json
{
  "text": "string (document content to compress)"
}
```
Response:

```json
{
  "status": "success",
  "num_chunks": 4,
  "dimensions": 288,
  "chunk_positions": [0, 224, 448, 672],
  "vectors": [
    [0.123, -0.456, 0.789, ...],
    [...]
  ]
}
```
### Notes:

Returns Float16 vectors for optimal storage efficiency

Chunk positions indicate original text alignment (useful for RAG)

Each chunk is processed in overlapping windows (256 tokens, 32 token overlap)

### Reconstruct Vectors
http
POST /api/v1/reconstruct
Request Body:

```json
{
  "compressed_payload": {
    "vectors": [[0.123, -0.456, ...], ...]
  }
}
```
Response:

```json
{
  "status": "success",
  "dimensions": 1024,
  "reconstructed_vectors": [
    [0.123, -0.456, 0.789, ...],
    [...]
  ]
}
```
### Notes:

Restores full 1024D Float32 vectors

MSE typically < 0.001 with proper calibration

Useful for downstream LLM processing or semantic search

### 🔒 Security & Compliance
### License Enforcement
Cryptographically signed JWT tokens validated offline

Expiration dates enforced with system clock verification

Tamper-proof via HS256 signatures

### Air-Gapped Operation
No external API calls

All models and matrices stored locally

Military-grade isolation for sensitive enterprises

### Audit Trail
Automatic calibration reports in JSON format

Performance metrics captured per operation

Full observability for compliance reviews

### 🛠️ Configuration
Environment Variables
Variable	Description	Required
CYBURN_LICENSE_KEY	Commercial license token	✅
MODEL_PATH	Path to BGE-M3 model (default: ./bge-m3-local)	❌

### Docker Compose Example
```yaml
version: '3.8'

services:
  sirs-engine:
    image: ghcr.io/thedevilhimselfcodes/sirs-engine:latest
    container_name: sirs-engine
    ports:
      - "8000:8000"
    environment:
      - CYBURN_LICENSE_KEY=${CYBURN_LICENSE_KEY}
    volumes:
      - ./calibration_data:/app/calibration_data
      - ./model_cache:/app/bge-m3-local
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
```
### 📊 Performance Benchmarks
Test Environment
GPU: NVIDIA A100 (40GB)

CPU: 16-core Intel Xeon

Model: BGE-M3 (1024D embeddings)

Operation	Latency (ms)	Throughput (docs/sec)
Calibration (10K docs)	45,000	N/A
Compression (per doc)	8.2	122
Reconstruction (per doc)	5.7	175
Similarity Search (1M vectors)	12.3	81,300
### 🚨 Troubleshooting
Common Issues
License Expired:

```
[CYBURN DIGITAL FATAL ERROR] Your pilot license has expired.
→ Contact support to renew your license.
```

Tampered License:

```
[CYBURN DIGITAL FATAL ERROR] Invalid or tampered license key.
→ Verify you haven't modified the license token.
```
Insufficient Calibration Data:

```
Data Volume Too Low for Safe SVD Calibration.
→ Provide at least 256 distinct text chunks.
```
GPU Out of Memory:
```
→ Use CPU mode or reduce batch sizes by modifying chunk_size.
```
### 💼 Contact & Support
For enterprise licensing, technical support, or custom deployments:

### 📧 Email: vindana@cyburndigital.com

### 📱 WhatsApp: +94 76 388 5727

### 🌐 Website: cyburndigital.com

### 📄 License
This is proprietary commercial software. Unauthorized use, reproduction, or distribution is strictly prohibited.

Copyright © 2026 CyBurn Digital. All rights reserved.

### 🙏 Acknowledgments
Built with ❤️ using:

### BGE-M3 Embedding Model

### PyTorch

### FastAPI

### Transformers
