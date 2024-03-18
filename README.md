# py-shinylive-alt-fetch
- Ultimate goal:

- Develope like this:
```python
# from pyodide import http
from pyodide_local import http

async api_call():
    r = await http.pyfectch(
        url: "http://localhost:8000/get-string",
        headers: {"Content-Type": "application/text"}
    )
    print(r.string())
```

- When deploying to Shinylive, just switch the commented imports
```python
from pyodide import http
# from pyodide_local import http
```

## How to use wrapper
- requirements: see `pyproject.toml`; the goal is for shiny/shinylive to be the only requirements

## pyfetch examples

```python
# Download, save extracted file to local virtual fs
from pyodide.http import pyfetch
response = await pyfetch("https://some_url/myfiles.zip")
await response.unpack_archive()
```

```python
# Download text file to local virtual fs, load into pandas
from pyodide.http import pyfetch

response = await pyodide.http.pyfetch(url())

with open("test.json", mode="wb") as file:
    file.write(await response.bytes())

df = pd.read_json("test.json")
```

```python
# Download text file into BytesIO memory buffer, load into pandas
from io import BytesIO
from pyodide.http import pyfetch

response = await pyodide.http.pyfetch(url())
buf = BytesIO(await response_c.bytes())

df = pd.read_json(buf)
```

## Install Test Dependencies
- `pip install -e '.[tests]'`

### Run regular tests
- activate venv: `source venv/bin/activate`
- start fastapi app: `python3 src_test_webserver/main.py`
- run pytest: `pytest -vv -x test`

### Run pyodide tests with pyfetch calls written identical to wrapper
- activate venv and start fastapi like above
- export shinylive app: `hinylive export ./test/tests_shinylive ./src_test_webserver/shinyapps`
- open shinylive app in edit mode: `http://localhost8000/apps/edit/`
- Click "Run tests"
- If all function names at the bottom are followed by "passed", then everything should be ok