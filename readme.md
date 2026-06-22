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