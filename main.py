from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.responses import JSONResponse
from typing import List, Optional, Dict
import uuid
from pathlib import Path
import shutil
import pandas as pd

from server_config import (
    store_csv_document,
    get_all_files,
    query_document,
    delete_document,
    get_file_content,  # Rename the import
    DocumentNotFoundError
)

from models import QueryRequest, FileResponse

app = FastAPI()

@app.post("/upload")
async def upload_file_endpoint(file: UploadFile = File(...)):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Only CSV files are allowed")
    
    try:
        # Generate unique file ID
        file_id = str(uuid.uuid4())
        
        # Create temp file and save uploaded content
        temp_path = Path(f"/tmp/{file_id}.csv")
        with temp_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Store in collection using server_config function
        await store_csv_document(str(temp_path), file_id, file.filename)
        
        # Clean up temp file
        temp_path.unlink()
        
        return JSONResponse(
            content={"file_id": file_id, "message": "Upload successful"},
            status_code=200
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/files", response_model=List[FileResponse])
async def list_files():
    try:
        files = await get_all_files()
        return [FileResponse(file_id=f["file_id"], file_name=f["file_name"], content=f["content"]) for f in files]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/query")
async def query_file_endpoint(request: QueryRequest):
    try:
        response = await query_document(request.file_id, request.query)
        return {"response": response}
    except DocumentNotFoundError:
        raise HTTPException(status_code=404, detail="File not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/file/{file_id}")
async def delete_file_endpoint(file_id: str):
    try:
        await delete_document(file_id)
        return {"message": "File deleted successfully"}
    except DocumentNotFoundError:
        raise HTTPException(status_code=404, detail="File not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/content/{file_id}")
async def get_file_content_endpoint(file_id: str):
    try:
        # print("Trying to get file content")
        content = await get_file_content(file_id)
        # print("Got file content")
        return {"response": content}
    except DocumentNotFoundError:
        raise HTTPException(status_code=404, detail="File not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
