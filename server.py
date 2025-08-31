# server/server.py
import socket
import threading
import json
from .game_manager import GameManager

HOST = '0.0.0.0'
PORT = 9009

clients = {}   # conn -> GameManager

def send_json(conn, obj):
    data = (json.dumps(obj) + "\n").encode('utf-8')
    conn.sendall(data)

def handle_client(conn, addr):
    gm = GameManager('easy')
    clients[conn] = gm
    send_json(conn, {'type': 'welcome', 'msg': 'Connected to Sudoku TCP server', 'state': gm.serialize()})
    try:
        buf = ""
        while True:
            chunk = conn.recv(4096)
            if not chunk:
                break
            buf += chunk.decode('utf-8')
            while "\n" in buf:
                line, buf = buf.split("\n", 1)
                if not line.strip():
                    continue
                try:
                    req = json.loads(line)
                except:
                    send_json(conn, {'type': 'error', 'msg': 'invalid_json'})
                    continue

                action = req.get('action')
                if action == 'new_game':
                    diff = req.get('difficulty', 'easy')
                    state = gm.new_game(diff)
                    send_json(conn, {'type': 'state', 'state': state})
                elif action == 'move':
                    r, c, v = req.get('row'), req.get('col'), req.get('val')
                    res = gm.apply_move(int(r), int(c), int(v))
                    lose = gm.lose_if_exceeded()
                    payload = {'type': 'move_result', 'result': res, 'lost': lose, 'state': gm.serialize()}
                    send_json(conn, payload)
                elif action == 'hint':
                    res = gm.hint()
                    send_json(conn, {'type': 'hint_result', 'result': res, 'state': gm.serialize()})
                elif action == 'reset':
                    state = gm.reset()
                    send_json(conn, {'type': 'state', 'state': state})
                elif action == 'finish':
                    res = gm.finish()
                    send_json(conn, {'type': 'finish_result', 'result': res})
                elif action == 'get_state':
                    send_json(conn, {'type': 'state', 'state': gm.serialize()})
                else:
                    send_json(conn, {'type': 'error', 'msg': 'unknown_action'})
    finally:
        conn.close()
        clients.pop(conn, None)
        print(f"Client {addr} disconnected.")

def start_server():
    print(f"Starting TCP server on {HOST}:{PORT}")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(5)
    try:
        while True:
            conn, addr = s.accept()
            print(f"Client connected: {addr}")
            t = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
            t.start()
    finally:
        s.close()

if __name__ == "__main__":
    start_server()
