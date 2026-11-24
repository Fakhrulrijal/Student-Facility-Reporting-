import http.server
import os

PORT = 3000
WEB_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "build", "web")

class SPANetworkHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=WEB_DIR, **kwargs)

    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "X-Requested-With, Content-Type")
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        super().end_headers()

    def do_GET(self):
        # Resolve physical path
        req_path = self.path.split("?")[0].split("#")[0]
        local_path = os.path.join(WEB_DIR, req_path.lstrip("/"))
        
        # If requested file doesn't exist and not a direct static asset, serve index.html for Flutter SPA
        if not os.path.exists(local_path) and not any(req_path.endswith(ext) for ext in [".js", ".wasm", ".json", ".png", ".jpg", ".ttf", ".otf", ".css", ".apk", ".docx"]):
            self.path = "/index.html"
            
        return super().do_GET()

if __name__ == "__main__":
    SPANetworkHandler.extensions_map.update({
        ".wasm": "application/wasm",
        ".js": "application/javascript",
        ".json": "application/json",
        ".apk": "application/vnd.android.package-archive",
        ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    })
    
    # Use ThreadingHTTPServer for concurrent, multi-threaded requests (essential for iOS & Chrome)
    server = http.server.ThreadingHTTPServer(("0.0.0.0", PORT), SPANetworkHandler)
    server.daemon_threads = True
    print(f"Flutter Multi-Threaded Web Server ready on port {PORT} serving {WEB_DIR}")
    server.serve_forever()
