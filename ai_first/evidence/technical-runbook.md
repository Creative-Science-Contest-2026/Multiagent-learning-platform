# Technical Runbook

## Project

Multiagent Learning Platform, derived from HKUDS/DeepTutor under Apache 2.0.

## Local run prerequisites

- Python 3.11+
- Node.js compatible with Next.js 16
- Backend dependencies from `requirements/server.txt`
- Frontend dependencies in `web/package.json`
- LLM and embedding provider settings

## Local run commands

```bash
pip install -r requirements/server.txt
pip install -e .
cd web && npm install && cd ..
python scripts/start_web.py
```

## Runtime data

- Chat/session SQLite: `data/user/chat_history.db`
- Knowledge bases: `data/knowledge_bases/`
- Memory: `data/memory/`
- Settings: `data/user/settings/`

## Demo notes

Use a prepared sample document and avoid relying on live external web search during the judged demo unless network access is confirmed.
