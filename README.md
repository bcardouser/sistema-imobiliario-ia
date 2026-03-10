# Sistema Imobiliário com Inteligência Artificial

Projeto acadêmico da disciplina de Laboratório Avançado de Software.

O objetivo deste projeto é desenvolver uma plataforma SaaS para gestão imobiliária com automação de processos e integração com Inteligência Artificial.

---

# Estrutura do Projeto

Este repositório foi organizado para facilitar o desenvolvimento em equipe.

## backend

Contém o código da API do sistema.

Aqui será desenvolvido o backend em Python utilizando FastAPI.  
Essa parte será responsável pelas regras de negócio do sistema e pela comunicação com o banco de dados.

Arquivo principal:

main.py → ponto inicial da aplicação backend.

---

## database

Contém o modelo do banco de dados.

O arquivo schema.sql define a estrutura das tabelas do sistema, incluindo:

- imobiliárias (tenants)
- usuários
- imóveis
- leads

Esse arquivo será utilizado para criar o banco de dados PostgreSQL do projeto.

---

## docs

Contém a documentação técnica do projeto.

Aqui ficam explicações sobre arquitetura, decisões técnicas e funcionamento do sistema.

---

## requirements.txt

Lista das bibliotecas Python utilizadas no projeto.

Quando alguém for rodar o projeto, basta executar:

pip install -r requirements.txt

---

# Arquitetura do Sistema

O sistema segue uma arquitetura de três camadas.

Frontend  
Interface do usuário (Streamlit).

Backend  
API desenvolvida em Python com FastAPI.

Banco de Dados  
PostgreSQL responsável pelo armazenamento das informações.

---

# Modelo SaaS

O sistema será multi-tenant.

Isso significa que várias imobiliárias poderão usar o sistema ao mesmo tempo, mas cada uma terá seus dados isolados.

Cada imobiliária poderá ter:

- usuários
- imóveis cadastrados
- leads de clientes
- histórico de atividades
