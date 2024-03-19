import json
import random
from pathlib import Path
from typing import List, Optional

from fastapi import APIRouter, Request, Response
from fastapi.responses import FileResponse, JSONResponse, StreamingResponse
from pydantic import BaseModel

router = APIRouter()


class AuthCheck(BaseModel):
    token: str
    groups_needed: Optional[List[str]] = None


class AuthResponse(BaseModel):
    token: str


@router.get("/get-string")
async def get_str():
    return Response(status_code=200, content="return a string")


@router.get("/get-json")
async def get_json():
    return JSONResponse(status_code=200, content={"json_obj": "return json"})


@router.get("/get-not-found-parameter/{search_item}")
async def get_not_found(search_item: str):
    if search_item == "found":
        return JSONResponse(status_code=200, content={"status": "item found"})
    return Response(status_code=204)


class SamplePayload(BaseModel):
    name: str
    age: int


@router.post("/post-payload", response_model=SamplePayload)
async def post_payload(request: Request, data: SamplePayload):
    return data


@router.get("/get-text-download")
async def get_file_download():
    return FileResponse(Path(__file__).resolve().parent / "files" / "test.csv", filename="test.csv")


@router.get("/get-image-download")
async def get_image_download():
    return FileResponse(Path(__file__).resolve().parent / "files" / "test.jpg", filename="test.csv")


async def fake_data_streamer():
    size = 40
    for i in range(size):
        yield json.dumps({"event": i, "data": random.random(), "is_last_event": i == size-1}) + '\n'
        # await asyncio.sleep(0)
    # return

@router.get("/get-streaming")
async def get_streaming():
    return StreamingResponse(fake_data_streamer(), media_type="application/x-ndjson")