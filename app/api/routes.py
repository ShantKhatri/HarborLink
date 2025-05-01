from fastapi import APIRouter
from .endpoints import api_parser, middleware, transformation, validator, projects

api_router = APIRouter()

api_router.include_router(api_parser.router)
api_router.include_router(middleware.router)
api_router.include_router(transformation.router)
api_router.include_router(validator.router)
api_router.include_router(projects.router)