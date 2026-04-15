import os
import bcrypt
import jwt
from datetime import datetime, timedelta, timezone 
from pymongo import MongoClient
from bson import ObjectId

# --- CONFIGURAÇÕES ---
MONGO_URI = "mongodb+srv://xaviergabriel739_db_user:YTJsV4uhIDV0cah1@cluster0.uwiae5z.mongodb.net/?appName=Cluster0"
SECRET_KEY = "locus_aura_secret_token_2026_seguranca_total" 

class LocusAuraAuth:
    def __init__(self, client):
        self.db = client['locus_aura_db']
        self.users = self.db['users']
        self.users.create_index("email", unique=True)

    def _generate_hash(self, password):
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(12)).decode('utf-8')

    def register(self, name, email, password):
        try:
            user_doc = {
                "full_name": name, "email": email.lower(),
                "password_hash": self._generate_hash(password),
                "role": "corretor", "lgpd_consent": True,
                "created_at": datetime.now(timezone.utc)
            }
            return self.users.insert_one(user_doc)
        except: return None

    def login(self, email, password):
        user = self.users.find_one({"email": email.lower()})
        if user and bcrypt.checkpw(password.encode('utf-8'), user["password_hash"].encode('utf-8')):
            payload = {"u_id": str(user["_id"]), "exp": datetime.now(timezone.utc) + timedelta(hours=2)}
            return {"token": jwt.encode(payload, SECRET_KEY, algorithm="HS256"), "name": user["full_name"], "id": user["_id"]}
        return None

class PropertyManager:
    def __init__(self, client):
        self.db = client['locus_aura_db']
        self.properties = self.db['properties']

    def add_property(self, broker_id, title, desc, price, pet=False, swap=False):
        doc = {
            "broker_id": broker_id,
            "title": title,
            "description": desc,
            "price": price,
            "features": {"pet_friendly": pet, "permuta": swap},
            "created_at": datetime.now(timezone.utc)
        }
        return self.properties.insert_one(doc)

# --- EXECUÇÃO ---
if __name__ == "__main__":
    client = MongoClient(MONGO_URI)
    auth = LocusAuraAuth(client)
    pm = PropertyManager(client)

    print("--- Testando Fluxo Completo ---")
    user = auth.login("gabriel@locusaura.com", "MinhaSenha123")
    
    if user:
        print(f"Login de {user['name']} realizado!")
        # Cadastrando um imóvel de teste para a Yasmin ver
        imovel = pm.add_property(
            user['id'], 
            "Apartamento na Planta - Centro", 
            "Lindo apê com varanda gourmet, aceita cachorro e permuta por carro.",
            450000, 
            pet=True, 
            swap=True
        )
        print(f"Imóvel cadastrado com sucesso! ID: {imovel.inserted_id}")
    else:
        print("Usuário não encontrado. Cadastre-se primeiro.")