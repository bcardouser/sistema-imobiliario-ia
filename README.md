# Sistema de Gestão Imobiliária com Inteligência Artificial

Projeto acadêmico da disciplina de Laboratório Avançado de Software.

O objetivo deste projeto é desenvolver uma plataforma SaaS para gestão imobiliária, com automação de processos e uso de Inteligência Artificial para facilitar a busca e organização de imóveis.

---

## Estrutura do Projeto

O repositório foi organizado para facilitar o desenvolvimento em equipe.

### backend
Contém o código do backend do sistema.

Aqui será desenvolvido o servidor da aplicação utilizando Python e FastAPI.  
Essa parte será responsável por processar as regras de negócio e comunicar com o banco de dados.

Arquivo principal:
- **main.py** → ponto inicial da aplicação backend.

---

### database
Contém a modelagem do banco de dados.

O arquivo **schema.sql** define a estrutura das tabelas utilizadas pelo sistema.

Principais entidades do banco:
- imobiliárias (tenants)
- usuários
- imóveis
- leads de clientes

Esse arquivo será utilizado para criar o banco PostgreSQL.

---

### docs
Contém a documentação técnica do projeto.

Aqui ficam explicações sobre arquitetura, decisões técnicas e funcionamento do sistema.

---

### requirements.txt
Lista das bibliotecas Python necessárias para rodar o projeto.

Para instalar as dependências:
```
pip install -r requirements.txt
```
```

## Arquitetura do Sistema

O sistema segue uma arquitetura de três camadas:

**Frontend**  
Interface do usuário (previsto para ser desenvolvido com Streamlit).

**Backend**  
API desenvolvida em Python utilizando FastAPI.

**Banco de Dados**  
PostgreSQL responsável pelo armazenamento das informações.

---

## Modelo do Sistema

O sistema será desenvolvido no modelo **SaaS multi-tenant**.

Isso significa que várias imobiliárias poderão utilizar a mesma plataforma, mas cada uma terá seus dados isolados.

Cada imobiliária poderá ter:
- usuários
- imóveis cadastrados
- leads de clientes
- histórico de atividades
