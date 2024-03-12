import json
import os
import pathlib

from pyodide import http
from shiny import App, Inputs, Outputs, Session, reactive, render, ui

app_ui = ui.page_fluid(
    ui.output_text_verbatim("text_id", "Check browser console for tests status"),
    ui.input_action_button("tests_btn", "Run tests")
)


def server(input: Inputs, output: Outputs, session: Session):
    @reactive.effect
    @reactive.event(input.tests_btn)
    async def all_tests():
        print("TEST GET STRING")
        r = await http.pyfetch("http://localhost:8000/get-string", method="GET")
        assert r.status == 200
        assert await r.string() == "return a string"

        print("TEST GET JSON")
        r = await http.pyfetch("http://localhost:8000/get-json", method="GET")
        assert r.status == 200
        assert await r.json() == {"json_obj": "return json"}

        print("TEST GET PARAM FOUND")
        r = await http.pyfetch("http://localhost:8000/get-not-found-parameter/found", method="GET")
        assert r.status == 200
        assert await r.json() == {"status": "item found"}

        print("TEST GET PARAM NOT FOUND")
        r = await http.pyfetch("http://localhost:8000/get-not-found-parameter/not", method="GET")
        assert r.status == 204

        print("TEST POST PAYLOAD")
        r = await http.pyfetch(
            "http://localhost:8000/post-payload", 
            headers={"Content-Type": "application/json"},
            method="POST",
            body=json.dumps({"name": "Ben", "age": 20})
        )
        print(r.status)
        assert r.status == 200
        assert await r.json() == {"name": "Ben", "age": 20}

        print("TEST TEXT FILE DOWNLOAD")
        r = await http.pyfetch(
            "http://localhost:8000/get-text-download", 
            method="GET"
        )
        assert r.status == 200
        data_bytes = await r.bytes()
        assert data_bytes.decode() == 'name,age,weight\nben,40,154\nsam,32,185'

        print("TEST IMAGE FILE DOWNLOAD")
        r = await http.pyfetch(
            "http://localhost:8000/get-image-download", 
            method="GET"
        )
        assert r.status == 200
        data_bytes = await r.bytes()
        with open("test.jpg", "wb") as f:
            f.write(data_bytes)
        assert os.path.isfile("test.jpg")
        assert os.path.getsize("test.jpg") == 338148
        # clean up
        if os.path.isfile("test.jpg"):
            pathlib.Path("test.jpg").unlink()
        assert os.path.isfile("test.jpg") is False

        print("TEST GET STREAMING FAKE")
        r = await http.pyfetch("http://localhost:8000/get-streaming")
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


app = App(app_ui, server)
