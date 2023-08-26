import requests


def get(url: str, params={}):
    try:
        res = requests.get(url, params=params, timeout=3)
    except Exception:
        return {"ok": False, "data": {}}

    try:
        return {"ok": res.ok, "data": res.json()}
    except Exception:
        return {"ok": res.ok, "data": {}}
