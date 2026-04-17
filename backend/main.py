import os
import certifi
from typing import List, Optional
from datetime import datetime
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from pydantic import BaseModel
from bson import ObjectId
from app_backend import LocusAuraAuth, PropertyManager

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")

app = FastAPI(title="Locus Aura - Ecossistema Imobiliário Oficial")

# Conexão e Atalhos
client = MongoClient(MONGO_URI, tlsCAFile=certifi.where())
db = client["locus_aura_db"]

# Inicialização dos Serviços Base
auth_service = LocusAuraAuth(client)
property_service = PropertyManager(client)

# --- 1. MODELOS DE DADOS ---

class LoginData(BaseModel):
    email: str
    password: str

class UserSignup(BaseModel):
    nome: str
    email: str
    password: str
    role: str
    creci: Optional[str] = None
    is_active: bool = False

class VerifyCode(BaseModel):
    email: str
    code: str

class LeadData(BaseModel):
    nome: str
    telefone: str
    email: str
    mensagem: Optional[str] = "Interesse via site"
    imovel_id: Optional[str] = None
    corretor_id: str
    status: str = "Novo"
    origem: str = "Site"

class ImovelData(BaseModel):
    titulo: str
    descricao: str
    localizacao: str
    preco: float
    condominio: Optional[float] = 0.0
    finalidade: str
    tipo_imovel: str
    tamanho_m2: float
    quartos: int
    suites: int
    banheiros: int
    vagas: int
    salas: int
    cozinhas: int
    varandas: int
    andares: Optional[int] = 1
    area_lazer: bool = False
    aceita_pets: bool = False
    fotos: List[str] = []
    corretor_id: str

class FavoriteAction(BaseModel):
    user_id: str
    imovel_id: str

class ClientListing(BaseModel):
    cliente_id: str
    status: str = "pendente"
    titulo: str
    descricao: str
    localizacao: str
    preco: float
    condominio: Optional[float] = 0.0
    finalidade: str
    tipo_imovel: str
    tamanho_m2: float
    quartos: int
    suites: int
    banheiros: int
    vagas: int
    salas: int
    cozinhas: int
    varandas: int
    andares: Optional[int] = 1
    area_lazer: bool = False
    aceita_pets: bool = False
    fotos: List[str] = []

class UpdateProfile(BaseModel):
    nome: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    creci: Optional[str] = None

class KanbanCard(BaseModel):
    lead_id: str
    corretor_id: str
    etapa: str = "Leads Frios"
    prioridade: int = 1
    notas_internas: Optional[str] = ""

class DealData(BaseModel):
    titulo_negocio: str
    valor_transacao: float
    etapa: str
    proximo_passo: str
    data_interacao: str
    descricao: str
    comissao_estimada: float
    corretor_id: str

# --- 2. ROTAS PÚBLICAS E GERAIS ---

@app.get("/")
def read_root():
    return {"status": "Locus Aura API Online", "database": "Conectado"}

@app.get("/imoveis", response_model=List[dict])
def listar_imoveis():
    imoveis = list(db.imoveis.find())
    for item in imoveis:
        item["_id"] = str(item["_id"])
    return imoveis

@app.get("/imoveis/busca-ia")
def busca_ia(pergunta: str):
    if "animal" in pergunta.lower() or "pet" in pergunta.lower() or "silencioso" in pergunta.lower():
        resultados = list(db.imoveis.find({"aceita_pets": True}).limit(3))
        for r in resultados:
            r["_id"] = str(r["_id"])
        return {"mensagem_ia": "Encontrei estes imóveis ideais para você!", "resultados": resultados}
    return {"mensagem_ia": "Pode me dar mais detalhes?"}

# --- 3. AUTENTICAÇÃO E PERFIL ---

@app.post("/login")
def login(data: LoginData):
    user = auth_service.login(data.email, data.password)
    if not user:
        raise HTTPException(status_code=401, detail="E-mail ou senha incorretos")
    return user

@app.post("/signup")
def signup(user: UserSignup):
    if db.users.find_one({"email": user.email.lower()}):
        raise HTTPException(status_code=400, detail="E-mail já cadastrado")

    user_doc = {
        "full_name": user.nome,
        "email": user.email.lower(),
        "password_hash": auth_service._generate_hash(user.password),
        "role": user.role,
        "creci": user.creci,
        "is_active": user.is_active
    }

    db.users.insert_one(user_doc)
    db.verifications.insert_one({
        "email": user.email.lower(),
        "code": "123456",
        "criado_em": datetime.now()
    })

    return {"status": "Usuário criado! Use 123456 para ativar."}

@app.post("/verify")
def verify_email(data: VerifyCode):
    if data.code == "123456":
        db.users.update_one({"email": data.email.lower()}, {"$set": {"is_active": True}})
        return {"status": "Conta ativada!"}
    raise HTTPException(status_code=400, detail="Código inválido")

@app.put("/perfil/{user_id}")
def atualizar_perfil(user_id: str, dados: UpdateProfile):
    update_data = dados.dict(exclude_unset=True)

    if "password" in update_data and update_data["password"]:
        update_data["password_hash"] = auth_service._generate_hash(update_data["password"])
        del update_data["password"]

    if "email" in update_data and update_data["email"]:
        update_data["email"] = update_data["email"].lower()

    db.users.update_one({"_id": ObjectId(user_id)}, {"$set": update_data})
    return {"status": "Perfil atualizado"}

@app.delete("/perfil/{user_id}")
def eliminar_conta(user_id: str):
    db.users.delete_one({"_id": ObjectId(user_id)})
    db.favorites.delete_many({"user_id": user_id})
    return {"status": "Dados excluídos"}

# --- 4. ÁREA DO CLIENTE ---

@app.post("/favoritos/toggle")
def toggle_favorito(action: FavoriteAction):
    q = {"user_id": action.user_id, "imovel_id": action.imovel_id}
    if db.favorites.find_one(q):
        db.favorites.delete_one(q)
        return {"status": "removido"}
    db.favorites.insert_one(q)
    return {"status": "adicionado"}

@app.post("/anuncios-cliente/enviar")
def enviar_anuncio_cliente(data: ClientListing):
    res = db.client_listings.insert_one(data.dict())
    return {"status": "sucesso", "id": str(res.inserted_id)}

@app.get("/corretores")
def listar_especialistas():
    especialistas = list(db.brokers.find({"is_active": True}))
    for e in especialistas:
        e["_id"] = str(e["_id"])
    return especialistas

# --- 5. ÁREA DO PROFISSIONAL (CRM & DASHBOARD) ---

@app.get("/dashboard/resumo/{corretor_id}")
def get_dashboard_summary(corretor_id: str):
    return {
        "total_leads": db.leads.count_documents({"corretor_id": corretor_id}),
        "novos_leads": db.leads.count_documents({"corretor_id": corretor_id, "status": "Novo"}),
        "imoveis_ativos": db.imoveis.count_documents({"corretor_id": corretor_id}),
        "anuncios_pendentes": db.client_listings.count_documents({"status": "pendente"})
    }

@app.get("/leads/lista/{corretor_id}")
def listar_leads_agenda(corretor_id: str, busca: Optional[str] = None):
    query = {"corretor_id": corretor_id}
    if busca:
        query["nome"] = {"$regex": busca, "$options": "i"}
    leads = list(db.leads.find(query))
    for l in leads:
        l["_id"] = str(l["_id"])
    return leads

@app.post("/leads/enviar")
def enviar_lead(lead: LeadData):
    db.leads.insert_one(lead.dict())
    return {"status": "Mensagem recebida"}

@app.post("/kanban/criar-card")
def criar_card_kanban(data: KanbanCard):
    res = db.kanban_cards.insert_one(data.dict())
    return {"id": str(res.inserted_id)}

@app.get("/kanban/board/{corretor_id}")
def listar_cards_kanban(corretor_id: str):
    cards = list(db.kanban_cards.find({"corretor_id": corretor_id}))
    for c in cards:
        c["_id"] = str(c["_id"])
        lead = db.leads.find_one({"_id": ObjectId(c["lead_id"])})
        c["nome_lead"] = lead["nome"] if lead else "Lead Excluído"
    return cards

@app.get("/deals/{corretor_id}")
def listar_negocios(corretor_id: str):
    deals = list(db.deals.find({"corretor_id": corretor_id}))
    for d in deals:
        d["_id"] = str(d["_id"])
    return deals

@app.get("/comissao/calcular")
def calcular_comissao(valor_venda: float):
    total = valor_venda * 0.05
    return {
        "valor_venda": valor_venda,
        "comissao_total": round(total, 2),
        "imobiliaria": round(total * 0.40, 2),
        "ganho_corretor": round(total * 0.30, 2)
    }
