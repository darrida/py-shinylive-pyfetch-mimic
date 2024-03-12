import asyncio
import json
import os
import pathlib
import sys

if "pyodide" in sys.modules:
    from pyodide import http
else:
    import pytest

    from src.pyodide_wrapper import http
    pytestmark = pytest.mark.asyncio


async def test_wrapper_get_string():
    r = await http.pyfetch("http://localhost:8000/get-string", headers={"Content-Type": "application/text"}, method="GET")
    assert r.status == 200
    assert await r.string() == "return a string"


async def test_wrapper_get_json():
    r = await http.pyfetch("http://localhost:8000/get-json", headers={"Content-Type": "application/json"}, method="GET")
    assert r.status == 200
    assert await r.json() == {"json_obj": "return json"}


async def test_wrapper_get_parameter_found():
    r = await http.pyfetch("http://localhost:8000/get-not-found-parameter/found", headers={"Content-Type": "application/json"}, method="GET")
    assert r.status == 200
    assert await r.json() == {"status": "item found"}


async def test_wrapper_get_parameter_not_found():
    r = await http.pyfetch("http://localhost:8000/get-not-found-parameter/not", headers={"Content-Type": "application/json"}, method="GET")
    assert r.status == 204


async def test_wrapper_post_payload():
    r = await http.pyfetch(
        "http://localhost:8000/post-payload",
        headers={"Content-Type": "application/json"},  
        method="POST",
        body=json.dumps({"name": "Ben", "age": 20})
    )
    assert r.status == 200
    assert await r.json() == {"name": "Ben", "age": 20}


async def test_wrapper_get_file_download():
    r = await http.pyfetch(
        "http://localhost:8000/get-text-download", 
        headers={"Content-Type": "application/json"},
        method="GET"
    )
    assert r.status == 200
    # buffer = r.bytes()
    data_bytes = await r.bytes()
    assert data_bytes.decode() == 'name,age,weight\nben,40,154\nsam,32,185'


async def test_wrapper_get_image_download():
    r = await http.pyfetch(
        "http://localhost:8000/get-image-download", 
        headers={"Content-Type": "application/json"},
        method="GET"
    )
    r.status == 200
    data_bytes = await r.bytes()
    with open("test.jpg", "wb") as f:
        f.write(data_bytes)
    assert os.path.isfile("test.jpg")
    assert os.path.getsize("test.jpg") == 338148
    # clean up
    if os.path.isfile("test.jpg"):
        pathlib.Path("test.jpg").unlink()
    assert os.path.isfile("test.jpg") is False


async def test_wrapper_streaming_fake():
    """Not a real streaming example, but showing that it can still pull from a streaming source
    """
    r = await http.pyfetch("http://localhost:8000/get-streaming", headers={"Content-Type": "application/json"},)
    assert r.status == 200
    data = await r.string()
    data = data.split("\n")
    for count, i in enumerate(data):
        if i == "":
            continue
        i = json.loads(i)
        assert count == i["event"]
        if count == 39:
            assert i["is_last_event"] is True
        else:
            assert i["is_last_event"] is False


async def test_throw_away_sleep():
    await asyncio.sleep(0)