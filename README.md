# pycob

```bash
python3 -m venv venv
source venv/bin/activate
python3 -m pip install --upgrade build
python3 -m pip install --upgrade twine
```

```bash
python3 -m build
python3 -m twine upload --repository testpypi dist/*                      
```

```bash
python3 -m build
python3 -m twine upload dist/*                      
```
