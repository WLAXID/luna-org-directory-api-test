from .buildings import router as buildings_router
from .organizations import router as organizations_router
from .activities import router as activities_router

__all__ = ["buildings_router", "organizations_router", "activities_router"]