from http.server import BaseHTTPRequestHandler, HTTPServer
import json

# Sample data
tasks = [
    {
        'id': 1,
        'title': 'Buy groceries',
        'done': False
    },
    {
        'id': 2,
        'title': 'Learn Python',
        'done': False
    }
]

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/tasks':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'tasks': tasks}).encode('utf-8'))
        else:
            task_id = self.path.split('/')[-1]
            if task_id.isdigit():
                task_id = int(task_id)
                task = next((task for task in tasks if task['id'] == task_id), None)
                if task:
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({'task': task}).encode('utf-8'))
                else:
                    self.send_response(404)
                    self.end_headers()
                    self.wfile.write(b'{"error": "Task not found"}')
            else:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b'{"error": "Not found"}')

    def do_POST(self):
        if self.path == '/tasks':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            new_task = json.loads(post_data.decode('utf-8'))
            if 'title' in new_task:
                new_task['id'] = tasks[-1]['id'] + 1
                new_task['done'] = False
                tasks.append(new_task)
                self.send_response(201)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'task': new_task}).encode('utf-8'))
            else:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b'{"error": "Bad Request"}')

    def do_PUT(self):
        task_id = self.path.split('/')[-1]
        if task_id.isdigit():
            task_id = int(task_id)
            content_length = int(self.headers['Content-Length'])
            put_data = self.rfile.read(content_length)
            updated_data = json.loads(put_data.decode('utf-8'))
            task = next((task for task in tasks if task['id'] == task_id), None)
            if task:
                task['title'] = updated_data.get('title', task['title'])
                task['done'] = updated_data.get('done', task['done'])
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'task': task}).encode('utf-8'))
            else:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b'{"error": "Task not found"}')
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'{"error": "Not found"}')

    def do_DELETE(self):
        task_id = self.path.split('/')[-1]
        if task_id.isdigit():
            task_id = int(task_id)
            global tasks
            tasks = [task for task in tasks if task['id'] != task_id]
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'{"result": true}')
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'{"error": "Not found"}')

def run(server_class=HTTPServer, handler_class=RequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting HTTP server on port {port}...')
    httpd.serve_forever()

if __name__ == '__main__':
    run()