import os
import torch
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
from engine import SIRSEngine

# Initialize the FastAPI application
app = FastAPI(
    title="CyBurn Digital SIRS Engine",
    description="Adaptive, air-gapped vector compression middleware for enterprise RAG pipelines.",
    version="1.6.0"
)

current_dir = os.path.dirname(os.path.abspath(__file__))
local_model_path = os.path.join(current_dir, "bge-m3-local")

print(f"Initializing SIRS Engine from: {local_model_path}")
try:
    engine = SIRSEngine(model_path=local_model_path)
except Exception as e:
    print(f"CRITICAL ERROR: Failed to load model. Details: {e}")
    raise e

try:
    engine.load_maps(load_dir=current_dir)
    print(f"SUCCESS: Loaded existing SIRS matrices. Active Dimensions: {engine.actual_primary_dim + engine.actual_residual_dim}D")
except Exception:
    print("WARNING: No calibration matrices found. Engine requires calibration.")

# --- API Data Models ---
class CalibrateRequest(BaseModel):
    domain_corpus_text: str

class CompressRequest(BaseModel):
    text: str

class ReconstructRequest(BaseModel):
    # Accepts the exact JSON dictionary outputted by the /compress endpoint
    compressed_payload: Dict[str, Any]

# --- Endpoints ---
@app.post("/api/v1/calibrate")
def calibrate_engine(request: CalibrateRequest):
    try:
        metrics = engine.calibrate(request.domain_corpus_text, save_dir=current_dir)
        engine.load_maps(load_dir=current_dir)
        
        # We cap the validation text to 2000 chars just for a quick API response proof
        validation = engine.validate_calibration(request.domain_corpus_text[:2000]) 
        
        return {
            "status": "success", 
            "message": "Engine calibrated. Compliance report saved to disk.",
            "optimization_metrics": metrics,
            "validation_proof": validation
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Calibration failed: {str(e)}")

@app.post("/api/v1/compress")
def compress_text_for_db(request: CompressRequest):
    if engine.primary_map is None:
        raise HTTPException(status_code=400, detail="Engine uncalibrated.")
    
    try:
        payload = engine.compress_for_db_with_indices(request.text)
        vectors = payload['vectors'].tolist()
        
        return {
            "status": "success", 
            "num_chunks": payload['num_chunks'],
            "dimensions": len(vectors[0]) if vectors else 0,
            "chunk_positions": payload['chunk_positions'],
            "vectors": vectors
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Compression failed: {str(e)}")

@app.post("/api/v1/reconstruct")
def reconstruct_vectors(request: ReconstructRequest):
    """
    Takes the lightweight Float16 JSON array and rebuilds it into 
    the full 1024D Float32 semantic vectors for downstream processing.
    """
    if engine.primary_map is None:
        raise HTTPException(status_code=400, detail="Engine uncalibrated.")
    
    try:
        # Convert the JSON array back into a PyTorch tensor
        dense_list = request.compressed_payload.get('vectors', [])
        if not dense_list:
            raise ValueError("Payload missing 'vectors' array.")
            
        tensor_payload = torch.tensor(dense_list, dtype=torch.float16).to(engine.device)
        
        # Use our new polymorphic reconstruct router!
        reconstructed_tensor = engine.reconstruct(tensor_payload)
        
        return {
            "status": "success",
            "dimensions": reconstructed_tensor.shape[1],
            "reconstructed_vectors": reconstructed_tensor.tolist()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Reconstruction failed: {str(e)}")

@app.get("/api/v1/health")
def health_check():
    is_calibrated = engine.primary_map is not None
    return {
        "status": "active",
        "device": str(engine.device),
        "engine_calibrated": is_calibrated,
        "active_dimensions": engine.actual_primary_dim + engine.actual_residual_dim if is_calibrated else None
    }