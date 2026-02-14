// pm-interview-coach/app/static/js/main.js

(function () {
  "use strict";

  function autoResize(textarea) {
    textarea.style.height = "auto";
    textarea.style.height = `${textarea.scrollHeight}px`;
  }

  function setupTextarea() {
    const textarea = document.querySelector("[data-auto-resize]");
    if (!textarea) return;

    autoResize(textarea);
    textarea.addEventListener("input", () => autoResize(textarea));
  }

  function setupTimer() {
    const form = document.getElementById("practice-form");
    if (!form) return;

    const textarea = document.getElementById("answer-text");
    const timeSpentInput = document.getElementById("time-spent");
    const submitBtn = document.getElementById("submit-btn");
    let startTime = null;

    if (textarea) {
      textarea.addEventListener("focus", () => {
        if (!startTime) {
          startTime = Date.now();
        }
      });
    }

    document.body.addEventListener("htmx:beforeRequest", (event) => {
      if (!form.contains(event.target)) return;
      if (startTime && timeSpentInput) {
        const seconds = Math.round((Date.now() - startTime) / 1000);
        timeSpentInput.value = String(seconds);
      }
      if (submitBtn) submitBtn.disabled = true;
    });

    document.body.addEventListener("htmx:afterSwap", (event) => {
      if (event.target && event.target.id === "feedback-panel") {
        if (submitBtn) submitBtn.disabled = false;
      }
    });
  }

  async function fetchJson(url) {
    const response = await fetch(url);
    if (!response.ok) {
      throw new Error(`Failed to load ${url}`);
    }
    return response.json();
  }

  async function initCharts() {
    if (!window.Chart) return;
    const trendCanvas = document.getElementById("trendChart");
    const categoryCanvas = document.getElementById("categoryChart");
    const heatmapCanvas = document.getElementById("heatmapChart");

    const accent = getComputedStyle(document.documentElement)
      .getPropertyValue("--color-accent")
      .trim() || "#2E8ECE";

    if (trendCanvas) {
      const trend = await fetchJson("/api/stats/trend");
      new Chart(trendCanvas, {
        type: "line",
        data: {
          labels: trend.map((row) => row.date),
          datasets: [
            {
              label: "Avg Score",
              data: trend.map((row) => row.avg_score),
              borderColor: accent,
              tension: 0.3,
            },
          ],
        },
      });
    }

    if (categoryCanvas) {
      const categories = await fetchJson("/api/stats/by-category");
      new Chart(categoryCanvas, {
        type: "bar",
        data: {
          labels: categories.map((row) => row.category.replace(/_/g, " ")),
          datasets: [
            {
              label: "Avg Score",
              data: categories.map((row) => row.avg_score),
              backgroundColor: accent,
            },
          ],
        },
      });
    }

    if (heatmapCanvas) {
      const heatmap = await fetchJson("/api/stats/heatmap");
      new Chart(heatmapCanvas, {
        type: "bar",
        data: {
          labels: heatmap.map((row) => row.date),
          datasets: [
            {
              label: "Attempts",
              data: heatmap.map((row) => row.count),
              backgroundColor: accent,
            },
          ],
        },
        options: {
          scales: {
            x: { display: false },
          },
        },
      });
    }
  }

  document.addEventListener("DOMContentLoaded", function () {
    setupTextarea();
    setupTimer();
    initCharts();
  });
})();
