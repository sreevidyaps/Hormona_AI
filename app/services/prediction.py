from datetime import datetime, timedelta

# ---------------------------------------------------------------------------
# Sleep penalty/bonus rules: (max_hours_exclusive, energy_delta, tip)
# Evaluated top-to-bottom; first match wins.
# ---------------------------------------------------------------------------
SLEEP_RULES = [
    (5,   -25, "Severe sleep deprivation detected. Avoid high-stakes decisions and rest whenever possible."),
    (6,   -15, "Low sleep is limiting your energy and focus. A short nap or early bedtime tonight will help."),
    (7,    -8, "Slightly under-rested. Moderate caffeine and light movement can restore alertness."),
    (8,     0, None),
    (9,    +5, "Well-rested! Your body is primed for a productive and balanced day."),
    (999,  -5, "Oversleeping can cause grogginess. Aiming for 7–8 hours tonight will sharpen your rhythm."),
]

# ---------------------------------------------------------------------------
# User-reported current mood modifiers: mood -> (energy_delta, optional_tip)
# ---------------------------------------------------------------------------
MOOD_MODIFIERS = {
    "Happy":     (+10, None),
    "Energetic": (+15, None),
    "Calm":      (  0, None),
    "Normal":    (  0, None),
    "Anxious":   (-10, "Elevated anxiety today. Try 4-7-8 breathing before any demanding tasks."),
    "Sad":       (-15, "Your emotional state matters. Gentle movement and connection can help lift your spirits."),
    "Irritable": (-12, "Higher irritability today. Avoid conflict-heavy situations and give yourself grace."),
    "Fatigued":  (-20, "You've reported fatigue. Prioritize rest, hydration, and iron-rich foods."),
}


# ---------------------------------------------------------------------------
# Phase detection — 9 granular phases across the cycle
# ---------------------------------------------------------------------------
def get_phase_data(cycle_day):
    if cycle_day < 3:
        return {
            "phase": "Menstrual",
            "energy": 30,
            "mood": "Reflective",
            "insight": "Early menstrual phase — your body is shedding. Rest is productive. Heat therapy eases cramps."
        }
    elif cycle_day < 6:
        return {
            "phase": "Menstrual",
            "energy": 40,
            "mood": "Recovering",
            "insight": "Bleeding is slowing and energy is beginning to return. Gentle yoga or walks are ideal."
        }
    elif cycle_day < 10:
        return {
            "phase": "Follicular",
            "energy": 65,
            "mood": "Motivated",
            "insight": "Estrogen is rising — great time for creative work, learning new skills, and social plans."
        }
    elif cycle_day < 13:
        return {
            "phase": "Follicular",
            "energy": 78,
            "mood": "Focused",
            "insight": "High follicular energy. Tackle complex projects, strategic thinking, and planning now."
        }
    elif cycle_day < 16:
        return {
            "phase": "Ovulatory",
            "energy": 90,
            "mood": "Confident",
            "insight": "Peak ovulatory phase — optimal for presentations, interviews, bold decisions, and networking."
        }
    elif cycle_day < 19:
        return {
            "phase": "Ovulatory",
            "energy": 82,
            "mood": "Energized",
            "insight": "Post-ovulation energy is still high. Excellent for collaboration, leadership, and teamwork."
        }
    elif cycle_day < 23:
        return {
            "phase": "Luteal",
            "energy": 58,
            "mood": "Calm",
            "insight": "Early luteal phase — good for detail-oriented work, editing, and completing existing tasks."
        }
    elif cycle_day < 27:
        return {
            "phase": "Luteal",
            "energy": 42,
            "mood": "Sensitive",
            "insight": "Progesterone is peaking — emotions may feel heightened. Self-care and firm boundaries matter."
        }
    else:
        return {
            "phase": "PMS",
            "energy": 28,
            "mood": "Irritable",
            "insight": "Late luteal / PMS phase — energy drops, irritability can spike. Magnesium and rest are your allies."
        }


# ---------------------------------------------------------------------------
# Adjustment engine — combines sleep and current mood on top of phase baseline
# ---------------------------------------------------------------------------
def apply_adjustments(base_energy, base_mood, base_phase, sleep_hours, current_mood):
    tips = []
    energy = base_energy

    # ── Sleep rules ────────────────────────────────────────────────────────────
    sleep_delta, sleep_tip = 0, None
    for threshold, delta, tip in SLEEP_RULES:
        if sleep_hours < threshold:
            sleep_delta, sleep_tip = delta, tip
            break
    energy += sleep_delta
    if sleep_tip:
        tips.append(sleep_tip)

    # ── Current mood modifier ─────────────────────────────────────────────────
    mood_delta, mood_tip = MOOD_MODIFIERS.get(current_mood, (0, None))
    energy += mood_delta
    if mood_tip:
        tips.append(mood_tip)

    # ── Compound interaction rules ────────────────────────────────────────────
    if sleep_hours < 6 and current_mood in ("Anxious", "Irritable", "Sad"):
        energy -= 8
        tips.append("Poor sleep combined with a low mood is a tough combination - be extra gentle with yourself today.")

    if sleep_hours >= 7.5 and current_mood in ("Happy", "Energetic"):
        energy += 5
        tips.append("Great sleep combined with a positive mood - you're set up for a high-performance day!")

    if current_mood == "Fatigued" and base_phase == "PMS":
        energy -= 5
        tips.append("Late-cycle fatigue is real and valid. Reduce social obligations and eat iron-rich foods.")

    if current_mood == "Fatigued" and base_phase in ("Luteal", "Menstrual"):
        tips.append("Your hormonal phase naturally lowers energy. Avoid over-scheduling and honour your body's signals.")

    if base_mood == "Confident" and current_mood in ("Anxious", "Sad"):
        tips.append("Your hormones are in a peak phase but your mood feels lower - this may be situational. Journalling or talking to someone can help clarify.")

    if base_phase == "Ovulatory" and sleep_hours < 6:
        tips.append("Even during your peak phase, severe sleep loss will blunt ovulatory energy. Protect your sleep tonight.")

    if current_mood == "Anxious" and base_phase in ("PMS", "Luteal"):
        energy -= 5
        tips.append("Anxiety during the luteal/PMS phase can be hormone-driven. Limit caffeine and try magnesium-rich foods.")

    if sleep_hours >= 8 and base_phase == "Menstrual":
        tips.append("Good sleep during your period aids recovery - keep it up.")

    # ── Clamp energy ──────────────────────────────────────────────────────────
    energy = max(5, min(100, int(energy)))

    # ── Resolve final displayed mood ─────────────────────────────────────────
    final_mood = _resolve_mood(energy, base_mood, current_mood)

    return energy, final_mood, tips


def _resolve_mood(energy, base_mood, current_mood):
    """Blend hormonal phase mood with user-reported state for the displayed label."""
    if current_mood == "Fatigued" and energy < 30:
        return "Exhausted"
    if current_mood == "Anxious" and energy < 45:
        return "Anxious"
    if current_mood == "Sad" and energy < 40:
        return "Low"
    # If user feels clearly better than the phase suggests, trust them
    if current_mood in ("Happy", "Energetic") and energy >= 70:
        return base_mood
    return base_mood


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------
def generate_prediction(last_period, cycle_length, sleep_hours=8.0, current_mood="Normal"):
    last_period_dt = datetime.strptime(last_period, "%Y-%m-%d")
    cycle_day = (datetime.today() - last_period_dt).days % cycle_length
    phase = get_phase_data(cycle_day)
    energy, mood, tips = apply_adjustments(
        phase["energy"], phase["mood"], phase["phase"], sleep_hours, current_mood
    )
    return {
        "cycle_day": cycle_day,
        "phase": phase["phase"],
        "energy": energy,
        "mood": mood,
        "insight": phase["insight"],
        "tips": tips
    }


def generate_forecast(last_period, cycle_length, sleep_hours=8.0, current_mood="Normal", days=7):
    last_period_dt = datetime.strptime(last_period, "%Y-%m-%d")
    today = datetime.today()
    forecast = []

    for i in range(days):
        target = today + timedelta(days=i)
        cycle_day = (target - last_period_dt).days % cycle_length
        phase = get_phase_data(cycle_day)

        # Sleep & mood adjustments apply to today only;
        # future days assume optimal sleep (8h) and neutral mood.
        if i == 0:
            energy, mood, tips = apply_adjustments(
                phase["energy"], phase["mood"], phase["phase"], sleep_hours, current_mood
            )
        else:
            energy, mood, tips = apply_adjustments(
                phase["energy"], phase["mood"], phase["phase"], 8.0, "Normal"
            )

        if i == 0:
            label = "Today"
        elif i == 1:
            label = "Tomorrow"
        else:
            label = target.strftime("%b %d")

        forecast.append({
            "day": label,
            "date": target.strftime("%Y-%m-%d"),
            "cycle_day": cycle_day,
            "phase": phase["phase"],
            "energy": energy,
            "mood": mood,
            "insight": phase["insight"],
            "tips": tips
        })

    return forecast