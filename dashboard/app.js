/* ─── Config ──────────────────────────────────────────────────────────── */
const FILES = {
  learning: '/api/memory?file=learning',
  goals:    '/api/memory?file=goals',
};

const DAY_NAMES = ['Вс', 'Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб'];

/* ─── Fetch ───────────────────────────────────────────────────────────── */
async function fetchMarkdown(url) {
  try {
    const res = await fetch(url + '?t=' + Date.now());
    if (!res.ok) return '';
    return await res.text();
  } catch {
    return '';
  }
}

/* ─── Parsers ─────────────────────────────────────────────────────────── */
function parseStreak(md) {
  const streakMatch = md.match(/Текущий:\s*(\d+)\s*дней подряд/);
  const dateMatch   = md.match(/Последний день учёбы:\s*(\d{4}-\d{2}-\d{2})/);
  return {
    streak:   streakMatch ? parseInt(streakMatch[1], 10) : 0,
    lastDate: dateMatch ? dateMatch[1] : null,
  };
}

function parseModules(md) {
  const done       = (md.match(/^### ✅/gm) || []).length;
  const inProgress = (md.match(/^### 🔶/gm) || []).length;
  const todo       = (md.match(/^### ⬜/gm) || []).length;
  const total      = done + inProgress + todo;

  let currentModule = '';
  const currentMatch = md.match(/### 🔶\s*(.+)/);
  if (currentMatch) currentModule = currentMatch[1].replace(/\s*\(В ПРОЦЕССЕ\)/, '').trim();

  // Parse individual modules for detail view
  const modules = [];
  const moduleRe = /^### (✅|🔶|⬜)\s*(.+?)(?:\s*\(В ПРОЦЕССЕ\))?$/gm;
  let m;
  while ((m = moduleRe.exec(md)) !== null) {
    modules.push({ icon: m[1], title: m[2].trim() });
  }

  return { done, inProgress, todo, total, currentModule, modules };
}

function parseWorkouts(md) {
  const weekDays = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс'];
  const rows = [];

  // Parse workout table rows
  const tableRe = /^\|\s*([А-Яа-яЁё]+)\s*\|\s*(.+?)\s*\|\s*(✅|❌)\s*\|\s*(\d+)?\s*\|\s*(\d+)?\s*\|/gm;
  let m;
  while ((m = tableRe.exec(md)) !== null) {
    rows.push({
      day:  m[1].trim(),
      name: m[2].trim(),
      done: m[3] === '✅',
      feel: m[4] || '—',
      effort: m[5] || '—',
    });
  }

  const weekDone  = rows.filter(r => r.done).length;
  const weekTotal = rows.length || 5;

  // Parse trainer plan
  const plan = [];
  const planSection = md.match(/###\s*План от тренера\n([\s\S]*?)(?=\n##|\n###|$)/);
  if (planSection) {
    const planLines = planSection[1].match(/^[-•]\s*.+/gm) || [];
    planLines.forEach(l => plan.push(l.replace(/^[-•]\s*/, '').trim()));
  }

  // Build week status from rows
  const dayStatus = {};
  rows.forEach(r => { dayStatus[r.day] = r.done; });

  return { weekDone, weekTotal, rows, plan, dayStatus, weekDays };
}

function parseWork(md) {
  const tasks = [];
  const goals = [];

  const taskSection = md.match(/###\s*Задачи\n([\s\S]*?)(?=\n##|\n###|$)/);
  if (taskSection) {
    const lines = taskSection[1].match(/^- \[[ x]\].+/gm) || [];
    lines.forEach(l => {
      tasks.push({ text: l.replace(/^- \[[ x]\]\s*/, '').trim(), done: l.includes('- [x]') });
    });
  }

  const goalSection = md.match(/###\s*Цели\n([\s\S]*?)(?=\n##|\n###|$)/);
  if (goalSection) {
    const lines = goalSection[1].match(/^- \[[ x]\].+/gm) || [];
    lines.forEach(l => {
      goals.push({ text: l.replace(/^- \[[ x]\]\s*/, '').trim(), done: l.includes('- [x]') });
    });
  }

  const done  = [...tasks, ...goals].filter(i => i.done).length;
  const total = tasks.length + goals.length;

  return { tasks, goals, done, total };
}

/* ─── Render cards ────────────────────────────────────────────────────── */
function renderCards(data) {
  const { learning, workouts, work } = data;

  // Learning
  const streakLabel = learning.streak === 1 ? 'день' :
                      learning.streak < 5   ? 'дня' : 'дней';
  setText('learning-metric',  `${learning.streak} ${streakLabel}`);
  setProgress('learning-progress', learning.total ? Math.round(learning.done / learning.total * 100) : 0, 'learning');
  setText('learning-status',
    learning.currentModule
      ? `В процессе: ${truncate(learning.currentModule, 40)}`
      : `${learning.done} из ${learning.total} модулей`
  );

  // Workouts
  setText('workouts-metric', `${workouts.weekDone}/${workouts.weekTotal}`);
  const workPct = workouts.weekTotal ? Math.round(workouts.weekDone / workouts.weekTotal * 100) : 0;
  setProgress('workouts-progress', workPct, 'workouts');
  setText('workouts-status', workouts.weekTotal
    ? `${workPct}% плана на неделю`
    : 'Нет данных о тренировках'
  );

  // Work
  const workDonePct = work.total ? Math.round(work.done / work.total * 100) : 0;
  setText('work-metric',    `${work.done}/${work.total}`);
  setProgress('work-progress', workDonePct, 'work');
  setText('work-status',
    work.total
      ? `${work.tasks.filter(t => !t.done).length} активных задач`
      : 'Нет данных о задачах'
  );
}

function setText(id, text) {
  const el = document.getElementById(id);
  if (el) el.textContent = text;
}

function setProgress(id, pct, section) {
  const el = document.getElementById(id);
  if (!el) return;
  el.style.width = pct + '%';
  const bar = el.closest('.progress-bar');
  if (bar) {
    bar.setAttribute('aria-valuenow', pct);
    bar.setAttribute('aria-label', `${section} ${pct}%`);
  }
}

function truncate(str, len) {
  return str.length > len ? str.slice(0, len) + '…' : str;
}

/* ─── Detail views ────────────────────────────────────────────────────── */
const DETAIL_TITLES = {
  learning: 'Учёба',
  workouts: 'Тренировки',
  work:     'Работа',
};

function showDetail(section, data) {
  const overlay = document.getElementById('detail');
  const title   = document.getElementById('detail-title');
  const content = document.getElementById('detail-content');

  title.textContent = DETAIL_TITLES[section] || section;
  content.innerHTML = '';

  if (section === 'learning')  content.appendChild(buildLearningDetail(data.learning));
  if (section === 'workouts')  content.appendChild(buildWorkoutsDetail(data.workouts));
  if (section === 'work')      content.appendChild(buildWorkDetail(data.work));

  overlay.classList.remove('hidden');
  overlay.focus();
  document.getElementById('main').setAttribute('aria-hidden', 'true');
}

function hideDetail() {
  document.getElementById('detail').classList.add('hidden');
  document.getElementById('main').removeAttribute('aria-hidden');
}

/* Learning detail */
function buildLearningDetail(learning) {
  const frag = document.createDocumentFragment();

  // Streak
  const streakSection = makeSection('Стрик');
  const row = el('div', 'stat-row');
  const num = el('div', 'stat-number');
  num.textContent = learning.streak;
  const lbl = el('div', 'stat-label');
  lbl.innerHTML = 'дней<br>подряд';
  if (learning.lastDate) {
    lbl.innerHTML += `<br><span style="font-size:11px;opacity:.6">последний: ${learning.lastDate}</span>`;
  }
  row.append(num, lbl);
  streakSection.querySelector('.detail-section').appendChild(row);
  frag.appendChild(streakSection);

  // Modules
  if (learning.modules.length) {
    const modSection = makeSection(`Модули ${learning.done}/${learning.total}`);
    const list = el('div', 'module-list');
    learning.modules.forEach(m => {
      const item = el('div', `module-item${m.icon === '✅' ? ' done' : m.icon === '🔶' ? ' active' : ''}`);
      const status = el('span', 'module-status');
      status.textContent = m.icon;
      const text = el('span', '');
      text.textContent = m.title;
      item.append(status, text);
      list.appendChild(item);
    });
    modSection.querySelector('.detail-section').appendChild(list);
    frag.appendChild(modSection);
  }

  return frag;
}

/* Workouts detail */
function buildWorkoutsDetail(workouts) {
  const frag = document.createDocumentFragment();

  // Week dots
  const weekSection = makeSection('Неделя');
  const dots = el('div', 'week-dots');
  workouts.weekDays.forEach(day => {
    const dot = el('div', `week-dot${workouts.dayStatus[day] ? ' done' : ''}`);
    const circle = el('div', 'week-dot-circle');
    const label  = el('span', '');
    label.textContent = day;
    dot.append(circle, label);
    dots.appendChild(dot);
  });
  weekSection.querySelector('.detail-section').appendChild(dots);
  frag.appendChild(weekSection);

  // Table
  if (workouts.rows.length) {
    const tableSection = makeSection('Тренировки');
    const table = el('table', 'workout-table');
    const thead = el('thead', '');
    thead.innerHTML = '<tr><th>День</th><th>Упражнение</th><th>✓</th><th>Самочув.</th><th>Усилие</th></tr>';
    const tbody = el('tbody', '');
    workouts.rows.forEach(r => {
      const tr = el('tr', '');
      tr.innerHTML = `<td>${r.day}</td><td>${r.name}</td><td>${r.done ? '✅' : '❌'}</td><td>${r.feel}</td><td>${r.effort}</td>`;
      tbody.appendChild(tr);
    });
    table.append(thead, tbody);
    tableSection.querySelector('.detail-section').appendChild(table);
    frag.appendChild(tableSection);
  }

  // Plan
  if (workouts.plan.length) {
    const planSection = makeSection('План от тренера');
    const list = el('div', 'task-list');
    workouts.plan.forEach(p => {
      const item = el('div', 'task-item');
      const icon = el('span', 'task-check empty');
      icon.innerHTML = svgDot();
      const text = el('span', '');
      text.textContent = p;
      item.append(icon, text);
      list.appendChild(item);
    });
    planSection.querySelector('.detail-section').appendChild(list);
    frag.appendChild(planSection);
  }

  if (!workouts.rows.length && !workouts.plan.length) {
    const empty = el('p', 'empty-state');
    empty.textContent = 'Нет данных о тренировках. Отправь план тренера боту.';
    frag.appendChild(empty);
  }

  return frag;
}

/* Work detail */
function buildWorkDetail(work) {
  const frag = document.createDocumentFragment();

  if (work.tasks.length) {
    const taskSection = makeSection('Задачи');
    taskSection.querySelector('.detail-section').appendChild(buildTaskList(work.tasks));
    frag.appendChild(taskSection);
  }

  if (work.goals.length) {
    const goalSection = makeSection('Цели');
    goalSection.querySelector('.detail-section').appendChild(buildTaskList(work.goals));
    frag.appendChild(goalSection);
  }

  if (!work.tasks.length && !work.goals.length) {
    const empty = el('p', 'empty-state');
    empty.textContent = 'Нет данных о задачах. Добавь через бота.';
    frag.appendChild(empty);
  }

  return frag;
}

function buildTaskList(items) {
  const list = el('div', 'task-list');
  items.forEach(item => {
    const div  = el('div', `task-item${item.done ? ' done' : ''}`);
    const icon = el('span', `task-check${item.done ? '' : ' empty'}`);
    icon.innerHTML = item.done ? svgCheck() : svgDot();
    const text = el('span', '');
    text.textContent = item.text;
    div.append(icon, text);
    list.appendChild(div);
  });
  return list;
}

/* ─── DOM helpers ─────────────────────────────────────────────────────── */
function el(tag, className) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  return node;
}

function makeSection(title) {
  const wrap = el('div', '');
  const sec  = el('div', 'detail-section');
  const h    = el('div', 'detail-section-title');
  h.textContent = title;
  sec.appendChild(h);
  wrap.appendChild(sec);
  return wrap;
}

function svgCheck() {
  return `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>`;
}

function svgDot() {
  return `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="4"/></svg>`;
}

/* ─── Last updated ────────────────────────────────────────────────────── */
function setLastUpdated() {
  const el = document.getElementById('last-updated');
  if (!el) return;
  const now = new Date();
  const hh  = String(now.getHours()).padStart(2, '0');
  const mm  = String(now.getMinutes()).padStart(2, '0');
  el.textContent = `обновлено ${hh}:${mm}`;
}

/* ─── Init ────────────────────────────────────────────────────────────── */
document.addEventListener('DOMContentLoaded', async () => {
  // Telegram Mini App init
  if (window.Telegram?.WebApp) {
    Telegram.WebApp.ready();
    Telegram.WebApp.expand();
  }

  const loadingEl = document.getElementById('loading');
  const mainEl    = document.getElementById('main');
  const errorEl   = document.getElementById('error');
  const errorMsg  = document.getElementById('error-msg');

  try {
    const [learningMd, goalsMd] = await Promise.all([
      fetchMarkdown(FILES.learning),
      fetchMarkdown(FILES.goals),
    ]);

    const data = {
      learning: { ...parseStreak(learningMd), ...parseModules(learningMd) },
      workouts: parseWorkouts(goalsMd),
      work:     parseWork(goalsMd),
    };

    loadingEl.classList.add('hidden');
    mainEl.classList.remove('hidden');

    renderCards(data);
    setLastUpdated();

    // Card click → detail
    document.querySelectorAll('.card').forEach(card => {
      const open = () => showDetail(card.dataset.section, data);
      card.addEventListener('click', open);
      card.addEventListener('keydown', e => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); open(); } });
    });

    // Back button
    document.getElementById('back-btn').addEventListener('click', hideDetail);

    // Back on Telegram hardware back button
    if (window.Telegram?.WebApp?.BackButton) {
      const BB = Telegram.WebApp.BackButton;
      document.getElementById('detail').addEventListener('transitionend', () => {});

      const observer = new MutationObserver(() => {
        const visible = !document.getElementById('detail').classList.contains('hidden');
        visible ? BB.show() : BB.hide();
      });
      observer.observe(document.getElementById('detail'), { attributes: true, attributeFilter: ['class'] });
      BB.onClick(hideDetail);
    }

  } catch (err) {
    loadingEl.classList.add('hidden');
    errorEl.classList.remove('hidden');
    errorMsg.textContent = 'Не удалось загрузить данные. Проверь подключение.';
  }
});
