// fullstackpm.tech — Marketplace analytics charts

(function () {
  "use strict";

  function getAccentColor() {
    return (
      getComputedStyle(document.documentElement)
        .getPropertyValue("--color-accent")
        .trim() || "#2E8ECE"
    );
  }

  function initRevenueChart() {
    const canvas = document.querySelector("[data-chart='revenue']");
    if (!canvas || !window.Chart) return;

    const labels = JSON.parse(canvas.dataset.labels || "[]");
    const values = JSON.parse(canvas.dataset.values || "[]");

    if (canvas._chart) {
      canvas._chart.destroy();
    }

    canvas._chart = new Chart(canvas, {
      type: "line",
      data: {
        labels,
        datasets: [
          {
            label: "Revenue",
            data: values,
            borderColor: getAccentColor(),
            backgroundColor: "rgba(46, 142, 206, 0.15)",
            fill: true,
            tension: 0.3,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false },
        },
        scales: {
          y: {
            ticks: {
              callback: (value) => `$${value}`,
            },
          },
        },
      },
    });
  }

  function updateExportLink() {
    const form = document.getElementById("marketplace-filters");
    const link = document.getElementById("export-link");
    if (!form || !link) return;

    const params = new URLSearchParams(new FormData(form));
    link.href = `/tools/marketplace-analytics/export?${params.toString()}`;
  }

  function syncFilterState() {
    const dashboard = document.getElementById("dashboard-content-inner");
    if (!dashboard) return;

    const sortBy = dashboard.dataset.sortBy || "revenue";
    const sortDir = dashboard.dataset.sortDir || "desc";
    const sortByInput = document.getElementById("sort-by");
    const sortDirInput = document.getElementById("sort-dir");

    if (sortByInput) sortByInput.value = sortBy;
    if (sortDirInput) sortDirInput.value = sortDir;
    updateExportLink();
  }

  function init() {
    initRevenueChart();
    syncFilterState();

    const form = document.getElementById("marketplace-filters");
    if (form) {
      form.addEventListener("change", updateExportLink);
    }
  }

  document.addEventListener("DOMContentLoaded", init);
  document.body.addEventListener("htmx:afterSwap", (event) => {
    if (event.target && event.target.id === "dashboard-content") {
      init();
    }
  });
})();
