# Sistema Imobiliário com Inteligência Artificial

Projeto acadêmico da disciplina de Laboratório Avançado de Software.

O objetivo do projeto é desenvolver uma plataforma SaaS (Software as a Service) para gestão imobiliária com suporte a Inteligência Artificial para busca inteligente de imóveis e automação de processos.

---

## Arquitetura do Sistema

O sistema segue uma arquitetura de três camadas:

Frontend
Interface do usuário desenvolvida com Streamlit.

Backend
API desenvolvida em Python utilizando FastAPI.

Banco de Dados
PostgreSQL responsável pelo armazenamento das informações.

---

## Modelo SaaS

O sistema será multi-tenant, permitindo que múltiplas imobiliárias utilizem a mesma plataforma com isolamento de dados.

Cada imobiliária terá:

- usuários
- imóveis cadastrados
- leads de clientes

---

## Estrutura do Projeto

backend
Código da API em Python.

database
Modelagem do banco de dados.

docs
Documentação técnica do projeto.

---

## Tecnologias utilizadas

Python  
FastAPI  
PostgreSQL  
Streamlit
