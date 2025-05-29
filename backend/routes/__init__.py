from fastapi import APIRouter
from .usuarios import router as usuarios_router
from .festas import router as festas_router
from .fornecedores import router as fornecedores_router
from .sugestoes import router as sugestoes_router
from .midias import router as midias_router
from .notificacoes import router as notificacoes_router

# Create a main router that includes all routers
api_router = APIRouter()
api_router.include_router(usuarios_router)
api_router.include_router(festas_router)
api_router.include_router(fornecedores_router)
api_router.include_router(sugestoes_router)
api_router.include_router(midias_router)
api_router.include_router(notificacoes_router)

__all__ = ['api_router']
