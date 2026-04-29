from fastapi import APIRouter
router = APIRouter()
@router.get("/tips")
async def health_tips():
    return {"tips":["Eat 5 portions of fruit/veg daily","Limit processed food to 3 meals/week","Stay hydrated — 8 glasses daily"]}
