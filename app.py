# app.py
import os
import json
from flask import Flask, request, session, jsonify, send_from_directory
from flask_socketio import SocketIO, emit, join_room, leave_room
from server.game_manager import GameManager

app = Flask(__name__, static_folder="web", template_folder="web")
app.config['SECRET_KEY'] = 'sudoku-secret'
socketio = SocketIO(app, async_mode='eventlet')

# Lưu game theo session id
games = {}
saved_games = {}
rooms = {}  # room_id -> GameManager + danh sách user

def get_sid():
    if 'sid' not in session:
        import uuid
        session['sid'] = str(uuid.uuid4())
    return session['sid']

# -------- Static pages --------
@app.route('/')
def index():
    return send_from_directory('web', 'index.html')

@app.route('/game')
def game_page():
    return send_from_directory('web', 'game.html')

@app.route('/instructions')
def instructions_page():
    return send_from_directory('web', 'instructions.html')

@app.route('/result')
def result_page():
    return send_from_directory('web', 'result.html')

@app.route('/css/<path:path>')
def css(path):
    return send_from_directory('web/css', path)

@app.route('/js/<path:path>')
def js(path):
    return send_from_directory('web/js', path)

# -------- REST API cho single-player --------
@app.route('/api/new_game', methods=['POST'])
def api_new_game():
    data = request.get_json(force=True)
    diff = data.get('difficulty', 'easy')
    sid = get_sid()
    gm = GameManager(diff)
    games[sid] = gm
    return jsonify({'ok': True, 'state': gm.serialize()})

@app.route('/api/state')
def api_state():
    sid = get_sid()
    gm = games.get(sid)
    if not gm:
        return jsonify({'ok': False, 'error': 'no_game'})
    return jsonify({'ok': True, 'state': gm.serialize()})

@app.route('/api/move', methods=['POST'])
def api_move():
    sid = get_sid()
    gm = games.get(sid)
    if not gm:
        return jsonify({'ok': False, 'error': 'no_game'})
    d = request.get_json(force=True)
    res = gm.apply_move(int(d['row']), int(d['col']), int(d['val']))
    lost = gm.lose_if_exceeded()
    return jsonify({'ok': True, 'result': res, 'lost': lost, 'state': gm.serialize()})

@app.route('/api/hint', methods=['POST'])
def api_hint():
    sid = get_sid()
    gm = games.get(sid)
    if not gm:
        return jsonify({'ok': False, 'error': 'no_game'})
    res = gm.hint()
    return jsonify({'ok': True, 'result': res, 'state': gm.serialize()})

@app.route('/api/reset', methods=['POST'])
def api_reset():
    sid = get_sid()
    gm = games.get(sid)
    if not gm:
        return jsonify({'ok': False, 'error': 'no_game'})
    state = gm.reset()
    return jsonify({'ok': True, 'state': state})

@app.route('/api/finish', methods=['POST'])
def api_finish():
    sid = get_sid()
    gm = games.get(sid)
    if not gm:
        return jsonify({'ok': False, 'error': 'no_game'})
    res = gm.finish()
    return jsonify({'ok': True, 'result': res})

@app.route('/api/save', methods=['POST'])
def api_save():
    sid = get_sid()
    gm = games.get(sid)
    if not gm:
        return jsonify({'ok': False, 'error': 'no_game'})
    saved_games[sid] = gm.serialize()
    return jsonify({'ok': True})

@app.route('/api/load')
def api_load():
    sid = get_sid()
    data = saved_games.get(sid)
    if not data:
        return jsonify({'ok': False, 'error': 'no_saved'})
    # Tạo GameManager từ saved state (đơn giản: new + replace board)
    gm = GameManager(data.get('difficulty', 'easy'))
    gm.board = data['board']
    gm.initial = data['initial']
    gm.hints_used = data['hints_used']
    gm.mistakes = data['mistakes']
    gm.finished = data['finished']
    games[sid] = gm
    return jsonify({'ok': True, 'state': gm.serialize()})

# -------- SocketIO cho multiplayer (đơn giản) --------
@socketio.on('join_room')
def join_room_evt(data):
    room = data['room']
    username = data.get('username', 'user')
    if room not in rooms:
        rooms[room] = {'gm': GameManager('easy'), 'users': set()}
    rooms[room]['users'].add(request.sid)
    join_room(room)
    gm = rooms[room]['gm']
    emit('room_message', {'msg': f'{username} đã tham gia phòng {room}'}, room=room)
    emit('state', {'state': gm.serialize()}, room=request.sid)

@socketio.on('leave_room')
def leave_room_evt(data):
    room = data['room']
    username = data.get('username', 'user')
    leave_room(room)
    if room in rooms and request.sid in rooms[room]['users']:
        rooms[room]['users'].remove(request.sid)
        emit('room_message', {'msg': f'{username} đã rời phòng'}, room=room)

@socketio.on('move')
def move_evt(data):
    room = data['room']
    gm = rooms[room]['gm']
    res = gm.apply_move(int(data['row']), int(data['col']), int(data['val']))
    lost = gm.lose_if_exceeded()
    emit('move_result', {'result': res, 'lost': lost, 'state': gm.serialize()}, room=room)

@socketio.on('hint')
def hint_evt(data):
    room = data['room']
    gm = rooms[room]['gm']
    res = gm.hint()
    emit('hint_result', {'result': res, 'state': gm.serialize()}, room=room)

@socketio.on('reset')
def reset_evt(data):
    room = data['room']
    gm = rooms[room]['gm']
    state = gm.reset()
    emit('state', {'state': state}, room=room)

@socketio.on('finish')
def finish_evt(data):
    room = data['room']
    gm = rooms[room]['gm']
    res = gm.finish()
    emit('finish_result', {'result': res}, room=room)

@socketio.on('chat')
def chat_evt(data):
    room = data['room']
    username = data.get('username', 'user')
    msg = data.get('msg', '')
    emit('chat', {'username': username, 'msg': msg}, room=room)

if __name__ == "__main__":
    socketio.run(app, host="127.0.0.1", port=5000, debug=True)
