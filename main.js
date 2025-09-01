let state = null;
let timerInterval = null;

async function fetchState() {
  const r = await fetch('/api/state');
  const data = await r.json();
  if (data.ok) {
    state = data.state;
    document.getElementById('lblDiff').innerText = state.difficulty;
    document.getElementById('mistakes').innerText = state.mistakes;
    document.getElementById('hints').innerText = 3 - state.hints_used;
    renderBoard(state.board, state.initial);
  }
}

function renderBoard(board, initial){
  const tbl = document.getElementById('board');
  tbl.innerHTML = '';
  for(let r=0;r<9;r++){
    const tr = document.createElement('tr');
    for(let c=0;c<9;c++){
      const td = document.createElement('td');
      td.dataset.r = r; td.dataset.c = c;
      const v = board[r][c];
      if(initial[r][c] !== 0){
        td.textContent = v;
        td.classList.add('fixed');
      }else{
        td.contentEditable = true;
        td.textContent = v === 0 ? '' : v;
        td.addEventListener('input', onEditCell);
      }
      tr.appendChild(td);
    }
    tbl.appendChild(tr);
  }
}

async function onEditCell(e){
  const td = e.target;
  let val = td.textContent.trim();
  if(!/^[1-9]?$/.test(val)){ td.textContent=''; return; }
  val = val === '' ? 0 : parseInt(val);
  td.classList.remove('error');
  const r = parseInt(td.dataset.r), c = parseInt(td.dataset.c);
  const resp = await fetch('/api/move', {
    method:'POST', headers:{'Content-Type':'application/json'},
    body: JSON.stringify({row: r, col: c, val})
  });
  const data = await resp.json();
  if(!data.ok){ return; }
  state = data.state;
  document.getElementById('mistakes').innerText = state.mistakes;
  if(data.result.ok !== true){
    td.classList.add('error');
    showMsg(data.result.reason === 'wrong_value' ? 'Sai số!' : 'Nước đi không hợp lệ.');
  }else{
    showMsg('');
  }
  if(data.lost){
    clearInterval(timerInterval);
    alert('Bạn thua (sai quá 3 lần).');
    location.href = '/';
  }
  renderBoard(state.board, state.initial);
}

function startTimer(){
  if(timerInterval) clearInterval(timerInterval);
  timerInterval = setInterval(async ()=>{
    await fetchState();
    document.getElementById('timer').innerText = state.time;
  }, 1000);
}

function showMsg(m){ document.getElementById('msg').innerText = m; }

document.getElementById('btnHint').onclick = async ()=>{
  const r = await fetch('/api/hint', {method:'POST'});
  const data = await r.json();
  if(data.ok){
    state = data.state;
    document.getElementById('hints').innerText = 3 - state.hints_used;
    renderBoard(state.board, state.initial);
  }
};

document.getElementById('btnReset').onclick = async ()=>{
  const r = await fetch('/api/reset', {method:'POST'});
  const data = await r.json();
  if(data.ok){
    state = data.state;
    renderBoard(state.board, state.initial);
    showMsg('Đã reset.');
  }
};

document.getElementById('btnSave').onclick = async ()=>{
  await fetch('/api/save', {method:'POST'});
  showMsg('Đã lưu game.');
};

document.getElementById('btnFinish').onclick = async ()=>{
  const r = await fetch('/api/finish', {method:'POST'});
  const data = await r.json();
  if(data.ok && data.result.win){
    clearInterval(timerInterval);
    localStorage.setItem('last_result', JSON.stringify(data.result));
    alert(`Chiến thắng! Thời gian: ${data.result.time}s, Điểm: ${data.result.score}`);
    location.href = '/result';
  }else{
    showMsg('Bảng chưa chính xác.');
  }
};

(async function init(){
  // Nếu chưa có game thì tạo theo độ khó đã chọn ở menu
  let s = await fetch('/api/state'); s = await s.json();
  if(!s.ok){
    const diff = localStorage.getItem('difficulty') || 'easy';
    await fetch('/api/new_game', {
      method:'POST', headers:{'Content-Type':'application/json'},
      body: JSON.stringify({difficulty: diff})
    });
  }
  await fetchState();
  startTimer();
})();
