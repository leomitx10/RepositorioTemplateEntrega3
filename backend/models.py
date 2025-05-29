from typing import List, Optional, Union
from enum import Enum
from pydantic import BaseModel, Field
from datetime import datetime, date

class TipoMidia(str, Enum):
    IMAGEM = "IMAGEM"
    VIDEO = "VIDEO"

class Perfil(BaseModel):
    avatar: Optional[bytes] = None
    capa: Optional[bytes] = None
    sobre: Optional[str] = None

class Midia(BaseModel):
    url: str
    tipo: TipoMidia
    dataUpload: datetime = Field(default_factory=datetime.now)

class Desejo(BaseModel):
    nome: str
    hyperlink: str
    foiAdquirido: bool = False

class Endereco(BaseModel):
    logradouro: str
    numero: str
    bairro: str
    cidade: str
    estado: str
    cep: str

class Opcao(BaseModel):
    texto: str
    correta: Optional[bool] = False

class Pergunta(BaseModel):
    texto: str
    opcoes: List[Opcao]

class Quiz(BaseModel):
    titulo: str
    numPerguntas: int
    respostaQuiz: Optional[datetime] = None
    tipo: str
    perguntas: List[Pergunta] = []

class Fornecedor(BaseModel):
    nome: str
    tags: List[str] = []
    contato: str
    portfolio: Optional[str] = None
    
    class Config:
        schema_extra = {
            "example": {
                "nome": "Fornecedor Exemplo",
                "tags": ["comida", "bebida"],
                "contato": "contato@fornecedor.com",
                "portfolio": "Diversos serviços de alimentação"
            }
        }

class Portfolio(BaseModel):
    contatos: str
    descricao: str

class Convite(BaseModel):
    destinatario_id: str = Field(..., alias="destinatario")
    remetente_id: str = Field(..., alias="remetente")
    imagens: Optional[bytes] = None
    video: Optional[bytes] = None
    mensagem: Optional[str] = None
    dataEnvio: datetime = Field(default_factory=datetime.now)
    status: str = "PENDENTE"

class Usuario(BaseModel):
    id: Optional[str] = None
    nome: str
    dataNascimento: date
    foto: Optional[bytes] = None
    sobreMim: Optional[str] = None
    tagsDePreferencias: List[str] = []
    perfil: Optional[Perfil] = None
    endereco: Optional[Endereco] = None
    quizzes: List[Quiz] = []
    
    class Config:
        schema_extra = {
            "example": {
                "nome": "João Silva",
                "dataNascimento": "1990-01-01",
                "sobreMim": "Gosto de festas e eventos",
                "tagsDePreferencias": ["música", "gastronomia"]
            }
        }

class Festa(BaseModel):
    id: Optional[str] = None
    listaConvidados: List[str] = []
    dataEvento: date
    temas: List[str] = []
    desejos: List[Desejo] = []
    convites: List[Convite] = []
    
    class Config:
        schema_extra = {
            "example": {
                "dataEvento": "2023-12-31",
                "temas": ["Ano Novo", "Festa"]
            }
        }

class TipoNotificacao(str, Enum):
    EMAIL = "EMAIL"
    WHATSAPP = "WHATSAPP"
    TELEGRAM = "TELEGRAM"

class MensagemNotificacao(BaseModel):
    destinatario: str
    mensagem: str
    tipo_notificacao: TipoNotificacao = TipoNotificacao.EMAIL

class SistemaDeSugestao(BaseModel):
    pass
