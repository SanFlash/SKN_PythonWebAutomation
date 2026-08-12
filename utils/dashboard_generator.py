"""Builds the self-contained, colorful, animated HTML test dashboard.

Produces a single-file HTML report using vendored copies of Chart.js
(2D charts) and Three.js (a real, interactive 3D bar visualization),
both inlined directly into the page — assets/chart.umd.min.js and
assets/three.min.js — so it renders fully offline with no CDN.

Visual features:
  - A real 3D "outcome skyline" (Three.js): three lit, colored bars
    sized by pass/fail/skip count, auto-rotating and mouse-interactive
  - Animated count-up numbers on every summary card
  - 3D tilt-on-hover for every card (mouse-tracked perspective transform)
  - An animated circular gauge for the pass rate
  - Chart.js doughnut/pie/bar charts with tuned, elastic-feeling
    animations and gradient fills
  - A filterable results table

This sits alongside Allure and pytest-html: those remain the full,
industry-standard reports; this is a fast, visually rich summary that's
generated and opened automatically the moment the run finishes (see
fixtures/dashboard_fixtures.py).

Author: Satyendra Kumar Namdeo
Project: Darshan Hotel — Playwright + Pytest + Allure Automation Framework
This authorship notice is part of the project source and must be preserved
in copies and forks (see NOTICE.md and LICENSE at the repository root).
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

_ASSETS_DIR = Path(__file__).resolve().parent.parent / "assets"
_CHARTJS_PATH = _ASSETS_DIR / "chart.umd.min.js"
_THREEJS_PATH = _ASSETS_DIR / "three.min.js"

_MODULE_PALETTE = [
    "#6366f1", "#06b6d4", "#ec4899", "#f97316", "#84cc16", "#8b5cf6", "#14b8a6",
]


def build_dashboard_html(
    results: list[dict[str, Any]],
    app_env: str,
    base_url: str,
    generated_at: str,
    author: str = "Satyendra Kumar Namdeo",
) -> str:
    total = len(results)
    passed = sum(1 for r in results if r["outcome"] == "passed")
    failed = sum(1 for r in results if r["outcome"] == "failed")
    skipped = sum(1 for r in results if r["outcome"] == "skipped")
    pass_rate = round((passed / total) * 100, 1) if total else 0.0
    total_duration = round(sum(r["duration"] for r in results), 2)

    modules: dict[str, int] = {}
    for r in results:
        modules[r["module"]] = modules.get(r["module"], 0) + 1

    chartjs_source = (
        _CHARTJS_PATH.read_text(encoding="utf-8") if _CHARTJS_PATH.exists() else ""
    )
    threejs_source = (
        _THREEJS_PATH.read_text(encoding="utf-8") if _THREEJS_PATH.exists() else ""
    )

    sorted_by_duration = sorted(results, key=lambda r: r["duration"], reverse=True)

    template = _TEMPLATE
    template = template.replace("__AUTHOR__", author)
    template = template.replace("__APP_ENV__", app_env)
    template = template.replace("__BASE_URL__", base_url)
    template = template.replace("__GENERATED_AT__", generated_at)
    template = template.replace("__TOTAL__", str(total))
    template = template.replace("__PASSED__", str(passed))
    template = template.replace("__FAILED__", str(failed))
    template = template.replace("__SKIPPED__", str(skipped))
    template = template.replace("__PASS_RATE__", str(pass_rate))
    template = template.replace("__TOTAL_DURATION__", str(total_duration))
    template = template.replace("__FAILED_CLASS__", "has-failures" if failed > 0 else "")
    template = template.replace("__RESULTS_JSON__", json.dumps(results))
    template = template.replace("__DURATIONS_JSON__", json.dumps(sorted_by_duration))
    template = template.replace("__MODULES_JSON__", json.dumps(modules))
    template = template.replace(
        "__MODULE_COLORS_JSON__",
        json.dumps(
            {m: _MODULE_PALETTE[i % len(_MODULE_PALETTE)] for i, m in enumerate(modules)}
        ),
    )
    template = template.replace("__CHARTJS_SOURCE__", chartjs_source)
    template = template.replace("__THREEJS_SOURCE__", threejs_source)
    return template


_TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<title>Darshan Hotel — Automation Dashboard</title>
<meta name="author" content="__AUTHOR__" />
<style>
  :root {
    --passed: #22c55e;
    --failed: #ef4444;
    --skipped: #f59e0b;
    --total: #6366f1;
    --duration: #06b6d4;
    --bg: #0f172a;
    --card-bg: #1e293b;
    --text: #e2e8f0;
    --muted: #94a3b8;
  }
  * { box-sizing: border-box; }
  body {
    margin: 0;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    background: var(--bg);
    color: var(--text);
  }

  @keyframes gradientShift {
    0%   { background-position: 0% 50%; }
    50%  { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
  }
  header {
    background: linear-gradient(120deg, #4f46e5, #7c3aed, #db2777, #7c3aed, #4f46e5);
    background-size: 300% 300%;
    animation: gradientShift 12s ease infinite;
    padding: 36px 40px;
    box-shadow: 0 4px 24px rgba(0,0,0,0.35);
    position: relative;
    overflow: hidden;
  }
  header h1 { margin: 0 0 6px; font-size: 28px; }
  header .meta { color: rgba(255,255,255,0.85); font-size: 14px; line-height: 1.7; }
  header .meta b { color: #fff; }

  main { padding: 32px 40px 60px; max-width: 1320px; margin: 0 auto; }

  @keyframes fadeSlideUp {
    from { opacity: 0; transform: translateY(18px); }
    to   { opacity: 1; transform: translateY(0); }
  }

  .cards { display: grid; grid-template-columns: repeat(auto-fit, minmax(170px, 1fr)); gap: 16px; margin-bottom: 32px; perspective: 800px; }
  .card {
    background: var(--card-bg);
    border-radius: 14px;
    padding: 20px;
    border-left: 5px solid var(--accent, #6366f1);
    box-shadow: 0 2px 10px rgba(0,0,0,0.25);
    opacity: 0;
    animation: fadeSlideUp .55s ease forwards;
    transition: transform .15s ease, box-shadow .15s ease;
    transform-style: preserve-3d;
    will-change: transform;
    cursor: default;
  }
  .card:hover { box-shadow: 0 12px 28px rgba(0,0,0,0.4); }
  .cards .card:nth-child(1) { animation-delay: .05s; }
  .cards .card:nth-child(2) { animation-delay: .12s; }
  .cards .card:nth-child(3) { animation-delay: .19s; }
  .cards .card:nth-child(4) { animation-delay: .26s; }
  .cards .card:nth-child(5) { animation-delay: .33s; }
  .cards .card:nth-child(6) { animation-delay: .40s; }
  .card .value { font-size: 30px; font-weight: 700; }
  .card .label { color: var(--muted); font-size: 13px; text-transform: uppercase; letter-spacing: .04em; margin-top: 4px; }
  .card.total { --accent: var(--total); }
  .card.passed { --accent: var(--passed); }
  .card.failed { --accent: var(--failed); }
  .card.skipped { --accent: var(--skipped); }
  .card.rate { --accent: #a855f7; }
  .card.duration { --accent: var(--duration); }
  .card.failed.has-failures { animation: fadeSlideUp .55s ease forwards, pulseGlow 2.4s ease-in-out .6s infinite; }
  @keyframes pulseGlow {
    0%, 100% { box-shadow: 0 2px 10px rgba(239,68,68,0.15); }
    50%      { box-shadow: 0 2px 24px rgba(239,68,68,0.55); }
  }

  .hero-3d {
    background: linear-gradient(160deg, #1e293b 0%, #16213a 100%);
    border-radius: 16px;
    padding: 20px 20px 4px;
    margin-bottom: 24px;
    box-shadow: 0 2px 14px rgba(0,0,0,0.3);
    opacity: 0;
    animation: fadeSlideUp .6s ease .1s forwards;
  }
  .hero-3d h3 { margin: 0 0 4px; font-size: 15px; color: var(--muted); font-weight: 600; text-transform: uppercase; letter-spacing: .04em; }
  .hero-3d .hint { color: var(--muted); font-size: 12px; margin-bottom: 8px; }
  #scene3d { width: 100%; height: 340px; border-radius: 12px; overflow: hidden; cursor: grab; }
  #scene3d canvas { display: block; }
  #scene3d-fallback { display: none; color: var(--muted); font-size: 13px; padding: 40px; text-align: center; }

  .charts { display: grid; grid-template-columns: repeat(auto-fit, minmax(340px, 1fr)); gap: 20px; margin-bottom: 32px; }
  .chart-box {
    background: var(--card-bg); border-radius: 14px; padding: 20px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.25);
    opacity: 0; animation: fadeSlideUp .6s ease .15s forwards;
  }
  .chart-box h3 { margin: 0 0 12px; font-size: 15px; color: var(--muted); font-weight: 600; text-transform: uppercase; letter-spacing: .04em; }
  .chart-box canvas { max-height: 280px; }

  .gauge-box { display: flex; align-items: center; justify-content: center; gap: 20px; flex-wrap: wrap; }
  .gauge-svg circle { transition: stroke-dashoffset 1.4s cubic-bezier(.22,1,.36,1); }
  .gauge-label { font-size: 26px; font-weight: 700; }
  .gauge-sub { color: var(--muted); font-size: 12px; text-transform: uppercase; letter-spacing: .04em; }

  .table-box { background: var(--card-bg); border-radius: 14px; padding: 20px; box-shadow: 0 2px 10px rgba(0,0,0,0.25); opacity: 0; animation: fadeSlideUp .6s ease .2s forwards; }
  .table-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px; flex-wrap: wrap; gap: 10px; }
  .table-header h3 { margin: 0; font-size: 15px; color: var(--muted); font-weight: 600; text-transform: uppercase; letter-spacing: .04em; }
  .filters button {
    background: #334155; color: var(--text); border: none; padding: 7px 14px;
    border-radius: 999px; font-size: 13px; cursor: pointer; margin-left: 6px; transition: background .15s, transform .15s;
  }
  .filters button:hover { background: #475569; transform: translateY(-1px); }
  .filters button.active { background: var(--total); color: #fff; }

  table { width: 100%; border-collapse: collapse; font-size: 14px; }
  th, td { text-align: left; padding: 10px 12px; border-bottom: 1px solid #334155; }
  th { color: var(--muted); font-weight: 600; font-size: 12px; text-transform: uppercase; letter-spacing: .03em; }
  tr { transition: background .12s; }
  tr:hover td { background: #263244; }
  .badge { display: inline-block; padding: 3px 10px; border-radius: 999px; font-size: 12px; font-weight: 600; color: #fff; }
  .badge.passed { background: var(--passed); }
  .badge.failed { background: var(--failed); }
  .badge.skipped { background: var(--skipped); }
  .marker-chip {
    display: inline-block; background: #334155; color: var(--muted); font-size: 11px;
    padding: 2px 8px; border-radius: 6px; margin-right: 4px;
  }
  footer { text-align: center; color: var(--muted); font-size: 13px; padding: 24px; }
</style>
</head>
<body>

<header>
  <h1>🏨 Darshan Hotel — Automation Dashboard</h1>
  <div class="meta">
    <div>Author: <b>__AUTHOR__</b> &nbsp;|&nbsp; Framework: <b>Python + Playwright + Pytest + Allure</b></div>
    <div>Environment: <b>__APP_ENV__</b> &nbsp;|&nbsp; Target: <b>__BASE_URL__</b></div>
    <div>Generated: <b>__GENERATED_AT__</b></div>
  </div>
</header>

<main>
  <div class="cards">
    <div class="card total"><div class="value" data-count="__TOTAL__">0</div><div class="label">Total Tests</div></div>
    <div class="card passed"><div class="value" data-count="__PASSED__">0</div><div class="label">Passed</div></div>
    <div class="card failed __FAILED_CLASS__"><div class="value" data-count="__FAILED__">0</div><div class="label">Failed</div></div>
    <div class="card skipped"><div class="value" data-count="__SKIPPED__">0</div><div class="label">Skipped</div></div>
    <div class="card rate"><div class="value" data-count="__PASS_RATE__" data-suffix="%" data-decimals="1">0%</div><div class="label">Pass Rate</div></div>
    <div class="card duration"><div class="value" data-count="__TOTAL_DURATION__" data-suffix="s" data-decimals="2">0s</div><div class="label">Total Duration</div></div>
  </div>

  <div class="hero-3d">
    <h3>🎮 3D Outcome Skyline</h3>
    <div class="hint">Auto-rotating — move your mouse over it to steer, or drag on touch devices.</div>
    <div id="scene3d"></div>
    <div id="scene3d-fallback">3D view needs WebGL, which isn't available in this browser — see the doughnut chart below instead.</div>
  </div>

  <div class="charts">
    <div class="chart-box">
      <h3>Outcome Breakdown</h3>
      <canvas id="outcomeChart"></canvas>
    </div>
    <div class="chart-box">
      <h3>Tests by Module</h3>
      <canvas id="moduleChart"></canvas>
    </div>
    <div class="chart-box gauge-box">
      <svg class="gauge-svg" width="160" height="160" viewBox="0 0 160 160">
        <circle cx="80" cy="80" r="70" fill="none" stroke="#334155" stroke-width="14" />
        <circle id="gaugeRing" cx="80" cy="80" r="70" fill="none" stroke="#a855f7" stroke-width="14"
                stroke-linecap="round" transform="rotate(-90 80 80)" />
      </svg>
      <div>
        <div class="gauge-label" id="gaugeLabel">0%</div>
        <div class="gauge-sub">Pass Rate</div>
      </div>
    </div>
    <div class="chart-box" style="grid-column: 1 / -1;">
      <h3>Duration per Test (seconds)</h3>
      <canvas id="durationChart"></canvas>
    </div>
  </div>

  <div class="table-box">
    <div class="table-header">
      <h3>Test Results</h3>
      <div class="filters">
        <button data-filter="all" class="active">All</button>
        <button data-filter="passed">Passed</button>
        <button data-filter="failed">Failed</button>
        <button data-filter="skipped">Skipped</button>
      </div>
    </div>
    <table id="resultsTable">
      <thead>
        <tr><th>Test</th><th>Module</th><th>Outcome</th><th>Duration (s)</th><th>Markers</th></tr>
      </thead>
      <tbody></tbody>
    </table>
  </div>
</main>

<footer>Darshan Hotel Automation Framework &copy; __AUTHOR__ — generated automatically after every test run</footer>

<script>
__CHARTJS_SOURCE__
</script>

<script>
__THREEJS_SOURCE__
</script>

<script>
  const results = __RESULTS_JSON__;
  const durationSorted = __DURATIONS_JSON__;
  const modules = __MODULES_JSON__;
  const moduleColors = __MODULE_COLORS_JSON__;
  const outcomeColors = { passed: "#22c55e", failed: "#ef4444", skipped: "#f59e0b" };

  const passedCount = results.filter(r => r.outcome === "passed").length;
  const failedCount = results.filter(r => r.outcome === "failed").length;
  const skippedCount = results.filter(r => r.outcome === "skipped").length;
  const passRateValue = results.length ? Math.round((passedCount / results.length) * 1000) / 10 : 0;

  // ---------------------------------------------------------------------
  // Animated count-up numbers
  // ---------------------------------------------------------------------
  function animateCount(el) {
    const target = parseFloat(el.dataset.count || "0");
    const decimals = parseInt(el.dataset.decimals || "0", 10);
    const suffix = el.dataset.suffix || "";
    const duration = 1100;
    const start = performance.now();
    function frame(now) {
      const p = Math.min(1, (now - start) / duration);
      const eased = 1 - Math.pow(1 - p, 3);
      const current = target * eased;
      el.textContent = current.toFixed(decimals) + suffix;
      if (p < 1) requestAnimationFrame(frame);
      else el.textContent = target.toFixed(decimals) + suffix;
    }
    requestAnimationFrame(frame);
  }
  document.querySelectorAll(".card .value[data-count]").forEach(animateCount);

  // ---------------------------------------------------------------------
  // 3D tilt-on-hover for every card
  // ---------------------------------------------------------------------
  document.querySelectorAll(".card").forEach(card => {
    card.addEventListener("mousemove", (e) => {
      const rect = card.getBoundingClientRect();
      const px = (e.clientX - rect.left) / rect.width - 0.5;
      const py = (e.clientY - rect.top) / rect.height - 0.5;
      card.style.transform = `perspective(600px) rotateX(${(-py * 10).toFixed(2)}deg) rotateY(${(px * 10).toFixed(2)}deg) translateZ(4px)`;
    });
    card.addEventListener("mouseleave", () => {
      card.style.transform = "perspective(600px) rotateX(0) rotateY(0) translateZ(0)";
    });
  });

  // ---------------------------------------------------------------------
  // Animated circular pass-rate gauge
  // ---------------------------------------------------------------------
  (function initGauge() {
    const ring = document.getElementById("gaugeRing");
    const label = document.getElementById("gaugeLabel");
    const r = 70;
    const circumference = 2 * Math.PI * r;
    ring.style.strokeDasharray = String(circumference);
    ring.style.strokeDashoffset = String(circumference);
    requestAnimationFrame(() => {
      const offset = circumference - (passRateValue / 100) * circumference;
      ring.style.strokeDashoffset = String(offset);
    });
    const start = performance.now();
    function frame(now) {
      const p = Math.min(1, (now - start) / 1200);
      label.textContent = (passRateValue * (1 - Math.pow(1 - p, 3))).toFixed(1) + "%";
      if (p < 1) requestAnimationFrame(frame);
      else label.textContent = passRateValue.toFixed(1) + "%";
    }
    requestAnimationFrame(frame);
  })();

  // ---------------------------------------------------------------------
  // Chart.js — doughnut / pie / bar, tuned animations + gradient fills
  // ---------------------------------------------------------------------
  Chart.defaults.color = "#94a3b8";
  Chart.defaults.borderColor = "#334155";

  new Chart(document.getElementById("outcomeChart"), {
    type: "doughnut",
    data: {
      labels: ["Passed", "Failed", "Skipped"],
      datasets: [{
        data: [passedCount, failedCount, skippedCount],
        backgroundColor: [outcomeColors.passed, outcomeColors.failed, outcomeColors.skipped],
        borderColor: "#1e293b",
        borderWidth: 3,
        hoverOffset: 10,
      }]
    },
    options: {
      responsive: true,
      animation: { animateRotate: true, animateScale: true, duration: 1400, easing: "easeOutQuart" },
      plugins: { legend: { position: "bottom" } }
    }
  });

  const moduleLabels = Object.keys(modules);
  const moduleValues = Object.values(modules);
  new Chart(document.getElementById("moduleChart"), {
    type: "pie",
    data: {
      labels: moduleLabels,
      datasets: [{
        data: moduleValues,
        backgroundColor: moduleLabels.map(m => moduleColors[m]),
        borderColor: "#1e293b",
        borderWidth: 3,
        hoverOffset: 10,
      }]
    },
    options: {
      responsive: true,
      animation: { animateRotate: true, animateScale: true, duration: 1400, easing: "easeOutQuart" },
      plugins: { legend: { position: "bottom" } }
    }
  });

  const durationCtx = document.getElementById("durationChart").getContext("2d");
  function barGradient(ctx, color) {
    const g = ctx.createLinearGradient(0, 0, 400, 0);
    g.addColorStop(0, color + "55");
    g.addColorStop(1, color);
    return g;
  }
  new Chart(durationCtx, {
    type: "bar",
    data: {
      labels: durationSorted.map(r => r.name),
      datasets: [{
        label: "Duration (s)",
        data: durationSorted.map(r => r.duration),
        backgroundColor: durationSorted.map(r => barGradient(durationCtx, outcomeColors[r.outcome] || "#6366f1")),
        borderRadius: 4,
      }]
    },
    options: {
      indexAxis: "y",
      responsive: true,
      animation: { duration: 1200, easing: "easeOutCubic" },
      plugins: { legend: { display: false } },
      scales: {
        x: { grid: { color: "#334155" } },
        y: { grid: { display: false } }
      }
    }
  });

  // ---------------------------------------------------------------------
  // Results table with filtering
  // ---------------------------------------------------------------------
  const tbody = document.querySelector("#resultsTable tbody");
  function renderTable(filter) {
    tbody.innerHTML = "";
    results
      .filter(r => filter === "all" || r.outcome === filter)
      .forEach(r => {
        const tr = document.createElement("tr");
        const markers = (r.markers || []).map(m => `<span class="marker-chip">${m}</span>`).join("");
        tr.innerHTML = `
          <td>${r.name}</td>
          <td>${r.module}</td>
          <td><span class="badge ${r.outcome}">${r.outcome}</span></td>
          <td>${r.duration}</td>
          <td>${markers}</td>
        `;
        tbody.appendChild(tr);
      });
  }
  renderTable("all");

  document.querySelectorAll(".filters button").forEach(btn => {
    btn.addEventListener("click", () => {
      document.querySelectorAll(".filters button").forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      renderTable(btn.dataset.filter);
    });
  });

  // ---------------------------------------------------------------------
  // Real 3D outcome skyline — Three.js
  // ---------------------------------------------------------------------
  (function init3D() {
    const container = document.getElementById("scene3d");
    const fallback = document.getElementById("scene3d-fallback");
    if (typeof THREE === "undefined") { fallback.style.display = "block"; return; }

    let renderer;
    try {
      renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    } catch (e) {
      fallback.style.display = "block";
      return;
    }

    const width = container.clientWidth || 600;
    const height = 340;

    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(45, width / height, 0.1, 1000);
    camera.position.set(6.5, 5.5, 9);
    camera.lookAt(0, 1, 0);

    renderer.setSize(width, height);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
    container.appendChild(renderer.domElement);

    scene.add(new THREE.AmbientLight(0xffffff, 0.55));
    const dirLight = new THREE.DirectionalLight(0xffffff, 0.9);
    dirLight.position.set(5, 10, 7);
    scene.add(dirLight);
    const pointLight = new THREE.PointLight(0x8b5cf6, 1.2, 60);
    pointLight.position.set(-6, 8, 4);
    scene.add(pointLight);

    const grid = new THREE.GridHelper(16, 16, 0x475569, 0x293548);
    scene.add(grid);

    const group = new THREE.Group();
    scene.add(group);

    function makeTextSprite(text, color) {
      const canvas = document.createElement("canvas");
      canvas.width = 300; canvas.height = 72;
      const ctx = canvas.getContext("2d");
      ctx.font = "bold 32px sans-serif";
      ctx.fillStyle = color;
      ctx.textAlign = "center";
      ctx.fillText(text, 150, 46);
      const texture = new THREE.CanvasTexture(canvas);
      const material = new THREE.SpriteMaterial({ map: texture, transparent: true, depthTest: false });
      const sprite = new THREE.Sprite(material);
      sprite.scale.set(3.4, 0.82, 1);
      return sprite;
    }

    const barData = [
      { label: "Passed: " + passedCount, value: passedCount, color: 0x22c55e },
      { label: "Failed: " + failedCount, value: failedCount, color: 0xef4444 },
      { label: "Skipped: " + skippedCount, value: skippedCount, color: 0xf59e0b },
    ];
    const maxVal = Math.max(1, ...barData.map(d => d.value));
    const barSize = 1.7;
    const spacing = 3.4;
    const startX = -((barData.length - 1) * spacing) / 2;

    barData.forEach((d, i) => {
      const h = Math.max(0.2, (d.value / maxVal) * 5);
      const geo = new THREE.BoxGeometry(barSize, h, barSize);
      const mat = new THREE.MeshStandardMaterial({
        color: d.color, metalness: 0.35, roughness: 0.35,
        emissive: d.color, emissiveIntensity: 0.18,
      });
      const bar = new THREE.Mesh(geo, mat);
      bar.position.set(startX + i * spacing, h / 2, 0);
      group.add(bar);

      const sprite = makeTextSprite(d.label, "#e2e8f0");
      sprite.position.set(startX + i * spacing, h + 1.0, 0);
      group.add(sprite);
    });

    let targetSpin = 0.005;
    let dragging = false;
    let lastX = 0;
    container.addEventListener("mousemove", (e) => {
      if (dragging) {
        const dx = e.clientX - lastX;
        group.rotation.y += dx * 0.01;
        lastX = e.clientX;
        return;
      }
      const rect = container.getBoundingClientRect();
      const nx = ((e.clientX - rect.left) / rect.width) * 2 - 1;
      targetSpin = 0.004 + nx * 0.02;
    });
    container.addEventListener("mousedown", (e) => { dragging = true; lastX = e.clientX; container.style.cursor = "grabbing"; });
    window.addEventListener("mouseup", () => { dragging = false; container.style.cursor = "grab"; });
    container.addEventListener("mouseleave", () => { dragging = false; container.style.cursor = "grab"; });

    function animate() {
      requestAnimationFrame(animate);
      if (!dragging) group.rotation.y += targetSpin;
      renderer.render(scene, camera);
    }
    animate();

    window.addEventListener("resize", () => {
      const w = container.clientWidth || width;
      camera.aspect = w / height;
      camera.updateProjectionMatrix();
      renderer.setSize(w, height);
    });
  })();
</script>

</body>
</html>
"""
