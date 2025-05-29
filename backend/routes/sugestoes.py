from fastapi import APIRouter, Query
from typing import List
from database.db import fornecedores_db

router = APIRouter(
    prefix="/sugestoes",
    tags=["Sugestões"]
)

@router.get("/por-tema/")
async def sugerir_fornecedor_por_tema(temas: List[str] = Query(...)):
    sugestoes = []
    
    for fornecedor_id, fornecedor in fornecedores_db.items():
        for tema in temas:
            if tema in fornecedor.tags:
                sugestoes.append(fornecedor)
                break
    
    return sugestoes

@router.get("/por-tags/")
async def sugerir_fornecedor_por_tags(tags: List[str] = Query(...)):
    sugestoes = []
    
    for fornecedor_id, fornecedor in fornecedores_db.items():
        for tag in tags:
            if tag in fornecedor.tags:
                sugestoes.append(fornecedor)
                break
    
    return sugestoes
