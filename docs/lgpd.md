# Documento LGPD - Sistema Imobiliário IA

## Objetivo
Garantir que o sistema esteja em conformidade com a LGPD, registrando o consentimento dos usuários e protegendo dados sensíveis.

---

## Coleta de Consentimento
O sistema deve exigir que o usuário aceite os termos antes de enviar seus dados.

### Implementação no Front-end
- Exibir checkbox obrigatório: "Aceito os termos de uso e política de privacidade"
- Os dados (nome, e-mail, telefone) só devem ser enviados se o checkbox estiver marcado

---

## Registro no Banco de Dados
O consentimento é armazenado nas tabelas `users` e `leads` com os seguintes campos:

- `lgpd_consent` → indica se o usuário aceitou os termos (true/false)
- `terms_version` → versão dos termos aceitos (ex: v1.0)
- `consent_timestamp` → data e hora do aceite

Esses dados permitem auditoria e comprovação de consentimento.

---

## Proteção de Dados Sensíveis

### Senhas
- Nunca são armazenadas em texto puro
- Utilizamos o campo `password_hash`
- A senha é criptografada no backend utilizando a biblioteca `bcrypt`

---

## Recuperação de Senha
- Utiliza a tabela `verification_codes`
- Um código temporário é gerado
- O código possui tempo de expiração
- Garante segurança no processo de redefinição

---

## Boas Práticas Implementadas
- Separação de autenticação e dados do usuário
- Uso de hash seguro para senhas
- Registro de consentimento (LGPD)
- Estrutura preparada para auditoria

---

## Conclusão
O sistema está estruturado para atender aos requisitos básicos da LGPD, garantindo:

- transparência no uso dos dados
- segurança das informações
- rastreabilidade do consentimento do usuário
