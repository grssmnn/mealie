from pathlib import Path
import os

import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

import startup
from routes import (
    backup_routes,
    meal_routes,
    migration_routes,
    recipe_routes,
    setting_routes,
    static_routes,
    user_routes,
)
from routes.setting_routes import scheduler
from settings import PORT
from utils.logger import logger

CWD = Path(__file__).parent
WEB_PATH = CWD.joinpath("dist")

app = FastAPI()


# Mount Vue Frontend only in production
env = os.environ.get("ENV")
if(env == "prod"):
    app.mount("/static", StaticFiles(directory=WEB_PATH, html=True))

# API Routes
app.include_router(recipe_routes.router)
app.include_router(meal_routes.router)
app.include_router(setting_routes.router)
app.include_router(backup_routes.router)
app.include_router(user_routes.router)
app.include_router(migration_routes.router)

# API 404 Catch all CALL AFTER ROUTERS
@app.get("/api/{full_path:path}", status_code=404, include_in_schema=False)
def invalid_api():
    return None


app.include_router(static_routes.router)

startup.ensure_dirs()
startup.generate_default_theme()


if __name__ == "__main__":
    logger.info("-----SYSTEM STARTUP-----")

    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=PORT,
        reload=True,
        debug=True,
        workers=1,
        forwarded_allow_ips="*",
    )
