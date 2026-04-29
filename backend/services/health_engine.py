"""
CookWise Health Engine v2 — extended Indian ingredient database, realistic scoring
"""
from typing import List, Dict

NUTRITION_DB: Dict[str, dict] = {
    # Staples
    "rice":         {"cal":130,"protein":2.7,"carbs":28, "fat":0.3,"fiber":0.4,"sodium":1},
    "atta":         {"cal":340,"protein":12,  "carbs":70, "fat":2,  "fiber":3.5,"sodium":2},
    "flour":        {"cal":364,"protein":10,  "carbs":76, "fat":1,  "fiber":2.7,"sodium":2},
    "bread":        {"cal":265,"protein":9,   "carbs":49, "fat":3,  "fiber":2.7,"sodium":491},
    "roti":         {"cal":297,"protein":9,   "carbs":61, "fat":2,  "fiber":3,  "sodium":2},
    "poha":         {"cal":333,"protein":6,   "carbs":76, "fat":1,  "fiber":1.5,"sodium":5},
    "oats":         {"cal":389,"protein":17,  "carbs":66, "fat":7,  "fiber":11, "sodium":2},
    "pasta":        {"cal":158,"protein":6,   "carbs":31, "fat":1,  "fiber":2,  "sodium":6},
    "noodles":      {"cal":380,"protein":8,   "carbs":58, "fat":14, "fiber":2,  "sodium":900},
    "maggi":        {"cal":380,"protein":8,   "carbs":58, "fat":14, "fiber":2,  "sodium":900},
    "suji":         {"cal":360,"protein":13,  "carbs":72, "fat":1,  "fiber":3.9,"sodium":1},
    "besan":        {"cal":387,"protein":22,  "carbs":58, "fat":6,  "fiber":10, "sodium":64},
    "cornflour":    {"cal":381,"protein":0.3, "carbs":91, "fat":0.6,"fiber":0.9,"sodium":9},
    "potato":       {"cal":77, "protein":2,   "carbs":17, "fat":0.1,"fiber":2.2,"sodium":6},
    "sweet potato": {"cal":86, "protein":1.6, "carbs":20, "fat":0.1,"fiber":3,  "sodium":55},
    # Dairy
    "milk":         {"cal":61, "protein":3.2, "carbs":4.8,"fat":3.3,"fiber":0,  "sodium":44},
    "butter":       {"cal":717,"protein":0.9, "carbs":0.1,"fat":81, "fiber":0,  "sodium":643},
    "cheese":       {"cal":403,"protein":25,  "carbs":1.3,"fat":33, "fiber":0,  "sodium":600},
    "paneer":       {"cal":265,"protein":18,  "carbs":1.2,"fat":21, "fiber":0,  "sodium":50},
    "curd":         {"cal":61, "protein":3.5, "carbs":4.7,"fat":3.3,"fiber":0,  "sodium":46},
    "yogurt":       {"cal":61, "protein":3.5, "carbs":4.7,"fat":3.3,"fiber":0,  "sodium":46},
    "ghee":         {"cal":900,"protein":0,   "carbs":0,  "fat":100,"fiber":0,  "sodium":1},
    "cream":        {"cal":340,"protein":2.8, "carbs":2.8,"fat":36, "fiber":0,  "sodium":38},
    # Protein
    "egg":          {"cal":155,"protein":13,  "carbs":1.1,"fat":11, "fiber":0,  "sodium":124},
    "chicken":      {"cal":165,"protein":31,  "carbs":0,  "fat":3.6,"fiber":0,  "sodium":74},
    "mutton":       {"cal":294,"protein":25,  "carbs":0,  "fat":21, "fiber":0,  "sodium":72},
    "fish":         {"cal":136,"protein":20,  "carbs":0,  "fat":6,  "fiber":0,  "sodium":60},
    "dal":          {"cal":116,"protein":9,   "carbs":20, "fat":0.4,"fiber":8,  "sodium":2},
    "chana":        {"cal":164,"protein":9,   "carbs":27, "fat":2.6,"fiber":8,  "sodium":24},
    "rajma":        {"cal":127,"protein":8,   "carbs":22, "fat":0.5,"fiber":6,  "sodium":2},
    "tofu":         {"cal":76, "protein":8,   "carbs":1.9,"fat":4.8,"fiber":0.3,"sodium":7},
    "soya":         {"cal":173,"protein":17,  "carbs":9,  "fat":9,  "fiber":4,  "sodium":15},
    "moong":        {"cal":105,"protein":7,   "carbs":19, "fat":0.4,"fiber":7.6,"sodium":15},
    # Vegetables
    "tomato":       {"cal":18, "protein":0.9, "carbs":3.9,"fat":0.2,"fiber":1.2,"sodium":5},
    "onion":        {"cal":40, "protein":1.1, "carbs":9.3,"fat":0.1,"fiber":1.7,"sodium":4},
    "garlic":       {"cal":149,"protein":6.4, "carbs":33, "fat":0.5,"fiber":2.1,"sodium":17},
    "ginger":       {"cal":80, "protein":1.8, "carbs":18, "fat":0.8,"fiber":2,  "sodium":13},
    "spinach":      {"cal":23, "protein":2.9, "carbs":3.6,"fat":0.4,"fiber":2.2,"sodium":79},
    "carrot":       {"cal":41, "protein":0.9, "carbs":10, "fat":0.2,"fiber":2.8,"sodium":69},
    "capsicum":     {"cal":31, "protein":1,   "carbs":6,  "fat":0.3,"fiber":2.1,"sodium":4},
    "mushroom":     {"cal":22, "protein":3.1, "carbs":3.3,"fat":0.3,"fiber":1,  "sodium":5},
    "cauliflower":  {"cal":25, "protein":1.9, "carbs":5,  "fat":0.3,"fiber":2,  "sodium":30},
    "peas":         {"cal":81, "protein":5.4, "carbs":14, "fat":0.4,"fiber":5.7,"sodium":5},
    "corn":         {"cal":86, "protein":3.3, "carbs":19, "fat":1.4,"fiber":2.7,"sodium":15},
    "chili":        {"cal":40, "protein":2,   "carbs":9,  "fat":0.4,"fiber":1.5,"sodium":7},
    "brinjal":      {"cal":25, "protein":1,   "carbs":6,  "fat":0.2,"fiber":3,  "sodium":2},
    "cabbage":      {"cal":25, "protein":1.3, "carbs":6,  "fat":0.1,"fiber":2.5,"sodium":18},
    # Fruits
    "banana":       {"cal":89, "protein":1.1, "carbs":23, "fat":0.3,"fiber":2.6,"sodium":1},
    "apple":        {"cal":52, "protein":0.3, "carbs":14, "fat":0.2,"fiber":2.4,"sodium":1},
    "mango":        {"cal":60, "protein":0.8, "carbs":15, "fat":0.4,"fiber":1.6,"sodium":1},
    "lemon":        {"cal":29, "protein":1.1, "carbs":9,  "fat":0.3,"fiber":2.8,"sodium":2},
    "coconut":      {"cal":354,"protein":3.3, "carbs":15, "fat":33, "fiber":9,  "sodium":20},
    # Condiments / spices
    "sugar":        {"cal":387,"protein":0,   "carbs":100,"fat":0,  "fiber":0,  "sodium":1},
    "salt":         {"cal":0,  "protein":0,   "carbs":0,  "fat":0,  "fiber":0,  "sodium":38758},
    "oil":          {"cal":884,"protein":0,   "carbs":0,  "fat":100,"fiber":0,  "sodium":0},
    "chocolate":    {"cal":546,"protein":5,   "carbs":60, "fat":31, "fiber":7,  "sodium":24},
    "honey":        {"cal":304,"protein":0.3, "carbs":82, "fat":0,  "fiber":0.2,"sodium":4},
    "ketchup":      {"cal":101,"protein":1.7, "carbs":24, "fat":0.4,"fiber":0.7,"sodium":907},
    "soy sauce":    {"cal":53, "protein":8,   "carbs":5,  "fat":0.1,"fiber":0.8,"sodium":5493},
    "tamarind":     {"cal":239,"protein":2.8, "carbs":63, "fat":0.6,"fiber":5.1,"sodium":28},
    "jaggery":      {"cal":383,"protein":0.4, "carbs":98, "fat":0.1,"fiber":0,  "sodium":19},
    "turmeric":     {"cal":354,"protein":8,   "carbs":65, "fat":10, "fiber":21, "sodium":38},
    "cumin":        {"cal":375,"protein":18,  "carbs":44, "fat":22, "fiber":11, "sodium":168},
    "coriander":    {"cal":23, "protein":2.1, "carbs":3.7,"fat":0.5,"fiber":2.8,"sodium":46},
    "mustard":      {"cal":508,"protein":26,  "carbs":28, "fat":36, "fiber":12, "sodium":1104},
    "butter milk":  {"cal":40, "protein":3.3, "carbs":4.8,"fat":0.9,"fiber":0,  "sodium":105},
}

PROCESSED  = {"maggi","noodles","pasta","bread","ketchup","soy sauce","cheese","butter","chips"}
HIGH_SODIUM= {"maggi","noodles","soy sauce","cheese","butter","ketchup","pickle","salt"}
HIGH_SUGAR = {"sugar","chocolate","honey","jaggery","ketchup","cola","condensed milk"}
HIGH_FAT   = {"butter","ghee","oil","cheese","cream","chocolate","coconut"}
SUPERFOODS = {"spinach","dal","chana","rajma","oats","turmeric","garlic","ginger","carrot","moong","besan"}


def analyze_health(ingredients: List[str], servings: int = 2) -> dict:
    total = {"cal":0,"protein":0,"carbs":0,"fat":0,"fiber":0,"sodium":0}
    matched = 0
    ing_lower = [i.lower().strip() for i in ingredients]

    for ing in ing_lower:
        for key, data in NUTRITION_DB.items():
            if key in ing or ing in key:
                for k in total:
                    total[k] += data[k]
                matched += 1
                break

    # Realistic per-serving calc: assume ~150g portion per matched ingredient per serving
    srv = max(servings, 1)
    divisor = max(matched, 1) * srv

    per_serving = {
        "cal":     min(round(total["cal"]     / divisor * 1.5), 1500),
        "protein": min(round(total["protein"] / divisor * 1.5), 80),
        "carbs":   min(round(total["carbs"]   / divisor * 1.5), 200),
        "fat":     min(round(total["fat"]     / divisor * 1.5), 100),
        "fiber":   min(round(total["fiber"]   / divisor * 1.5), 30),
        "sodium":  min(round(total["sodium"]  / divisor * 1.5), 5000),
    }

    if matched == 0:
        per_serving = {"cal":250,"protein":8,"carbs":35,"fat":8,"fiber":3,"sodium":300}

    # Warnings
    warnings, positives = [], []
    proc_n  = sum(1 for i in ing_lower if any(p in i for p in PROCESSED))
    sodium_n= sum(1 for i in ing_lower if any(p in i for p in HIGH_SODIUM) and "salt" not in ing_lower)
    sugar_n = sum(1 for i in ing_lower if any(p in i for p in HIGH_SUGAR))
    fat_n   = sum(1 for i in ing_lower if any(p in i for p in HIGH_FAT))
    super_n = sum(1 for i in ing_lower if any(p in i for p in SUPERFOODS))

    if proc_n  >= 2: warnings.append({"type":"processed","message":"⚠️ Multiple processed foods — avoid daily consumption."})
    if sodium_n >= 1: warnings.append({"type":"sodium","message":"🧂 Elevated sodium — watch salt intake if consuming regularly."})
    if sugar_n >= 1: warnings.append({"type":"sugar","message":"🍬 High sugar content — limit frequency, especially for diabetics."})
    if fat_n   >= 2: warnings.append({"type":"fat","message":"🧈 High fat content — great for energy, eat in moderation."})

    if super_n >= 1: positives.append("🥦 Contains nutrient-dense ingredients — excellent choice!")
    if per_serving["protein"] >= 12: positives.append("💪 Good protein source — supports muscle recovery.")
    if per_serving["fiber"]   >= 4:  positives.append("🌾 High dietary fiber — excellent for digestion.")
    if not warnings:                 positives.append("✅ Clean ingredient profile — well balanced meal.")

    # Calorie label
    c = per_serving["cal"]
    if   c < 200: lbl, em = "Low Calorie",       "🟢"
    elif c < 450: lbl, em = "Moderate Calorie",  "🟡"
    elif c < 700: lbl, em = "High Calorie",       "🟠"
    else:         lbl, em = "Very High Calorie",  "🔴"

    # Health score
    score = 72
    score -= proc_n   * 8
    score -= sodium_n * 5
    score -= sugar_n  * 8
    score -= fat_n    * 4
    score += super_n  * 7
    score += min(per_serving["fiber"],   10)
    score += min(per_serving["protein"], 20) // 4
    score  = max(20, min(100, score))

    return {
        "per_serving": per_serving,
        "calorie_label": lbl,
        "calorie_emoji": em,
        "health_score": score,
        "warnings": warnings,
        "positives": positives,
        "matched_ingredients": matched,
        "summary": f"{em} {lbl} — {per_serving['cal']} kcal/serving"
    }
