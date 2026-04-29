"""
CookWise AI Service — Gemini 3
"""
import os, json, re, asyncio
from dotenv import load_dotenv
from typing import List, Optional
from google import genai
from google.genai import types

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
MODEL  = "gemini-3-flash-preview"

CHEF_PERSONAS = {
    "gordon":  "You are Gordon Ramsay. Be brutally honest, passionate, short punchy sentences, demand quality, occasionally dramatic but give brilliant technique.",
    "sanjeev": "You are Sanjeev Kapoor, India's most beloved chef. Be warm, encouraging, deeply knowledgeable about Indian masalas, regional techniques, and spice combinations.",
    "dadi":    "You are someone's Dadi (Indian grandmother). Be loving, use hand-measurement tips ('ek mutthi', 'thoda sa'), share small secrets passed down generations.",
    "jamie":   "You are Jamie Oliver. Be enthusiastic, rustic, fun. Focus on bold flavours and making cooking joyful.",
}

CUISINE_CONTEXTS = {
    "north_indian":  "Focus on North Indian cuisine — use ghee, whole spices, rich gravies, dum cooking techniques.",
    "south_indian":  "Focus on South Indian cuisine — use curry leaves, mustard seeds, coconut, tamarind, rice-based dishes.",
    "street_food":   "Focus on Indian street food — chaat, vada pav, pav bhaji, bhel, tangy and spicy street-style.",
    "mughlai":       "Focus on Mughlai cuisine — rich kormas, biryanis, kebabs, creamy sauces, saffron, dry fruits.",
    "chinese":       "Focus on Indo-Chinese fusion — manchurian, fried rice, noodles, hakka style.",
    "italian":       "Focus on Italian cuisine — pasta, risotto, pizza, fresh herbs, olive oil.",
    "continental":   "Focus on Continental cuisine — sauces, baked dishes, grilled proteins, European techniques.",
    "healthy":       "Focus on healthy cooking — minimal oil, lots of vegetables, lean protein, whole grains.",
    "": ""
}

def _clean_json(text: str) -> dict:
    text = re.sub(r"```(?:json)?","",text).strip().rstrip("```").strip()
    try: return json.loads(text)
    except json.JSONDecodeError:
        m = re.search(r"\{.*\}",text,re.DOTALL)
        if m: return json.loads(m.group())
        raise ValueError(f"Cannot parse JSON:\n{text[:400]}")

def _call_gemini(prompt: str) -> str:
    r = client.models.generate_content(
        model=MODEL, contents=prompt,
        config=types.GenerateContentConfig(
            thinking_config=types.ThinkingConfig(thinking_level="low"),
            temperature=0.85,
        ),
    )
    return r.text

async def generate_recipe(
    ingredients: List[str], mood: Optional[str]=None,
    user_type: Optional[str]=None, jugaad_mode: bool=False,
    reality_roast: bool=False, servings: int=2,
    dietary_restrictions: Optional[List[str]]=None,
    expiry_priority: Optional[List[str]]=None,
    chef_persona: Optional[str]=None,
    cuisine_preference: Optional[str]=None,
    language: Optional[str]=None,
) -> dict:

    persona  = CHEF_PERSONAS.get(chef_persona,"You are CookWise, an expert culinary AI.")
    cuisine  = CUISINE_CONTEXTS.get(cuisine_preference or "","")
    lang_note= f"\n\nIMPORTANT: Write the recipe_name, tagline, steps instructions, pro_tips, chef_note, garnish_and_plating, storage_tip, and reality_roast in {language}. Keep JSON keys in English." if language and language!="english" else ""

    parts = [
        f"Available ingredients: {', '.join(ingredients)}",
        f"Servings: {servings}",
        f"Mood: {mood} — tailor recipe energy accordingly." if mood else "",
        f"User type: {user_type} — adjust nutrition focus." if user_type else "",
        cuisine,
        "JUGAAD MODE: Be wildly creative. Use limited/unusual ingredients to make something surprisingly good. Give clever hacks." if jugaad_mode else "",
        f"STRICT dietary restrictions — never violate: {', '.join(dietary_restrictions)}." if dietary_restrictions else "",
        f"URGENT — prioritize these expiring ingredients, build recipe around them: {', '.join(expiry_priority)}." if expiry_priority else "",
    ]
    context = "\n".join(p for p in parts if p)

    roast_inst = ""
    if reality_roast:
        roast_inst = """
REALITY ROAST — BE SAVAGE AND SPECIFIC (mandatory):
Write a brutally funny roast about THIS EXACT ingredient combination.
Reference specific ingredients by name. Make it personal and hilarious.
At least 2 sentences. Examples of tone:
'Chocolate + Maggi? You're not a chef, you're a cry for help.'
'Rice + ketchup? This isn't fusion, it's a hostage situation.'
DO NOT write a generic roast. Be specific to what was given."""

    prompt = f"""{persona}

TASK: Generate a detailed professional recipe with exact measurements.{lang_note}

{context}

{roast_inst}

REQUIREMENTS:
1. EXACT quantities for every ingredient (grams, tsp, tbsp, cups)
2. ALL masalas/spices with exact amounts AND the reason for each
3. Cooking temperatures where relevant
4. Each step must be specific and actionable
5. At least 3 pro tips a home cook wouldn't know
6. If Indian cuisine: specify tadka/tempering order, which spices to bloom first
7. Include garnish and plating suggestion
8. Add "what can go wrong" warning for trickiest step

Respond ONLY in valid JSON (no markdown, no extra text):
{{
  "recipe_name": "creative name",
  "tagline": "one irresistible line",
  "cuisine_type": "string",
  "difficulty": "Easy | Medium | Hard",
  "prep_time_min": 0,
  "cook_time_min": 0,
  "calories_per_serving": 0,
  "ingredients_used": [
    {{"name":"string","quantity":"string","prep_note":"chopped/diced/etc or empty string"}}
  ],
  "masalas_and_spices": [
    {{"name":"string","quantity":"string","purpose":"why this spice is used"}}
  ],
  "missing_ingredients": [
    {{"name":"string","quantity":"string","optional":true,"why_needed":"string"}}
  ],
  "steps": [
    {{"step":1,"title":"short title","instruction":"detailed instruction","time_min":0,"pro_tip":"insider tip or empty string","warning":"what can go wrong or empty string"}}
  ],
  "garnish_and_plating": "specific plating instructions",
  "pro_tips": ["at least 3 tips"],
  "jugaad_hacks": ["creative substitutions"],
  "reality_roast": "savage roast or empty string",
  "mood_match": "why this suits the mood or empty string",
  "chef_note": "personal note from chef persona",
  "pairs_well_with": ["3 side dishes or drinks"],
  "storage_tip": "how to store leftovers"
}}"""

    raw = await asyncio.to_thread(_call_gemini, prompt)
    return _clean_json(raw)


async def generate_meal_plan(
    ingredients: List[str], days: int=7,
    user_type: Optional[str]=None, budget_per_day: Optional[float]=None,
) -> dict:
    ctx = "\n".join(filter(None,[
        f"User type: {user_type}." if user_type else "",
        f"Budget per day: Rs.{budget_per_day}." if budget_per_day else "",
    ]))
    prompt = f"""You are CookWise. Create a varied nutritionally balanced {days}-day meal plan.
Primary ingredients: {', '.join(ingredients)}
{ctx}
Rules: no two consecutive days same cuisine, vary light/hearty meals, include 2 high-protein days.

Respond ONLY in valid JSON:
{{
  "plan":[{{"day":1,"day_theme":"e.g. Light Monday","breakfast":{{"name":"string","time_min":0,"calories":0}},"lunch":{{"name":"string","time_min":0,"calories":0}},"dinner":{{"name":"string","time_min":0,"calories":0}},"snack":{{"name":"string","time_min":0,"calories":0}}}}],
  "shopping_list":[{{"item":"string","quantity":"string","estimated_cost_inr":0,"category":"vegetable|dairy|spice|protein|staple"}}],
  "weekly_nutrition_summary":{{"avg_calories_per_day":0,"protein_level":"Low|Medium|High","variety_score":0,"healthiness_score":0}},
  "meal_prep_tips":["2-3 batch cooking tips"]
}}"""
    raw = await asyncio.to_thread(_call_gemini, prompt)
    return _clean_json(raw)


async def get_surprise_ingredients() -> dict:
    prompt = """You are CookWise. Suggest a fun creative workable Indian or fusion ingredient combination.
Respond ONLY in valid JSON:
{"ingredients":["3-5 ingredient names"],"teaser":"one exciting line","difficulty_hint":"Easy|Medium|Hard"}"""
    raw = await asyncio.to_thread(_call_gemini, prompt)
    return _clean_json(raw)
