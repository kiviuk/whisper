from fastapi import FastAPI, File, UploadFile, HTTPException
from loguru import logger
from typing import List
from fastapi.responses import JSONResponse, RedirectResponse
from pathlib import Path
import whisper
import torch

from tempfile import NamedTemporaryFile

#DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
DEVICE = "cpu"

model = whisper.load_model("base", device=DEVICE)

app = FastAPI(title="Whisper", debug=False)
logger.add("log_file_{time}.log", format="{time} {level} {message}", level="DEBUG")
app.logger = logger

@app.post("/whisper")
@logger.catch
async def handler(audioFiles: List[UploadFile] = File(...)):
    logger.debug("/whisper start")

    if not audioFiles:
        raise HTTPException(status_code=400, detail="Error: Please upload at least one audio file.") 

    results = []

    for audioFile in audioFiles:
        with NamedTemporaryFile(suffix=".wav") as temp:
            logger.debug("Creating temp audio file {}", temp.name)
            with open(temp.name, "wb") as temp_file:
                temp_file.write(audioFile.file.read())
            logger.debug("Processing temp audio file {} in whisper", temp.name)
            result = model.transcribe(temp.name, verbose=True)    
        
            results.append(
                    {
                        "filename": audioFile.filename,
                        "transcript": result["text"]
                        #"transcript": "text"
                    }
            )
            logger.debug("Results: {}", results)

    logger.debug("/whisper end")
    return JSONResponse(content={'audio': results})

@app.get("/", response_class=RedirectResponse)
@logger.catch
async def redirect_to_docs():
    logger.debug("REDIRECT")
    return "/docs"
