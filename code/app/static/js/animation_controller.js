(function () {
  'use strict';

  const DEFAULTS = {
    speedMs: 500,
    maxMonths: 36,
    lifecycleConfig: { baseDefaultRate: 1, earlyPayoffRate: 1, recoveryRate: 1 },
    onTick: null,
    onComplete: null,
    onPause: null,
  };

  const state = {
    playing: false,
    month: 0,
    speedMs: DEFAULTS.speedMs,
    maxMonths: DEFAULTS.maxMonths,
    lifecycleConfig: { ...DEFAULTS.lifecycleConfig },
    timer: null,
    snapshots: [],
    portfolio: null,
    charts: new Map(),
    kpis: new Map(),
    callbacks: {
      onTick: null,
      onComplete: null,
      onPause: null,
    },
  };

  function clearTimer() {
    if (state.timer) {
      clearTimeout(state.timer);
      state.timer = null;
    }
  }

  function notify(snapshot) {
    state.charts.forEach(({ chart, updateFn }) => {
      updateFn(snapshot, state.month, state.snapshots);
      chart.update('none');
    });

    state.kpis.forEach(({ element, valueFn }) => {
      if (!element) return;
      element.textContent = String(valueFn(snapshot, state.month, state.snapshots));
    });

    if (typeof state.callbacks.onTick === 'function') {
      state.callbacks.onTick(snapshot, state.month, state.snapshots);
    }
  }

  function tick() {
    if (!state.playing || !state.portfolio) return;

    if (state.month >= state.maxMonths) {
      state.playing = false;
      clearTimer();
      if (typeof state.callbacks.onComplete === 'function') {
        state.callbacks.onComplete(state.snapshots[state.snapshots.length - 1], state.month, state.snapshots);
      }
      return;
    }

    const nextMonth = state.month + 1;
    const stepped = lifecycleEngine.stepMonth(state.portfolio, nextMonth, state.lifecycleConfig);
    state.month = nextMonth;
    state.snapshots = [...state.portfolio.snapshots];
    notify(stepped.snapshot);

    if (state.playing) {
      state.timer = setTimeout(tick, state.speedMs);
    }
  }

  function init(portfolio, config) {
    clearTimer();
    state.playing = false;
    state.month = portfolio?.month ?? 0;
    state.portfolio = portfolio || null;

    const cfg = { ...DEFAULTS, ...(config || {}) };
    state.speedMs = cfg.speedMs;
    state.maxMonths = cfg.maxMonths;
    state.lifecycleConfig = { ...DEFAULTS.lifecycleConfig, ...(cfg.lifecycleConfig || {}) };
    state.callbacks.onTick = cfg.onTick;
    state.callbacks.onComplete = cfg.onComplete;
    state.callbacks.onPause = cfg.onPause;

    state.snapshots = portfolio?.snapshots ? [...portfolio.snapshots] : [];
  }

  function play() {
    if (!state.portfolio) return;
    if (state.playing) return;
    state.playing = true;

    if (state.month >= state.maxMonths) {
      const latest = state.snapshots[state.snapshots.length - 1] || null;
      if (latest) notify(latest);
      state.playing = false;
      return;
    }

    tick();
  }

  function pause() {
    state.playing = false;
    clearTimer();
    if (typeof state.callbacks.onPause === 'function') {
      state.callbacks.onPause(state.snapshots[state.snapshots.length - 1] || null, state.month, state.snapshots);
    }
  }

  function resume() {
    play();
  }

  function seekTo(month) {
    if (!state.portfolio) return;
    const target = Math.max(0, Math.min(month, state.maxMonths));

    if (target <= state.month) {
      state.month = target;
      const snapshot = state.snapshots.find((s) => s.month === target) || state.snapshots[state.snapshots.length - 1];
      if (snapshot) notify(snapshot);
      return;
    }

    for (let m = state.month + 1; m <= target; m++) {
      const stepped = lifecycleEngine.stepMonth(state.portfolio, m, state.lifecycleConfig);
      state.snapshots = [...state.portfolio.snapshots];
      state.month = m;
      if (m === target) notify(stepped.snapshot);
    }
  }

  function reset() {
    pause();
    if (!state.portfolio) return;
    state.month = 0;
    const snapshot = state.snapshots.find((s) => s.month === 0) || state.snapshots[0];
    if (snapshot) notify(snapshot);
  }

  function setSpeed(speedMs) {
    state.speedMs = speedMs;
  }

  function registerChart(chartId, chartInstance, updateFn) {
    state.charts.set(chartId, { chart: chartInstance, updateFn });
  }

  function registerKPI(elementId, valueFn) {
    const element = document.getElementById(elementId);
    state.kpis.set(elementId, { element, valueFn });
  }

  function getState() {
    return {
      month: state.month,
      playing: state.playing,
      snapshots: [...state.snapshots],
      portfolio: state.portfolio,
      speedMs: state.speedMs,
      maxMonths: state.maxMonths,
    };
  }

  window.animationController = {
    init,
    play,
    pause,
    resume,
    seekTo,
    reset,
    setSpeed,
    registerChart,
    registerKPI,
    getState,
  };
})();
