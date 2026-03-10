# 🌸 Hormona AI

> A personalised hormone & mood forecasting web app — built with FastAPI, Chart.js, and a soothing hibiscus-pink UI designed for women's wellness.

---

## ✨ Features

- **Today's Insight** — Energy level, mood, and phase-specific wellness advice based on your cycle day
- **Tomorrow's Mood Prediction** — Know how you'll feel before the day starts
- **7-Day Energy Forecast** — Interactive Chart.js line graph colour-coded by hormonal phase
- **9 Granular Cycle Phases** — From early menstrual through PMS, not just four blunt zones
- **Sleep Adjustment Rules** — 6-tier sleep scoring (+/- energy based on hours slept)
- **Current Mood Modifier** — 8 mood options that shift your energy and surface personalised tips
- **Compound Interaction Rules** — Cross-condition logic (e.g. poor sleep + PMS = extra guidance)
- **Personalised 💡 Tips** — Actionable advice combining your phase, sleep, and current mood

---

## 🖥️ Tech Stack

| Layer     | Technology                        |
|-----------|-----------------------------------|
| Backend   | Python · FastAPI · Pydantic       |
| Frontend  | Jinja2 Templates · Vanilla JS     |
| Chart     | Chart.js                          |
| Styling   | Custom CSS · Google Fonts (Playfair Display + Nunito) |
| Server    | Uvicorn (ASGI)                    |

---

## 📁 Project Structure

```
hormona-ai/
├── app/
│   ├── main.py                  # FastAPI app, routes, template config
│   ├── routes/
│   │   └── predict.py           # /predict and /forecast API endpoints
│   ├── services/
│   │   └── prediction.py        # Core prediction & forecasting engine
│   ├── static/
│   │   ├── css/style.css        # Hibiscus-pink theme
│   │   └── js/app.js            # Form logic, fetch calls, chart rendering
│   └── templates/
│       ├── base.html            # Shared layout, nav, floating petals
│       ├── index.html           # Home / hero page
│       └── demo.html            # Forecast demo page
├── app.py                       # Entry point (optional)
├── requirements.txt
└── README.md
```

---

## 🚀 Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/YOUR_USERNAME/hormona-ai.git
cd hormona-ai
```

### 2. Create a virtual environment

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the development server

```bash
uvicorn app.main:app --reload
```

Open [http://localhost:8000](http://localhost:8000) in your browser.

---

## 🌐 Deploy to Railway (free)

1. Push the project to a GitHub repository
2. Go to [railway.app](https://railway.app) → **New Project → Deploy from GitHub repo**
3. Select your repo — Railway auto-detects Python
4. Your app will be live at a `.railway.app` URL in ~2 minutes

> Make sure your `requirements.txt` is present and your start command is:
> `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

---

## 🔌 API Reference

### `POST /predict`
Returns today's insight.

**Request body:**
```json
{
  "last_period": "2026-02-20",
  "cycle_length": 28,
  "sleep_hours": 7.5,
  "current_mood": "Anxious"
}
```

**Response:**
```json
{
  "cycle_day": 18,
  "phase": "Luteal",
  "energy": 35,
  "mood": "Anxious",
  "insight": "Progesterone is peaking — emotions may feel heightened.",
  "tips": ["Elevated anxiety today. Try 4-7-8 breathing before any demanding tasks."]
}
```

---

### `POST /forecast`
Returns a 7-day array (today + 6 days). Same request body as `/predict`.
Future days assume optimal sleep (8h) and neutral mood.

---

## 🎨 Cycle Phases

| Phase | Cycle Days | Base Mood | Base Energy |
|-------|-----------|-----------|-------------|
| Menstrual (early) | 0–2 | Reflective | 30% |
| Menstrual (recovering) | 3–5 | Recovering | 40% |
| Follicular | 6–9 | Motivated | 65% |
| Follicular (focused) | 10–12 | Focused | 78% |
| Ovulatory | 13–15 | Confident | 90% |
| Ovulatory (post) | 16–18 | Energized | 82% |
| Luteal (early) | 19–22 | Calm | 58% |
| Luteal (sensitive) | 23–26 | Sensitive | 42% |
| PMS | 27+ | Irritable | 28% |

---

## 📄 License

MIT — feel free to use, adapt, and build on this project.

---

<p align="center">Made with 🌸 for every woman's wellness journey</p>
