// ═══════════════════════════════════════════════════════════════════
// PM MULTIVERSE — multiverse.js
// Handles index page (problem list) and problem page (5-step experience)
// ═══════════════════════════════════════════════════════════════════

const PAGE = document.body.dataset.page;

if (PAGE === 'index') initIndex();
else if (PAGE === 'experience') initExperience();

// ─────────────────────────────────────────────────────────────────
// SHARED CONSTANTS (not problem-specific)
// ─────────────────────────────────────────────────────────────────

const BLEND_MEANINGS = {
  'doshi-cagan':  "You think strategically before shipping, but you also know the difference between analysis and paralysis. You want the sharpest bet with the least risk.",
  'doshi-torres': "You want strategic clarity AND evidence. You'll pick a wedge, but you won't bet on it until the opportunity tree validates it.",
  'doshi-lenny':  "You think in frameworks but love a growth lever. You'll define the strategy, then obsess over the experiment that proves it.",
  'doshi-exec':   "You have a strong strategic bias — but you know speed matters. You'd ship the wedge fast rather than perfect it slowly.",
  'cagan-torres': "You are deeply risk-conscious and evidence-driven. You'd rather be slow and right than fast and wrong — and you have the discovery receipts to prove it.",
  'cagan-doshi':  "You want strategic clarity before committing, but you're also rigorous about de-risking. You'd write the pre-mortem before the PRD.",
  'cagan-lenny':  "You want to de-risk before investing, but you love a good growth loop. You'd validate the flywheel hypothesis before building it.",
  'cagan-exec':   "You have discovery instincts but feel the competitive urgency. You might be more cautious than you think.",
  'torres-doshi': "You are an evidence-first strategist. You want opportunity mapping before you'll commit to a wedge.",
  'lenny-exec':   "You lean toward shipping and learning, with a strong bias for growth mechanics. You'd be live before most PMs finish their assumptions doc.",
  'exec-lenny':   "Speed is your default. You'd have a referral engine running before anyone else has a discovery plan.",
  'default':      "You blend strategic thinking with practical action. You'd de-risk the big bets but move faster than most."
};

const PERSONA_ORDER = ['cagan', 'torres', 'doshi', 'lenny', 'exec'];

// ─────────────────────────────────────────────────────────────────
// INDEX PAGE
// ─────────────────────────────────────────────────────────────────

async function initIndex() {
  try {
    const problems = await fetch('/api/pmm/problems').then(r => r.json());
    renderProblemGrid(problems);
    updateIndexProgress(problems);
  } catch (e) {
    document.getElementById('problemsGrid').innerHTML =
      '<p style="color:var(--muted); text-align:center; padding:40px;">Failed to load problems. Please refresh.</p>';
  }
}

function renderProblemGrid(problems) {
  const grid = document.getElementById('problemsGrid');
  const tagColors = ['', 't2', 't3', 't4', 't5'];

  grid.innerHTML = problems.map((p, i) => {
    const done = localStorage.getItem(`pmm_done_${p.id}`);
    const delay = Math.min(i + 1, 5);
    return `
      <div class="problem-card ${done ? 'done-card' : ''} anim-fade-up delay-${delay}"
           onclick="selectProblem('${p.id}', '${p.file}')">
        ${done ? '<div class="done-badge">✓</div>' : ''}
        <div class="problem-tags">
          ${p.tags.slice(0, 2).map((t, ti) => `<span class="problem-tag ${tagColors[ti]}">${t}</span>`).join('')}
        </div>
        <h3>${escHtml(p.title)}</h3>
        <p>${escHtml(p.prompt.substring(0, 110))}${p.prompt.length > 110 ? '…' : ''}</p>
        <div class="available-badge">
          <div class="available-dot"></div>
          ${done ? 'Play again' : 'Play now'}
        </div>
      </div>
    `;
  }).join('');
}

function selectProblem(id, file) {
  window.location.href = `/tools/pm-multiverse/problem?id=${encodeURIComponent(id)}&file=${encodeURIComponent(file)}`;
}

function updateIndexProgress(problems) {
  const done = problems.filter(p => localStorage.getItem(`pmm_done_${p.id}`)).length;
  document.getElementById('progressFill').style.width = `${(done / 10) * 100}%`;
  document.getElementById('progressLabel').textContent = `${done}/10`;
}

// ─────────────────────────────────────────────────────────────────
// EXPERIENCE PAGE — DATA LAYER
// ─────────────────────────────────────────────────────────────────

let PROBLEM = null;    // raw JSON
let QUESTIONS = [];    // normalized
let PERSONAS = {};     // normalized (keyed by id: cagan, torres, etc.)
let VOTE_SEED = {};    // JSON voteResults as fallback

async function initExperience() {
  const params = new URLSearchParams(window.location.search);
  const problemId = params.get('id');
  const file = params.get('file');

  if (!problemId || !file) {
    window.location.href = '/tools/pm-multiverse';
    return;
  }

  try {
    const raw = await fetch(`/static/data/pmm/problems/${encodeURIComponent(file)}`).then(r => {
      if (!r.ok) throw new Error('Not found');
      return r.json();
    });

    PROBLEM = raw;
    QUESTIONS = raw.yourTakeFirst.questions.map(normalizeQuestion);
    Object.entries(raw.personas).forEach(([key, p]) => {
      PERSONAS[key] = normalizePersona(p);
    });
    VOTE_SEED = raw.voteResults || {};

    // Remove loading screen, activate quiz
    document.getElementById('loading').style.display = 'none';
    goToStep(1);
    updateTopbar();
  } catch (e) {
    document.getElementById('loading').innerHTML =
      '<p style="color:var(--red);">Failed to load problem. <a href="/" style="color:var(--accent);">Go back</a></p>';
  }
}

// ─────────────────────────────────────────────────────────────────
// DATA NORMALIZATION (JSON schema → experience format)
// ─────────────────────────────────────────────────────────────────

function normalizeQuestion(q) {
  return {
    text: q.text,
    options: q.options.map(o => ({
      label: o.label,
      text: o.text,
      weights: o.personaWeights,
    })),
  };
}

function normalizePersona(raw) {
  return {
    id: raw.id,
    name: raw.name,
    emoji: raw.emoji,
    color: raw.color,
    role: raw.role,
    tagline: raw.summary,
    quote: raw.spicyQuote,
    breakdown: raw.breakdown,
    solution: raw.solution,
    disagree: raw.disagreement,
    mvp: raw.mvp,
    metrics: raw.metrics,
    roadmap: raw.roadmap.map(parseRoadmapEntry),
    scores: {
      speed: raw.scoreboard.speed,
      risk: raw.scoreboard.riskManagement,
      strategy: raw.scoreboard.strategicClarity,
      growth: raw.scoreboard.growthPotential,
    },
  };
}

function parseRoadmapEntry(str) {
  // Handles two formats:
  //   "Phase: Label — description text"   (ideal)
  //   "Phase: full text"                  (some problems)
  const colonIdx = str.indexOf(': ');
  if (colonIdx === -1) return { phase: '', label: '', text: str.trim() };
  const phase = str.substring(0, colonIdx).trim();
  const rest = str.substring(colonIdx + 2).replace(/\s+/g, ' ').trim();
  const dashIdx = rest.indexOf(' — ');
  if (dashIdx === -1) return { phase, label: '', text: rest };
  return {
    phase,
    label: rest.substring(0, dashIdx).trim(),
    text: rest.substring(dashIdx + 3).trim(),
  };
}

// ─────────────────────────────────────────────────────────────────
// EXPERIENCE STATE
// ─────────────────────────────────────────────────────────────────

let currentStep = 0;
let currentQuestion = 0;
let answers = [];
let userWeights = { cagan: 0, torres: 0, doshi: 0, lenny: 0, exec: 0 };
let hasVoted = false;
let activePersona = 'cagan';
let comparePersonaA = 'cagan';
let comparePersonaB = 'doshi';
let currentView = 'single';

// ─────────────────────────────────────────────────────────────────
// NAVIGATION
// ─────────────────────────────────────────────────────────────────

function goToStep(step) {
  if (currentStep > 0) {
    const prev = document.getElementById(`screen-${currentStep}`);
    if (prev) prev.classList.remove('active');
  }
  currentStep = step;
  const next = document.getElementById(`screen-${step}`);
  if (next) next.classList.add('active');
  updateTopbar();
  window.scrollTo(0, 0);

  if (step === 1) renderQuizScreen();
  if (step === 2) renderPersonaMatch();
  if (step === 3) renderArena();
  if (step === 4) renderVoteGrid();
  if (step === 5) renderDNACard();
}

function updateTopbar() {
  const fill = document.getElementById('progressFill');
  const label = document.getElementById('progressLabel');
  const dots = document.getElementById('stepDots');
  if (!fill || !label || !dots) return;

  // Problems progress
  const doneCount = PERSONA_ORDER.length > 0
    ? countDoneProblems()
    : 0;
  fill.style.width = `${(doneCount / 10) * 100}%`;
  label.textContent = `${doneCount}/10`;

  // Step dots (5 steps total on experience page)
  dots.innerHTML = '';
  for (let i = 1; i <= 5; i++) {
    const d = document.createElement('div');
    d.className = 'step-dot' +
      (i < currentStep ? ' done' : i === currentStep ? ' active' : '');
    dots.appendChild(d);
  }
}

function countDoneProblems() {
  return Object.keys(localStorage).filter(k => k.startsWith('pmm_done_')).length;
}

// ─────────────────────────────────────────────────────────────────
// STEP 1: QUIZ
// ─────────────────────────────────────────────────────────────────

function renderQuizScreen() {
  currentQuestion = 0;
  answers = [];
  userWeights = { cagan: 0, torres: 0, doshi: 0, lenny: 0, exec: 0 };

  // Set problem statement
  document.getElementById('quizProblemText').innerHTML =
    `<strong>The Problem:</strong> ${escHtml(PROBLEM.prompt)}`;

  // Reset progress bars
  for (let i = 0; i < 3; i++) {
    const seg = document.getElementById(`qseg${i}`);
    if (seg) seg.className = 'quiz-progress-seg' + (i === 0 ? ' active' : '');
  }

  renderQuestion();
}

function renderQuestion() {
  const q = QUESTIONS[currentQuestion];
  const letters = ['A', 'B', 'C', 'D'];

  // Update progress segments
  for (let i = 0; i < 3; i++) {
    const seg = document.getElementById(`qseg${i}`);
    if (seg) {
      seg.className = 'quiz-progress-seg' +
        (i < currentQuestion ? ' done' : i === currentQuestion ? ' active' : '');
    }
  }

  const container = document.getElementById('quizContainer');

  // Answered history
  let answeredHTML = '';
  for (let i = 0; i < currentQuestion; i++) {
    const prevQ = QUESTIONS[i];
    const selectedOpt = prevQ.options[answers[i]];
    answeredHTML += `
      <div class="quiz-answered anim-fade-up">
        <div class="quiz-answered-qnum">Question ${i + 1} of 3</div>
        <div class="quiz-answered-question">${escHtml(prevQ.text)}</div>
        <div class="quiz-answered-selection">
          <div class="quiz-answered-letter">${letters[answers[i]]}</div>
          <div class="quiz-answered-label">${escHtml(selectedOpt.label)}</div>
          <div class="quiz-answered-check">✓</div>
        </div>
      </div>
    `;
  }
  if (currentQuestion > 0) answeredHTML += '<div class="quiz-divider"></div>';

  container.innerHTML = `
    ${answeredHTML}
    <div class="quiz-header anim-fade-up">
      <div class="quiz-q-num">Question ${currentQuestion + 1} of 3</div>
      <div class="quiz-question">${escHtml(q.text)}</div>
    </div>
    <div class="quiz-options">
      ${q.options.map((opt, i) => `
        <div class="quiz-option anim-fade-up delay-${i + 1}" onclick="selectOption(${i})">
          <div class="quiz-option-letter">${letters[i]}</div>
          <div><strong>${escHtml(opt.label)}</strong></div>
          <div style="margin-top:6px;font-size:12px;color:var(--muted);line-height:1.5;">${escHtml(opt.text)}</div>
        </div>
      `).join('')}
    </div>
  `;

  if (currentQuestion > 0) {
    setTimeout(() => {
      const header = container.querySelector('.quiz-header');
      if (header) header.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }, 100);
  }
}

function selectOption(idx) {
  const options = document.querySelectorAll('.quiz-option');
  options.forEach((o, i) => {
    if (i === idx) o.classList.add('selected');
    else { o.style.opacity = '0.3'; o.style.pointerEvents = 'none'; }
  });

  const weights = QUESTIONS[currentQuestion].options[idx].weights;
  Object.keys(weights).forEach(k => { userWeights[k] = (userWeights[k] || 0) + weights[k]; });
  answers.push(idx);

  setTimeout(() => {
    if (currentQuestion < 2) {
      currentQuestion++;
      renderQuestion();
    } else {
      goToStep(2);
    }
  }, 700);
}

// ─────────────────────────────────────────────────────────────────
// STEP 2: PERSONA MATCH
// ─────────────────────────────────────────────────────────────────

function getPersonaBlend() {
  const total = Object.values(userWeights).reduce((a, b) => a + b, 0) || 1;
  const sorted = Object.entries(userWeights)
    .map(([id, w]) => ({ id, pct: Math.round((w / total) * 100) }))
    .sort((a, b) => b.pct - a.pct);

  let sum = sorted.reduce((a, b) => a + b.pct, 0);
  sorted[0].pct += (100 - sum);
  return sorted.filter(p => p.pct > 0);
}

function renderPersonaMatch() {
  const blend = getPersonaBlend();
  const top = blend[0];
  const second = blend[1];

  const p1 = PERSONAS[top.id];
  const p2 = second ? PERSONAS[second.id] : null;

  document.getElementById('revealHeadline').innerHTML =
    `You think like <span class="accent">${escHtml(p1.name)}</span>` +
    (p2 ? ` + <span class="purple">${escHtml(p2.name)}</span>` : '');

  const classes = ['primary', 'secondary', 'tertiary'];
  document.getElementById('blendRow').innerHTML = blend.slice(0, 3).map((p, i) => {
    const persona = PERSONAS[p.id];
    return `
      <div class="persona-blend-card ${classes[i]} anim-scale delay-${i + 1}">
        <div class="persona-blend-pct">${p.pct}%</div>
        <div class="persona-blend-name">${escHtml(persona.name)}</div>
        <div class="persona-blend-role">${escHtml(persona.role)}</div>
      </div>
    `;
  }).join('');

  const key1 = `${top.id}-${second ? second.id : ''}`;
  const key2 = second ? `${second.id}-${top.id}` : '';
  const meaning = BLEND_MEANINGS[key1] || BLEND_MEANINGS[key2] || BLEND_MEANINGS['default'];
  document.getElementById('blendMeaning').innerHTML =
    `<strong>What this means:</strong> ${escHtml(meaning)}`;
}

// ─────────────────────────────────────────────────────────────────
// STEP 3: THE SPLIT + ARENA
// ─────────────────────────────────────────────────────────────────

function renderArena() {
  const split = PROBLEM.theSplit;
  const posClasses = ['pos-0', 'pos-1', 'pos-2'];

  // Render The Split
  document.getElementById('splitQuestion').textContent = split.question;
  document.getElementById('splitPositions').innerHTML = split.sides.map((side, i) => `
    <div class="split-pos">
      <div class="split-pos-label ${posClasses[i] || 'pos-2'}">${escHtml(side.position)}</div>
      <div class="split-pos-personas">
        <strong style="color:var(--text)">${escHtml(side.personas.join(' · '))}</strong><br>
        ${escHtml(side.reasoning)}
      </div>
    </div>
  `).join('');

  // Render tabs
  activePersona = PERSONA_ORDER[0];
  document.getElementById('arenaTabs').innerHTML = PERSONA_ORDER.map(id => {
    const p = PERSONAS[id];
    return `<button class="arena-tab ${id === activePersona ? 'active' : ''}"
      onclick="switchPersona('${id}', this)">${p.emoji} ${escHtml(p.name)}</button>`;
  }).join('');

  renderPersonaPanel(activePersona);
  renderCompareView();
}

function switchPersona(id, el) {
  activePersona = id;
  document.querySelectorAll('.arena-tab').forEach(t => t.classList.remove('active'));
  el.classList.add('active');
  renderPersonaPanel(id);
}

function renderPersonaPanel(id) {
  const p = PERSONAS[id];
  const container = document.getElementById('arenaContent');

  container.innerHTML = `
    <div class="persona-panel active">
      <div class="persona-header">
        <div class="persona-avatar" style="background:${p.color}22;border:1px solid ${p.color}44;">${p.emoji}</div>
        <div class="persona-header-text">
          <h2>${escHtml(p.name)}</h2>
          <p>${escHtml(p.role)} &mdash; ${escHtml(p.tagline)}</p>
        </div>
      </div>

      <div class="spicy-quote">"${escHtml(p.quote)}"</div>

      <div class="two-col">
        <div class="persona-section">
          <h4>Problem Breakdown</h4>
          <ul>${p.breakdown.map(b => `<li>${escHtml(b)}</li>`).join('')}</ul>
        </div>
        <div class="persona-section">
          <h4>Solution Direction</h4>
          <ul>${p.solution.map(s => `<li>${escHtml(s)}</li>`).join('')}</ul>
        </div>
      </div>

      <div class="disagree-box">
        <h4>Where They Disagree</h4>
        <p>${escHtml(p.disagree)}</p>
      </div>

      <div class="two-col">
        <div class="persona-section">
          <h4>MVP Focus</h4>
          <ul>${p.mvp.map(m => `<li>${escHtml(m)}</li>`).join('')}</ul>
        </div>
        <div class="persona-section">
          <h4>Key Metrics</h4>
          <ul>${p.metrics.map(m => `<li>${escHtml(m)}</li>`).join('')}</ul>
        </div>
      </div>

      <div class="persona-section" style="margin-bottom:16px;">
        <h4>Roadmap</h4>
        <div class="roadmap-phases">
          ${p.roadmap.map(r => `
            <div class="roadmap-phase">
              <div class="phase-label" style="color:${p.color}">${escHtml(r.phase)}</div>
              ${r.label ? `<strong style="font-size:12px;display:block;margin-bottom:4px;">${escHtml(r.label)}</strong>` : ''}
              <p>${escHtml(r.text)}</p>
            </div>
          `).join('')}
        </div>
      </div>

      ${renderScoreboard(p)}
    </div>
  `;

  setTimeout(() => animateScores(), 100);
}

function renderScoreboard(p) {
  const dims = [
    { key: 'speed',    label: 'Speed to Market' },
    { key: 'risk',     label: 'Risk Management' },
    { key: 'strategy', label: 'Strategic Clarity' },
    { key: 'growth',   label: 'Growth Potential' },
  ];
  return `
    <div class="scoreboard">
      <h4>Scoreboard</h4>
      ${dims.map(d => {
        const val = p.scores[d.key];
        const color = val >= 7.5 ? 'var(--green)' : val >= 5 ? 'var(--yellow)' : 'var(--red)';
        return `
          <div class="score-row">
            <div class="score-label">${d.label}</div>
            <div class="score-bar-outer">
              <div class="score-bar-fill" data-val="${val}" style="background:${color};"></div>
            </div>
            <div class="score-val" style="color:${color}">${val}</div>
          </div>
        `;
      }).join('')}
    </div>
  `;
}

function animateScores() {
  document.querySelectorAll('.score-bar-fill').forEach(bar => {
    bar.style.width = `${parseFloat(bar.dataset.val) / 10 * 100}%`;
  });
}

function toggleView(view) {
  currentView = view;
  const single = document.getElementById('singleView');
  const compare = document.getElementById('compareViewSection');
  const sBtn = document.getElementById('singleViewBtn');
  const cBtn = document.getElementById('compareViewBtn');

  if (view === 'single') {
    single.style.display = 'block';
    compare.classList.remove('active');
    sBtn.classList.add('active');
    cBtn.classList.remove('active');
  } else {
    single.style.display = 'none';
    compare.classList.add('active');
    sBtn.classList.remove('active');
    cBtn.classList.add('active');
    renderCompareView();
  }
}

function renderCompareView() {
  const section = document.getElementById('compareViewSection');
  if (!section) return;
  const dims = [
    { key: 'speed',    label: 'Speed' },
    { key: 'risk',     label: 'Risk Mgmt' },
    { key: 'strategy', label: 'Strategy' },
    { key: 'growth',   label: 'Growth' },
  ];

  const makeSelect = (selectedId, onchangeFn) =>
    `<select onchange="${onchangeFn}=this.value;renderCompareView();"
      style="background:var(--card2);border:1px solid var(--border);color:var(--text);padding:6px 10px;border-radius:8px;font-size:13px;margin-bottom:14px;">
      ${PERSONA_ORDER.map(id => `<option value="${id}" ${id === selectedId ? 'selected' : ''}>${PERSONAS[id].name}</option>`).join('')}
    </select>`;

  const renderCol = (id, selectHtml) => {
    const p = PERSONAS[id];
    return `
      <div class="compare-col">
        ${selectHtml}
        <div style="font-size:20px;margin-bottom:4px;">${p.emoji} <strong>${escHtml(p.name)}</strong></div>
        <div style="font-size:12px;color:var(--muted);margin-bottom:16px;">${escHtml(p.role)}</div>
        ${dims.map(d => {
          const val = p.scores[d.key];
          const color = val >= 7.5 ? 'var(--green)' : val >= 5 ? 'var(--yellow)' : 'var(--red)';
          return `
            <div class="compare-score-row">
              <div style="font-size:12px;color:var(--muted);width:80px;">${d.label}</div>
              <div class="compare-score-bar">
                <div class="compare-score-fill" style="width:${val/10*100}%;background:${color};"></div>
              </div>
              <div style="font-size:12px;font-weight:700;color:${color};width:24px;text-align:right;">${val}</div>
            </div>
          `;
        }).join('')}
        <div style="margin-top:16px;font-size:13px;color:var(--muted);font-style:italic;line-height:1.5;border-top:1px solid var(--border);padding-top:14px;">
          "${escHtml((p.quote || '').substring(0, 120))}..."
        </div>
      </div>
    `;
  };

  section.innerHTML =
    renderCol(comparePersonaA, makeSelect(comparePersonaA, 'comparePersonaA')) +
    renderCol(comparePersonaB, makeSelect(comparePersonaB, 'comparePersonaB'));
}

// ─────────────────────────────────────────────────────────────────
// STEP 4: VOTE
// ─────────────────────────────────────────────────────────────────

function renderVoteGrid() {
  const problemId = PROBLEM.id;
  const savedVote = localStorage.getItem(`pmm_vote_${problemId}`);
  if (savedVote) hasVoted = true;

  const grid = document.getElementById('voteGrid');
  grid.innerHTML = PERSONA_ORDER.map(id => {
    const p = PERSONAS[id];
    const isVoted = savedVote === id;
    return `
      <div class="vote-card ${isVoted ? 'voted' : ''} ${savedVote && !isVoted ? 'dimmed' : ''} anim-fade-up"
           onclick="castVote('${id}', this)">
        <div class="vote-emoji">${p.emoji}</div>
        <div class="vote-name">${escHtml(p.name)}</div>
        <div class="vote-tagline">${escHtml(p.tagline)}</div>
      </div>
    `;
  }).join('');

  if (savedVote) {
    const p = PERSONAS[savedVote];
    showVotePickSummary(p);
    setTimeout(() => fetchAndShowResults(), 300);
  }
}

async function castVote(id, el) {
  if (hasVoted) return;
  hasVoted = true;

  const problemId = PROBLEM.id;
  localStorage.setItem(`pmm_vote_${problemId}`, id);

  // Highlight selected, dim others
  document.querySelectorAll('.vote-card').forEach(c => {
    if (c === el) c.classList.add('voted');
    else { c.style.opacity = '0.35'; c.style.pointerEvents = 'none'; }
  });

  const p = PERSONAS[id];
  setTimeout(() => showVotePickSummary(p), 600);

  // POST to API
  try {
    await fetch('/api/pmm/votes', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ problem_id: problemId, persona: id }),
    });
  } catch (e) {
    // Vote stored in localStorage, API failure is non-fatal
  }
}

function showVotePickSummary(p) {
  document.getElementById('voteYourPick').innerHTML = `
    <div class="vote-your-pick-emoji">${p.emoji}</div>
    <div>
      <div class="vote-your-pick-label">Your pick</div>
      <div class="vote-your-pick-name">${escHtml(p.name)}</div>
      <div class="vote-your-pick-tagline">${escHtml(p.tagline)}</div>
    </div>
    <div style="margin-left:auto;color:var(--accent);font-size:16px;">✓</div>
  `;
  const part2 = document.getElementById('votePart2');
  part2.style.display = 'block';
  part2.scrollIntoView({ behavior: 'smooth', block: 'center' });
}

function react(btn, type) {
  document.querySelectorAll('.reaction-btn').forEach(b => {
    b.classList.remove('active');
    b.style.opacity = '0.4';
    b.style.pointerEvents = 'none';
  });
  btn.classList.add('active');
  btn.style.opacity = '1';
  localStorage.setItem(`pmm_reaction_${PROBLEM.id}`, type);
  setTimeout(() => fetchAndShowResults(), 500);
}

async function fetchAndShowResults() {
  let counts = {};
  try {
    counts = await fetch('/api/pmm/votes/' + encodeURIComponent(PROBLEM.id)).then(r => r.json());
  } catch (e) {
    counts = {};
  }

  // Build display percents: use DB counts if we have them, else fall back to seed
  const total = Object.values(counts).reduce((a, b) => a + b, 0);
  let percents;
  if (total > 0) {
    percents = {};
    PERSONA_ORDER.forEach(id => {
      percents[id] = Math.round(((counts[id] || 0) / total) * 100);
    });
    // Normalize to 100
    const sum = Object.values(percents).reduce((a, b) => a + b, 0);
    const topKey = PERSONA_ORDER.reduce((a, b) => percents[a] > percents[b] ? a : b);
    percents[topKey] += (100 - sum);
  } else {
    // Seed data as percentages (they sum to 100 by design)
    percents = { ...VOTE_SEED };
  }

  showVoteResults(percents, total);
}

function showVoteResults(percents, totalVotes) {
  const results = document.getElementById('voteResults');
  results.classList.add('show');

  const bars = document.getElementById('voteResultBars');
  bars.innerHTML = PERSONA_ORDER.map(id => {
    const p = PERSONAS[id];
    const pct = percents[id] || 0;
    return `
      <div class="vote-result-bar-row">
        <div class="vote-result-name">${p.emoji} ${escHtml(p.name)}</div>
        <div class="vote-result-bar-outer">
          <div class="vote-result-bar-fill" data-pct="${pct}"></div>
        </div>
        <div class="vote-result-pct">${pct}%</div>
      </div>
    `;
  }).join('');

  if (totalVotes > 0) {
    bars.insertAdjacentHTML('afterend',
      `<p style="font-size:11px;color:var(--muted);margin-top:8px;text-align:right;">${totalVotes} vote${totalVotes !== 1 ? 's' : ''} total</p>`);
  }

  setTimeout(() => {
    document.querySelectorAll('.vote-result-bar-fill').forEach(bar => {
      bar.style.width = bar.dataset.pct + '%';
    });
  }, 100);

  setTimeout(() => results.scrollIntoView({ behavior: 'smooth', block: 'center' }), 200);
}

// ─────────────────────────────────────────────────────────────────
// STEP 5: DNA CARD
// ─────────────────────────────────────────────────────────────────

function renderDNACard() {
  // Mark this problem as done
  localStorage.setItem(`pmm_done_${PROBLEM.id}`, '1');

  const blend = getPersonaBlend();
  const colors = {
    cagan: '#ff6b8a', torres: '#5ee4ff', doshi: '#c49bff',
    lenny: '#ffb86c', exec: '#7cf49a',
  };

  // Count completed problems
  const doneKeys = Object.keys(localStorage).filter(k => k.startsWith('pmm_done_'));
  const doneCount = doneKeys.length;
  const unlocked = doneCount >= 3;

  // Complete banner
  document.getElementById('completeBannerMsg').textContent =
    `You've tackled ${escHtml(PROBLEM.title)}. Your PM instincts have been recorded.`;

  // Unlock progress dots
  const dots = document.getElementById('unlockDots');
  const unlockLabel = document.getElementById('unlockLabel');
  dots.innerHTML = [1, 2, 3].map(n => {
    const isDone = doneCount >= n;
    const isCurrent = !isDone && doneCount === n - 1;
    return `<div class="unlock-dot ${isDone ? 'done' : ''} ${isCurrent ? 'current' : ''}">${isDone ? '✓' : n}</div>`;
  }).join('');

  if (unlocked) {
    unlockLabel.textContent = 'Your PM DNA Card is unlocked!';
  } else {
    const needed = 3 - doneCount;
    unlockLabel.textContent = `Complete ${needed} more problem${needed !== 1 ? 's' : ''} to unlock your shareable PM DNA Card`;
  }

  // Donut SVG
  const svg = document.getElementById('donutSvg');
  const cx = 70, cy = 70, r = 52, strokeWidth = 18;
  const circumference = 2 * Math.PI * r;
  let runningOffset = 0;

  svg.innerHTML = blend.slice(0, 3).map(p => {
    const dash = (p.pct / 100) * circumference;
    const start = runningOffset;
    runningOffset += dash;
    return `<circle cx="${cx}" cy="${cy}" r="${r}" fill="none"
      stroke="${colors[p.id] || '#444'}" stroke-width="${strokeWidth}"
      stroke-dasharray="${dash} ${circumference - dash}"
      stroke-dashoffset="${circumference - start}"
      transform="rotate(-90 ${cx} ${cy})"/>`;
  }).join('');

  // Legend
  document.getElementById('dnaLegend').innerHTML = blend.slice(0, 3).map(p => `
    <div class="dna-legend-item">
      <div class="dna-legend-dot" style="background:${colors[p.id]};"></div>
      <span>${escHtml(PERSONAS[p.id].name)} ${p.pct}%</span>
    </div>
  `).join('');

  // Archetype from problem JSON pmDnaBlends
  const top = blend[0];
  const second = blend[1];
  const blends = PROBLEM.pmDnaBlends || {};
  const key1 = `${top.id}_${second ? second.id : ''}`;
  const key2 = second ? `${second.id}_${top.id}` : '';
  const dnaBlend = blends[key1] || blends[key2] || null;

  // Fallback archetypes (top persona based)
  const fallbackArchetypes = {
    cagan: { name: 'The Risk Architect',    tagline: 'You lead with validation and never ship without receipts' },
    torres: { name: 'The Evidence Builder', tagline: 'You need to know why before you commit to what' },
    doshi: { name: 'The Strategic Wedge',   tagline: 'You find the sharpest bet and cut through the noise' },
    lenny: { name: 'The Loop Engineer',     tagline: 'You see growth mechanics where others see features' },
    exec: { name: 'The Velocity Machine',   tagline: 'You know speed is strategy and learn by doing' },
  };
  const arch = dnaBlend || fallbackArchetypes[top.id];

  document.getElementById('dnaArchetype').textContent = arch.name;
  document.getElementById('dnaTagline').textContent = `"${arch.tagline}"`;

  // Show/blur the card
  const cardEl = document.getElementById('dnaCardPreview');
  const lockOverlay = document.getElementById('dnaLockOverlay');
  const shareBtn = document.getElementById('shareBtn');

  if (unlocked) {
    cardEl.classList.remove('dna-card-blur');
    if (lockOverlay) lockOverlay.style.display = 'none';
    if (shareBtn) shareBtn.classList.remove('btn-disabled');
  }
}

// ─────────────────────────────────────────────────────────────────
// UTILITIES
// ─────────────────────────────────────────────────────────────────

function escHtml(str) {
  if (str == null) return '';
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}
