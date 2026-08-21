# task-manager-api

API de Task Manager em Python/Flask usada como entrada do desafio `refactor-arch`. Diferente dos outros projetos, este já possui alguma separação de camadas (`models/`, `routes/`, `services/`, `utils/`), mas ainda contém problemas arquiteturais e de qualidade.

## Como rodar

```bash
pip install -r requirements.txt
python seed.py
python app.py
```

A aplicação sobe em `http://localhost:5000`. O `seed.py` popula o banco SQLite (`tasks.db`) com usuários, categorias e tasks de exemplo — **rode-o antes do primeiro boot**, caso contrário os endpoints vão retornar listas vazias.

## Segunda execução da skill `refactor-arch` (21/08/2026)

`SECRET_KEY` e `JWT_SECRET` agora são valores exclusivamente de ambiente e o boot em produção falha quando ausentes. O fallback MD5 foi removido e a autenticação usa token assinado com expiração. O boot de desenvolvimento e `/health`/`/` responderam `200`; a validação de produção sem segredos falhou como esperado.
