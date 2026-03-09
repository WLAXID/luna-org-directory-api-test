from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.routers import buildings_router, organizations_router, activities_router

app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    description="REST API for organization directory with buildings and activities"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(buildings_router)
app.include_router(organizations_router)
app.include_router(activities_router)


@app.get("/")
def root():
    return {"message": "Organization Directory API", "version": "1.0.0"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)