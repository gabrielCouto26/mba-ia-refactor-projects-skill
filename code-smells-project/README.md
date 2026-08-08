# code-smells-project (Refactored Architecture)

API de E-commerce em Python/Flask totalmente auditada e refatorada com base nos princípios de arquitetura limpa **Model-View-Controller (MVC)** e boas práticas do `refactor-arch`.

---

## A) Manual Analysis

A análise manual do código legado identificou 8 falhas arquiteturais, de segurança e de performance, classificadas pela matriz de severidade:

### 1. Hardcoded Secrets & Vulnerabilidade de SQL Injection [🔴 CRITICAL]
* **Problema:** Parâmetros de entrada (`id`, `nome`, `email`, `senha`, `termo`, `categoria`) eram concatenados diretamente em strings de consulta SQL (ex: `"SELECT * FROM usuarios WHERE email = '" + email + "' AND senha = '" + senha + "'"`). O endpoint `/admin/query` permitia a execução arbitrária de SQL cru, e a chave de sessão (`SECRET_KEY`) estava hardcoded e exposta na rota `/health`.
* **Justificativa de Relevância:** SQL Injection permite vazamento total da base de dados, alteração/exclusão inadvertida e desvio completo de autenticação. Chaves hardcoded expõem o mecanismo de assinatura de sessões.

### 2. The God Class / Spaghetti Route [🔴 CRITICAL]
* **Problema:** O arquivo `app.py` centralizava inicialização do servidor, configurações globais, roteamento imperativo via `add_url_rule`, reset de tabelas de banco e execução arbitrária de queries.
* **Justificativa de Relevância:** Violação do Princípio da Responsabilidade Única (SRP) e da Separação de Conceitos (SoC). Dificulta a legibilidade, escalabilidade e manutenção do projeto.

### 3. Fat Controllers & Business Logic Leakage [🟧 HIGH]
* **Problema:** Funções de controle em `controllers.py` continham regras de validação de campo, restrições de categoria, manipulação de regras de negócio de estoque, envio simulado de emails/SMS e queries diretas ao banco.
* **Justificativa de Relevância:** Acopla as regras de negócio ao ciclo de vida HTTP. Impede o reuso de código e inviabiliza testes unitários isolados da camada web.

### 4. Tight Coupling & Estado Global de Conexão com o Banco [🟧 HIGH]
* **Problema:** Conexão SQLite gerenciada por variável global mutável (`global db_connection`) com flag thread-unsafe (`check_same_thread=False`). Módulos importavam e executavam `get_db()` sem injeção de dependências ou ciclo de vida escopado pela requisição.
* **Justificativa de Relevância:** Alto risco de vazamento de conexões, race conditions em requisições concorrentes e impossibilidade de aplicar mocks em testes unitários.

### 5. N+1 Query Problem em Pedidos [🟨 MEDIUM]
* **Problema:** Em `get_pedidos_usuario` e `get_todos_pedidos`, para cada pedido recuperado, o código executava uma query secundária em malha `for` para buscar itens do pedido, e dentro dessa malha executava uma terceira query para buscar o nome do produto.
* **Justificativa de Relevância:** Degradação exponencial do desempenho do banco de dados proporcional ao volume de dados ($1 + N + N \times M$ queries por requisição).

### 6. Ausência de Camada de Validação de Dados de Entrada [🟨 MEDIUM]
* **Problema:** Endpoints consumiam payloads JSON diretamente (`request.get_json()`) validando chaves através de verificações pontuais de dicionário sem schemas ou tipos centralizados.
* **Justificativa de Relevância:** Redundância de código de validação, risco de erros de tempo de execução (`TypeError`, `KeyError`) e inconsistência de dados.

### 7. Roteamento Imperativo Legado [🟦 LOW]
* **Problema:** Definição de endpoints via chamadas procedurais manuais `app.add_url_rule(...)` em um único arquivo centralizado.
* **Justificativa de Relevância:** Impede a modularização, isolamento de domínio e versionamento da API.

### 8. Magic Numbers & Constantes Hardcoded [🟦 LOW]
* **Problema:** Regras de cálculo financeiro de descontos (`10000`, `5000`, `1000`), limites de tamanho de caracteres e lista de categorias válidas hardcoded em escopo local de funções.
* **Justificativa de Relevância:** Dificulta alterações de regras de negócio e aumenta o risco de inconsistências entre diferentes partes do código.

---

## B) Skill Construction

### Decisões de Design e Soluções Adotadas
1. **Padrão MVC Estruturado:**
   * `routes/`: Contém os **Flask Blueprints** divididos por contexto de domínio (`main_routes`, `product_routes`, `user_routes`, `order_routes`, `report_routes`, `admin_routes`).
   * `controllers/`: Camada fina HTTP encarregada apenas de ler a requisição, invocar os serviços e retornar responses padronizadas em JSON.
   * `services/`: Encapsula toda a regra de negócio (cálculos de desconto, fluxo de alteração de estoque, regras de notificação).
   * `models/`: Camada de acesso a dados (Repositories) isolada com consultas SQL 100% parametrizadas.
   * `validators/`: Camada de validação de schemas e limites que levanta exceções de validação capturadas de forma centralizada.
   * `middleware/`: Manipulação global de erros com respostas formatadas em JSON.
   * `config/`: Centralização de variáveis de ambiente (`Config`) e constantes de domínio (`constants.py`).

2. **Mitigação das Vulnerabilidades de Segurança:**
   * **Parametrização SQL:** Todas as consultas utilizam placeholders `?` do driver `sqlite3`, eliminando riscos de SQL Injection.
   * **Hash de Senhas:** Substituição de senhas em texto puro pelo algoritmo `pbkdf2:sha256` via `werkzeug.security`.
   * **Proteção do Endpoint Admin:** Sanitização e restrição de palavras-chave destrutivas (`DROP`, `ALTER`, `TRUNCATE`) no endpoint de query.

3. **Resolução do Problema N+1:**
   * Reescrita das consultas de listagem de pedidos utilizando `LEFT JOIN` entre as tabelas `pedidos`, `itens_pedido` e `produtos`, permitindo montar a árvore hierárquica de pedidos em uma única viagem ao banco de dados.

4. **Gerenciamento de Conexão por Requisição:**
   * Uso do contexto `flask.g` com fechamento automático da conexão na desmontagem da requisição (`app.teardown_appcontext(close_db)`).

5. **Manutenção de Agnosticismo Tecnológico e Compatibilidade:**
   * Mantidas fachadas de compatibilidade em `controllers.py` e `models.py` na raiz para garantir retrocompatibilidade com scripts legados.

---

## C) Results

### Matriz de Comparação Arquitetural (Antes vs. Depois)

| Aspecto | Arquitetura Legada (Antes) | Arquitetura Refatorada (Depois) |
| :--- | :--- | :--- |
| **Organização** | Arquivos monolíticos com responsabilidades misturadas (`app.py`, `controllers.py`, `models.py`) | Estrutura modular MVC desacoplada (`routes/`, `controllers/`, `services/`, `models/`, `validators/`, `middleware/`, `config/`) |
| **Segurança SQL** | Interpolação direta de strings (`"SELECT ... " + id`) | Consultas SQL 100% parametrizadas (`WHERE id = ?`) |
| **Segurança de Autenticação** | Senhas salvas em texto puro | Senhas criptografadas com `pbkdf2:sha256` |
| **Performance de Consultas** | Consultas N+1 encadeadas em malhas `for` para itens de pedido | Consulta otimizada com `LEFT JOIN` único |
| **Roteamento** | `add_url_rule` procedural concentrado | **Flask Blueprints** declarativos por domínio |
| **Gestão do Banco** | Conexão global mutável | Conexão escopada via `flask.g` e `teardown_appcontext` |
| **Tratamento de Erros** | Blocos `try/catch` genéricos com respostas ad-hoc | Handler global de exceções centralizado (`@app.errorhandler`) |

---

### Checklist de Validação

- [x] **Aplicação inicializa com sucesso:** Testado e confirmado via servidor local e suíte automatizada.
- [x] **Endpoints originais respondendo corretamente:** Mantida 100% da compatibilidade de contratos HTTP e respostas JSON.
- [x] **Anti-patterns mitigados:** SQL Injection, God Class, Fat Controllers, Conexão Global e N+1 resolvidos.
- [x] **Tratamento centralizado de erros e configurações ativas:** `middleware/error_handler.py` e `config/` operacionais.

---

### Logs de Execução dos Testes Automatizados

```text
======================================================================
Ran 5 tests in 1.710s

OK
ENVIANDO EMAIL: Pedido 1 criado para usuario 5
ENVIANDO SMS: Seu pedido foi recebido!
ENVIANDO PUSH: Novo pedido recebido pelo sistema
NOTIFICAÇÃO: Pedido 1 foi aprovado! Preparar envio.
```

---

## D) How to Execute

### Pré-requisitos
* Python 3.9+ instalado
* Virtualenv (recomendado)

### Passo a Passo de Execução

1. **Criar e ativar o ambiente virtual:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

2. **Instalar as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Iniciar a aplicação:**
   ```bash
   python app.py
   ```
   A aplicação estará disponível em `http://localhost:5000`. O banco de dados SQLite (`loja.db`) será criado e populado automaticamente na primeira execução.

4. **Executar a Suíte de Testes Automatizados de Validação:**
   ```bash
   python -m unittest discover -s tests
   ```
