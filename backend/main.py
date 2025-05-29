from fastapi import FastAPI, HTTPException, UploadFile, File, Form, Depends, Body, Query, Path
from fastapi.responses import JSONResponse
from typing import List, Optional
from datetime import datetime, date
import uuid
from models import *

app = FastAPI(
    title="Sistema de Eventos",
    description="API para gerenciamento de festas, convites e sugestões",
    version="1.0.0"
)

usuarios_db = {}
festas_db = {}
fornecedores_db = {}

@app.post("/usuarios/", response_model=Usuario, tags=["Usuários"])
async def criar_usuario(usuario: Usuario):
    usuario_id = str(uuid.uuid4())
    usuario.id = usuario_id
    usuarios_db[usuario_id] = usuario
    return usuario

@app.get("/usuarios/", response_model=List[Usuario], tags=["Usuários"])
async def listar_usuarios():
    return list(usuarios_db.values())

@app.get("/usuarios/{usuario_id}", response_model=Usuario, tags=["Usuários"])
async def obter_usuario(usuario_id: str):
    if usuario_id not in usuarios_db:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return usuarios_db[usuario_id]

@app.put("/usuarios/{usuario_id}", response_model=Usuario, tags=["Usuários"])
async def atualizar_usuario(usuario_id: str, usuario: Usuario):
    if usuario_id not in usuarios_db:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    usuario.id = usuario_id
    usuarios_db[usuario_id] = usuario
    return usuario

@app.post("/usuarios/{usuario_id}/alterar-foto", tags=["Usuários"])
async def alterar_foto(usuario_id: str, imagem: UploadFile = File(...)):
    if usuario_id not in usuarios_db:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    conteudo = await imagem.read()
    usuarios_db[usuario_id].foto = conteudo
    return {"message": "Foto atualizada com sucesso"}

@app.post("/festas/", response_model=Festa, tags=["Festas"])
async def criar_festa(festa: Festa):
    festa_id = str(uuid.uuid4())
    festa.id = festa_id
    festas_db[festa_id] = festa
    return festa

@app.get("/festas/", response_model=List[Festa], tags=["Festas"])
async def listar_festas():
    return list(festas_db.values())

@app.get("/festas/{festa_id}", response_model=Festa, tags=["Festas"])
async def obter_festa(festa_id: str):
    if festa_id not in festas_db:
        raise HTTPException(status_code=404, detail="Festa não encontrada")
    return festas_db[festa_id]

@app.post("/festas/{festa_id}/adicionar-convidado/{usuario_id}", tags=["Festas"])
async def adicionar_convidado(festa_id: str, usuario_id: str):
    if festa_id not in festas_db:
        raise HTTPException(status_code=404, detail="Festa não encontrada")
    
    if usuario_id not in usuarios_db:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    if usuario_id not in festas_db[festa_id].listaConvidados:
        festas_db[festa_id].listaConvidados.append(usuario_id)
    
    return {"message": "Convidado adicionado com sucesso"}

@app.post("/festas/{festa_id}/adicionar-desejo", response_model=Desejo, tags=["Festas"])
async def adicionar_desejo(festa_id: str, desejo: Desejo):
    if festa_id not in festas_db:
        raise HTTPException(status_code=404, detail="Festa não encontrada")
    
    festas_db[festa_id].desejos.append(desejo)
    return desejo

@app.put("/festas/{festa_id}/marcar-desejo-adquirido", tags=["Festas"])
async def marcar_desejo(festa_id: str, nome_desejo: str = Query(...)):
    if festa_id not in festas_db:
        raise HTTPException(status_code=404, detail="Festa não encontrada")
    
    for desejo in festas_db[festa_id].desejos:
        if desejo.nome == nome_desejo:
            desejo.foiAdquirido = True
            return {"message": f"Desejo '{nome_desejo}' marcado como adquirido"}
    
    raise HTTPException(status_code=404, detail="Desejo não encontrado")

@app.post("/festas/{festa_id}/enviar-convites", tags=["Festas"])
async def enviar_convites(festa_id: str):
    if festa_id not in festas_db:
        raise HTTPException(status_code=404, detail="Festa não encontrada")
    
    for usuario_id in festas_db[festa_id].listaConvidados:
        convite = Convite(
            destinatario=usuario_id,
            remetente=festa_id,
            mensagem=f"Você está convidado para a festa!",
            dataEnvio=datetime.now()
        )
        festas_db[festa_id].convites.append(convite)
    
    return {"message": f"{len(festas_db[festa_id].listaConvidados)} convites enviados com sucesso"}

@app.post("/fornecedores/", response_model=Fornecedor, tags=["Fornecedores"])
async def criar_fornecedor(fornecedor: Fornecedor):
    fornecedor_id = str(uuid.uuid4())
    fornecedores_db[fornecedor_id] = fornecedor
    return fornecedor

@app.get("/fornecedores/", response_model=List[Fornecedor], tags=["Fornecedores"])
async def listar_fornecedores():
    return list(fornecedores_db.values())

@app.get("/sugestoes/por-tema/", tags=["Sugestões"])
async def sugerir_fornecedor_por_tema(temas: List[str] = Query(...)):
    sugestoes = []
    
    for fornecedor_id, fornecedor in fornecedores_db.items():
        for tema in temas:
            if tema in fornecedor.tags:
                sugestoes.append(fornecedor)
                break
    
    return sugestoes

@app.get("/sugestoes/por-tags/", tags=["Sugestões"])
async def sugerir_fornecedor_por_tags(tags: List[str] = Query(...)):
    sugestoes = []
    
    for fornecedor_id, fornecedor in fornecedores_db.items():
        for tag in tags:
            if tag in fornecedor.tags:
                sugestoes.append(fornecedor)
                break
    
    return sugestoes

@app.post("/midias/", tags=["Mídias"])
async def adicionar_midia(
    url: str = Form(...),
    tipo: TipoMidia = Form(...),
):
    midia = Midia(url=url, tipo=tipo)
    return midia

@app.delete("/midias/{url}", tags=["Mídias"])
async def remover_midia(url: str):
    return {"message": f"Mídia {url} removida com sucesso"}
