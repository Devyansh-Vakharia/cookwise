from typing import List, Optional, Dict

PRICE_DB: Dict[str, dict] = {
    "rice":     {"price":60, "unit":"kg"},   "atta":   {"price":45,"unit":"kg"},
    "flour":    {"price":35, "unit":"kg"},   "bread":  {"price":40,"unit":"loaf"},
    "oats":     {"price":80, "unit":"500g"}, "pasta":  {"price":55,"unit":"500g"},
    "noodles":  {"price":15, "unit":"packet"},"maggi": {"price":14,"unit":"packet"},
    "milk":     {"price":25, "unit":"500ml"},"butter": {"price":55,"unit":"100g"},
    "cheese":   {"price":90, "unit":"200g"}, "paneer": {"price":80,"unit":"200g"},
    "curd":     {"price":35, "unit":"400g"}, "cream":  {"price":45,"unit":"200ml"},
    "ghee":     {"price":120,"unit":"500ml"},"yogurt": {"price":35,"unit":"400g"},
    "tomato":   {"price":30, "unit":"kg"},   "onion":  {"price":25,"unit":"kg"},
    "potato":   {"price":20, "unit":"kg"},   "garlic": {"price":40,"unit":"100g"},
    "ginger":   {"price":30, "unit":"100g"}, "spinach":{"price":20,"unit":"bunch"},
    "mushroom": {"price":60, "unit":"200g"}, "chili":  {"price":15,"unit":"100g"},
    "capsicum": {"price":40, "unit":"250g"}, "carrot": {"price":30,"unit":"kg"},
    "peas":     {"price":40, "unit":"250g"}, "corn":   {"price":20,"unit":"piece"},
    "egg":      {"price":7,  "unit":"piece"},"chicken":{"price":180,"unit":"500g"},
    "dal":      {"price":90, "unit":"500g"}, "chana":  {"price":80,"unit":"500g"},
    "rajma":    {"price":90, "unit":"500g"}, "moong":  {"price":80,"unit":"500g"},
    "tofu":     {"price":80, "unit":"200g"}, "mutton": {"price":350,"unit":"500g"},
    "fish":     {"price":200,"unit":"500g"},
    "salt":     {"price":20, "unit":"kg"},   "sugar":  {"price":45,"unit":"kg"},
    "oil":      {"price":130,"unit":"litre"},"honey":  {"price":180,"unit":"250g"},
    "soy sauce":{"price":70, "unit":"200ml"},"ketchup":{"price":90,"unit":"500g"},
    "chocolate":{"price":50, "unit":"50g"},  "coffee": {"price":140,"unit":"100g"},
    "besan":    {"price":60, "unit":"500g"}, "suji":   {"price":30,"unit":"500g"},
    "tamarind": {"price":30, "unit":"100g"}, "jaggery":{"price":50,"unit":"250g"},
    "banana":   {"price":30, "unit":"dozen"},"lemon":  {"price":5, "unit":"piece"},
    "mango":    {"price":60, "unit":"kg"},   "coconut":{"price":30,"unit":"piece"},
}

ALTERNATIVES: Dict[str, dict] = {
    "butter":    {"name":"oil",           "price":10, "savings_pct":82,"note":"Use ½ tsp oil per 1 tsp butter"},
    "cream":     {"name":"milk + butter", "price":8,  "savings_pct":80,"note":"¾ cup milk + 3 tbsp butter"},
    "paneer":    {"name":"tofu",          "price":60, "savings_pct":25,"note":"Silken tofu works well"},
    "chicken":   {"name":"egg",           "price":14, "savings_pct":85,"note":"2 eggs replace 100g chicken"},
    "chocolate": {"name":"cocoa + sugar", "price":15, "savings_pct":70,"note":"1 tbsp cocoa + 1 tsp sugar"},
    "cheese":    {"name":"paneer",        "price":60, "savings_pct":33,"note":"Grated paneer works in most recipes"},
    "mushroom":  {"name":"soya chunks",   "price":20, "savings_pct":67,"note":"Soaked soya for similar texture"},
    "honey":     {"name":"jaggery",       "price":15, "savings_pct":90,"note":"Equal quantity jaggery syrup"},
    "soy sauce": {"name":"salt + vinegar","price":5,  "savings_pct":93,"note":"½ tsp salt + few drops vinegar"},
    "cream":     {"name":"curd",          "price":10, "savings_pct":78,"note":"Hung curd for similar richness"},
}

def _get_cost(ingredient: str):
    ingredient = ingredient.lower().strip()
    for key, data in PRICE_DB.items():
        if key in ingredient or ingredient in key:
            return {**data, "name": key}
    return None

def analyze_budget(missing_ingredients: List[dict], budget: Optional[float]) -> dict:
    if not missing_ingredients:
        return {"total_estimated_cost":0,"within_budget":True,"budget_status":"no_missing","verdict":"✅ No missing ingredients needed!","items":[],"savings_tips":[]}
    items=[]; total=0; total_alt=0; tips=[]
    for item in missing_ingredients:
        name    = item.get("name","") if isinstance(item,dict) else str(item)
        optional= item.get("optional",False) if isinstance(item,dict) else False
        pd      = _get_cost(name)
        cost    = pd["price"] if pd else 50
        alt     = ALTERNATIVES.get(name.lower())
        alt_cost= alt["price"] if alt else cost
        within  = True if not budget else (total+cost)<=budget
        items.append({"name":name,"estimated_cost_inr":cost,"unit":pd["unit"] if pd else "unit","optional":optional,"within_budget":within,"alternative":alt})
        if not optional:
            total+=cost; total_alt+=alt_cost
        if alt and (cost-alt_cost)>5:
            tips.append(f"💡 Replace {name} with {alt['name']} — save ₹{cost-alt_cost:.0f} ({alt['savings_pct']}% cheaper). {alt['note']}")
    if budget:
        if   total<=budget:         verdict=f"✅ Within budget! Total ≈ ₹{total:.0f} / ₹{budget:.0f}"; status="within"
        elif total_alt<=budget:     verdict=f"✅ With alternatives fits ₹{budget:.0f}! (₹{total_alt:.0f})"; status="fits_with_alternatives"
        else:                       verdict=f"⚠️ Over budget by ₹{total-budget:.0f}. Try alternatives."; status="over_budget"
    else:
        verdict=f"ℹ️ Estimated shopping cost: ₹{total:.0f}"; status="no_budget_set"
    return {"total_estimated_cost":round(total),"total_with_alternatives":round(total_alt),"within_budget":budget is None or total<=budget,"budget_status":status,"verdict":verdict,"items":items,"savings_tips":tips[:3]}
