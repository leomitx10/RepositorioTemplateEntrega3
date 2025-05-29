from fastapi import APIRouter, HTTPException
from models import MensagemNotificacao, TipoNotificacao
from notification import (
    NotificationService, 
    EmailNotificationFactory, 
    WhatsAppNotificationFactory, 
    TelegramNotificationFactory
)

router = APIRouter(
    prefix="/notificacoes",
    tags=["Notificações"]
)

@router.post("/")
async def enviar_notificacao(mensagem_notificacao: MensagemNotificacao):
    # Selecionar a fábrica apropriada com base no tipo de notificação
    factory_map = {
        TipoNotificacao.EMAIL: EmailNotificationFactory(),
        TipoNotificacao.WHATSAPP: WhatsAppNotificationFactory(),
        TipoNotificacao.TELEGRAM: TelegramNotificationFactory()
    }
    
    factory = factory_map.get(mensagem_notificacao.tipo_notificacao)
    if not factory:
        raise HTTPException(status_code=400, detail="Tipo de notificação inválido")
    
    # Criar o serviço de notificação com a fábrica selecionada
    notification_service = NotificationService(factory)
    
    # Enviar a notificação
    notification_service.notify(
        mensagem_notificacao.destinatario,
        mensagem_notificacao.mensagem
    )
    
    return {"message": f"Notificação enviada com sucesso via {mensagem_notificacao.tipo_notificacao}"}
