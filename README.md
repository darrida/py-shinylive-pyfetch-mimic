# py-shinylive-alt-fetch

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