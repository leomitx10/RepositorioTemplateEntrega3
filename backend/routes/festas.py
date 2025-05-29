from fastapi import APIRouter, HTTPException, Body, Query
from typing import List
import uuid
from datetime import datetime
from models import Festa, Desejo, Convite, TipoNotificacao
from database.db import festas_db, usuarios_db
from notification import (
    NotificationService, 
    EmailNotificationFactory, 
    WhatsAppNotificationFactory, 
    TelegramNotificationFactory
)

router = APIRouter(
    prefix="/festas",
    tags=["Festas"]
)

@router.post("/", response_model=Festa)
async def criar_festa(festa: Festa):
    festa_id = str(uuid.uuid4())
    festa.id = festa_id
    festas_db[festa_id] = festa
    return festa

@router.get("/", response_model=List[Festa])
async def listar_festas():
    return list(festas_db.values())

@router.get("/{festa_id}", response_model=Festa)
async def obter_festa(festa_id: str):
    if festa_id not in festas_db:
        raise HTTPException(status_code=404, detail="Festa não encontrada")
    return festas_db[festa_id]

@router.post("/{festa_id}/adicionar-convidado/{usuario_id}")
async def adicionar_convidado(festa_id: str, usuario_id: str):
    if festa_id not in festas_db:
        raise HTTPException(status_code=404, detail="Festa não encontrada")
    
    if usuario_id not in usuarios_db:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    if usuario_id not in festas_db[festa_id].listaConvidados:
        festas_db[festa_id].listaConvidados.append(usuario_id)
    
    return {"message": "Convidado adicionado com sucesso"}

@router.post("/{festa_id}/adicionar-desejo", response_model=Desejo)
async def adicionar_desejo(festa_id: str, desejo: Desejo):
    if festa_id not in festas_db:
        raise HTTPException(status_code=404, detail="Festa não encontrada")
    
    festas_db[festa_id].desejos.append(desejo)
    return desejo

@router.put("/{festa_id}/marcar-desejo-adquirido")
async def marcar_desejo(festa_id: str, nome_desejo: str = Query(...)):
    if festa_id not in festas_db:
        raise HTTPException(status_code=404, detail="Festa não encontrada")
    
    for desejo in festas_db[festa_id].desejos:
        if desejo.nome == nome_desejo:
            desejo.foiAdquirido = True
            return {"message": f"Desejo '{nome_desejo}' marcado como adquirido"}
    
    raise HTTPException(status_code=404, detail="Desejo não encontrado")

@router.post("/{festa_id}/enviar-convites")
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

@router.post("/{festa_id}/notificar-convidados")
async def notificar_convidados(
    festa_id: str, 
    mensagem: str = Body(..., embed=True),
    tipo_notificacao: TipoNotificacao = Body(TipoNotificacao.EMAIL, embed=True)
):
    if festa_id not in festas_db:
        raise HTTPException(status_code=404, detail="Festa não encontrada")
    
    # Selecionar a fábrica apropriada com base no tipo de notificação
    factory_map = {
        TipoNotificacao.EMAIL: EmailNotificationFactory(),
        TipoNotificacao.WHATSAPP: WhatsAppNotificationFactory(),
        TipoNotificacao.TELEGRAM: TelegramNotificationFactory()
    }
    
    factory = factory_map.get(tipo_notificacao)
    notification_service = NotificationService(factory)
    
    # Enviar notificação para cada convidado
    for usuario_id in festas_db[festa_id].listaConvidados:
        if usuario_id in usuarios_db:
            notification_service.notify(
                usuarios_db[usuario_id].nome,  # Usando o nome como destinatário para simplificar
                mensagem
            )
    
    return {
        "message": f"{len(festas_db[festa_id].listaConvidados)} convidados notificados com sucesso",
        "tipo_notificacao": tipo_notificacao
    }
