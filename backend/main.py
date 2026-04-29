import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from routes import recipe, meal_planner, health, user
import uvicorn

app = FastAPI(title="CookWise API", version="2.0.0", docs_url="/api/docs")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
app.include_router(recipe.router,       prefix="/api/recipe",       tags=["Recipe"])
app.include_router(meal_planner.router, prefix="/api/meal-planner", tags=["Meal Planner"])
app.include_router(health.router,       prefix="/api/health",       tags=["Health"])
app.include_router(user.router,         prefix="/api/user",         tags=["User"])

BASE     = os.path.dirname(os.path.abspath(__file__))
FRONT    = os.path.join(BASE, "..", "frontend")
STATIC   = os.path.join(FRONT, "static")
if os.path.isdir(STATIC):
    app.mount("/static", StaticFiles(directory=STATIC), name="static")

@app.get("/", include_in_schema=False)
async def landing(): return FileResponse(os.path.join(FRONT,"index.html"))
@app.get("/app", include_in_schema=False)
async def main_app(): return FileResponse(os.path.join(FRONT,"app.html"))
@app.get("/api/ping")
async def ping(): return {"status":"ok","message":"CookWise 2.0 running 🍳"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
