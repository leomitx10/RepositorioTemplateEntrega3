from fastapi import APIRouter, Form
from models import Midia, TipoMidia

router = APIRouter(
    prefix="/midias",
    tags=["Mídias"]
)

@router.post("/")
async def adicionar_midia(
    url: str = Form(...),
    tipo: TipoMidia = Form(...),
):
    midia = Midia(url=url, tipo=tipo)
    return midia

@router.delete("/{url}")
async def remover_midia(url: str):
    return {"message": f"Mídia {url} removida com sucesso"}
