from fastapi import APIRouter

from .chats_routes import router as chats_router
from .documents_routes import router as documents_router
from .llm_config_routes import router as llm_config_router
from .logs_routes import router as logs_router
from .podcasts_routes import router as podcasts_router
from .search_source_connectors_routes import router as search_source_connectors_router
from .search_spaces_routes import router as search_spaces_router

router = APIRouter()

router.include_router(search_spaces_router)
router.include_router(documents_router)
router.include_router(podcasts_router)
router.include_router(chats_router)
router.include_router(search_source_connectors_router)
router.include_router(llm_config_router)
router.include_router(logs_router)
