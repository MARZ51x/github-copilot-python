// Modern client-side app for Sudoku.
const SIZE = 9;
let puzzle = [];
let timerInterval = null;
let secondsElapsed = 0;
let hintsUsed = 0;

function formatTime(s){
  const mm = String(Math.floor(s/60)).padStart(2,'0');
  const ss = String(s%60).padStart(2,'0');
  return `${mm}:${ss}`;
}

function createBoard(){
  const board = document.getElementById('sudoku-board');
  board.innerHTML = '';
  for(let r=0;r<SIZE;r++){
    for(let c=0;c<SIZE;c++){
      const inp = document.createElement('input');
      inp.type='text'; inp.maxLength=1; inp.className='sudoku-cell';
      inp.dataset.row = r; inp.dataset.col = c;
      // region class for alternating 3x3
      const region = ((Math.floor(r/3) + Math.floor(c/3)) % 2) ? 'region-A' : 'region-B';
      inp.classList.add(region);
      inp.addEventListener('input', (e)=>{
        e.target.value = e.target.value.replace(/[^1-9]/g,'');
        validateCellImmediate(e.target);
      });
      inp.addEventListener('keydown', (e)=>{
        // allow navigation with arrows
        const key = e.key;
        if(['ArrowUp','ArrowDown','ArrowLeft','ArrowRight'].includes(key)){
          e.preventDefault();
          navigateCell(e.target, key);
        }
      });
      board.appendChild(inp);
    }
  }
}

function navigateCell(el, key){
  const r = parseInt(el.dataset.row,10);
  const c = parseInt(el.dataset.col,10);
  let nr=r,nc=c;
  if(key==='ArrowUp') nr=Math.max(0,r-1);
  if(key==='ArrowDown') nr=Math.min(8,r+1);
  if(key==='ArrowLeft') nc=Math.max(0,c-1);
  if(key==='ArrowRight') nc=Math.min(8,c+1);
  const idx = nr*SIZE + nc;
  const board = document.getElementById('sudoku-board');
  board.children[idx].focus();
}

function renderPuzzle(puz){
  puzzle = puz;
  const board = document.getElementById('sudoku-board');
  board.classList.add('board-wipe');
  setTimeout(()=>{
    board.classList.remove('board-wipe');
    board.classList.add('board-reveal');
    createBoard();
    for(let r=0;r<SIZE;r++){
      for(let c=0;c<SIZE;c++){
        const idx = r*SIZE + c;
        const cell = board.children[idx];
        const val = puzzle[r][c];
        if(val && val !== 0){
          cell.value = val; cell.disabled = true; cell.classList.add('prefilled','cell-locked');
        } else { cell.value=''; cell.disabled=false; }
        cell.classList.remove('cell-update-valid','cell-update-invalid','cell-hint');
      }
    }
    board.classList.remove('board-reveal');
    const empties = Array.from(board.children).filter(c=>!c.disabled && !c.value);
    document.getElementById('hint').disabled = empties.length===0;
  }, 150);
}

async function newGame(){
  stopTimer(); secondsElapsed=0; hintsUsed=0; updateTimerDisplay();
  const diff = document.getElementById('difficulty').value;
  const res = await fetch(`/api/new?difficulty=${encodeURIComponent(diff)}`);
  const data = await res.json();
  renderPuzzle(data.puzzle);
  startTimer();
  document.getElementById('message').innerText='';
}

function startTimer(){
  stopTimer();
  timerInterval = setInterval(()=>{ secondsElapsed++; updateTimerDisplay(); },1000);
}
function stopTimer(){ if(timerInterval) clearInterval(timerInterval); timerInterval=null }
function updateTimerDisplay(){ document.getElementById('timer').innerText = formatTime(secondsElapsed); }

function getBoardState(){
  const board = document.getElementById('sudoku-board');
  const state = Array.from({length:SIZE},()=>Array(SIZE).fill(0));
  for(let r=0;r<SIZE;r++) for(let c=0;c<SIZE;c++){
    const idx=r*SIZE+c; const v = board.children[idx].value; state[r][c] = v?parseInt(v,10):0;
  }
  return state;
}

async function checkSolution(){
  const board = getBoardState();
  const res = await fetch('/api/check',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({board})});
  const data = await res.json();
  const msg = document.getElementById('message');
  if(data.error){ msg.innerText = data.error; return; }
  const incorrect = new Set(data.incorrect.map(x=>x[0]*SIZE + x[1]));
  const cells = document.getElementById('sudoku-board').children;
  for(let i=0;i<cells.length;i++){
    const c = cells[i]; if(c.disabled) continue; c.classList.remove('cell-invalid','cell-valid');
    if(incorrect.has(i)) c.classList.add('cell-invalid'); else if(c.value) c.classList.add('cell-valid');
  }
  if(incorrect.size===0){
    stopTimer();
    showWinPopup(`You completed the board in ${formatTime(secondsElapsed)} with ${hintsUsed} hint(s)!`);
  } else {
    msg.innerText = 'Some cells are incorrect.';
  }
}

function showWinPopup(message){
  document.getElementById('message').innerText = '';
  document.getElementById('win-popup-message').innerText = message;
  document.getElementById('win-popup').classList.remove('hidden');
}

function closeWinPopup(){
  document.getElementById('win-popup').classList.add('hidden');
}

async function saveScorePrompt(timeSeconds){
  const key='sudoku_leaderboard'; const raw=localStorage.getItem(key); const list=raw?JSON.parse(raw):[];
  const qualifies = list.length < 10 || timeSeconds < list[list.length-1].time;
  if(!qualifies){ renderLeaderboard(); return; }
  const name = prompt('Nice! Enter your name to save on the Top 10 (or Cancel)');
  if(!name) return;
  const difficulty = document.getElementById('difficulty').value;
  saveScore({name, time: timeSeconds, difficulty, hints: hintsUsed});
  renderLeaderboard();
}

function saveScore(entry){
  const key = 'sudoku_leaderboard';
  const raw = localStorage.getItem(key); const list = raw?JSON.parse(raw):[];
  list.push(entry);
  list.sort((a,b)=>a.time - b.time);
  const top = list.slice(0,10);
  localStorage.setItem(key, JSON.stringify(top));
}

function renderLeaderboard(){
  const key='sudoku_leaderboard'; const raw=localStorage.getItem(key); const list=raw?JSON.parse(raw):[];
  const tbody = document.querySelector('#leaderboard-table tbody');
  tbody.innerHTML = '';
  for(const item of list){
    const tr = document.createElement('tr');
    const columns = [item.name, formatTime(item.time), item.difficulty, item.hints];
    for(const text of columns){
      const td = document.createElement('td');
      td.innerText = text;
      tr.appendChild(td);
    }
    tbody.appendChild(tr);
  }
}

async function hint(){
  const res = await fetch('/api/hint',{method:'POST'});
  const data = await res.json();
  if(data.error){ alert(data.error); return; }
  const idx = data.row*SIZE + data.col;
  const cell = document.getElementById('sudoku-board').children[idx];
  cell.value = data.value;
  cell.disabled = true;
  cell.classList.add('cell-locked','prefilled','cell-hint');
  hintsUsed++;
  setTimeout(()=> cell.classList.remove('cell-hint'), 1800);
  const empties = Array.from(document.getElementById('sudoku-board').children).filter(c=>!c.disabled && !c.value);
  document.getElementById('hint').disabled = empties.length===0;
}

async function validateCellImmediate(cell){
  const r = parseInt(cell.dataset.row,10), c = parseInt(cell.dataset.col,10);
  const v = cell.value ? parseInt(cell.value,10) : 0;
  if(!v){
    cell.classList.remove('cell-invalid','cell-update-valid','cell-update-invalid');
    return;
  }
  const state = getBoardState();
  const conflicts = [];
  for(let i=0;i<SIZE;i++){
    if(i!==c && state[r][i]===v) conflicts.push([r,i]);
    if(i!==r && state[i][c]===v) conflicts.push([i,c]);
  }
  const br = Math.floor(r/3)*3, bc = Math.floor(c/3)*3;
  for(let i=br;i<br+3;i++){
    for(let j=bc;j<bc+3;j++){
      if((i!==r||j!==c) && state[i][j]===v) conflicts.push([i,j]);
    }
  }
  const hasConflict = conflicts.length>0;
  cell.classList.toggle('cell-invalid', hasConflict);
  cell.classList.toggle('cell-update-valid', !hasConflict);
  cell.classList.toggle('cell-update-invalid', hasConflict);
  setTimeout(()=>{
    cell.classList.remove('cell-update-valid','cell-update-invalid');
  }, 1500);
}

function setThemeIcon(){
  const button = document.getElementById('theme-toggle');
  const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
  button.innerHTML = isDark ? '🌙' : '☀️';
}

function toggleTheme(){
  document.documentElement.classList.add('theme-transition');
  const current = document.documentElement.getAttribute('data-theme');
  const next = current==='dark' ? '' : 'dark';
  if(next) document.documentElement.setAttribute('data-theme','dark'); else document.documentElement.removeAttribute('data-theme');
  localStorage.setItem('sudoku_theme', next || 'light');
  setThemeIcon();
  window.setTimeout(()=> document.documentElement.classList.remove('theme-transition'), 500);
}

function loadTheme(){
  const t = localStorage.getItem('sudoku_theme');
  if(t==='dark') document.documentElement.setAttribute('data-theme','dark');
  else document.documentElement.removeAttribute('data-theme');
  setThemeIcon();
}

window.addEventListener('load', ()=>{
  document.getElementById('new-game').addEventListener('click', newGame);
  document.getElementById('check-solution').addEventListener('click', checkSolution);
  document.getElementById('hint').addEventListener('click', hint);
  document.getElementById('theme-toggle').addEventListener('click', toggleTheme);
  document.getElementById('save-score').addEventListener('click', async ()=>{
    await saveScorePrompt(secondsElapsed);
    closeWinPopup();
  });
  document.getElementById('close-popup').addEventListener('click', closeWinPopup);
  loadTheme(); renderLeaderboard(); newGame();
});
