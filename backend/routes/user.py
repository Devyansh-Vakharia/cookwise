from fastapi import APIRouter
router = APIRouter()
@router.get("/preferences")
async def get_prefs(): return {"status":"ok"}
