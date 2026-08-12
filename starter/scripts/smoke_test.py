import urllib.request
import urllib.error
import json
import time

def get(url):
    with urllib.request.urlopen(url, timeout=5) as resp:
        return json.loads(resp.read().decode())

def post(url, data):
    data_bytes = json.dumps(data).encode()
    req = urllib.request.Request(url, data=data_bytes, headers={'Content-Type':'application/json'})
    with urllib.request.urlopen(req, timeout=5) as resp:
        return json.loads(resp.read().decode())

def wait_for_server(url, timeout=10.0):
    start = time.time()
    while time.time() - start < timeout:
        try:
            get(url)
            return True
        except Exception:
            time.sleep(0.3)
    return False

base = 'http://127.0.0.1:5000'
if not wait_for_server(base + '/api/new'):
    print('Server not available')
    raise SystemExit(2)

res = get(base + '/api/new?difficulty=Easy')
prefilled = sum(1 for r in res['puzzle'] for v in r if v != 0)
print('NEW: difficulty=', res.get('difficulty'), 'prefilled=', prefilled)

hint = post(base + '/api/hint', {})
print('HINT:', hint)

empty_board = [[0]*9 for _ in range(9)]
chk = post(base + '/api/check', {'board': empty_board})
print('CHECK returned incorrect count=', len(chk.get('incorrect', [])))

print('Smoke test completed')
