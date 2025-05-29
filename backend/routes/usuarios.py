from fastapi import APIRouter, HTTPException, UploadFile, File
from typing import List
import uuid
from models import Usuario
from database.db import usuarios_db

router = APIRouter(
    prefix="/usuarios",
    tags=["Usuários"]
)

@router.post("/", response_model=Usuario)
async def criar_usuario(usuario: Usuario):
    usuario_id = str(uuid.uuid4())
    usuario.id = usuario_id
    usuarios_db[usuario_id] = usuario
    return usuario

@router.get("/", response_model=List[Usuario])
async def listar_usuarios():
    return list(usuarios_db.values())

@router.get("/{usuario_id}", response_model=Usuario)
async def obter_usuario(usuario_id: str):
    if usuario_id not in usuarios_db:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return usuarios_db[usuario_id]

@router.put("/{usuario_id}", response_model=Usuario)
async def atualizar_usuario(usuario_id: str, usuario: Usuario):
    if usuario_id not in usuarios_db:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    usuario.id = usuario_id
    usuarios_db[usuario_id] = usuario
    return usuario

@router.post("/{usuario_id}/alterar-foto")
async def alterar_foto(usuario_id: str, imagem: UploadFile = File(...)):
    if usuario_id not in usuarios_db:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    conteudo = await imagem.read()
    usuarios_db[usuario_id].foto = conteudo
    return {"message": "Foto atualizada com sucesso"}
