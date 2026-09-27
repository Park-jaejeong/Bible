from http.server import BaseHTTPRequestHandler
import json

AI_VOICES = [
    {"id": "ai:ko-KR-SunHiNeural", "name": "선희 (자연스러운 AI 음성)", "gender": "female"},
    {"id": "ai:ko-KR-InJoonNeural", "name": "인준 (중후하고 신뢰감 있는 AI 음성)", "gender": "male"},
    {"id": "ai:ko-KR-HyunsuMultilingualNeural", "name": "현수 (부드럽고 차분한 AI 음성)", "gender": "male"},
]

class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', '*')
        self.end_headers()

    def do_GET(self):
        data = json.dumps(AI_VOICES, ensure_ascii=False).encode('utf-8')
        self.send_response(200)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Cache-Control', 'public, max-age=86400')
        self.send_header('Content-Length', str(len(data)))
        self.end_headers()
        self.wfile.write(data)
