from fastapi import APIRouter

from app.api.v1.endpoints import (
    contact,
    dashboards,
    experiences,
    health,
    notebooks,
    profile,
    profiles,
    projects,
    technologies,
)

api_router = APIRouter()
api_router.include_router(health.router)
api_router.include_router(profile.router)
api_router.include_router(profiles.router)
api_router.include_router(experiences.router)
api_router.include_router(projects.router)
api_router.include_router(technologies.router)
api_router.include_router(dashboards.router)
api_router.include_router(notebooks.router)
api_router.include_router(contact.router)
