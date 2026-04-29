import traceback
from fastapi import APIRouter, HTTPException, Body, Query
from typing import List, Optional
from models.user_input import RecipeRequest, HealthAnalysisRequest
from services import ai_service, taste_engine, budget_engine, health_engine
from datetime import datetime, timezone

router = APIRouter()

@router.post("/generate")
async def generate_recipe(
    request: RecipeRequest,
    chef_persona: Optional[str] = Query(None),
    language: Optional[str] = Query(None),
):
    names = [i.name for i in request.ingredients]
    expiry = [i.name for i in request.ingredients if i.expiry_days is not None and i.expiry_days <= 2]
    try:
        recipe = await ai_service.generate_recipe(
            ingredients=names,
            mood=request.mood.value if request.mood else None,
            user_type=request.user_type.value if request.user_type else None,
            jugaad_mode=request.jugaad_mode,
            reality_roast=request.reality_roast,
            servings=request.servings,
            dietary_restrictions=request.dietary_restrictions,
            expiry_priority=expiry or None,
            chef_persona=chef_persona,
            cuisine_preference=request.cuisine_preference,
            language=language,
        )
        taste  = taste_engine.calculate_taste_score(names)
        budget = budget_engine.analyze_budget(recipe.get("missing_ingredients",[]), request.budget)
        health = health_engine.analyze_health(names, request.servings)
        cw_score = round(taste["score"]*0.40 + health["health_score"]*0.35 + (100 if budget["within_budget"] else 50)*0.25)
        return {
            "status":"success",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "recipe": recipe, "taste_score": taste, "budget": budget, "health": health,
            "cookwise_score": cw_score,
            "expiry_note": {"ingredients":expiry,"message":f"Used {', '.join(expiry)} first — expiring soon!"} if expiry else None,
            "metadata": {"servings":request.servings,"mood":request.mood.value if request.mood else None,"user_type":request.user_type.value if request.user_type else None,"jugaad_mode":request.jugaad_mode,"reality_roast_enabled":request.reality_roast,"chef_persona":chef_persona,"language":language}
        }
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Recipe generation failed: {str(e)}")

@router.post("/taste-check")
async def taste_check(ingredients: List[str] = Body(...)):
    if not ingredients: raise HTTPException(status_code=400, detail="Provide ingredients")
    return {"status":"success","taste_score":taste_engine.calculate_taste_score(ingredients)}

@router.post("/health-check")
async def health_check_route(request: HealthAnalysisRequest):
    return {"status":"success","health":health_engine.analyze_health(request.ingredients, request.servings)}

@router.get("/surprise")
async def surprise_me():
    try: return {"status":"success",**(await ai_service.get_surprise_ingredients())}
    except Exception as e: raise HTTPException(status_code=500, detail=str(e))

@router.get("/recent")
async def get_recent(): return {"status":"ok","recipes":[]}

@router.get("/test-ai")
async def test_ai():
    try:
        r = await ai_service.generate_recipe(ingredients=["rice","egg"], servings=1)
        return {"status":"ok","recipe_name":r.get("recipe_name")}
    except Exception as e:
        traceback.print_exc(); raise HTTPException(status_code=500, detail=str(e))
