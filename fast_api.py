from fastapi import FastAPI, File, UploadFile, HTTPException
from typing import List
from fastapi.responses import JSONResponse, RedirectResponse
import whisper
import torch
from tempfile import NamedTemporaryFile

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

model = whisper.load_model("base", device=DEVICE)

app = FastAPI()

@app.post("/whisper")
async def handler(audioFiles: List[UploadFile] = File(...)):
    if not audioFiles:
        raise HTTPException(status_code=400, detail="Error: Please upload at least one WAV file.") 

    results = []

    for audioFile in audioFiles:
        with NamedTemporaryFile(suffix=".wav") as temp:
            with open(temp.name, "wb") as temp_file:
                temp_file.write(audioFile.file.read())
            result = model.transcribe(temp.name)    
        
            results.append(
                    {
                        "filename": audioFile.filename,
                        "transcript": result["text"]
                    }
            )

    return JSONResponse(content={'audio': results})

@app.get("/", response_class=RedirectResponse)
async def redirect_to_docs():
    return "/docs"
