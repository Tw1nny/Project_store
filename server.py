"""
Простое веб-приложение без использования фреймворков.

- На любой GET-запрос возвращает страницу "Контакты" (templates/contacts.html).
- Принимает POST-запрос (например, отправку формы обратной связи) и печатает
  полученные от пользователя данные в консоль.
- Дополнительно реализованы страницы 404 (несуществующий метод/ресурс)
  и 500 (внутренняя ошибка сервера, например если шаблон не найден).

Bootstrap подключается на самих HTML-страницах с удаленного CDN
(https://cdnjs.cloudflare.com), поэтому дополнительной раздачи статики
для стилей не требуется.
"""

from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs
import os
import traceback

HOST = "localhost"
PORT = 8000

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
CONTACTS_PAGE = os.path.join(TEMPLATES_DIR, "contacts.html")


def read_template(filename: str) -> str:
    """Читает содержимое HTML-файла с помощью контекстного менеджера."""
    path = os.path.join(TEMPLATES_DIR, filename)
    with open(path, "r", encoding="utf-8") as file:
        return file.read()


class RequestHandler(BaseHTTPRequestHandler):

    def _send_html(self, status_code: int, html: str) -> None:
        encoded = html.encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def _send_404(self) -> None:
        html = (
            "<html><head><meta charset='utf-8'><title>404</title></head>"
            "<body><h1>404 — Страница не найдена</h1>"
            "<p><a href='/'>Вернуться на главную</a></p></body></html>"
        )
        self._send_html(404, html)

    def _send_500(self, error: Exception) -> None:
        # Печатаем полную трассировку в консоль, чтобы было видно, что пошло не так
        print("Ошибка на сервере:")
        traceback.print_exc()

        html = (
            "<html><head><meta charset='utf-8'><title>500</title></head>"
            "<body><h1>500 — Внутренняя ошибка сервера</h1>"
            f"<p>{error}</p></body></html>"
        )
        self._send_html(500, html)

    # --- GET: любой запрос отдает страницу "Контакты" ---
    def do_GET(self):
        if self.path == "/favicon.ico":
            self.send_response(204)
            self.end_headers()
            return
        try:
            html = read_template("contacts.html")
            self._send_html(200, html)
        except FileNotFoundError as error:
            self._send_500(error)
        except Exception as error:  # noqa: BLE001 - демонстрация страницы 500
            self._send_500(error)

    # --- POST: принимаем данные формы и печатаем их в консоль ---
    def do_POST(self):
        try:
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length).decode("utf-8")
            data = parse_qs(body)

            print("Получены данные от пользователя (POST /):")
            for key, values in data.items():
                print(f"  {key}: {values[0]}")

            html = (
                "<html><head><meta charset='utf-8'><title>Спасибо</title></head>"
                "<body><h1>Данные получены, спасибо!</h1>"
                "<p><a href='/'>Вернуться к контактам</a></p></body></html>"
            )
            self._send_html(200, html)
        except Exception as error:  # noqa: BLE001 - демонстрация страницы 500
            self._send_500(error)


def run(server_class=HTTPServer, handler_class=RequestHandler):
    server_address = (HOST, PORT)
    httpd = server_class(server_address, handler_class)
    print(f"Сервер запущен: http://{HOST}:{PORT}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Остановка сервера...")
        httpd.server_close()


if __name__ == "__main__":
    run()
