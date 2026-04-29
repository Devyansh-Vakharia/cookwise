from fastapi import APIRouter, HTTPException
from models.user_input import MealPlanRequest
from services import ai_service

router = APIRouter()

@router.post("/generate")
async def generate_meal_plan(request: MealPlanRequest):
    try:
        plan = await ai_service.generate_meal_plan(
            ingredients=[i.name for i in request.ingredients],
            days=request.days,
            user_type=request.user_type.value if request.user_type else None,
            budget_per_day=request.budget_per_day
        )
        return {"status":"success","meal_plan":plan}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
