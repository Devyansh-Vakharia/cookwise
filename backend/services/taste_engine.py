from typing import List, Tuple

FLAVOR_MAP = {
    "sugar":"sweet","honey":"sweet","jaggery":"sweet","chocolate":"sweet",
    "banana":"sweet","mango":"sweet","condensed milk":"sweet","nutella":"sweet",
    "salt":"salty","soy sauce":"salty","maggi masala":"salty","pickle":"salty",
    "maggi":"umami","cheese":"umami","mushroom":"umami","tomato paste":"umami","soya sauce":"umami",
    "lemon":"sour","lime":"sour","vinegar":"sour","tamarind":"sour","curd":"sour","yogurt":"sour","tomato":"sour",
    "coffee":"bitter","dark chocolate":"bitter","bitter gourd":"bitter","green tea":"bitter","turmeric":"bitter",
    "chili":"spicy","pepper":"spicy","ginger":"spicy","wasabi":"spicy","hot sauce":"spicy","mustard":"spicy",
    "butter":"creamy","cream":"creamy","milk":"creamy","coconut milk":"creamy","paneer":"creamy","ghee":"creamy","avocado":"creamy",
    "oil":"fat","coconut":"fat",
    "rice":"starchy","pasta":"starchy","bread":"starchy","noodles":"starchy","potato":"starchy","flour":"starchy","oats":"starchy","atta":"starchy","roti":"starchy","poha":"starchy","suji":"starchy",
    "egg":"protein","chicken":"protein","paneer":"protein","dal":"protein","beans":"protein","tofu":"protein","fish":"protein","mutton":"protein","chana":"protein","rajma":"protein","moong":"protein",
}

RULES: List[Tuple[str,str,int,str]] = [
    ("sweet","salty",  +15,"Classic sweet-salty balance works beautifully"),
    ("sour","spicy",   +12,"Tangy heat is a crowd favourite"),
    ("umami","creamy", +18,"Umami richness + cream = restaurant quality"),
    ("starchy","creamy",+15,"Carb + fat is comfort food gold"),
    ("sweet","bitter", +10,"Contrast creates sophisticated depth"),
    ("protein","starchy",+12,"Complete meal macros — great combo"),
    ("spicy","creamy", +14,"Spice cooled by cream — Indian classic"),
    ("sour","creamy",  +10,"Balanced tang — works in most cuisines"),
    ("starchy","starchy",-5,"Two starches can feel heavy"),
    ("bitter","sour",   -3,"Bitter + sour can overwhelm"),
    ("fat","creamy",    -5,"Double fat may taste greasy"),
    ("sweet","spicy",  -10,"Sweet + heat is experimental — polarising"),
    ("sweet","umami",  -20,"Sweet + savoury mismatch — risky"),
    ("bitter","spicy", -15,"Double harsh notes — challenging palate"),
    ("bitter","bitter",-25,"Too much bitterness — very risky"),
]

RISKY_PAIRS = {
    frozenset(["chocolate","maggi"]): ("Chocolate Maggi is genuinely experimental 😬",-30),
    frozenset(["milk","fish"]):       ("Milk + fish causes digestive issues ⚠️",    -35),
    frozenset(["cola","milk"]):       ("Curdles badly — avoid 🥛❌🥤",              -35),
}

REGRET_MSGS = {
    (80,101):("🌟 No regrets here!",    "This is a solid, delicious combination."),
    (60, 80):("😊 You'll enjoy this!",  "Slightly unusual but generally tasty."),
    (40, 60):("🤔 Risky territory…",    "This might work but no guarantees."),
    (20, 40):("😅 You may regret this.","Bold choice. Very experimental."),
    (0,  20):("😱 High regret probability!","This is culinary chaos. Proceed with caution."),
}

def _flavor(ing):
    ing = ing.lower().strip()
    for k,v in FLAVOR_MAP.items():
        if k in ing or ing in k: return v
    return "neutral"

def calculate_taste_score(ingredients: List[str]) -> dict:
    if not ingredients:
        return {"score":50,"label":"Unknown","emoji":"🤷","reasons":[],"warnings":[],"breakdown":{"delicious_pct":50,"experimental_pct":30,"risky_pct":20},"regret_predictor":{"title":"","description":""},"flavor_profiles":[]}
    score = 65; reasons = []; warnings = []
    ing_set = {i.lower() for i in ingredients}
    for pair,(msg,mod) in RISKY_PAIRS.items():
        if pair.issubset(ing_set): score+=mod; warnings.append(msg)
    profiles = [_flavor(i) for i in ingredients]
    profile_set = set(profiles)
    applied = set()
    for i,p1 in enumerate(profiles):
        for j,p2 in enumerate(profiles):
            if i>=j: continue
            pk=frozenset([p1,p2])
            if pk in applied: continue
            applied.add(pk)
            for fa,fb,mod,reason in RULES:
                if {fa,fb}=={p1,p2}:
                    score+=mod
                    reasons.append(("✅ " if mod>0 else "⚠️ ")+reason)
    unique = len(profile_set-{"neutral"})
    if unique>=3: score+=8; reasons.append("✅ Great flavour variety across ingredients")
    elif unique<=1: score-=5; reasons.append("⚠️ Limited flavour diversity")
    score=max(0,min(100,score))
    if   score>=75: lbl,em="Delicious","🌟"
    elif score>=55: lbl,em="Good","😋"
    elif score>=40: lbl,em="Experimental","🧪"
    elif score>=25: lbl,em="Risky","⚠️"
    else:           lbl,em="Avoid","🚫"
    rt,rd="",""
    for (lo,hi),(t,d) in REGRET_MSGS.items():
        if lo<=score<hi: rt,rd=t,d; break
    return {
        "score":round(score),"label":lbl,"emoji":em,
        "breakdown":{"delicious_pct":min(100,max(0,score)),"experimental_pct":max(0,min(40,100-score-10)) if score<70 else 10,"risky_pct":max(0,min(30,100-score)) if score<50 else 5},
        "reasons":reasons[:5],"warnings":warnings,
        "regret_predictor":{"title":rt,"description":rd},
        "flavor_profiles":list(profile_set-{"neutral"})
    }
