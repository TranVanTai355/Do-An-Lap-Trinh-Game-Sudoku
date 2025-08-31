# client/client.py
from .socket_handler import SocketClient

def print_board(b):
    print("+-------+-------+-------+")
    for i, row in enumerate(b):
        s = ""
        for j, v in enumerate(row):
            s += " " + (str(v) if v != 0 else ".")
            if j % 3 == 2:
                s += " |"
        print("|" + s + "")
        if i % 3 == 2:
            print("+-------+-------+-------+")

def main():
    c = SocketClient()
    c.connect()
    print("Connected.")
    welcome = c.recv()
    state = welcome.get('state', {})
    print_board(state['board'])

    while True:
        cmd = input("cmd (new [easy/medium/hard]/move r c v/hint/reset/finish/quit): ").strip().lower()
        if cmd == 'quit':
            break
        if cmd.startswith('new'):
            parts = cmd.split()
            level = parts[1] if len(parts) > 1 else 'easy'
            c.send({'action': 'new_game', 'difficulty': level})
            resp = c.recv()
            print_board(resp['state']['board'])
        elif cmd.startswith('move'):
            try:
                _, r, c2, v = cmd.split()
                c.send({'action': 'move', 'row': int(r), 'col': int(c2), 'val': int(v)})
                resp = c.recv()
                print(resp['result']['reason'], "mistakes:", resp['result']['mistakes'])
                print_board(resp['state']['board'])
                if resp['lost']:
                    print("Bạn đã thua (quá 3 lần sai).")
                    break
            except Exception as e:
                print("Sai cú pháp. Ví dụ: move 0 1 9")
        elif cmd == 'hint':
            c.send({'action': 'hint'})
            resp = c.recv()
            print(resp['result'])
            print_board(resp['state']['board'])
        elif cmd == 'reset':
            c.send({'action': 'reset'})
            resp = c.recv()
            print("Reset xong.")
            print_board(resp['state']['board'])
        elif cmd == 'finish':
            c.send({'action': 'finish'})
            resp = c.recv()
            print(resp['result'])
        else:
            print("Lệnh không hợp lệ.")
    c.close()

if __name__ == "__main__":
    main()
