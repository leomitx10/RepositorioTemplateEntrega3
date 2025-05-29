from fastapi import APIRouter, HTTPException
from typing import List, Optional
import uuid
from pydantic import BaseModel
from database.db import fornecedores_db
from fornecedor_factory import get_fornecedor_factory

router = APIRouter(
    prefix="/fornecedores",
    tags=["Fornecedores"]
)

class FornecedorCreate(BaseModel):
    nome: str
    tipo: str  # "pizzaria", "confeitaria", "churrascaria"
    tags: List[str] = []
    contato: str
    portfolio: Optional[str] = None
    
    class Config:
        schema_extra = {
            "example": {
                "nome": "Pizzaria Delícia",
                "tipo": "pizzaria",
                "tags": ["pizza", "italiana", "forno a lenha"],
                "contato": "contato@pizzariadelicia.com",
                "portfolio": "Especialistas em pizzas estilo napolitano"
            }
        }

@router.post("/")
async def criar_fornecedor(fornecedor_data: FornecedorCreate):
    try:
        factory = get_fornecedor_factory(fornecedor_data.tipo)
        
        fornecedor_obj = factory.create_fornecedor(
            nome=fornecedor_data.nome,
            tags=fornecedor_data.tags,
            contato=fornecedor_data.contato,
            portfolio=fornecedor_data.portfolio
        )
        
        fornecedor_id = str(uuid.uuid4())
        
        fornecedor_dict = {
            "id": fornecedor_id,
            "nome": fornecedor_obj.nome,
            "tags": fornecedor_obj.tags,
            "contato": fornecedor_obj.contato,
            "portfolio": fornecedor_obj.portfolio,
            "tipo": fornecedor_data.tipo,
            "servicos": fornecedor_obj.listar_servicos(),
            "preco_base": fornecedor_obj.calcular_preco()
        }
        
        fornecedores_db[fornecedor_id] = fornecedor_dict
        return fornecedor_dict
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{fornecedor_id}/detalhes")
async def obter_detalhes_fornecedor(fornecedor_id: str):
    if fornecedor_id not in fornecedores_db:
        raise HTTPException(status_code=404, detail="Fornecedor não encontrado")
    
    fornecedor = fornecedores_db[fornecedor_id]
    
    try:
        factory = get_fornecedor_factory(fornecedor["tipo"])
        fornecedor_obj = factory.create_fornecedor(
            nome=fornecedor["nome"],
            tags=fornecedor["tags"],
            contato=fornecedor["contato"],
            portfolio=fornecedor.get("portfolio")
        )
        
        return {
            "id": fornecedor_id,
            "informacoes": fornecedor_obj.exibir_info(),
            "preco_estimado": fornecedor_obj.calcular_preco(),
            "servicos_disponiveis": fornecedor_obj.listar_servicos(),
            "tipo": fornecedor["tipo"]
        }
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
