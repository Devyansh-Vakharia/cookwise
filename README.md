# 🍳 CookWise v2.0 — AI-Powered Smart Recipe Intelligence

> *"Not just recipes — decision intelligence."*

---

## 🚀 What's New in v2.0

| Feature | Description |
|---------|-------------|
| 🍽️ **8 Cuisine Styles** | North Indian, South Indian, Street Food, Mughlai, Indo-Chinese, Italian, Continental, Healthy |
| 🌐 **11 Languages** | Hindi, Marathi, Tamil, Telugu, Gujarati, Bengali, Punjabi, Kannada, Spanish, French, English |
| 🌙 **Day/Night Mode** | Full light/dark theme toggle |
| 🔍 **Ingredient Autocomplete** | 40+ Indian ingredients with emoji, hints (batata, paneer, besan, etc.) |
| 🏆 **CookWise Score™** | Composite score: 40% taste + 35% health + 25% budget |
| ⏱ **Cook Mode Timer** | Click any step to activate countdown timer |
| 😂 **Savage Reality Roast** | Specific to YOUR ingredients — not generic |
| 🎲 **Surprise Me** | AI suggests random creative ingredient combos |
| 👨‍🍳 **4 Chef Personas** | Gordon Ramsay, Sanjeev Kapoor, Your Dadi, Jamie Oliver |
| 🌶️ **Masala Intelligence** | Exact spice quantities with purpose explained |
| 🎊 **Confetti** | Fires when CookWise Score ≥ 80 |

---

## 📁 Project Structure

```
cookwise/
├── backend/
│   ├── main.py                  ← FastAPI entry point
│   ├── requirements.txt
│   ├── .env.example             ← copy to .env and fill keys
│   ├── routes/
│   │   ├── recipe.py            ← /api/recipe/* endpoints
│   │   ├── meal_planner.py      ← /api/meal-planner/*
│   │   ├── health.py
│   │   └── user.py
│   ├── services/
│   │   ├── ai_service.py        ← Gemini 3 integration
│   │   ├── taste_engine.py      ← ⭐ Taste Compatibility (USP)
│   │   ├── budget_engine.py     ← Budget optimizer
│   │   └── health_engine.py     ← Nutrition analyzer
│   ├── models/
│   │   └── user_input.py        ← Pydantic schemas
│   └── database/
│       └── mongo.py             ← MongoDB (optional)
│
├── frontend/
│   ├── index.html               ← Landing page
│   ├── app.html                 ← Main app
│   └── static/
│
└── README.md
```

---

## ⚡ Setup (5 Minutes)

### 1. Navigate to backend
```bash
cd cookwise/backend
```

### 2. Create virtual environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Create .env file
```bash
cp .env.example .env
```
Open `.env` and fill in:
```env
GEMINI_API_KEY=your_key_here
```

> **Get free Gemini API key:** https://aistudio.google.com/app/apikey

### 5. Run
```bash
python main.py
```

### 6. Open in browser
| URL | Page |
|-----|------|
| http://localhost:8000 | Landing page |
| http://localhost:8000/app | Main application |
| http://localhost:8000/api/docs | Swagger API docs |
| http://localhost:8000/api/recipe/test-ai | Quick AI test |

---

## 🔌 API Reference

### `POST /api/recipe/generate`
**Main endpoint — full recipe with all analysis**

Query params:
- `chef_persona` — `gordon` / `sanjeev` / `dadi` / `jamie`
- `language` — `hindi` / `marathi` / `tamil` / etc.

```json
{
  "ingredients": [{"name": "paneer"}, {"name": "atta"}],
  "budget": 50,
  "mood": "quick",
  "user_type": "student",
  "jugaad_mode": false,
  "reality_roast": true,
  "servings": 2,
  "cuisine_preference": "north_indian"
}
```

### `GET /api/recipe/surprise`
Returns a random creative ingredient combination.

### `POST /api/meal-planner/generate`
Generates a 7-day meal plan with shopping list.

### `GET /api/recipe/test-ai`
Quick health check for Gemini connection.

---

## 🧠 The Taste Engine (Core USP)

Located in `services/taste_engine.py`.

1. **Flavor Profile Mapping** — Each ingredient mapped to sweet / sour / spicy / umami / creamy / starchy / protein / bitter / fat
2. **20+ Compatibility Rules** — `umami + creamy → +18`, `sweet + umami → -20`, etc.
3. **Specific Combo Warnings** — Known bad combos (chocolate + Maggi, milk + fish)
4. **Variety Bonus** — 3+ distinct flavor profiles get a score boost
5. **Regret Predictor** — Score maps to regret probability message

---

## 🗺️ Roadmap

| Phase | Feature |
|-------|---------|
| v2.1 | User accounts + recipe history |
| v2.2 | Fridge scanner (camera input) |
| v2.3 | ML-based taste prediction |
| v3.0 | Zomato/Swiggy ingredient ordering integration |
| v3.1 | Social sharing + community recipes |

---

## 🎯 One-liner for Viva / Pitch

> *"CookWise takes user ingredients and constraints, processes them through AI generation, proprietary taste evaluation, budget optimization, and health analysis, and produces a decision-aware recipe recommendation — not just a recipe."*

---

<p align="center">Built with ❤️ and Gemini AI · <strong>CookWise 2.0</strong></p>
