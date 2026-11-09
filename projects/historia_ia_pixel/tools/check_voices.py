import urllib.request, json, os

env_path = '.env'
api_key = open(env_path).read().split('=')[1].strip()
req = urllib.request.Request('https://api.elevenlabs.io/v1/voices', headers={'xi-api-key': api_key})
with urllib.request.urlopen(req) as resp:
    data = json.loads(resp.read().decode())
    print(f"Total voices: {len(data['voices'])}")
    for v in data['voices']:
        labels = v.get('labels', {})
        print(f"{v['voice_id']}: {v['name']} | lang: {labels.get('language','')} | accent: {labels.get('accent','')} | gender: {labels.get('gender','')}")
