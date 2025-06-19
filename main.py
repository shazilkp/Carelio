from fastapi import FastAPI, UploadFile, File
from fastapi.exceptions import HTTPException
import os
import shutil
from report_parser import report_parser
app = FastAPI()


@app.get("/")
def example():
    return {"First example" : "FASTAPI"}

@app.post("/upload-parse")
async def image_upload(file:  UploadFile = File(...)):
    content_type = file.content_type
    if content_type not in ["image/jpeg", "image/png", "image/gif"]:
        raise HTTPException(status_code=400, detail="Invalid file type")
    
    upload_dir = os.path.join(os.getcwd(), "uploads")
    # Create the upload directory if it doesn't exist
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)

    # get the destination path
    dest = os.path.join(upload_dir, file.filename)
    print(dest)

    # copy the file contents
    with open(dest, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    json_rep = report_parser(dest)
    return json_rep