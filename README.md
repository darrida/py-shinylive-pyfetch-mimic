# pyfetch-mimic
- This is a simple module that mimicks `pyodide.http.pyfetch` to make local development for `shinylive` projects easier. It may work with `pyodide` in general, but that use case hasn't been tested.

## How to use wrapper
- Include the following conditional import statement at the beginning of the module that will use `http.pyfetch`:
    ```python
    if "pyodide" in sys.modules:
        from pyodide import http
    else:
        from pyfetch_mimic import http
    ```
- Use `http.pyfetch` as usual
- **NOTE**: The wrapper is a *work in progress* and does not support all use case variations yet. It will be updated as need arises.

## pyfetch examples

```python
# Download, save extracted file to local virtual fs
if "pyodide" in sys.modules:
    from pyodide import http
else:
    from pyfetch_mimic import http

response = await pyfetch("https://some_url/myfiles.zip")
await response.unpack_archive()
```

```python
# Download text file to local virtual fs, load into pandas
if "pyodide" in sys.modules:
    from pyodide import http
else:
    from pyfetch_mimic import http

response = await pyodide.http.pyfetch(url())

with open("test.json", mode="wb") as file:
    file.write(await response.bytes())

df = pd.read_json("test.json")
```

```python
# Download text file into BytesIO memory buffer, load into pandas
from io import BytesIO
if "pyodide" in sys.modules:
    from pyodide import http
else:
    from pyfetch_mimic import http

response = await pyodide.http.pyfetch(url())
buf = BytesIO(await response_c.bytes())

df = pd.read_json(buf)
```

## Install Test Dependencies
- `pip install -e '.[tests]'`

### Run regular tests (verifes test endpoints and tests `pyfetch-mimic`)
- activate venv: `source venv/bin/activate`
- start fastapi app: `python3 src_test_webserver/main.py`
- run pytest: `pytest -vv -x test`

### Run pyodide tests with pyfetch calls written identical to `pyfetch-mimc`
- activate venv and start fastapi like above
- export shinylive app: `shinylive export ./test/tests_shinylive ./src_test_webserver/shinyapps`
- open shinylive app in edit mode: `http://localhost8000/apps/edit/`
- Click "Run tests"
- If all function names at the bottom are followed by "passed", then everything should be ok