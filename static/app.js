/**
 * IMU CET ONLINE CBT TEST PORTAL - CLIENT APPLICATION
 * Minimalist Light Mode Study Interface (Notion / Linear inspired)
 * Features: NTA/IMU Standard CBT Engine, MathJax LaTeX Parsing, Live Question Palette,
 * Official Marking Scheme (+1.0 / -0.25), Step-by-Step Solutions, and Sectional Practice.
 */

(function () {
  'use strict';

  // Application State
  const state = {
    exams: [],
    chapters: [],
    activeExam: null,
    pendingExamConfig: null,
    questions: [],
    currentIndex: 0,
    responses: {},       // { [qid]: "A" | "B" | "C" | "D" }
    questionStatus: {},  // { [qid]: "not_visited" | "not_answered" | "answered" | "review" | "answered_review" }
    timeRemainingSeconds: 0,
    totalTimeSeconds: 0,
    timerInterval: null,
    isSubmitting: false,
    submissionResult: null,
    currentReviewFilter: 'all',
    // Lightweight Webcam-Free Proctoring State
    proctoring: {
      active: false,
      warningCount: 0,
      tabSwitches: 0,
      fullscreenExits: 0,
      totalAwaySeconds: 0,
      tabAwayStartTime: null,
      windowBlurStartTime: null,
      lastEventTimestamp: 0,
      lastEventType: null,
      events: []
    }
  };

  // Section Duration presets in minutes
  const SECTION_DURATIONS = {
    "English": 35,
    "General Aptitude, Reasoning & GK": 35,
    "Mathematics": 50,
    "Physics": 50,
    "Chemistry": 20,
    "Full": 180
  };

  // DOM Elements Cache
  const el = {
    headerDbStatus: document.getElementById('db-connection-text'),
    brandHomeBtn: document.getElementById('brand-home-btn'),
    navHomeBtn: document.getElementById('nav-home-btn'),
    navTestsBtn: document.getElementById('nav-tests-btn'),
    navChaptersBtn: document.getElementById('nav-chapters-btn'),
    navInstructionsBtn: document.getElementById('nav-instructions-btn'),
    navResultsBtn: document.getElementById('nav-results-btn'),
    testHeaderControls: document.getElementById('test-header-controls'),
    timerDisplay: document.getElementById('cbt-timer-display'),
    btnHeaderSubmit: document.getElementById('btn-header-submit'),
    btnInstallPwa: document.getElementById('btn-install-pwa'),

    // Views
    viewDashboard: document.getElementById('view-dashboard'),
    viewTest: document.getElementById('view-test'),
    viewResults: document.getElementById('view-results'),

    // Dashboard
    examsGrid: document.getElementById('exams-grid'),
    filterFullBtn: document.getElementById('filter-full-btn'),
    filterSectionBtn: document.getElementById('filter-section-btn'),
    filterChapterBtn: document.getElementById('filter-chapter-btn'),

    // CBT Interface
    examTitle: document.getElementById('cbt-exam-title'),
    sectionTabsBar: document.getElementById('section-tabs-bar'),
    qNumberPill: document.getElementById('q-number-pill'),
    qSectionBadge: document.getElementById('q-section-badge'),
    qTopicBadge: document.getElementById('q-topic-badge'),
    qDiffBadge: document.getElementById('q-diff-badge'),
    questionTextBox: document.getElementById('question-text-box'),
    optionsContainer: document.getElementById('options-container'),

    // Action buttons
    btnMarkReview: document.getElementById('btn-mark-review'),
    btnClearResponse: document.getElementById('btn-clear-response'),
    btnPrevQuestion: document.getElementById('btn-prev-question'),
    btnSaveNext: document.getElementById('btn-save-next'),
    btnSubmitTest: document.getElementById('btn-submit-test'),

    // Palette
    paletteSectionName: document.getElementById('palette-section-name'),
    paletteGrid: document.getElementById('palette-grid'),
    statAnswered: document.getElementById('stat-answered'),
    statNotAnswered: document.getElementById('stat-not-answered'),
    statNotVisited: document.getElementById('stat-not-visited'),
    statReview: document.getElementById('stat-review'),
    statAnsweredReview: document.getElementById('stat-answered-review'),
    btnPaletteSummary: document.getElementById('btn-palette-summary'),
    btnTogglePalette: document.getElementById('btn-toggle-palette'),
    btnClosePalette: document.getElementById('btn-close-palette'),
    paletteBackdrop: document.getElementById('palette-backdrop'),
    paletteSidebar: document.getElementById('cbt-palette-sidebar'),

    // Confirmation Modal
    modalConfirmSubmit: document.getElementById('modal-confirm-submit'),
    modalSummaryTbody: document.getElementById('modal-summary-tbody'),
    btnModalCancel: document.getElementById('btn-modal-cancel'),
    btnModalConfirm: document.getElementById('btn-modal-confirm'),

    // Instructions Modal
    modalInstructions: document.getElementById('modal-instructions'),
    modalInstructionsExamName: document.getElementById('modal-instructions-exam-name'),
    instDurationVal: document.getElementById('inst-duration-val'),
    instQuestionsVal: document.getElementById('inst-questions-val'),
    btnCloseInstructionsX: document.getElementById('btn-close-instructions-x'),
    btnModalInstructionsCancel: document.getElementById('btn-modal-instructions-cancel'),
    btnModalInstructionsStart: document.getElementById('btn-modal-instructions-start'),

    // Results
    resExamTitle: document.getElementById('res-exam-title'),
    resTimestamp: document.getElementById('res-timestamp'),
    resScore: document.getElementById('res-score'),
    resMaxScore: document.getElementById('res-max-score'),
    resAccuracy: document.getElementById('res-accuracy'),
    resPercentage: document.getElementById('res-percentage'),
    resCorrect: document.getElementById('res-correct'),
    resIncorrect: document.getElementById('res-incorrect'),
    resUnanswered: document.getElementById('res-unanswered'),
    resTimeSpent: document.getElementById('res-time-spent'),
    sectionalTbody: document.getElementById('sectional-tbody'),
    reviewList: document.getElementById('review-list'),
    cntRevAll: document.getElementById('cnt-rev-all'),
    cntRevCorr: document.getElementById('cnt-rev-corr'),
    cntRevInc: document.getElementById('cnt-rev-inc'),
    cntRevUnans: document.getElementById('cnt-rev-unans'),
    btnDownloadPdf: document.getElementById('btn-download-pdf'),
    btnRetakeExam: document.getElementById('btn-retake-exam'),
    btnBackDashboard: document.getElementById('btn-back-dashboard'),
    btnPrintResults: document.getElementById('btn-print-results'),
    pdfToast: document.getElementById('pdf-toast'),
    pdfToastText: document.getElementById('pdf-toast-text'),

    // Lightweight Proctoring Elements
    proctorStatusBadge: document.getElementById('proctor-status-badge'),
    proctorStatusText: document.getElementById('proctor-status-text'),
    proctorWarningBanner: document.getElementById('proctor-warning-banner'),
    proctorWarningTitle: document.getElementById('proctor-warning-title'),
    proctorWarningMsg: document.getElementById('proctor-warning-msg'),
    btnProctorAction: document.getElementById('btn-proctor-action'),
    btnProctorDismiss: document.getElementById('btn-proctor-dismiss'),
    resProctorTabSwitches: document.getElementById('res-proctor-tab-switches'),
    resProctorFullscreenExits: document.getElementById('res-proctor-fullscreen-exits'),
    resProctorAwayTime: document.getElementById('res-proctor-away-time'),
    resProctorTotalAlerts: document.getElementById('res-proctor-total-alerts'),
    proctorLogTbody: document.getElementById('proctor-log-tbody')
  };

  // ==========================================================================
  // MATHEMATICAL & LATEX RENDERING ENGINE
  // ==========================================================================
  const MATH_KEYWORDS = new Set([
    "sin", "cos", "tan", "cot", "sec", "csc", "log", "ln", "lim", "det", 
    "dx", "dy", "dz", "dt", "sqrt", "frac", "int", "lambda", "omega", "theta"
  ]);

  function isMathWord(word) {
    const clean = word.replace(/[:,.;?(){}[\]]/g, '');
    if (!clean) return false;
    if (word.startsWith('\\') || word.includes('^') || word.includes('_') || word.includes('{') || word.includes('}')) return true;
    if (/^[0-9.]+$/.test(clean)) return true;
    if (['+', '-', '*', '/', '=', '<', '>', '|', '||', '->', '\\to', '=>'].includes(clean)) return true;
    if (clean.length === 1 && /[a-zA-Z]/.test(clean)) return true;
    if (/^[a-zA-Z]\([a-zA-Z0-9,+-/*\s]+\)$/.test(clean)) return true;
    if (MATH_KEYWORDS.has(clean.toLowerCase())) return true;
    return false;
  }

  function formatMathContent(text, isOption = false) {
    if (!text) return '';
    let str = String(text);

    // 1. Preserve fill-in-the-blank lines like ______
    const blankPlaceholders = [];
    str = str.replace(/_{2,}/g, (match) => {
      blankPlaceholders.push(match);
      return `###CBT_BLANK_${blankPlaceholders.length - 1}###`;
    });

    // If text already has MathJax delimiters, return directly with blanks restored
    if (/\\\([\s\S]*?\\\)|\$[\s\S]*?\$|\\\[[\s\S]*?\\\]/.test(str)) {
      blankPlaceholders.forEach((blank, idx) => {
        str = str.replace(`###CBT_BLANK_${idx}###`, `<span class="cbt-blank">${blank}</span>`);
      });
      return str;
    }

    // Check if string is purely a math formula without English sentence structure
    const hasEnglishWords = /\b(what|find|calculate|which|the|is|are|of|in|to|for|with|from|by|at|if|then|when|where|let|suppose|determine|evaluate|given|consider|true|false|equal|matrix|triangle|vector)\b/i.test(str);
    const hasMathSyntax = str.includes('\\') || str.includes('^') || str.includes('_') || /[-+*/=]/.test(str);

    if ((isOption || !hasEnglishWords) && hasMathSyntax) {
      let cleanFormula = str.trim();
      let trail = '';
      while (cleanFormula && /[:,.;?!]/.test(cleanFormula.slice(-1))) {
        trail = cleanFormula.slice(-1) + trail;
        cleanFormula = cleanFormula.slice(0, -1);
      }
      return `\\(${cleanFormula}\\)${trail}`;
    }

    // Question text: split by words and group mathematical clusters
    const tokens = str.split(' ');
    const outTokens = [];
    let mathBuf = [];

    const flushMath = () => {
      if (!mathBuf.length) return;
      let segment = mathBuf.join(' ');
      mathBuf = [];

      let trail = '';
      while (segment && /[:,.;?!]/.test(segment.slice(-1))) {
        trail = segment.slice(-1) + trail;
        segment = segment.slice(0, -1);
      }

      const hasRealMath = segment.includes('\\') || segment.includes('^') || segment.includes('_') || segment.includes('{') || segment.includes('}') || /[-+*/=]/.test(segment);
      if (hasRealMath) {
        outTokens.push(`\\(${segment}\\)${trail}`);
      } else {
        outTokens.push(`${segment}${trail}`);
      }
    };

    for (const t of tokens) {
      const clean = t.replace(/[:,.;?!(){}[\]]/g, '');
      if (t.includes('\\') || t.includes('^') || t.includes('_') || t.includes('{') || t.includes('}') || (clean.length === 1 && /[a-zA-Z]/.test(clean)) || ['+', '-', '=', '*', '/'].includes(clean) || /^[a-zA-Z]\([a-zA-Z0-9,\s\-+*/]+\)$/.test(clean)) {
        mathBuf.push(t);
      } else if (isMathWord(t)) {
        mathBuf.push(t);
      } else {
        flushMath();
        outTokens.push(t);
      }
    }
    flushMath();
    str = outTokens.join(' ');

    // Restore fill-in-the-blank placeholders
    blankPlaceholders.forEach((blank, idx) => {
      str = str.replace(`###CBT_BLANK_${idx}###`, `<span class="cbt-blank">${blank}</span>`);
    });

    return str;
  }

  function renderMath(targetElement) {
    if (!targetElement) return;
    if (window.MathJax && window.MathJax.typesetPromise) {
      window.MathJax.typesetPromise([targetElement]).catch((err) => {
        console.warn("MathJax rendering warning:", err);
      });
    }
  }

  // ==========================================================================
  // VIEW ROUTER
  // ==========================================================================
  function showView(viewName) {
    el.viewDashboard.classList.add('hidden');
    el.viewTest.classList.add('hidden');
    el.viewResults.classList.add('hidden');

    // Update global nav active state
    if (el.navHomeBtn) el.navHomeBtn.classList.remove('active');
    if (el.navTestsBtn) el.navTestsBtn.classList.remove('active');
    if (el.navChaptersBtn) el.navChaptersBtn.classList.remove('active');
    if (el.navInstructionsBtn) el.navInstructionsBtn.classList.remove('active');
    if (el.navResultsBtn) el.navResultsBtn.classList.remove('active');

    if (viewName === 'dashboard') {
      el.viewDashboard.classList.remove('hidden');
      el.testHeaderControls.classList.add('hidden');
      if (el.navHomeBtn) el.navHomeBtn.classList.add('active');
      clearInterval(state.timerInterval);
      window.scrollTo({ top: 0, behavior: 'smooth' });
    } else if (viewName === 'test') {
      el.viewTest.classList.remove('hidden');
      el.testHeaderControls.classList.remove('hidden');
      window.scrollTo({ top: 0, behavior: 'smooth' });
    } else if (viewName === 'results') {
      el.viewResults.classList.remove('hidden');
      el.testHeaderControls.classList.add('hidden');
      if (el.navResultsBtn) {
        el.navResultsBtn.classList.remove('hidden');
        el.navResultsBtn.classList.add('active');
      }
      clearInterval(state.timerInterval);
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }
  }

  // ==========================================================================
  // INSTRUCTIONS MODAL
  // ==========================================================================
  function openInstructionsModal(examConfig = null) {
    state.pendingExamConfig = examConfig;

    if (examConfig) {
      el.modalInstructionsExamName.textContent = examConfig.title;
      let durationMins = 50;
      let qCountText = 'Subject Test';
      
      if (examConfig.exam_type === 'chapter' || examConfig.chapter) {
        durationMins = examConfig.duration_minutes || 50;
        qCountText = `${examConfig.total_questions || 50} Questions (Chapter Mock)`;
      } else if (examConfig.section === 'all') {
        durationMins = SECTION_DURATIONS["Full"];
        qCountText = '200 Questions';
      } else {
        durationMins = SECTION_DURATIONS[examConfig.section] || 50;
        qCountText = 'Subject Test';
      }
      el.instDurationVal.textContent = `${durationMins} Minutes`;
      el.instQuestionsVal.textContent = qCountText;
      el.btnModalInstructionsStart.textContent = 'Start Test Now';
      el.btnModalInstructionsStart.classList.remove('hidden');
    } else {
      el.modalInstructionsExamName.textContent = 'General Candidate Guidelines';
      el.instDurationVal.textContent = '180 Minutes (Full) / 20–50 Mins (Subject & Chapter)';
      el.instQuestionsVal.textContent = '200 Questions (Full Paper) / 50 Qs (Chapter)';
      el.btnModalInstructionsStart.textContent = 'Begin Default Test';
      // Default to first exam if available
      if (state.exams.length) {
        const first = state.exams[0];
        state.pendingExamConfig = {
          year: first.year,
          shift: first.shift,
          section: 'all',
          title: `${first.title} - Full Mock`
        };
      }
    }

    el.modalInstructions.classList.remove('hidden');
  }

  function closeInstructionsModal() {
    el.modalInstructions.classList.add('hidden');
    state.pendingExamConfig = null;
  }

  // ==========================================================================
  // DASHBOARD & EXAM FETCHING
  // ==========================================================================
  async function loadExams() {
    try {
      const response = await fetch('/api/exams');
      if (!response.ok) throw new Error('Failed to load exam data');
      const data = await response.json();
      state.exams = data.exams || [];
      state.chapters = data.chapters || [];

      // Fallback check if chapters wasn't present in exams endpoint
      if (!state.chapters.length) {
        try {
          const chRes = await fetch('/api/chapters');
          if (chRes.ok) {
            const chData = await chRes.json();
            state.chapters = chData.chapters || [];
          }
        } catch (_) {}
      }

      renderExamsGrid('full');
      
      const totalFull = state.exams.reduce((sum, e) => sum + (e.total_questions || 0), 0);
      const totalChapters = state.chapters.reduce((sum, c) => sum + (c.total_questions || 0), 0);
      const totalAvailable = totalFull + totalChapters;
      if (el.headerDbStatus) {
        el.headerDbStatus.textContent = `${totalAvailable} Questions Available (${totalFull} Full · ${totalChapters} Chapter)`;
      }
    } catch (err) {
      console.error(err);
      el.examsGrid.innerHTML = `
        <div class="loading-state">
          <p style="color: var(--state-danger-text); font-weight: 600;">Could not connect to test database.</p>
          <p style="font-size: 0.85rem; margin-top: 6px;">Ensure server.py is running on port 8000.</p>
        </div>
      `;
    }
  }

  function renderChapterCards() {
    if (!state.chapters || !state.chapters.length) {
      el.examsGrid.innerHTML = `
        <div class="loading-state">
          <p style="color: var(--text-primary); font-weight: 600;">No chapter mock papers detected.</p>
          <p style="font-size: 0.85rem; margin-top: 6px;">Ensure chapter database is present in the chapter folder.</p>
        </div>
      `;
      return;
    }

    el.examsGrid.innerHTML = '';

    state.chapters.forEach((ch) => {
      const card = document.createElement('article');
      card.className = 'chapter-mock-card';
      card.setAttribute('data-chapter', ch.id);

      const easyCnt = (ch.difficulty && ch.difficulty.easy) || 0;
      const medCnt = (ch.difficulty && ch.difficulty.medium) || 0;
      const hardCnt = (ch.difficulty && ch.difficulty.hard) || 0;
      const total = ch.total_questions || (easyCnt + medCnt + hardCnt) || 50;
      const easyPct = Math.round((easyCnt / total) * 100);
      const medPct = Math.round((medCnt / total) * 100);
      const hardPct = Math.max(0, 100 - easyPct - medPct);

      const topicOptions = (ch.topics || []).map(t => `
        <option value="${encodeURIComponent(t.name)}">${t.name} (${t.count} Qs)</option>
      `).join('');

      const topicChips = (ch.topics || []).map(t => `
        <span class="chapter-topic-chip" title="${t.name}: ${t.count} questions">
          ${t.name} <small>(${t.count})</small>
        </span>
      `).join('');

      card.innerHTML = `
        <div class="exam-card-header">
          <div style="display:flex; gap:6px; align-items:center;">
            <span class="chapter-subject-tag">${ch.subject || 'Mathematics'}</span>
            <span class="chapter-badge-tag">Chapter Mock #1</span>
          </div>
          <span class="exam-total-pill">${total} Questions · ${ch.duration_minutes || 50}m</span>
        </div>

        <div>
          <h3 class="exam-card-title">${ch.title}</h3>
          <p class="chapter-desc-text" style="margin-top: 6px;">
            Master this high-weightage chapter for IMU CET entrance with a full CBT exam simulation covering order, degree, separable variables, integrating factors, homogeneous equations, and applications.
          </p>
        </div>

        <div class="chapter-topics-container">
          <div class="chapter-topics-header">Core Syllabus Topics (${(ch.topics || []).length}):</div>
          <div class="chapter-topics-wrap">
            ${topicChips}
          </div>
        </div>

        <div class="chapter-diff-bar-container">
          <div class="chapter-diff-labels">
            <span><span class="diff-dot easy"></span>Easy: ${easyCnt}</span>
            <span><span class="diff-dot medium"></span>Medium: ${medCnt}</span>
            <span><span class="diff-dot hard"></span>Hard: ${hardCnt}</span>
          </div>
          <div class="chapter-diff-track">
            <div class="chapter-diff-seg easy" style="width: ${easyPct}%;" title="Easy (${easyCnt})"></div>
            <div class="chapter-diff-seg medium" style="width: ${medPct}%;" title="Medium (${medCnt})"></div>
            <div class="chapter-diff-seg hard" style="width: ${hardPct}%;" title="Hard (${hardCnt})"></div>
          </div>
        </div>

        <div class="chapter-marking-pill">
          <span>Marking Scheme:</span>
          <strong>+1.0 Correct</strong> · 
          <strong>-0.25 Negative</strong> · 
          <span>0.0 Unattempted</span>
        </div>

        <div class="exam-card-actions">
          <button class="btn btn-primary btn-block btn-start-chapter" 
                  data-chapter="${ch.id}"
                  data-title="${ch.title} — Chapter Mock Test">
            Start Full Chapter Mock (${total} Qs · 50m)
          </button>

          <div class="chapter-topic-row">
            <select class="cbt-select topic-picker-select" aria-label="Select Specific Topic">
              <option value="all">Practice All Topics (${total} Qs)</option>
              ${topicOptions}
            </select>
            <button class="btn btn-secondary btn-start-topic" 
                    data-chapter="${ch.id}"
                    data-title="${ch.title}">
              Practice Topic
            </button>
          </div>
        </div>
      `;

      // Event listener for full chapter mock button
      const startChBtn = card.querySelector('.btn-start-chapter');
      if (startChBtn) {
        startChBtn.addEventListener('click', () => {
          openInstructionsModal({
            exam_type: 'chapter',
            chapter: ch.id,
            section: ch.subject || 'Mathematics',
            duration_minutes: ch.duration_minutes || 50,
            total_questions: total,
            title: `${ch.title} — Chapter Mock Test`
          });
        });
      }

      // Event listener for topic practice
      const startTopicBtn = card.querySelector('.btn-start-topic');
      const topicSelect = card.querySelector('.topic-picker-select');
      if (startTopicBtn && topicSelect) {
        startTopicBtn.addEventListener('click', () => {
          const rawVal = topicSelect.value;
          if (rawVal === 'all') {
            openInstructionsModal({
              exam_type: 'chapter',
              chapter: ch.id,
              section: ch.subject || 'Mathematics',
              duration_minutes: ch.duration_minutes || 50,
              total_questions: total,
              title: `${ch.title} — Chapter Mock Test`
            });
          } else {
            const topicName = decodeURIComponent(rawVal);
            const tObj = (ch.topics || []).find(t => t.name === topicName);
            const qCnt = tObj ? tObj.count : 10;
            const durationMins = Math.max(15, Math.round(qCnt * 1.5));
            openInstructionsModal({
              exam_type: 'chapter',
              chapter: ch.id,
              topic: topicName,
              section: ch.subject || 'Mathematics',
              duration_minutes: durationMins,
              total_questions: qCnt,
              title: `${ch.title} (${topicName}) — Topic Practice`
            });
          }
        });
      }

      el.examsGrid.appendChild(card);
    });
  }

  window.switchFilter = function(filter) {
    document.querySelectorAll('.filter-tab').forEach(b => {
      if (b.getAttribute('data-filter') === filter) {
        b.classList.add('active');
      } else {
        b.classList.remove('active');
      }
    });
    if (el.navChaptersBtn && el.navHomeBtn) {
      if (filter === 'chapter') {
        el.navChaptersBtn.classList.add('active');
        el.navHomeBtn.classList.remove('active');
      } else {
        el.navChaptersBtn.classList.remove('active');
        el.navHomeBtn.classList.add('active');
      }
    }
    renderExamsGrid(filter);
  };

  function renderExamsGrid(filter = 'full') {
    if (filter === 'chapter') {
      if (!state.chapters || !state.chapters.length) {
        el.examsGrid.innerHTML = `
          <div class="loading-state">
            <div class="spinner"></div>
            <p style="margin-top: 10px;">Loading Chapter Mock papers...</p>
          </div>
        `;
        fetch('/api/chapters')
          .then(res => res.json())
          .then(data => {
            state.chapters = data.chapters || [];
            if (!state.chapters.length) {
              return fetch('/api/exams').then(r => r.json()).then(exData => {
                state.chapters = exData.chapters || [];
              });
            }
          })
          .catch(err => {
            console.error('Failed to load chapters:', err);
          })
          .finally(() => {
            renderChapterCards();
          });
        return;
      }

      renderChapterCards();
      return;
    }

    if (!state.exams.length) {
      el.examsGrid.innerHTML = '<div class="loading-state"><p>No usable exams found in database.</p></div>';
      return;
    }

    el.examsGrid.innerHTML = '';

    state.exams.forEach((exam) => {
      const card = document.createElement('article');
      card.className = 'exam-card';
      card.setAttribute('data-year', exam.year);

      const shiftTag = exam.shift ? `${exam.shift}` : 'Official';

      let actionsHtml = '';
      let metaPillText = `${exam.total_questions} Questions · 180m`;

      if (filter === 'section') {
        // Sectional Practice View
        metaPillText = `${exam.sections.length} Subjects Available`;
        const selectOptions = exam.sections.map(s => `
          <option value="${encodeURIComponent(s.section)}">${s.section} (${s.count} Qs)</option>
        `).join('');

        actionsHtml = `
          <div class="sectional-select-row">
            <select class="cbt-select section-picker-select" aria-label="Select Subject">
              <option value="">Subject Practice...</option>
              ${selectOptions}
            </select>
            <button class="btn btn-primary btn-start-section"
                    data-year="${exam.year}" 
                    data-shift="${exam.shift || ''}"
                    data-title="${exam.title}">
              Practice
            </button>
          </div>
        `;
      } else {
        // Full Mock View (Default)
        actionsHtml = `
          <button class="btn btn-primary btn-block btn-start-full" 
                  data-year="${exam.year}" 
                  data-shift="${exam.shift || ''}"
                  data-title="${exam.title} - Full Mock">
            Start Mock
          </button>
        `;
      }

      card.innerHTML = `
        <div class="exam-card-header">
          <span class="exam-year-tag">${exam.year} · ${shiftTag}</span>
          <span class="exam-total-pill">${metaPillText}</span>
        </div>
        <h3 class="exam-card-title">${exam.title}</h3>
        <div class="exam-card-actions">
          ${actionsHtml}
        </div>
      `;

      // Event listener for Full Mock button
      const startFullBtn = card.querySelector('.btn-start-full');
      if (startFullBtn) {
        startFullBtn.addEventListener('click', () => {
          openInstructionsModal({
            year: exam.year,
            shift: exam.shift,
            section: 'all',
            title: `${exam.title} (Full Mock)`
          });
        });
      }

      // Event listener for sectional select dropdown
      const startSecBtn = card.querySelector('.btn-start-section');
      const secPicker = card.querySelector('.section-picker-select');
      if (startSecBtn && secPicker) {
        startSecBtn.addEventListener('click', () => {
          const chosenSection = decodeURIComponent(secPicker.value);
          if (!chosenSection) {
            alert('Please select a subject to practice.');
            return;
          }
          openInstructionsModal({
            year: exam.year,
            shift: exam.shift,
            section: chosenSection,
            title: `${exam.title} - ${chosenSection}`
          });
        });
      }

      el.examsGrid.appendChild(card);
    });
  }

  // ==========================================================================
  // LIGHTWEIGHT WEBCAM-FREE PROCTORING MODULE
  // ==========================================================================
  let proctorWarningTimer = null;

  function isFullscreen() {
    return !!(
      document.fullscreenElement ||
      document.webkitFullscreenElement ||
      document.mozFullScreenElement ||
      document.msFullscreenElement
    );
  }

  function requestTestFullscreen() {
    try {
      const de = document.documentElement;
      if (de.requestFullscreen) {
        de.requestFullscreen().catch(() => {
          // Gracefully handle unsupported or restricted fullscreen (e.g. mobile/iframe environments)
        });
      } else if (de.webkitRequestFullscreen) {
        de.webkitRequestFullscreen();
      } else if (de.mozRequestFullScreen) {
        de.mozRequestFullScreen();
      } else if (de.msRequestFullscreen) {
        de.msRequestFullscreen();
      }
    } catch (e) {
      // Non-blocking catch
    }
  }

  function exitTestFullscreen() {
    try {
      if (isFullscreen()) {
        if (document.exitFullscreen) {
          document.exitFullscreen().catch(() => {});
        } else if (document.webkitExitFullscreen) {
          document.webkitExitFullscreen();
        } else if (document.mozCancelFullScreen) {
          document.mozCancelFullScreen();
        } else if (document.msExitFullscreen) {
          document.msExitFullscreen();
        }
      }
    } catch (e) {}
  }

  function showProctoringWarning(options) {
    if (!el.proctorWarningBanner) return;
    if (proctorWarningTimer) clearTimeout(proctorWarningTimer);

    if (el.proctorWarningTitle) el.proctorWarningTitle.textContent = options.title || 'Integrity Alert';
    if (el.proctorWarningMsg) el.proctorWarningMsg.textContent = options.message || '';

    if (options.actionText && el.btnProctorAction) {
      el.btnProctorAction.textContent = options.actionText;
      el.btnProctorAction.style.display = 'inline-flex';
      el.btnProctorAction.onclick = () => {
        if (typeof options.onAction === 'function') options.onAction();
      };
    } else if (el.btnProctorAction) {
      el.btnProctorAction.style.display = 'none';
    }

    el.proctorWarningBanner.classList.remove('hidden');

    // Auto-dismiss after 9 seconds so it is completely non-blocking
    proctorWarningTimer = setTimeout(() => {
      hideProctoringWarning();
    }, 9000);
  }

  function hideProctoringWarning() {
    if (el.proctorWarningBanner) {
      el.proctorWarningBanner.classList.add('hidden');
    }
    if (proctorWarningTimer) {
      clearTimeout(proctorWarningTimer);
      proctorWarningTimer = null;
    }
  }

  function updateProctoringBadge() {
    if (!el.proctorStatusBadge || !el.proctorStatusText) return;
    const count = state.proctoring.warningCount;
    if (count === 0) {
      el.proctorStatusBadge.classList.remove('has-warnings');
      el.proctorStatusText.textContent = 'Proctoring Active';
      el.proctorStatusBadge.title = 'Webcam-free session integrity monitoring active (Clean session)';
    } else {
      el.proctorStatusBadge.classList.add('has-warnings');
      el.proctorStatusText.textContent = `${count} Alert${count > 1 ? 's' : ''}`;
      el.proctorStatusBadge.title = `Integrity monitoring recorded ${count} browser focus observation(s)`;
    }
  }

  function logProctoringEvent(type, label, details, durationSeconds = 0) {
    if (!state.proctoring.active) return;
    const now = Date.now();

    // Debounce duplicate events within 1500ms of same type
    if (state.proctoring.lastEventType === type && (now - state.proctoring.lastEventTimestamp) < 1500) {
      return;
    }

    state.proctoring.lastEventTimestamp = now;
    state.proctoring.lastEventType = type;
    state.proctoring.warningCount += 1;

    if (type === 'fullscreen_exit') {
      state.proctoring.fullscreenExits += 1;
    } else if (type === 'tab_switch' || type === 'window_blur') {
      state.proctoring.tabSwitches += 1;
    }

    const record = {
      id: state.proctoring.events.length + 1,
      type: type,
      label: label,
      details: details,
      timestamp: new Date().toISOString(),
      formattedTime: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' }),
      durationSeconds: durationSeconds
    };
    state.proctoring.events.push(record);
    updateProctoringBadge();
  }

  function setupProctoringListeners() {
    // 1. Fullscreen monitoring
    const onFullscreenChange = () => {
      if (!state.proctoring.active) return;
      if (!isFullscreen()) {
        logProctoringEvent(
          'fullscreen_exit',
          'Fullscreen Exited',
          'Exam window exited fullscreen mode.'
        );
        showProctoringWarning({
          title: 'Fullscreen Exited',
          message: 'The examination has exited fullscreen mode. Please return to fullscreen to preserve exam focus.',
          actionText: 'Return to Fullscreen',
          onAction: () => {
            requestTestFullscreen();
            hideProctoringWarning();
          }
        });
      } else {
        if (state.proctoring.lastEventType === 'fullscreen_exit') {
          hideProctoringWarning();
        }
      }
    };

    document.addEventListener('fullscreenchange', onFullscreenChange);
    document.addEventListener('webkitfullscreenchange', onFullscreenChange);
    document.addEventListener('mozfullscreenchange', onFullscreenChange);
    document.addEventListener('MSFullscreenChange', onFullscreenChange);

    // 2. Tab-switch detection via Page Visibility API
    document.addEventListener('visibilitychange', () => {
      if (!state.proctoring.active) return;

      if (document.visibilityState === 'hidden' || document.hidden) {
        state.proctoring.tabAwayStartTime = Date.now();
      } else if (document.visibilityState === 'visible' || !document.hidden) {
        if (state.proctoring.tabAwayStartTime) {
          const awayMs = Date.now() - state.proctoring.tabAwayStartTime;
          const awaySec = Math.max(1, Math.round(awayMs / 1000));
          state.proctoring.totalAwaySeconds += awaySec;
          state.proctoring.tabAwayStartTime = null;

          logProctoringEvent(
            'tab_switch',
            'Tab Switched',
            `Candidate navigated away from the exam tab for ~${awaySec}s.`,
            awaySec
          );

          showProctoringWarning({
            title: 'Tab Switch Detected',
            message: `You navigated away from the exam tab (${awaySec}s). Tab switches are logged for exam integrity.`,
            actionText: 'Acknowledge',
            onAction: () => {
              hideProctoringWarning();
            }
          });
        }
      }
    });

    // 3. Supplementary Window Blur / Focus detection
    window.addEventListener('blur', () => {
      if (!state.proctoring.active) return;
      // Only set windowBlurStartTime if tab is not already hidden (to prevent duplicate events with Visibility API)
      if (!document.hidden && state.proctoring.tabAwayStartTime === null) {
        state.proctoring.windowBlurStartTime = Date.now();
      }
    });

    window.addEventListener('focus', () => {
      if (!state.proctoring.active) return;
      if (state.proctoring.windowBlurStartTime && !document.hidden) {
        const blurMs = Date.now() - state.proctoring.windowBlurStartTime;
        const blurSec = Math.round(blurMs / 1000);
        state.proctoring.windowBlurStartTime = null;

        // Supplementary: Only record if focus was lost for at least 2 seconds
        if (blurSec >= 2) {
          logProctoringEvent(
            'window_blur',
            'Window Focus Lost',
            `Browser window lost focus for ~${blurSec}s.`,
            blurSec
          );

          showProctoringWarning({
            title: 'Window Focus Lost',
            message: `Exam window lost focus for ~${blurSec}s. Please maintain active focus on the test screen.`,
            actionText: 'Acknowledge',
            onAction: () => {
              hideProctoringWarning();
            }
          });
        }
      }
    });

    if (el.btnProctorDismiss) {
      el.btnProctorDismiss.addEventListener('click', hideProctoringWarning);
    }
  }

  // ==========================================================================
  // TEST ENGINE & CBT WORKSPACE
  // ==========================================================================
  async function startExam(examConfig) {
    const { year, shift, section, title, exam_type, chapter, topic, duration_minutes, total_questions } = examConfig;
    state.activeExam = { ...examConfig };
    state.responses = {};
    state.questionStatus = {};
    state.currentIndex = 0;
    state.isSubmitting = false;

    // Initialize Lightweight Proctoring session
    state.proctoring = {
      active: true,
      warningCount: 0,
      tabSwitches: 0,
      fullscreenExits: 0,
      totalAwaySeconds: 0,
      tabAwayStartTime: null,
      windowBlurStartTime: null,
      lastEventTimestamp: 0,
      lastEventType: null,
      events: []
    };
    updateProctoringBadge();
    hideProctoringWarning();
    requestTestFullscreen();

    closeInstructionsModal();

    // Show loading state
    el.questionTextBox.innerHTML = '<div class="spinner"></div><p style="text-align:center; color: var(--text-muted);">Loading questions from database...</p>';
    showView('test');

    try {
      let url = '';
      if (exam_type === 'chapter' || chapter) {
        url = `/api/questions?chapter=${encodeURIComponent(chapter)}`;
        if (topic && topic !== 'all') {
          url += `&topic=${encodeURIComponent(topic)}`;
        }
      } else {
        url = `/api/questions?year=${year}`;
        if (shift) url += `&shift=${encodeURIComponent(shift)}`;
        if (section && section !== 'all') url += `&section=${encodeURIComponent(section)}`;
      }

      const res = await fetch(url);
      if (!res.ok) throw new Error('Failed to retrieve question set');
      const data = await res.json();
      state.questions = data.questions || [];

      if (!state.questions.length) {
        alert('No questions found for this exam selection.');
        showView('dashboard');
        return;
      }

      // Initialize status tracking
      state.questions.forEach((q, idx) => {
        state.questionStatus[q.id] = (idx === 0) ? 'not_answered' : 'not_visited';
      });

      // Setup exam headers & duration
      el.examTitle.textContent = title;
      
      let durationMins = 50;
      if (duration_minutes) {
        durationMins = duration_minutes;
      } else if (exam_type === 'chapter') {
        durationMins = 50;
      } else if (section === 'all') {
        durationMins = SECTION_DURATIONS["Full"];
      } else {
        durationMins = SECTION_DURATIONS[section] || 50;
      }
      
      state.totalTimeSeconds = durationMins * 60;
      state.timeRemainingSeconds = state.totalTimeSeconds;
      startTimer();

      setupSectionTabs();
      renderCurrentQuestion();
      updatePalette();
    } catch (err) {
      console.error(err);
      alert('Error loading questions: ' + err.message);
      showView('dashboard');
    }
  }

  function startTimer() {
    clearInterval(state.timerInterval);
    updateTimerDisplay();

    state.timerInterval = setInterval(() => {
      state.timeRemainingSeconds -= 1;
      updateTimerDisplay();

      if (state.timeRemainingSeconds <= 0) {
        clearInterval(state.timerInterval);
        alert('Time has expired! Submitting your examination responses automatically.');
        submitExam();
      }
    }, 1000);
  }

  function updateTimerDisplay() {
    const s = Math.max(0, state.timeRemainingSeconds);
    const hrs = Math.floor(s / 3600);
    const mins = Math.floor((s % 3600) / 60);
    const secs = s % 60;

    let timeText = '';
    if (hrs > 0) {
      timeText = `${String(hrs).padStart(2, '0')}:${String(mins).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;
    } else {
      timeText = `${String(mins).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;
    }

    el.timerDisplay.textContent = timeText;

    // Visual urgency indicators
    if (s <= 300) { // 5 minutes
      el.timerDisplay.className = 'timer-countdown critical';
    } else if (s <= 600) { // 10 minutes
      el.timerDisplay.className = 'timer-countdown warning';
    } else {
      el.timerDisplay.className = 'timer-countdown';
    }
  }

  function setupSectionTabs() {
    el.sectionTabsBar.innerHTML = '';
    
    // Determine unique sections present in this test attempt
    const sectionCounts = {};
    state.questions.forEach(q => {
      sectionCounts[q.section] = (sectionCounts[q.section] || 0) + 1;
    });

    Object.keys(sectionCounts).forEach(secName => {
      const tabBtn = document.createElement('button');
      tabBtn.className = 'section-tab-btn';
      tabBtn.setAttribute('data-section', secName);
      tabBtn.innerHTML = `
        <span>${secName}</span>
        <span class="section-tab-count">${sectionCounts[secName]}</span>
      `;

      tabBtn.addEventListener('click', () => {
        const targetIdx = state.questions.findIndex(q => q.section === secName);
        if (targetIdx !== -1) {
          saveCurrentResponse();
          state.currentIndex = targetIdx;
          renderCurrentQuestion();
          updatePalette();
        }
      });

      el.sectionTabsBar.appendChild(tabBtn);
    });
  }

  function updateActiveSectionTab(currentSection) {
    const tabs = el.sectionTabsBar.querySelectorAll('.section-tab-btn');
    tabs.forEach(tab => {
      if (tab.getAttribute('data-section') === currentSection) {
        tab.classList.add('active');
        tab.scrollIntoView({ behavior: 'smooth', inline: 'nearest', block: 'nearest' });
      } else {
        tab.classList.remove('active');
      }
    });

    if (el.paletteSectionName) {
      el.paletteSectionName.textContent = currentSection;
    }
  }

  function renderCurrentQuestion() {
    const q = state.questions[state.currentIndex];
    if (!q) return;

    if (state.questionStatus[q.id] === 'not_visited') {
      state.questionStatus[q.id] = 'not_answered';
    }

    // Update Meta Pills
    el.qNumberPill.textContent = `Question ${state.currentIndex + 1} of ${state.questions.length}`;
    el.qSectionBadge.textContent = q.section;
    el.qTopicBadge.textContent = q.topic || 'General';
    el.qDiffBadge.textContent = q.difficulty || 'Standard';

    updateActiveSectionTab(q.section);

    // Render Question Text with LaTeX
    el.questionTextBox.innerHTML = formatMathContent(q.question_text);

    // Render Options
    el.optionsContainer.innerHTML = '';
    const currentSelectedOption = state.responses[q.id] || null;

    const options = [
      { key: 'A', text: q.option_a },
      { key: 'B', text: q.option_b },
      { key: 'C', text: q.option_c },
      { key: 'D', text: q.option_d }
    ];

    options.forEach(opt => {
      const card = document.createElement('div');
      card.className = 'option-card' + (currentSelectedOption === opt.key ? ' selected' : '');
      card.setAttribute('role', 'radio');
      card.setAttribute('aria-checked', currentSelectedOption === opt.key ? 'true' : 'false');
      card.setAttribute('data-option', opt.key);

      card.innerHTML = `
        <div class="option-indicator">${opt.key}</div>
        <div class="option-text">${formatMathContent(opt.text, true)}</div>
      `;

      card.addEventListener('click', () => {
        selectOption(opt.key);
      });

      el.optionsContainer.appendChild(card);
    });

    // Update navigation buttons
    el.btnPrevQuestion.disabled = (state.currentIndex === 0);
    el.btnSaveNext.textContent = (state.currentIndex === state.questions.length - 1) ? 'Save & Finish' : 'Save & Next';

    // Typeset MathJax
    renderMath(el.questionTextBox);
    renderMath(el.optionsContainer);
  }

  function selectOption(optionKey) {
    const q = state.questions[state.currentIndex];
    state.responses[q.id] = optionKey;

    // Update visual option card selection
    const cards = el.optionsContainer.querySelectorAll('.option-card');
    cards.forEach(c => {
      if (c.getAttribute('data-option') === optionKey) {
        c.classList.add('selected');
        c.setAttribute('aria-checked', 'true');
      } else {
        c.classList.remove('selected');
        c.setAttribute('aria-checked', 'false');
      }
    });

    if (state.questionStatus[q.id] === 'review' || state.questionStatus[q.id] === 'answered_review') {
      state.questionStatus[q.id] = 'answered_review';
    } else {
      state.questionStatus[q.id] = 'answered';
    }

    updatePalette();
  }

  function clearCurrentResponse() {
    const q = state.questions[state.currentIndex];
    delete state.responses[q.id];

    const cards = el.optionsContainer.querySelectorAll('.option-card');
    cards.forEach(c => {
      c.classList.remove('selected');
      c.setAttribute('aria-checked', 'false');
    });

    state.questionStatus[q.id] = 'not_answered';
    updatePalette();
  }

  function saveCurrentResponse() {
    const q = state.questions[state.currentIndex];
    if (state.responses[q.id]) {
      if (state.questionStatus[q.id] === 'review' || state.questionStatus[q.id] === 'answered_review') {
        state.questionStatus[q.id] = 'answered_review';
      } else {
        state.questionStatus[q.id] = 'answered';
      }
    } else {
      if (state.questionStatus[q.id] !== 'review') {
        state.questionStatus[q.id] = 'not_answered';
      }
    }
  }

  function markCurrentForReview() {
    const q = state.questions[state.currentIndex];
    if (state.responses[q.id]) {
      state.questionStatus[q.id] = 'answered_review';
    } else {
      state.questionStatus[q.id] = 'review';
    }
    updatePalette();

    if (state.currentIndex < state.questions.length - 1) {
      state.currentIndex += 1;
      renderCurrentQuestion();
      updatePalette();
    }
  }

  function navigateToQuestion(newIndex) {
    if (newIndex >= 0 && newIndex < state.questions.length) {
      saveCurrentResponse();
      state.currentIndex = newIndex;
      renderCurrentQuestion();
      updatePalette();

      if (window.innerWidth <= 900 && el.paletteSidebar) {
        el.paletteSidebar.classList.remove('open');
        if (el.paletteBackdrop) el.paletteBackdrop.classList.add('hidden');
      }
    }
  }

  // ==========================================================================
  // PALETTE MATRIX & SUMMARY CALCULATION
  // ==========================================================================
  function updatePalette() {
    el.paletteGrid.innerHTML = '';

    let cntAnswered = 0;
    let cntNotAnswered = 0;
    let cntNotVisited = 0;
    let cntReview = 0;
    let cntAnsweredReview = 0;

    state.questions.forEach((q, idx) => {
      const status = state.questionStatus[q.id] || 'not_visited';
      const isCurrent = (idx === state.currentIndex);

      if (status === 'answered') cntAnswered++;
      else if (status === 'not_answered') cntNotAnswered++;
      else if (status === 'not_visited') cntNotVisited++;
      else if (status === 'review') cntReview++;
      else if (status === 'answered_review') cntAnsweredReview++;

      const btn = document.createElement('button');
      btn.className = `palette-q-btn status-${status.replace('_', '-')}` + (isCurrent ? ' current' : '');
      btn.textContent = idx + 1;
      btn.title = `Q${idx + 1} (${q.section}): ${status.replace('_', ' ').toUpperCase()}`;

      btn.addEventListener('click', () => {
        navigateToQuestion(idx);
      });

      el.paletteGrid.appendChild(btn);
    });

    // Update Legend Counters
    el.statAnswered.textContent = cntAnswered;
    el.statNotAnswered.textContent = cntNotAnswered;
    el.statNotVisited.textContent = cntNotVisited;
    el.statReview.textContent = cntReview;
    el.statAnsweredReview.textContent = cntAnsweredReview;
  }

  function getSectionSummary() {
    const sections = {};
    state.questions.forEach(q => {
      const sec = q.section;
      if (!sections[sec]) {
        sections[sec] = { total: 0, answered: 0, notAnswered: 0, review: 0, notVisited: 0 };
      }
      sections[sec].total += 1;
      const status = state.questionStatus[q.id] || 'not_visited';
      if (status === 'answered' || status === 'answered_review') sections[sec].answered += 1;
      else if (status === 'not_answered') sections[sec].notAnswered += 1;
      else if (status === 'review') sections[sec].review += 1;
      else if (status === 'not_visited') sections[sec].notVisited += 1;
    });
    return sections;
  }

  function showConfirmModal() {
    saveCurrentResponse();
    updatePalette();

    // Close mobile palette drawer if open
    if (el.paletteSidebar) el.paletteSidebar.classList.remove('open');
    if (el.paletteBackdrop) el.paletteBackdrop.classList.add('hidden');

    const summary = getSectionSummary();
    el.modalSummaryTbody.innerHTML = '';

    Object.keys(summary).forEach(sec => {
      const s = summary[sec];
      const tr = document.createElement('tr');
      tr.innerHTML = `
        <td>${sec}</td>
        <td>${s.total}</td>
        <td class="text-success font-semibold">${s.answered}</td>
        <td class="text-danger font-semibold">${s.notAnswered}</td>
        <td class="text-warning font-semibold">${s.review}</td>
      `;
      el.modalSummaryTbody.appendChild(tr);
    });

    el.modalConfirmSubmit.classList.remove('hidden');
  }

  function hideConfirmModal() {
    el.modalConfirmSubmit.classList.add('hidden');
  }

  // ==========================================================================
  // SUBMISSION & RESULTS ANALYSIS
  // ==========================================================================
  async function submitExam() {
    if (state.isSubmitting) return;
    state.isSubmitting = true;
    hideConfirmModal();
    clearInterval(state.timerInterval);

    // Conclude proctoring monitoring
    state.proctoring.active = false;
    exitTestFullscreen();
    hideProctoringWarning();

    const timeSpent = state.totalTimeSeconds - Math.max(0, state.timeRemainingSeconds);

    const payload = {
      responses: state.responses,
      time_spent_seconds: timeSpent,
      proctoring: {
        total_tab_switches: state.proctoring.tabSwitches,
        total_fullscreen_exits: state.proctoring.fullscreenExits,
        total_away_seconds: state.proctoring.totalAwaySeconds,
        warning_count: state.proctoring.warningCount,
        events: state.proctoring.events
      }
    };

    if (state.activeExam && (state.activeExam.exam_type === 'chapter' || state.activeExam.chapter)) {
      payload.exam_type = 'chapter';
      payload.chapter = state.activeExam.chapter;
      if (state.activeExam.topic) payload.topic = state.activeExam.topic;
    } else if (state.activeExam) {
      payload.year = state.activeExam.year;
      payload.shift = state.activeExam.shift;
      payload.section = state.activeExam.section;
    }

    try {
      const res = await fetch('/api/submit', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      if (!res.ok) throw new Error('Failed to score examination');
      const result = await res.json();
      state.submissionResult = result;
      showView('results');
      renderResults(result);
    } catch (err) {
      console.error(err);
      alert('Error during submission: ' + err.message);
    } finally {
      state.isSubmitting = false;
    }
  }

  function renderResults(res) {
    el.resExamTitle.textContent = `${state.activeExam.title} — Official Scorecard`;
    el.resTimestamp.textContent = `Completed on ${new Date().toLocaleString()}`;

    // Score radial showcase
    el.resScore.textContent = res.total_score >= 0 ? res.total_score.toFixed(2) : res.total_score.toFixed(2);
    el.resMaxScore.textContent = `/ ${res.max_marks.toFixed(2)}`;

    // Stat tiles
    el.resAccuracy.textContent = `${res.accuracy}%`;
    el.resPercentage.textContent = `${res.percentage}%`;
    el.resCorrect.textContent = res.correct;
    el.resIncorrect.textContent = res.incorrect;
    el.resUnanswered.textContent = res.unanswered;

    const mins = Math.floor(res.time_spent_seconds / 60);
    const secs = res.time_spent_seconds % 60;
    el.resTimeSpent.textContent = `${mins}m ${secs}s`;

    // Sectional Performance Table
    el.sectionalTbody.innerHTML = '';
    res.sections.forEach(s => {
      const accuracy = s.attempted > 0 ? ((s.correct / s.attempted) * 100).toFixed(1) : '0.0';
      const tr = document.createElement('tr');
      tr.innerHTML = `
        <td>${s.section}</td>
        <td>${s.total}</td>
        <td>${s.attempted}</td>
        <td class="text-success font-semibold">${s.correct}</td>
        <td class="text-danger font-semibold">${s.incorrect}</td>
        <td style="color: var(--text-muted);">${s.unanswered}</td>
        <td class="text-accent font-semibold">${s.score.toFixed(2)} / ${s.max_score.toFixed(2)}</td>
        <td>${accuracy}%</td>
      `;
      el.sectionalTbody.appendChild(tr);
    });

    // Render Proctoring & Session Integrity Summary
    const proctor = (res && res.proctoring && typeof res.proctoring === 'object' && Object.keys(res.proctoring).length)
      ? res.proctoring
      : {
          total_tab_switches: state.proctoring.tabSwitches,
          total_fullscreen_exits: state.proctoring.fullscreenExits,
          total_away_seconds: state.proctoring.totalAwaySeconds,
          warning_count: state.proctoring.warningCount,
          events: state.proctoring.events
        };

    if (el.resProctorTabSwitches) el.resProctorTabSwitches.textContent = proctor.total_tab_switches || 0;
    if (el.resProctorFullscreenExits) el.resProctorFullscreenExits.textContent = proctor.total_fullscreen_exits || 0;
    if (el.resProctorAwayTime) el.resProctorAwayTime.textContent = `${proctor.total_away_seconds || 0}s`;
    if (el.resProctorTotalAlerts) el.resProctorTotalAlerts.textContent = proctor.warning_count || 0;

    if (el.proctorLogTbody) {
      el.proctorLogTbody.innerHTML = '';
      const events = proctor.events || [];
      if (events.length === 0) {
        const tr = document.createElement('tr');
        tr.innerHTML = `
          <td colspan="4" style="text-align: center; color: var(--state-success-text); padding: 16px;">
            <span class="badge-proctor-clean" style="margin-right: 6px;">✓ Clean Session</span>
            No tab switches or fullscreen exits were observed during this attempt.
          </td>
        `;
        el.proctorLogTbody.appendChild(tr);
      } else {
        events.forEach((ev, i) => {
          const tr = document.createElement('tr');
          tr.innerHTML = `
            <td style="font-family: var(--font-mono); color: var(--text-muted);">${i + 1}</td>
            <td style="font-family: var(--font-mono); font-size: 0.78rem;">${ev.formattedTime || '—'}</td>
            <td><span class="badge-proctor-alert">${ev.label || ev.type}</span></td>
            <td style="color: var(--text-secondary);">${ev.details}</td>
          `;
          el.proctorLogTbody.appendChild(tr);
        });
      }
    }

    // Review counts
    el.cntRevAll.textContent = res.review.length;
    el.cntRevCorr.textContent = res.correct;
    el.cntRevInc.textContent = res.incorrect;
    el.cntRevUnans.textContent = res.unanswered;

    renderReviewList('all');
  }

  function renderReviewList(filter = 'all') {
    state.currentReviewFilter = filter;
    el.reviewList.innerHTML = '';

    const list = state.submissionResult.review.filter(q => {
      if (filter === 'correct') return q.status === 'correct';
      if (filter === 'incorrect') return q.status === 'incorrect';
      if (filter === 'unanswered') return q.status === 'unanswered';
      return true;
    });

    if (!list.length) {
      el.reviewList.innerHTML = `
        <div class="loading-state">
          <p>No questions matched filter: <strong>${filter}</strong></p>
        </div>
      `;
      return;
    }

    list.forEach(q => {
      const card = document.createElement('article');
      card.className = `review-card status-${q.status}`;

      let tagClass = 'tag-unanswered';
      let tagText = 'Unanswered (0.0)';
      if (q.status === 'correct') {
        tagClass = 'tag-correct';
        tagText = 'Correct (+1.0)';
      } else if (q.status === 'incorrect') {
        tagClass = 'tag-incorrect';
        tagText = 'Incorrect (-0.25)';
      }

      const options = [
        { key: 'A', text: q.option_a },
        { key: 'B', text: q.option_b },
        { key: 'C', text: q.option_c },
        { key: 'D', text: q.option_d }
      ];

      const optionsHtml = options.map(opt => {
        let optClass = 'review-option-pill';
        let badge = `[${opt.key}]`;
        if (opt.key === q.correct_option) {
          optClass += ' is-correct';
          badge = `[${opt.key}] · Correct Answer`;
        } else if (opt.key === q.candidate_answer && q.status === 'incorrect') {
          optClass += ' is-candidate-wrong';
          badge = `[${opt.key}] · Your Choice`;
        }
        return `
          <div class="${optClass}">
            <strong>${badge}</strong>
            <span>${formatMathContent(opt.text, true)}</span>
          </div>
        `;
      }).join('');

      card.innerHTML = `
        <div class="review-card-header">
          <div class="review-q-meta">
            <span class="q-number-pill">Q.${q.question_number}</span>
            <span class="q-section-badge">${q.section}</span>
            <span class="q-topic-badge">${q.topic}</span>
            <span class="q-diff-badge">${q.difficulty}</span>
          </div>
          <span class="review-status-tag ${tagClass}">${tagText}</span>
        </div>

        <div class="review-question-text">
          ${formatMathContent(q.question_text)}
        </div>

        <div class="review-options-grid">
          ${optionsHtml}
        </div>

        <div class="review-explanation-box">
          <div class="explanation-heading">Step-by-Step Solution</div>
          <div class="explanation-body">${formatMathContent(q.explanation)}</div>
        </div>
      `;

      el.reviewList.appendChild(card);
    });

    setTimeout(() => {
      renderMath(el.reviewList);
    }, 20);
  }

  // ==========================================================================
  // PDF SCORECARD & CANDIDATE RESPONSE SHEET GENERATION ENGINE
  // ==========================================================================
  function showPdfToast(msg, duration = 4000) {
    if (el.pdfToast && el.pdfToastText) {
      el.pdfToastText.textContent = msg;
      el.pdfToast.classList.remove('hidden');
      setTimeout(() => {
        el.pdfToast.classList.add('hidden');
      }, duration);
    }
  }

  function generateScorecardPDFElement(res) {
    const wrapper = document.createElement('div');
    wrapper.className = 'pdf-export-container';

    const mins = Math.floor(res.time_spent_seconds / 60);
    const secs = res.time_spent_seconds % 60;
    const timeStr = `${mins}m ${secs}s`;
    const examTitle = state.activeExam ? state.activeExam.title : 'IMU CET CBT Mock Examination';
    const dateStr = new Date().toLocaleString();

    // Section-wise breakdown rows
    const sectionRows = res.sections.map(s => {
      const acc = s.attempted > 0 ? ((s.correct / s.attempted) * 100).toFixed(1) : '0.0';
      return `
        <tr>
          <td><strong>${s.section}</strong></td>
          <td style="text-align:center;">${s.total}</td>
          <td style="text-align:center;">${s.attempted}</td>
          <td style="text-align:center; color:#16A34A; font-weight:600;">${s.correct}</td>
          <td style="text-align:center; color:#DC2626; font-weight:600;">${s.incorrect}</td>
          <td style="text-align:center; color:#64748B;">${s.unanswered}</td>
          <td style="text-align:center; font-weight:600; color:#2563EB;">${s.score.toFixed(2)}</td>
          <td style="text-align:center;">${acc}%</td>
        </tr>
      `;
    }).join('');

    // Full Candidate Response Sheet Table rows
    const responseRows = res.review.map(q => {
      let statusHtml = '<span class="pdf-badge-unans">Unanswered</span>';
      let marksHtml = '0.00';
      if (q.status === 'correct') {
        statusHtml = '<span class="pdf-badge-corr">Correct</span>';
        marksHtml = '+1.00';
      } else if (q.status === 'incorrect') {
        statusHtml = '<span class="pdf-badge-inc">Incorrect</span>';
        marksHtml = '-0.25';
      }

      return `
        <tr>
          <td style="text-align:center; font-weight:600;">${q.question_number}</td>
          <td>${q.section}</td>
          <td style="font-size:0.7rem; color:#475569;">${q.topic || 'General'}</td>
          <td style="text-align:center; font-weight:600; ${q.status === 'incorrect' ? 'color:#DC2626;' : ''}">${q.candidate_answer || '—'}</td>
          <td style="text-align:center; font-weight:600; color:#16A34A;">${q.correct_option}</td>
          <td style="text-align:center;">${statusHtml}</td>
          <td style="text-align:center; font-weight:600;">${marksHtml}</td>
        </tr>
      `;
    }).join('');

    wrapper.innerHTML = `
      <div class="pdf-header-box">
        <div>
          <div class="pdf-logo-title">INDIAN MARITIME UNIVERSITY (IMU CET)</div>
          <div class="pdf-logo-sub">Computer Based Examination — Official Candidate Scorecard & Response Sheet</div>
        </div>
        <div class="pdf-meta-col">
          <div>Candidate: <strong>Cadet Aspirant</strong></div>
          <div>Exam: <strong>${examTitle}</strong></div>
          <div>Date: ${dateStr}</div>
        </div>
      </div>

      <div class="pdf-scorecard-grid">
        <div class="pdf-score-radial">
          <div class="pdf-score-num">${res.total_score.toFixed(2)}</div>
          <div class="pdf-score-denom">/ ${res.max_marks.toFixed(2)} Total Marks</div>
          <div style="font-size:0.75rem; color:#16A34A; font-weight:600; margin-top:4px;">Percentage: ${res.percentage}%</div>
        </div>
        <div class="pdf-stats-quad">
          <div class="pdf-stat-box">
            <div class="pdf-stat-val" style="color:#2563EB;">${res.accuracy}%</div>
            <div class="pdf-stat-lbl">Accuracy Rate</div>
          </div>
          <div class="pdf-stat-box">
            <div class="pdf-stat-val" style="color:#16A34A;">${res.correct}</div>
            <div class="pdf-stat-lbl">Correct (+1.0)</div>
          </div>
          <div class="pdf-stat-box">
            <div class="pdf-stat-val" style="color:#DC2626;">${res.incorrect}</div>
            <div class="pdf-stat-lbl">Incorrect (-0.25)</div>
          </div>
          <div class="pdf-stat-box">
            <div class="pdf-stat-val">${res.attempted} / ${res.review.length}</div>
            <div class="pdf-stat-lbl">Attempted</div>
          </div>
          <div class="pdf-stat-box">
            <div class="pdf-stat-val" style="color:#64748B;">${res.unanswered}</div>
            <div class="pdf-stat-lbl">Unanswered</div>
          </div>
          <div class="pdf-stat-box">
            <div class="pdf-stat-val">${timeStr}</div>
            <div class="pdf-stat-lbl">Time Elapsed</div>
          </div>
        </div>
      </div>

      <h4 style="font-size:0.92rem; font-weight:600; margin-bottom:8px; color:#111827;">Section-wise Performance Breakdown</h4>
      <table class="pdf-table">
        <thead>
          <tr>
            <th>Section</th>
            <th>Total Qs</th>
            <th>Attempted</th>
            <th>Correct</th>
            <th>Incorrect</th>
            <th>Unanswered</th>
            <th>Score</th>
            <th>Accuracy</th>
          </tr>
        </thead>
        <tbody>
          ${sectionRows}
        </tbody>
      </table>

      <!-- Session Integrity Summary in PDF -->
      <div style="margin-top: 14px; margin-bottom: 8px; padding: 10px 14px; background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 6px; font-size: 0.74rem;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 5px;">
          <strong style="color: #0F172A;">Session Integrity Observation Summary (Webcam-Free)</strong>
          <span style="color: #2563EB; font-weight: 600;">Status: ${(res.proctoring && res.proctoring.warning_count > 0) ? res.proctoring.warning_count + ' Observations Logged' : 'Verified Clean Attempt'}</span>
        </div>
        <div style="display: flex; gap: 20px; color: #475569; font-size: 0.72rem;">
          <div>Tab Switches: <strong>${(res.proctoring && res.proctoring.total_tab_switches) || 0}</strong></div>
          <div>Fullscreen Exits: <strong>${(res.proctoring && res.proctoring.total_fullscreen_exits) || 0}</strong></div>
          <div>Time Outside Tab: <strong>${(res.proctoring && res.proctoring.total_away_seconds) || 0}s</strong></div>
          <div>Privacy: <strong>Camera & Mic Not Accessed</strong></div>
        </div>
      </div>

      <div class="pdf-page-break"></div>
      <div class="pdf-header-box">
        <div>
          <div class="pdf-logo-title">CANDIDATE RESPONSE SHEET</div>
          <div class="pdf-logo-sub">${examTitle} — Official Answer Key Comparison</div>
        </div>
        <div class="pdf-meta-col">
          <div>Candidate: <strong>Cadet Aspirant</strong></div>
          <div>Marking: +1.0 / -0.25</div>
        </div>
      </div>

      <table class="pdf-table pdf-sheet-table">
        <thead>
          <tr>
            <th style="width:38px;">Q.#</th>
            <th>Section</th>
            <th>Topic</th>
            <th style="width:75px;">Your Ans</th>
            <th style="width:75px;">Key</th>
            <th style="width:80px;">Status</th>
            <th style="width:55px;">Marks</th>
          </tr>
        </thead>
        <tbody>
          ${responseRows}
        </tbody>
      </table>
    `;

    return wrapper;
  }

  async function downloadResultsPDF(resultData = null) {
    const res = resultData || state.submissionResult;
    if (!res) {
      alert('No completed examination result available to download.');
      return;
    }

    showPdfToast('Generating official Scorecard & Response PDF...');

    const safeTitle = (state.activeExam ? state.activeExam.title : 'IMU_CET')
      .replace(/[^a-zA-Z0-9]/g, '_');
    const filename = `${safeTitle}_Scorecard_Response.pdf`;

    try {
      if (typeof window.html2pdf !== 'function') {
        showPdfToast('Opening print dialog for PDF save...');
        window.print();
        return;
      }

      const element = generateScorecardPDFElement(res);

      const mount = document.createElement('div');
      mount.className = 'pdf-export-hidden';
      mount.appendChild(element);
      document.body.appendChild(mount);

      const opt = {
        margin:       [8, 8, 8, 8],
        filename:     filename,
        image:        { type: 'jpeg', quality: 0.98 },
        html2canvas:  { scale: 2, useCORS: true, logging: false },
        jsPDF:        { unit: 'mm', format: 'a4', orientation: 'portrait' }
      };

      await html2pdf().set(opt).from(element).save();

      document.body.removeChild(mount);
      showPdfToast('Scorecard PDF downloaded successfully!');
    } catch (err) {
      console.error('PDF generation error:', err);
      showPdfToast('Opening print dialog for PDF save...');
      window.print();
    }
  }

  // ==========================================================================
  // EVENT LISTENERS & SHORTCUTS
  // ==========================================================================
  function setupEventListeners() {
    // Brand home click
    el.brandHomeBtn.addEventListener('click', () => {
      showView('dashboard');
    });

    // Navigation links
    if (el.navHomeBtn) {
      el.navHomeBtn.addEventListener('click', () => {
        showView('dashboard');
      });
    }

    if (el.navTestsBtn) {
      el.navTestsBtn.addEventListener('click', () => {
        showView('dashboard');
        const section = document.querySelector('.dashboard-exams-section');
        if (section) section.scrollIntoView({ behavior: 'smooth' });
      });
    }

    if (el.navChaptersBtn) {
      el.navChaptersBtn.addEventListener('click', () => {
        showView('dashboard');
        if (el.navChaptersBtn) el.navChaptersBtn.classList.add('active');
        if (el.navHomeBtn) el.navHomeBtn.classList.remove('active');
        [el.filterFullBtn, el.filterSectionBtn, el.filterChapterBtn].forEach(b => {
          if (b) b.classList.remove('active');
        });
        if (el.filterChapterBtn) el.filterChapterBtn.classList.add('active');
        renderExamsGrid('chapter');
        const section = document.querySelector('.dashboard-exams-section');
        if (section) section.scrollIntoView({ behavior: 'smooth' });
      });
    }

    if (el.navInstructionsBtn) {
      el.navInstructionsBtn.addEventListener('click', () => {
        openInstructionsModal(null);
      });
    }

    if (el.navResultsBtn) {
      el.navResultsBtn.addEventListener('click', () => {
        if (state.submissionResult) {
          showView('results');
        } else {
          alert('No completed exam result available yet.');
        }
      });
    }

    // Instructions Modal controls
    if (el.btnCloseInstructionsX) {
      el.btnCloseInstructionsX.addEventListener('click', closeInstructionsModal);
    }
    if (el.btnModalInstructionsCancel) {
      el.btnModalInstructionsCancel.addEventListener('click', closeInstructionsModal);
    }
    if (el.btnModalInstructionsStart) {
      el.btnModalInstructionsStart.addEventListener('click', () => {
        if (state.pendingExamConfig) {
          startExam(state.pendingExamConfig);
        } else if (state.exams.length) {
          const first = state.exams[0];
          startExam({
            year: first.year,
            shift: first.shift,
            section: 'all',
            title: `${first.title} (Full Mock)`
          });
        }
      });
    }

    // Test Action Bar
    el.btnSaveNext.addEventListener('click', () => {
      saveCurrentResponse();
      if (state.currentIndex < state.questions.length - 1) {
        state.currentIndex += 1;
        renderCurrentQuestion();
        updatePalette();
      } else {
        showConfirmModal();
      }
    });

    el.btnPrevQuestion.addEventListener('click', () => {
      if (state.currentIndex > 0) {
        saveCurrentResponse();
        state.currentIndex -= 1;
        renderCurrentQuestion();
        updatePalette();
      }
    });

    el.btnMarkReview.addEventListener('click', () => {
      markCurrentForReview();
    });

    el.btnClearResponse.addEventListener('click', () => {
      clearCurrentResponse();
    });

    el.btnSubmitTest.addEventListener('click', showConfirmModal);
    el.btnHeaderSubmit.addEventListener('click', showConfirmModal);
    el.btnPaletteSummary.addEventListener('click', showConfirmModal);

    // Mobile Palette Drawer Toggle
    if (el.btnTogglePalette) {
      el.btnTogglePalette.addEventListener('click', () => {
        if (el.paletteSidebar) el.paletteSidebar.classList.toggle('open');
        if (el.paletteBackdrop) el.paletteBackdrop.classList.toggle('hidden');
      });
    }

    if (el.btnClosePalette) {
      el.btnClosePalette.addEventListener('click', () => {
        if (el.paletteSidebar) el.paletteSidebar.classList.remove('open');
        if (el.paletteBackdrop) el.paletteBackdrop.classList.add('hidden');
      });
    }

    if (el.paletteBackdrop) {
      el.paletteBackdrop.addEventListener('click', () => {
        if (el.paletteSidebar) el.paletteSidebar.classList.remove('open');
        if (el.paletteBackdrop) el.paletteBackdrop.classList.add('hidden');
      });
    }

    // Modal
    el.btnModalCancel.addEventListener('click', hideConfirmModal);
    el.btnModalConfirm.addEventListener('click', submitExam);

    // Results Actions
    el.btnRetakeExam.addEventListener('click', () => {
      if (state.activeExam) {
        startExam(state.activeExam);
      }
    });

    el.btnBackDashboard.addEventListener('click', () => {
      showView('dashboard');
    });

    if (el.btnDownloadPdf) {
      el.btnDownloadPdf.addEventListener('click', () => {
        downloadResultsPDF();
      });
    }

    el.btnPrintResults.addEventListener('click', () => {
      window.print();
    });

    // Review Filters
    const reviewFilterBtns = document.querySelectorAll('.review-filter-btn');
    reviewFilterBtns.forEach(btn => {
      btn.addEventListener('click', (e) => {
        reviewFilterBtns.forEach(b => b.classList.remove('active'));
        e.currentTarget.classList.add('active');
        const filter = e.currentTarget.getAttribute('data-filter');
        renderReviewList(filter);
      });
    });

    // Global delegation for filter tabs
    document.addEventListener('click', (e) => {
      const tabBtn = e.target.closest('.filter-tab');
      if (tabBtn) {
        const filter = tabBtn.getAttribute('data-filter');
        if (filter && typeof window.switchFilter === 'function') {
          window.switchFilter(filter);
        }
      }
    });

    // Dashboard Filters direct listeners
    [el.filterFullBtn, el.filterSectionBtn, el.filterChapterBtn].forEach(btn => {
      if (!btn) return;
      btn.addEventListener('click', (e) => {
        const filter = e.currentTarget.getAttribute('data-filter');
        if (filter && typeof window.switchFilter === 'function') {
          window.switchFilter(filter);
        }
      });
    });

    // Keyboard Shortcuts (Standard CBT convenience)
    window.addEventListener('keydown', (e) => {
      if (e.target.tagName === 'INPUT' || e.target.tagName === 'SELECT' || e.target.tagName === 'TEXTAREA') return;
      if (!el.modalConfirmSubmit.classList.contains('hidden')) {
        if (e.key === 'Escape') hideConfirmModal();
        return;
      }
      if (!el.modalInstructions.classList.contains('hidden')) {
        if (e.key === 'Escape') closeInstructionsModal();
        return;
      }
      if (el.viewTest.classList.contains('hidden')) return;

      const key = e.key.toUpperCase();
      if (key === 'A' || key === '1') { selectOption('A'); }
      else if (key === 'B' || key === '2') { selectOption('B'); }
      else if (key === 'C' || key === '3') { selectOption('C'); }
      else if (key === 'D' || key === '4') { selectOption('D'); }
      else if (key === 'N') {
        saveCurrentResponse();
        if (state.currentIndex < state.questions.length - 1) {
          state.currentIndex += 1;
          renderCurrentQuestion();
          updatePalette();
        }
      }
      else if (key === 'P') {
        if (state.currentIndex > 0) {
          saveCurrentResponse();
          state.currentIndex -= 1;
          renderCurrentQuestion();
          updatePalette();
        }
      }
      else if (key === 'M') {
        markCurrentForReview();
      }
    });

    // Initialize proctoring event listeners
    setupProctoringListeners();
  }

  // Progressive Web App (PWA) Support
  let deferredInstallPrompt = null;

  function registerServiceWorker() {
    if ('serviceWorker' in navigator) {
      window.addEventListener('load', () => {
        navigator.serviceWorker.register('/sw.js', { scope: '/' })
          .then((reg) => {
            console.log('[PWA] Service Worker registered successfully with scope:', reg.scope);
            reg.onupdatefound = () => {
              const installingWorker = reg.installing;
              if (installingWorker) {
                installingWorker.onstatechange = () => {
                  if (installingWorker.state === 'installed' && navigator.serviceWorker.controller) {
                    console.log('[PWA] New content is available; please refresh.');
                  }
                };
              }
            };
          })
          .catch((err) => {
            console.warn('[PWA] Service Worker registration failed:', err);
          });
      });
    }
  }

  function setupPwaInstallPrompt() {
    if (!el.btnInstallPwa) return;

    window.addEventListener('beforeinstallprompt', (e) => {
      // Prevent standard browser mini-infobar prompt
      e.preventDefault();
      // Store event to trigger later on user tap
      deferredInstallPrompt = e;
      // Reveal the custom install button in the navigation header
      el.btnInstallPwa.classList.remove('hidden');
    });

    el.btnInstallPwa.addEventListener('click', async () => {
      if (!deferredInstallPrompt) return;
      // Show native install prompt modal
      deferredInstallPrompt.prompt();
      const choiceResult = await deferredInstallPrompt.userChoice;
      console.log('[PWA] User install choice:', choiceResult.outcome);
      deferredInstallPrompt = null;
      el.btnInstallPwa.classList.add('hidden');
    });

    window.addEventListener('appinstalled', () => {
      console.log('[PWA] Application successfully installed.');
      deferredInstallPrompt = null;
      if (el.btnInstallPwa) {
        el.btnInstallPwa.classList.add('hidden');
      }
    });
  }

  // Application Entry Point
  document.addEventListener('DOMContentLoaded', () => {
    setupEventListeners();
    loadExams();
    registerServiceWorker();
    setupPwaInstallPrompt();
  });

})();
