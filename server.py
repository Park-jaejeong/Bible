import os
import sys
import asyncio
import urllib.parse
from http.server import HTTPServer, SimpleHTTPRequestHandler
import edge_tts

PORT = 8080
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

AI_VOICES = [
    {"id": "ai:ko-KR-SunHiNeural", "name": "선희 (자연스러운 AI 음성)", "gender": "female"},
    {"id": "ai:ko-KR-InJoonNeural", "name": "인준 (중후하고 신뢰감 있는 AI 음성)", "gender": "male"},
    {"id": "ai:ko-KR-HyunsuMultilingualNeural", "name": "현수 (부드럽고 차분한 AI 음성)", "gender": "male"},
]

class BibleRequestHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def end_headers(self):
        # CORS 허용 헤더 추가
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', '*')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        
        # 1. AI 음성 목록 API
        if parsed.path == '/api/voices':
            import json
            data = json.dumps(AI_VOICES, ensure_ascii=False).encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Content-Length', str(len(data)))
            self.end_headers()
            self.wfile.write(data)
            return

        # 2. 고품질 AI 음성 스트리밍 API
        if parsed.path == '/api/tts':
            query = urllib.parse.parse_qs(parsed.query)
            voice = query.get('voice', ['ko-KR-SunHiNeural'])[0]
            if voice.startswith('ai:'):
                voice = voice.replace('ai:', '')
            text = query.get('text', [''])[0].strip()
            rate = query.get('rate', ['+15%'])[0]

            if not text:
                self.send_response(400)
                self.end_headers()
                return

            try:
                # edge-tts 오디오 생성 (mp3 바이트 스트림)
                async def generate_audio():
                    communicate = edge_tts.Communicate(text, voice, rate=rate)
                    chunks = []
                    async for chunk in communicate.stream():
                        if chunk["type"] == "audio":
                            chunks.append(chunk["data"])
                    return b"".join(chunks)

                audio_data = asyncio.run(generate_audio())

                self.send_response(200)
                self.send_header('Content-Type', 'audio/mpeg')
                self.send_header('Content-Length', str(len(audio_data)))
                self.send_header('Cache-Control', 'public, max-age=86400')
                self.end_headers()
                self.wfile.write(audio_data)
                return
            except Exception as e:
                print("TTS 생성 오류:", e)
                self.send_response(500)
                self.end_headers()
                return

        # 일반 정적 파일 서빙
        super().do_GET()

def run():
    server_address = ('', PORT)
    httpd = HTTPServer(server_address, BibleRequestHandler)
    print(f"Bible Web Server running on port {PORT} with AI TTS support...")
    httpd.serve_forever()

if __name__ == '__main__':
    run()
