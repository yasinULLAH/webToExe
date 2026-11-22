import os
import sys
import importlib.util

_pyw = os.path.join(os.path.dirname(os.path.abspath(__file__)), "app.pyw")
if os.path.isfile(_pyw):
    _spec = importlib.util.spec_from_file_location("app_pyw", _pyw)
    _mod = importlib.util.module_from_spec(_spec)
    _spec.loader.exec_module(_mod)
    globals().update({k: getattr(_mod, k) for k in dir(_mod) if not k.startswith("__")})

if __name__ == "__main__":
    if "main" in globals() and callable(globals()["main"]):
        globals()["main"]()
