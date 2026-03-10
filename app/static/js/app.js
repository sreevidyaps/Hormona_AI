const MOOD_COLORS = {
  "Reflective": "#a78bfa",
  "Recovering": "#c4b5fd",
  "Motivated":  "#34d399",
  "Focused":    "#38bdf8",
  "Confident":  "#f59e0b",
  "Energized":  "#fb923c",
  "Calm":       "#2dd4bf",
  "Sensitive":  "#f87171",
  "Irritable":  "#ef4444",
  "Anxious":    "#facc15",
  "Sad":        "#94a3b8",
  "Low":        "#94a3b8",
  "Exhausted":  "#64748b"
};

const MOOD_EMOJI = {
  "Reflective": "🌙",
  "Recovering": "🌱",
  "Motivated":  "⚡",
  "Focused":    "🎯",
  "Confident":  "🌟",
  "Energized":  "🔥",
  "Calm":       "🍃",
  "Sensitive":  "🌸",
  "Irritable":  "😤",
  "Anxious":    "😰",
  "Sad":        "😢",
  "Low":        "😶",
  "Exhausted":  "😞"
};

let chartInstance = null;

document.getElementById("forecastForm").addEventListener("submit", async function (e) {
  e.preventDefault();

  const last_period  = document.getElementById("last_period").value;
  const cycle_length = parseInt(document.getElementById("cycle_length").value);
  const current_mood = document.getElementById("current_mood").value;
  const sleep_hours  = parseFloat(document.getElementById("sleep_hours").value);

  if (!last_period) {
    alert("Please select your last period date.");
    return;
  }

  const res = await fetch("/forecast", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ last_period, cycle_length, current_mood, sleep_hours })
  });

  const data = await res.json();

  // ── Today card ──────────────────────────────────────────────────────────────
  const today = data[0];
  const todayCard = document.getElementById("todayCard");
  const todayTips = today.tips && today.tips.length
    ? `<ul class="tips-list">${today.tips.map(t => `<li>${t}</li>`).join("")}</ul>`
    : "";
  todayCard.innerHTML = `
    <h3>Today's Insight ${MOOD_EMOJI[today.mood] || ""}</h3>
    <span class="phase-badge">${today.phase}</span>
    <div class="card-grid">
      <div class="stat-box">
        <span class="stat-label">Cycle Day</span>
        <span class="stat-value">${today.cycle_day}</span>
      </div>
      <div class="stat-box">
        <span class="stat-label">Energy</span>
        <span class="stat-value">${today.energy}%</span>
      </div>
      <div class="stat-box">
        <span class="stat-label">Mood</span>
        <span class="stat-value" style="color:${MOOD_COLORS[today.mood] || '#ff4fa3'}">${today.mood}</span>
      </div>
    </div>
    <p class="insight-text">${today.insight}</p>
    ${todayTips}
  `;
  todayCard.classList.remove("hidden");

  // ── Tomorrow card ────────────────────────────────────────────────────────────
  const tomorrow = data[1];
  const color = MOOD_COLORS[tomorrow.mood] || "#ff4fa3";
  const tomorrowCard = document.getElementById("tomorrowCard");
  tomorrowCard.innerHTML = `
    <h3>Tomorrow's Mood Prediction ${MOOD_EMOJI[tomorrow.mood] || ""}</h3>
    <span class="phase-badge">${tomorrow.phase}</span>
    <div class="tomorrow-mood" style="background:${color}18; border-left:4px solid ${color}">
      <p class="mood-label" style="color:${color}">${tomorrow.mood}</p>
      <p><strong>Energy Level:</strong> ${tomorrow.energy}%</p>
      <p class="insight-text">${tomorrow.insight}</p>
    </div>
  `;
  tomorrowCard.classList.remove("hidden");

  // ── 7-day chart ──────────────────────────────────────────────────────────────
  document.getElementById("chartSection").classList.remove("hidden");

  const labels      = data.map(d => d.day);
  const energies    = data.map(d => d.energy);
  const moods       = data.map(d => d.mood);
  const pointColors = data.map(d => MOOD_COLORS[d.mood] || "#ff4fa3");

  if (chartInstance) chartInstance.destroy();

  const ctx = document.getElementById("energyChart").getContext("2d");
  chartInstance = new Chart(ctx, {
    type: "line",
    data: {
      labels,
      datasets: [{
        label: "Energy Level (%)",
        data: energies,
        borderColor: "#ff4fa3",
        backgroundColor: "rgba(255,79,163,0.08)",
        pointBackgroundColor: pointColors,
        pointBorderColor: pointColors,
        pointRadius: 8,
        pointHoverRadius: 10,
        borderWidth: 2.5,
        tension: 0.4,
        fill: true
      }]
    },
    options: {
      responsive: true,
      plugins: {
        tooltip: {
          callbacks: {
            label: ctx => ` Energy: ${ctx.parsed.y}%`,
            afterLabel: ctx => ` Mood: ${MOOD_EMOJI[moods[ctx.dataIndex]] || ""} ${moods[ctx.dataIndex]}`
          }
        },
        legend: { display: false }
      },
      scales: {
        y: {
          min: 0,
          max: 100,
          ticks: { callback: v => v + "%" },
          grid: { color: "rgba(0,0,0,0.05)" }
        },
        x: {
          grid: { display: false }
        }
      }
    }
  });

  // ── Mood legend below chart ──────────────────────────────────────────────────
  const legend = document.getElementById("moodLegend");
  legend.innerHTML = data.map(d => `
    <div class="legend-item">
      <span class="legend-dot" style="background:${MOOD_COLORS[d.mood] || '#ff4fa3'}"></span>
      <span>${d.day}: ${MOOD_EMOJI[d.mood] || ""} ${d.mood} <span class="legend-phase">(${d.phase})</span></span>
    </div>
  `).join("");
});