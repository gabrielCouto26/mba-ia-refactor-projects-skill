# Relatório de Auditoria Arquitetural e Refatoração (Refactor-Arch Report)

**Projeto:** `task-manager-api`  
**Skill Aplicada:** `refactor-arch`  
**Data:** 10/08/2026  
**Autor:** `refactor-arch` (Especialista em Arquitetura de Software e Auditoria de Código)

---

## 1. Visão Geral do Projeto Legado

O projeto analisado consiste em uma API REST de gerenciamento de tarefas desenvolvida em Python com Flask, SQLAlchemy e SQLite. A aplicação cobre cadastro de usuários, autenticação simples, criação e busca de tarefas, categorias e relatórios operacionais.

Apesar de já possuir alguma divisão inicial por pastas (`models/`, `routes/`, `services/`, `utils/`), a base apresentava sinais de arquitetura parcialmente acoplada: handlers HTTP ainda concentravam validações, relatórios executavam agregações e consultas repetitivas em serviços grandes, configurações sensíveis tinham fallback inseguro e regras de domínio apareciam como literais espalhados.

### Métricas de Código Analisado

* **Linguagem & Framework:** Python 3.9+ / Flask `3.0.0`
* **Banco de Dados:** SQLite via Flask-SQLAlchemy `3.1.1`
* **Validação:** Marshmallow `3.20.1`
* **Total de Arquivos Analisados:** 26 arquivos do projeto, incluindo `app.py`, `config.py`, `database.py`, `exceptions.py`, `constants.py`, `models/`, `routes/`, `schemas/`, `services/`, `utils/`, `seed.py`, `README.md` e `requirements.txt`.
* **Total de Linhas Analisadas:** 1.231 linhas
* **Média de Linhas por Arquivo:** ~47 LOC por arquivo
* **Entidades de Banco de Dados Mapeadas:** `users`, `tasks`, `categories`

---

## 2. Relatório Detalhado da Auditoria Arquitetural

A base foi auditada contra o Catálogo de Anti-Patterns da skill `refactor-arch`. Foram identificados **7 problemas relevantes**, classificados por severidade:

```text
[CRITICAL] 1 achado
[HIGH]     2 achados
[MEDIUM]   3 achados
[LOW]      1 achado
```

### Detalhamento das Desconformidades Identificadas

#### 1. [CRITICAL] Anti-Pattern: Hardcoded Secrets / Configuração Sensível com Fallback Inseguro

* **Localização:** `config.py` linhas 6-16
* **Sinal de Detecção:** As variáveis `SECRET_KEY` e `JWT_SECRET` são carregadas do ambiente, porém possuem fallbacks previsíveis (`default-secret-key-change-me` e `jwt-secret-key`). O token de autenticação também é montado com trecho do segredo em `services/user_service.py` linhas 85-90.
* **Impacto:** Em ambientes mal configurados, a aplicação sobe com segredo previsível, facilitando falsificação de tokens e comportamento inseguro em produção.
* **Recomendação:** Tornar `SECRET_KEY` e `JWT_SECRET` obrigatórios fora do ambiente de desenvolvimento, validar a configuração no boot e substituir o token manual por JWT assinado com expiração.

#### 2. [HIGH] Anti-Pattern: Fat Service / Relatório com Responsabilidade Excessiva

* **Localização:** `services/report_service.py` linhas 16-93, 96-127 e 129-187
* **Sinal de Detecção:** `ReportService` concentra geração de relatórios, estatísticas, produtividade por usuário, gestão de categorias e regras de atraso. O método `summary_report` combina contagens, laços, filtros, montagem de payload e cálculos temporais em um único fluxo.
* **Impacto:** Baixa coesão e alto custo de manutenção. Mudanças em relatórios podem afetar CRUD de categorias, e testes unitários ficam maiores por atravessar muitos caminhos de lógica.
* **Recomendação:** Separar responsabilidades em `TaskReportService`, `UserProductivityService` e `CategoryService`, preservando o controller apenas como adaptador HTTP.

#### 3. [HIGH] Anti-Pattern: Tight Coupling & Acesso Estático a Serviços

* **Localização:** `routes/task_routes.py` linhas 1-61, `routes/user_routes.py` linhas 1-63, `routes/report_routes.py` linhas 1-53
* **Sinal de Detecção:** As rotas importam classes de serviço diretamente e chamam métodos estáticos (`TaskService`, `UserService`, `ReportService`). Não há injeção explícita de dependências.
* **Impacto:** Testes precisam monkeypatchar imports globais ou subir aplicação real. A arquitetura fica menos flexível para troca de persistência, mocks, fakes ou composição por ambiente.
* **Recomendação:** Introduzir factories para serviços ou injeção via application factory, permitindo instâncias configuráveis e isolamento por teste.

#### 4. [MEDIUM] Anti-Pattern: N+1 Query Problem em Relatórios e Usuários

* **Localização:** `services/report_service.py` linhas 55-60 e 129-136; `services/user_service.py` linhas 8-14
* **Sinal de Detecção:** `summary_report` busca todos os usuários e executa uma query por usuário para contar tarefas. `list_categories` busca categorias e executa uma query por categoria. `get_all_users` acessa `len(u.tasks)` para cada usuário, podendo disparar lazy loads repetidos.
* **Impacto:** O número de queries cresce linearmente com usuários e categorias, degradando relatórios e listagens à medida que a base aumenta.
* **Recomendação:** Usar agregações SQL (`GROUP BY`) ou eager loading com `joinedload`/`selectinload`. Para contagens, preferir consultas agregadas por `user_id` e `category_id`.

#### 5. [MEDIUM] Anti-Pattern: Missing Input Validation Parcial

* **Localização:** `routes/task_routes.py` linhas 20-30 e 32-42; `routes/user_routes.py` linhas 18-28, 30-40 e 53-63; `routes/report_routes.py` linhas 26-38 e 40-51
* **Sinal de Detecção:** A validação com Marshmallow foi introduzida, mas permanece repetida nos handlers com blocos `try/except` quase idênticos. Além disso, os serviços ainda fazem validações manuais complementares de existência e conteúdo.
* **Impacto:** Duplicação de tratamento de erro e risco de respostas inconsistentes conforme novos endpoints forem criados.
* **Recomendação:** Criar um middleware/decorator de validação de schema para padronizar `request.get_json()`, captura de erros e retorno de payloads.

#### 6. [MEDIUM] Anti-Pattern: Deprecated API Usage / APIs Legadas do SQLAlchemy

* **Localização:** `services/task_service.py` linhas 34, 40, 65, 70, 77 e 107; `services/report_service.py` linhas 97, 160 e 178; `services/user_service.py` linhas 17, 28, 53 e 68
* **Sinal de Detecção:** Uso recorrente de `Model.query.get(...)`, API considerada legada na linha 2.x do SQLAlchemy.
* **Impacto:** A aplicação funciona hoje, mas acumula dívida técnica e warnings em upgrades futuros de ORM.
* **Recomendação:** Migrar para `db.session.get(Model, id)` e padronizar consultas em repositórios ou serviços de persistência.

#### 7. [LOW] Anti-Pattern: Magic Strings & Numbers

* **Localização:** `app.py` linha 45; `config.py` linhas 7-16; `constants.py` linhas 21-24; `services/task_service.py` linhas 47-48; `services/report_service.py` linhas 26-31 e 47-48
* **Sinal de Detecção:** Ainda existem literais de porta (`5000`), host (`0.0.0.0`), janela de relatório (`7` dias), prioridades numéricas e fallbacks de configuração em múltiplos pontos.
* **Impacto:** Alterações de regra operacional exigem busca manual e podem gerar divergência entre validação, persistência e relatórios.
* **Recomendação:** Centralizar parâmetros operacionais no `Config` e parâmetros de domínio no `constants.py`, com nomes explícitos para janela de atividade, host, porta e prioridades padrão.

---

## 3. Playbook de Transformação Aplicado

A refatoração consolidou a aplicação em uma arquitetura em camadas no estilo Service-Repository/MVC leve para Flask:

1. **MVC Separation:** As rotas foram separadas por domínio em `routes/task_routes.py`, `routes/user_routes.py` e `routes/report_routes.py`. O boot da aplicação ficou concentrado em `app.py`, que registra os blueprints nas linhas 19-21.
2. **Config Extraction:** As configurações foram centralizadas em `config.py`, carregando variáveis via `python-dotenv` e `os.getenv`.
3. **Controller Slimming:** Os handlers HTTP delegam a execução principal para `TaskService`, `UserService` e `ReportService`.
4. **Validation Layering:** Schemas Marshmallow foram criados em `schemas/`, com validação de usuários, tarefas e categorias.
5. **Centralized Error Handling:** O arquivo `exceptions.py` define uma hierarquia de erros de API, e `app.py` linhas 34-42 centraliza respostas para `APIError` e 404.
6. **Security Modernization:** `models/user.py` linhas 31-45 usa `werkzeug.security` para hashes modernos e mantém fallback de MD5 apenas para migração automática de senhas legadas.
7. **Query Optimization Parcial:** `TaskService` usa `joinedload` em `get_all_tasks`, `get_task_by_id` e `search_tasks` (`services/task_service.py` linhas 11-24 e 120-141), reduzindo lazy loads de usuário e categoria.
8. **Constants Extraction:** Estados, papéis e prioridades passaram a ser enumerados em `constants.py`.

### Estrutura Arquitetural Resultante

```text
task-manager-api/
├── app.py                      # Boot Flask, registro de blueprints e handlers globais
├── config.py                   # Configurações de ambiente
├── constants.py                # Enums e constantes de domínio
├── database.py                 # Instância Flask-SQLAlchemy
├── exceptions.py               # Erros padronizados da API
├── seed.py                     # Popularização inicial do SQLite
├── requirements.txt            # Dependências Python
├── README.md                   # Instruções de execução
├── models/
│   ├── user.py                 # Entidade User e hash de senha
│   ├── task.py                 # Entidade Task e serialização
│   └── category.py             # Entidade Category
├── routes/
│   ├── user_routes.py          # Endpoints de usuários e login
│   ├── task_routes.py          # Endpoints de tasks
│   └── report_routes.py        # Endpoints de relatórios e categorias
├── schemas/
│   ├── user_schema.py          # Validação de usuários/login
│   ├── task_schema.py          # Validação de tasks e busca
│   └── category_schema.py      # Validação de categorias
├── services/
│   ├── user_service.py         # Regras de usuário e autenticação
│   ├── task_service.py         # Regras de tarefas
│   ├── report_service.py       # Relatórios e categorias
│   └── notification_service.py # Integração/notificação
└── utils/
    └── helpers.py              # Funções auxiliares
```

---

## 4. Resultados da Validação

Foram executadas validações estáticas e de boot básico da aplicação refatorada.

### Comandos Executados

```bash
PYTHONPYCACHEPREFIX=/private/tmp/task-manager-api-pycache ./venv/bin/python -m compileall -q .
./venv/bin/python - <<'PY'
from app import app
client = app.test_client()
print('GET /health', client.get('/health').status_code)
print('GET /', client.get('/').status_code, client.get('/').json)
PY
```

### Resultado Observado

```text
GET /health 200
GET / 200 {'message': 'Task Manager API', 'version': '1.0'}
```

### Checklist de Validação

* **Application boot:** A aplicação importa corretamente via `from app import app`.
* **Endpoints básicos preservados:** `GET /health` e `GET /` responderam com `200 OK`.
* **Tratamento centralizado de erro:** `APIError` e 404 são tratados em `app.py`.
* **Schemas de validação presentes:** Marshmallow está em uso nos endpoints de criação, atualização, login, busca e categorias.
* **Mitigação parcial de N+1:** `joinedload` foi aplicado aos fluxos principais de tarefas.
* **Risco residual identificado:** Relatórios e listagens de usuários/categorias ainda podem disparar N+1 e devem ser otimizados em próxima iteração.
* **Suíte automatizada:** Não há arquivos de teste no repositório; recomenda-se adicionar testes de integração para `/users`, `/tasks`, `/reports/summary`, `/categories` e `/login`.

---

## 5. Conclusão

A refatoração elevou o `task-manager-api` para uma organização significativamente mais limpa que a base inicial: rotas foram separadas por domínio, regras de negócio foram movidas para serviços, validação foi padronizada com Marshmallow, erros de API ganharam hierarquia própria e a configuração foi centralizada.

O projeto ainda possui pontos de evolução antes de ser considerado uma arquitetura plenamente madura: autenticação precisa de JWT real, segredos não devem ter fallback inseguro em produção, relatórios devem ser quebrados em serviços menores e consultas agregadas precisam substituir os N+1 remanescentes.

Em termos da skill `refactor-arch`, o objetivo principal foi atingido: a aplicação saiu de um desenho parcialmente acoplado para uma estrutura MVC/Service Layer auditável, extensível e mais segura, com riscos residuais documentados para a próxima rodada de melhoria.

## Segunda execução da skill (21/08/2026)

A reauditoria confirmou que os fallbacks de `SECRET_KEY`/`JWT_SECRET`, o token fabricado e o fallback MD5 ainda eram riscos executáveis. Os segredos agora são exclusivamente ambientais e a configuração de produção falha fechada quando ausentes; MD5 foi removido e o token passou a ser assinado com `itsdangerous` e expiração. O boot de desenvolvimento respondeu `200` em `/health` e `/`; o teste de produção sem segredos falhou como esperado.
