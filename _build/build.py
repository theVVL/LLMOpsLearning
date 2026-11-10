# -*- coding: utf-8 -*-
"""Сборка курса DevOps+AI: IT-DEVOPS.txt + тест/."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BUILD = Path(__file__).resolve().parent
SOURCE = BUILD / "source"
OUT_DIR = ROOT / "тест"
TOTAL_EXPECTED = 546

RANK = {"БАЗА": 0, "ДЖУН": 1, "МИДЛ": 2}


def parse_questions(path):
    result = []
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        m = re.match(r"^(\d+)•\[(БАЗА|ДЖУН|МИДЛ)\]\s*(.+)$", line.strip())
        if m:
            result.append((int(m.group(1)), m.group(2), m.group(3).strip()))
    return result


OLD = {n: (lvl, text) for n, lvl, text in parse_questions(SOURCE / "old-question-list.txt")}
OLD.update({n: (lvl, text) for n, lvl, text in parse_questions(SOURCE / "old-block12.md")})
NEW = json.loads((BUILD / "new_questions.json").read_text(encoding="utf-8"))

CHAPTERS = [
    {
        "title": "Linux и администрирование",
        "file": "01-Linux.md",
        "src": ("old", 1, 41),
        "topics": [
            "Linux против Unix, POSIX и философия «всё есть файл»",
            "Файловая система, FHS, /proc и /sys",
            "Права, пользователи, sudo, SUID/SGID/Sticky Bit",
            "Процессы, сигналы, PID 1, лимиты ресурсов",
            "systemd, journald, cron и таймеры",
            "Пакеты, монтирование, LVM и диски",
            "Диагностика: load average, iostat, lsof, dmesg",
        ],
        "goal": "Свободно жить в Linux-сервере: найти процесс, лог, диск и причину тормозов.",
        "skills": [
            "читать man и диагностировать по логам",
            "управлять процессами и службами systemd",
            "понимать права, inodes, лимиты и swap",
        ],
        "apply": "Найти лог упавшего inference-пода, убить зависший процесс, написать systemd-юнит для локального сервиса.",
    },
    {
        "title": "Сети и сетевые протоколы",
        "file": "02-Сети.md",
        "src": ("old", 42, 79),
        "topics": [
            "OSI и TCP/IP, IP-адресация и CIDR",
            "TCP/UDP, порты, handshake и состояния сокета",
            "DNS, HTTP, TLS и WebSocket",
            "ARP, routing, NAT, DHCP",
            "Диагностика: ping, traceroute, dig, ss, tcpdump",
            "Балансировка L4/L7, Proxy Protocol, MTU",
            "VLAN, STP, OSPF/BGP, VPN, bonding",
        ],
        "goal": "Локализовать сетевую проблему по слоям, а не гадать.",
        "skills": [
            "считать подсети и читать таблицу маршрутов",
            "объяснять путь пакета и работу DNS/TLS",
            "диагностировать refused/timeout/MTU/conntrack",
        ],
        "apply": "Понять, почему агент не достучался до MCP-сервера или почему latency RAG выросла из-за DNS.",
    },
    {
        "title": "Git, GitLab и VS Code",
        "file": "03-Git-и-VS-Code.md",
        "src": ("old", 143, 168),
        "topics": [
            "Репозиторий, коммиты и объекты Git",
            "Ветки, merge, rebase, конфликты",
            "reset, revert, stash, cherry-pick, reflog",
            "Remote, SSH-ключи и безопасный доступ",
            "Hooks, LFS, submodules и worktree",
            "Trunk-based development и Git Flow",
            "VS Code: сравнение файлов, blame и автосохранение",
        ],
        "goal": "Вести историю так, чтобы её можно было откатить и объяснить.",
        "skills": [
            "безопасно разрешать конфликты и откатывать изменения",
            "работать с remote по SSH",
            "версионировать не только код, но и конфиги с промптами",
        ],
        "apply": "Хранить промпты и конфиги инфраструктуры в Git и откатывать неудачный «деплой промпта».",
    },
    {
        "title": "Docker и контейнеризация",
        "file": "04-Docker.md",
        "src": ("old", 80, 106),
        "topics": [
            "Контейнер против виртуальной машины",
            "Dockerfile, образ, контейнер и слои Overlay2",
            "Compose, сети и volumes",
            "CMD/ENTRYPOINT, COPY/ADD, кэш сборки",
            "Multi-stage, Alpine, .dockerignore",
            "Логи, лимиты ресурсов и траблшутинг",
            "Namespaces, cgroups, рантаймы и безопасность",
        ],
        "goal": "Собирать компактные и безопасные образы и объяснять, что под капотом.",
        "skills": [
            "писать Dockerfile с кэшем и multi-stage",
            "дебажить контейнер по логам, inspect и stats",
            "понимать namespaces/cgroups и exit code 137",
        ],
        "apply": "Собрать компактный образ с vLLM или Ollama, не таща в прод лишние зависимости.",
    },
    {
        "title": "Kubernetes",
        "file": "05-Kubernetes.md",
        "src": ("old", 271, 307),
        "topics": [
            "Архитектура Control Plane и worker nodes",
            "Pod, Deployment, ReplicaSet, StatefulSet, DaemonSet",
            "Service, Ingress, CoreDNS и CNI",
            "ConfigMap, Secret, PV/PVC/StorageClass",
            "Probes, requests/limits и QoS",
            "Scheduling, RBAC, HPA/PDB, NetworkPolicy",
            "Отладка подов и обслуживание кластера",
        ],
        "goal": "Разворачивать и отлаживать сервисы в кластере без паники.",
        "skills": [
            "читать describe/logs/events и ставить диагноз",
            "объяснять путь трафика от Ingress до пода",
            "понимать requests/limits и причины Pending/OOMKilled",
        ],
        "apply": "Развернуть Ollama или vLLM в поде, пробросить порт и смотреть логи через kubectl.",
    },
    {
        "title": "Инфраструктура как код: Ansible и Terraform",
        "file": "06-IaC-Ansible-Terraform.md",
        "src": ("old", 224, 249),
        "topics": [
            "IaC, декларативный и императивный подход",
            "Ansible: inventory, playbook, task, module, facts",
            "Идемпотентность, роли и Galaxy",
            "Vault, async, pipelining и Mitogen",
            "Terraform: init/plan/apply/destroy",
            "State, remote backend, locking, import",
            "Модули, count/for_each, lifecycle и связка с Ansible",
        ],
        "goal": "Описывать инфраструктуру кодом и не терять состояние.",
        "skills": [
            "писать идемпотентные плейбуки и роли",
            "объяснять plan и опасные destroy/create изменения",
            "работать с remote state и блокировками",
        ],
        "apply": "Описать GPU-ноды, VPC и S3 для моделей модулем Terraform, а настройку — ролью Ansible.",
    },
    {
        "title": "Облако",
        "file": "07-Облако.md",
        "src": ("old", 330, 339),
        "topics": [
            "IaaS, PaaS, SaaS и модели ответственности",
            "Регионы, зоны доступности и отказоустойчивость",
            "VPC, подсети, route tables, NAT",
            "Security Group и NACL",
            "IAM, роли и least privilege",
            "S3 против блочного диска",
            "Балансировщики, autoscaling, managed-сервисы, spot",
        ],
        "goal": "Понимать, за что платишь в облаке и где проходит граница ответственности.",
        "skills": [
            "проектировать VPC и доступы по least privilege",
            "выбирать между managed и self-hosted",
            "строить архитектуру, устойчивую к отзыву spot-инстанса",
        ],
        "apply": "Настроить роль для пода, который читает секреты, но не может их менять.",
    },
    {
        "title": "CI/CD: GitLab и GitHub Actions",
        "file": "08-CI-CD-GitLab-GitHub.md",
        "src": ("old", 107, 132),
        "topics": [
            "Анатомия .gitlab-ci.yml: stages, jobs, script",
            "Runners, executors и config.toml",
            "Cache против artifacts",
            "Переменные: Variable и File, masked/protected",
            "include, extends, rules, needs и parallel:matrix",
            "Docker-сборка в CI: DinD и socket binding",
            "Registry, cleanup, environments и rollback",
            "GitHub Actions: workflow_dispatch и pull_request_target",
        ],
        "goal": "Строить пайплайны, которые быстро собирают, безопасно деплоят и не жгут минуты.",
        "skills": [
            "объяснять DAG и ускорять пайплайн через needs",
            "защищать секреты и не допускать RCE через форки",
            "выбирать безопасный способ сборки образов",
        ],
        "apply": "Пайплайн, который при пуше собирает образ, гоняет eval промпта и деплоит в staging.",
    },
    {
        "title": "Базы данных, брокеры и кэширование",
        "file": "09-БД-брокеры-кэш.md",
        "src": ("old", 169, 223),
        "topics": [
            "SQL/NoSQL, ACID и CAP, CRUD",
            "Индексы, EXPLAIN и медленные запросы",
            "Пул коннектов и PgBouncer",
            "Бэкапы, PITR, репликация и шардинг",
            "MVCC, VACUUM, bloat, WAL и pg_wal",
            "Память PostgreSQL: shared_buffers и work_mem",
            "Redis: типы, персистентность, eviction, кластер",
            "Очереди: RabbitMQ против Kafka, ACK, DLX",
        ],
        "goal": "Не бояться базы: понимать, где тормозит, что бэкапить и как не потерять данные.",
        "skills": [
            "читать EXPLAIN и находить узкое место",
            "объяснять WAL, VACUUM и репликацию",
            "выбирать кэш и брокер под задачу",
        ],
        "apply": "Поднять pgvector рядом с приложением и не убить базу пулом соединений.",
    },
    {
        "title": "Мониторинг и observability",
        "file": "10-Мониторинг.md",
        "src": ("old", 250, 270),
        "topics": [
            "Мониторинг против observability, три столпа",
            "Prometheus: pull, exporters, TSDB",
            "PromQL: rate, irate, sum by, range vector",
            "Alertmanager: дедупликация, silence, inhibition",
            "Grafana и dashboards as code",
            "Логи: ELK/EFK против PLG",
            "Трейсы, OpenTelemetry, Thanos и SLO-алерты",
        ],
        "goal": "Понимать, что происходит в системе, до того как позвонит пользователь.",
        "skills": [
            "писать PromQL и объяснять High Cardinality",
            "строить алерты без шума",
            "связывать метрики, логи и трейсы в одну картину",
        ],
        "apply": "Обернуть вызовы LLM в трейсы и увидеть, какой шаг агента самый дорогой и медленный.",
    },
    {
        "title": "Декларативный CD и GitOps",
        "file": "11-GitOps.md",
        "src": ("old", 133, 142),
        "topics": [
            "GitOps и single source of truth",
            "Push против pull-модели деплоя",
            "ArgoCD против Flux",
            "Helm против Kustomize",
            "Reconciliation loop и configuration drift",
            "Sync waves и hooks, App-of-Apps",
            "Секреты в GitOps и прогрессивный деплой",
        ],
        "goal": "Деплоить через Git так, чтобы кластер сам приводил себя к нужному состоянию.",
        "skills": [
            "объяснять pull-модель и её безопасность",
            "читать diff в ArgoCD и чинить drift",
            "выбирать Helm или Kustomize под задачу",
        ],
        "apply": "Держать манифесты inference-сервиса в Git и катить их через ArgoCD.",
    },
    {
        "title": "Философия DevOps, SRE и методологии",
        "file": "12-Философия-DevOps.md",
        "src": ("old", 308, 329),
        "topics": [
            "CALMS и Infinity Loop",
            "DORA-метрики",
            "SLI, SLO, SLA и error budget",
            "Postmortem, runbook и incident management",
            "USE и RED, four golden signals",
            "Toil, on-call и capacity planning",
            "Platform engineering, supply chain security, FinOps, feature flags",
        ],
        "goal": "Говорить на языке бизнеса и надёжности, а не только команд.",
        "skills": [
            "объяснять SLO и error budget на примере",
            "строить blameless postmortem",
            "отличать DevOps, SRE и platform engineering",
        ],
        "apply": "Защитить решение «катить или не катить» арифметикой error budget.",
    },
    {
        "title": "Python, Bash и практические сценарии",
        "file": "13-Python-Bash-сценарии.md",
        "src": ("mix13",),
        "topics": [
            "Python: структуры данных, функции, исключения",
            "venv, pip, uv и управление зависимостями",
            "Файлы, subprocess, HTTP и конфиги",
            "Pydantic, logging и pytest",
            "Async, типизация, FastAPI и упаковка CLI",
            "Bash: set -euo pipefail, кавычки, циклы, trap",
            "Сценарии траблшутинга: сайт, диск, деплой",
        ],
        "goal": "Писать код и скрипты, которыми можно автоматизировать инфраструктуру и AI-сервисы.",
        "skills": [
            "писать надёжный bash и не молчать об ошибках",
            "вызывать API и внешние команды из Python",
            "оборачивать логику в сервис и тесты",
        ],
        "apply": "Скрипт, который собирает метрики с inference-сервера и отправляет их в мониторинг.",
    },
    {
        "title": "LLM-инженерия",
        "file": "14-LLM-инженерия.md",
        "src": ("new", "14"),
        "topics": [
            "Как модель генерирует текст: токены и вероятности",
            "Контекстное окно и параметры генерации",
            "Роли сообщений и стриминг",
            "Провайдеры, OpenAI-совместимый API и LiteLLM",
            "Промпт-инжиниринг: что такое промпт и как он работает",
            "Context engineering: что такое контекст и как им управлять",
            "Structured output: JSON mode, Pydantic, Instructor",
            "Галлюцинации, seed, лимиты и кэширование",
            "Fine-tuning против RAG, выбор модели",
            "Трансформер, KV-cache, батчинг, квантизация",
        ],
        "goal": "Обращаться с моделью как с управляемым сервисом: знать цену, задержки и ограничения.",
        "skills": [
            "считать токены и стоимость запроса",
            "получать валидируемый JSON вместо текста",
            "выбирать модель и режим под задачу",
        ],
        "apply": "Посчитать стоимость агента на 1000 запросов и понять, где сократить контекст.",
    },
    {
        "title": "Оценка качества LLM",
        "file": "15-Evaluation.md",
        "src": ("new", "15"),
        "topics": [
            "Зачем eval и почему автотесты не работают",
            "Golden set и rubric",
            "Метрики: exact match, similarity, LLM-as-judge",
            "promptfoo, Ragas и DeepEval",
            "Eval в CI/CD и порог качества",
            "Оценка RAG и агентов",
            "Синтетика, статистика, дрейф и human-in-the-loop",
        ],
        "goal": "Измерять качество LLM-системы, а не верить на слово.",
        "skills": [
            "собрать golden set по своему домену",
            "прогнать сравнение промптов и моделей",
            "встроить eval в пайплайн и поймать регрессию",
        ],
        "apply": "Гонять golden set при каждом изменении промпта или модели и блокировать деградацию.",
    },
    {
        "title": "RAG",
        "file": "16-RAG.md",
        "src": ("new", "16"),
        "topics": [
            "Зачем RAG и как устроен пайплайн",
            "Эмбеддинги и векторные БД",
            "Чанкинг и overlap",
            "Qdrant, pgvector, Chroma и FAISS",
            "Метрики близости, HNSW и IVF",
            "Гибридный поиск и reranking",
            "Метаданные, multi-tenancy и права",
            "LlamaIndex, обновление индекса и agentic RAG",
            "Продвинутый чанкинг, GraphRAG и масштаб",
        ],
        "goal": "Превратить модель в эксперта по внутренним документам и уметь это измерить.",
        "skills": [
            "собрать RAG руками и через фреймворк",
            "объяснить, где теряется качество: chunking или retrieval",
            "защитить индекс от отравления и утечек",
        ],
        "apply": "Поднять Qdrant в Docker, загрузить документацию проекта и измерить context recall.",
    },
    {
        "title": "MCP и агенты",
        "file": "17-MCP-и-агенты.md",
        "src": ("new", "17"),
        "topics": [
            "Tool calling и MCP: зачем стандарт",
            "Клиент, сервер и transports",
            "Агентский цикл и LangGraph",
            "Готовые MCP-серверы: K8s, Docker, Prometheus",
            "Ошибки инструментов, память и циклы",
            "Human-in-the-loop и sandboxing",
            "Мультиагенты, A2A и наблюдаемость",
            "A2A: протокол «агент — агент» и его отличия от MCP",
            "Безопасность, права, идемпотентность, прод",
        ],
        "goal": "Дать модели руки и не дать ей сломать прод.",
        "skills": [
            "написать MCP-сервер и подключить его к агенту",
            "строить граф агента с fallback и лимитами",
            "объяснять approval-gate и least privilege",
        ],
        "apply": "Агент, который по запросу «почему упал под» вызывает MCP-инструмент, читает логи и делает RCA.",
    },
    {
        "title": "Harness-инжиниринг",
        "file": "18-Harness-инжиниринг.md",
        "src": ("new", "18"),
        "topics": [
            "Что такое harness и harness engineering",
            "Harness против фреймворка и модели",
            "Компоненты: prompt, tools, контекст, цикл, память",
            "Права, sandbox и approvals",
            "Ошибки, лимиты, checkpoint и resume",
            "Телеметрия и тестирование harness",
            "Coding-агенты: Claude Code, Codex, Cursor",
            "Безопасность и антипаттерны",
        ],
        "goal": "Собрать надёжную обвязку вокруг модели, а не просто «хороший промпт».",
        "skills": [
            "объяснять, из чего состоит harness и зачем каждый компонент",
            "проектировать инструменты, контекст и лимиты",
            "тестировать и трассировать агента",
        ],
        "apply": "Собрать harness для агента, который читает логи и предлагает фикс, с sandbox и approval-gate.",
    },
    {
        "title": "Разработка больших проектов с ИИ",
        "file": "19-AI-проекты.md",
        "src": ("new", "19"),
        "topics": [
            "Spec-driven development и постановка задачи",
            "AGENTS.md, CLAUDE.md и контекст репозитория",
            "Декомпозиция, plan/act/review",
            "Параллельные агенты и git worktree",
            "Тесты, CI и code review сгенерированного кода",
            "Память проекта, ADR и безопасность",
            "Стоимость, метрики и мультиагентность",
            "Кейс: от идеи до деплоя с ИИ",
        ],
        "goal": "Вести большой проект с ИИ так, чтобы он не разваливался от скорости изменений.",
        "skills": [
            "писать спеку и критерии готовности",
            "декомпозировать работу и проверять результат",
            "держать контекст проекта и не сливать секреты",
        ],
        "apply": "Провести фичу через пайплайн «спека → задачи → код → тесты → ревью → деплой» с ИИ.",
    },
    {
        "title": "Локальный хостинг и GPU",
        "file": "20-Local-GPU.md",
        "src": ("new", "20"),
        "topics": [
            "Зачем локальный хостинг и когда он проигрывает API",
            "Ollama, LM Studio, GGUF и llama.cpp",
            "Требования к VRAM и пропускной способности",
            "vLLM, TGI, SGLang и PagedAttention",
            "vLLM в Docker и Kubernetes",
            "GPU Operator, MIG и time-slicing",
            "Spot-инстансы и model registry",
            "DCGM, TTFT, tensor parallelism и экономика GPU",
        ],
        "goal": "Поднять модель на своём железе и не разорить компанию.",
        "skills": [
            "объяснять, что даёт PagedAttention и continuous batching",
            "запросить GPU в K8s и проверить, что она не простаивает",
            "считать cost per 1M токенов",
        ],
        "apply": "Задеплоить vLLM в Kubernetes и сравнить latency и throughput с Ollama на одной модели.",
    },
    {
        "title": "LLM Observability и AIOps",
        "file": "21-LLM-Observability-AIOps.md",
        "src": ("new", "21"),
        "topics": [
            "Чем LLM observability отличается от обычной",
            "Трейсы, spans и путь одного запроса",
            "Логирование промптов, PII и секреты",
            "Метрики: TTFT, latency, tokens/s, cost",
            "Langfuse, LangSmith и Phoenix",
            "Дашборды, алерты и обратная связь",
            "Галлюцинации, RCA-агенты и атрибуция стоимости",
        ],
        "goal": "Видеть, что делает LLM-система в проде, и находить дорогие и медленные шаги.",
        "skills": [
            "строить трейс запроса и агента",
            "настраивать алерты на стоимость и деградацию",
            "объяснять, как работает AIOps-агент",
        ],
        "apply": "Обернуть все вызовы LLM в Langfuse и найти самый дорогой шаг агента.",
    },
    {
        "title": "AI Security",
        "file": "22-AI-Security.md",
        "src": ("new", "22"),
        "topics": [
            "Новые поверхности атаки в AI",
            "Prompt injection: direct и indirect",
            "Недоверие к выводу модели",
            "Jailbreak и защита системного промпта",
            "PII, DLP и guardrails",
            "Безопасность RAG и агентов",
            "Аудит, GDPR, supply chain и red teaming",
        ],
        "goal": "Не допустить, чтобы модель или агент стали дырой в безопасности.",
        "skills": [
            "объяснять indirect prompt injection через документы",
            "ставить guardrails и least privilege",
            "проводить red teaming LLM-приложения",
        ],
        "apply": "Добавить input-guardrail против инъекций и аудит-лог всех действий агента.",
    },
    {
        "title": "AI FinOps",
        "file": "23-AI-FinOps.md",
        "src": ("new", "23"),
        "topics": [
            "Из чего складывается стоимость LLM",
            "Cost per request, user и tenant",
            "Model routing и fallback",
            "Кэш, batch API и prompt caching",
            "Бюджеты, quotas и алерты",
            "Оптимизация промптов в деньгах",
            "GPU против API и chargeback",
        ],
        "goal": "Сделать AI-нагрузку предсказуемой по деньгам.",
        "skills": [
            "считать unit-экономику LLM-фичи",
            "настраивать routing и лимиты",
            "объяснять, когда локальный GPU дешевле API",
        ],
        "apply": "Настроить routing: простые запросы — на дешёвую локальную модель, сложные — на дорогую облачную.",
    },
]


def source_items(src):
    kind = src[0]
    if kind == "old":
        _, lo, hi = src
        return [(OLD[n][0], OLD[n][1]) for n in range(lo, hi + 1)]
    if kind == "new":
        return [(lvl, text) for lvl, text in NEW[src[1]]]
    if kind == "mix13":
        items = [(lvl, text) for lvl, text in NEW["13"]]
        items += [(OLD[n][0], OLD[n][1]) for n in range(340, 346)]
        items += [(OLD[n][0], OLD[n][1]) for n in range(346, 350)]
        items.sort(key=lambda x: RANK[x[0]])
        return items
    raise ValueError(src)


def build():
    number = 1
    for chapter in CHAPTERS:
        items = source_items(chapter["src"])
        chapter["items"] = []
        for lvl, text in items:
            chapter["items"].append((number, lvl, text))
            number += 1
    total = number - 1
    if total != TOTAL_EXPECTED:
        raise SystemExit(f"Ожидалось {TOTAL_EXPECTED} вопросов, получилось {total}")

    # --- IT-DEVOPS.txt ---
    header = (
        "Привет! Ниже — единый план обучения DevOps + AI (редакция от 10 ноября 2026).\n"
        "ГЛАВНАЯ ЦЕЛЬ — подготовить меня к собеседованию на junior DevOps и вырасти в DevOps + AI инженера.\n"
        "Список разложен по 23 главам и пронумерован сквозным списком (1–546).\n"
        "Эти вопросы я скидываю в чаты ИИ и учусь с телефона в свободное время.\n"
        "\n"
        "Правила работы:\n"
        "1. ВСЕ ВОПРОСЫ УЖЕ ПРОНУМЕРОВАНЫ. Не перенумеровывай их, не меняй порядок и не сжимай список — работай строго по готовым номерам.\n"
        "2. Идём по одному вопросу за раз. Не отвечай на всё сразу и не забегай вперёд.\n"
        "3. Формат объяснений: «на пальцах» — максимально просто, с жизненными аналогиями и примерами. Сначала короткий ответ, затем объяснение.\n"
        "4. Без интерактива: никаких тестов, квизов и опросников — с телефона на них неудобно отвечать. Просто выдавай качественную порцию теории.\n"
        "5. В конце каждого ответа напоминай, какой вопрос разобрали и какой номер следующий, и жди команды «Дальше».\n"
        "6. Если вопрос устарел, избыточен или дублирует другой — скажи об этом и предложи пропустить или заменить.\n"
        "7. Цель — DevOps + AI: мы не готовим data scientist, а учимся эксплуатировать LLM, RAG, агентов и GPU-инфраструктуру.\n"
        "\n"
        "Дальше идут главы.\n\n"
    )
    lines = [header]
    for idx, chapter in enumerate(CHAPTERS, start=1):
        first = chapter["items"][0][0]
        last = chapter["items"][-1][0]
        lines.append(f"Глава {idx}: {chapter['title'].upper()}\n")
        for num, lvl, text in chapter["items"]:
            lines.append(f"{num}•[{lvl}] {text}\n")
        lines.append("\n")
    (ROOT / "IT-DEVOPS.txt").write_text("".join(lines), encoding="utf-8")

    # --- тест/ ---
    OUT_DIR.mkdir(exist_ok=True)
    for old_file in OUT_DIR.glob("*.md"):
        old_file.unlink()
    for idx, chapter in enumerate(CHAPTERS, start=1):
        first = chapter["items"][0][0]
        last = chapter["items"][-1][0]
        count = len(chapter["items"])
        part = []
        part.append(f"# Глава {idx}. {chapter['title']}\n\n")
        part.append(f"> Курс: DevOps + AI. Вопросы {first}–{last} из {total}.\n")
        part.append("> Нумерация сквозная — не менять, не переставлять.\n\n")
        part.append("## Темы блока\n\n")
        for topic in chapter["topics"]:
            part.append(f"- {topic}\n")
        part.append("\n---\n\n")
        for num, lvl, text in chapter["items"]:
            part.append(f"{num}•[{lvl}] {text}\n\n")
        (OUT_DIR / chapter["file"]).write_text("".join(part).rstrip() + "\n", encoding="utf-8")

    # --- оглавление ---
    toc = ["| Глава | Название | Вопросы | Кол-во |", "|---|---|---|---|"]
    for idx, chapter in enumerate(CHAPTERS, start=1):
        first = chapter["items"][0][0]
        last = chapter["items"][-1][0]
        toc.append(f"| {idx} | {chapter['title']} | {first}–{last} | {len(chapter['items'])} |")
    toc_text = "\n".join(toc)

    master = f"""# МАСТЕР-ПРОМТ: подготовка к собеседованию junior DevOps и рост в DevOps + AI

Ты — опытный DevOps/SRE-инженер, который также строит LLM-приложения и AI-инфраструктуру. Ты терпеливый наставник. Я готовлюсь к собеседованию на junior DevOps и хочу вырасти в DevOps + AI инженера. Учусь с телефона.

В этом чате я отправляю тебе этот мастер-промт и **один файл с блоком вопросов**. Работай только с вопросами из этого блока.

**Общайся со мной только на русском языке** — все объяснения, примеры, уточнения и вопросы. Технические термины можно оставлять в оригинале, но пояснять их нужно по-русски.

## Главная цель

Не «пройти список», а научить меня объяснять тему своими словами так, чтобы я выдержал вопросы на собеседовании и мог применить это на работе.

## Правила

1. Вопросы пронумерованы сквозным списком (1–{total}) и разложены по 23 главам. Не перенумеровывай их, не меняй порядок, не объединяй и не сжимай список.
2. Идём по одному вопросу за раз. Не отвечай на несколько вопросов сразу и не забегай вперёд.
3. Отвечай на русском, простым языком, без лишней академической теории. Сначала короткий ответ, потом объяснение.
4. Не генерируй тесты, квизы и опросники. Мне неудобно отвечать на них с телефона.
5. В конце каждого ответа пиши: какой вопрос разобрали, какой номер следующий, и жди команды «Дальше».
6. Если вопрос устарел, избыточен для junior-собеседования или дублирует другой — скажи об этом открыто и предложи пропустить или заменить.
7. Если я не понял — объясни иначе: короче, с другой аналогией, с другим примером. Не повторяй тот же текст.
8. Не выдумывай факты. Если не уверен в деталях (версии, лимиты, поведение облака) — прямо скажи, что это зависит от версии или провайдера.
9. Не запоминай и не отслеживай мой прогресс между чатами. Не спрашивай «где мы остановились». В каждом новом чате старт одинаковый: темы или номер.
10. Не пересказывай весь блок и не выдавай «план обучения» без моей просьбы. Мы идём по вопросам.

## Формат ответа на один вопрос

**Короткий ответ.** 1–3 предложения — суть, которую можно сказать на собеседовании.

**Разбор «на пальцах».** Простое объяснение с аналогией из жизни: почему это так работает и зачем нужно.

**Пример.** Короткий практический пример: команда, конфиг, ситуация из работы.

**Где применить.** 1–2 предложения: как это используется в реальном проекте или pet-проекте.

**Цена и метрики.** Для глав 14–21 обязательно: токены, latency, throughput, деньги. Для глав 1–13 — только если уместно.

**Запомнить.** Одна строка — главная мысль, которую нельзя забыть.

## Команды

- «Темы» — краткий список тем блока.
- Номер вопроса (например, `412`) — сразу разбор этого вопроса.
- «Дальше» — дай следующий вопрос блока.
- «Повтори» — объясни текущий вопрос заново, другими словами.
- «Короче» — сожми ответ до сути.
- «Подробнее» — углуби разбор текущего вопроса.
- «Пример» — добавь практический пример или мини-сценарий.
- «Пропустить» — перейди к следующему вопросу.
- «Стоп» — остановись и жди.

## Старт

После того как прочитаешь этот мастер-промт, **не отвечай на вопросы**. Скажи коротко: «Понял. Пришли файл блока — покажу темы и спрошу, с чего начать».

После того как я пришлю файл блока:

1. Напиши название главы, диапазон номеров и количество вопросов.
2. Спроси: «Показать краткий список тем блока или начнём с конкретного номера? Если знаешь номер — просто назови его.»
3. Не начинай разбор, пока я не выберу «Темы» или не назову номер.
4. Если номер относится к другой главе — скажи, какая это глава, и попроси прислать её файл.
5. Если номер вне диапазона 1–{total} — скажи, что такого вопроса нет.

## Оглавление курса

{toc_text}

**Всего: {total} вопросов.** Файлы глав загружаются по одному и содержат только вопросы своей главы.
"""
    (OUT_DIR / "00-Мастер-промт.md").write_text(master, encoding="utf-8")

    # --- роадмап ---
    road = []
    road.append("# РОАДМАП: DevOps + AI\n\n")
    road.append("Курс собран под цель: дойти до уровня junior DevOps и вырасти в DevOps + AI инженера. Учёба идёт с телефона: один чат = мастер-промт + один файл главы.\n\n")
    road.append("## Как устроен курс\n\n")
    road.append("- **23 главы, {total} вопросов**, сквозная нумерация.\n".format(total=total))
    road.append("- **Часть I (главы 1–13)** — фундамент DevOps: Linux, сети, Git, Docker, Kubernetes, IaC, облако, CI/CD, БД, мониторинг, GitOps, философия, Python/Bash.\n")
    road.append("- **Часть II (главы 14–23)** — AI-слой: LLM-инженерия, оценка качества, RAG, MCP и агенты, harness-инжиниринг, разработка больших проектов с ИИ, GPU, observability/AIOps, безопасность, FinOps.\n")
    road.append("- Внутри каждой главы вопросы идут от `[БАЗА]` к `[МИДЛ]`.\n\n")
    road.append("## Почему такой порядок\n\n")
    road.append("Сначала фундамент: без Linux, сети и контейнеров не отладить ни inference-сервер, ни агента. Затем Python — язык вызова LLM API, RAG и MCP-серверов. Дальше AI-слой растёт монотонно: API → оценка → retrieval → агенты → harness → большие проекты → GPU-инфраструктура → эксплуатация → безопасность → деньги.\n\n")

    road.append("## Глоссарий: где про что\n\n")
    road.append("| Термин | Глава |\n|---|---|\n")
    road.append("| Промпт, токены, контекст | 14 |\n")
    road.append("| Evaluation | 15 |\n")
    road.append("| RAG | 16 |\n")
    road.append("| MCP, агенты, A2A | 17 |\n")
    road.append("| Harness, harness engineering | 18 |\n")
    road.append("| Большие проекты с ИИ, best practices | 19 |\n")
    road.append("| GPU, vLLM, инференс | 20 |\n")
    road.append("| Observability, AIOps | 21 |\n")
    road.append("| AI Security | 22 |\n")
    road.append("| AI FinOps | 23 |\n\n")

    road.append("## Карта курса\n\n")
    road.append(toc_text + "\n\n")

    for part_title, start, end in (("Часть I. Фундамент DevOps", 1, 13), ("Часть II. AI-слой", 14, 23)):
        road.append(f"## {part_title}\n\n")
        for idx in range(start, end + 1):
            chapter = CHAPTERS[idx - 1]
            first = chapter["items"][0][0]
            last = chapter["items"][-1][0]
            road.append(f"### Глава {idx}. {chapter['title']}\n\n")
            road.append(f"**Вопросы:** {first}–{last} · **Файл:** `{chapter['file']}`\n\n")
            road.append(f"**Цель:** {chapter['goal']}\n\n")
            road.append("**Что освоить:**\n\n")
            for skill in chapter["skills"]:
                road.append(f"- {skill}\n")
            road.append(f"\n**Как применить:** {chapter['apply']}\n\n")

    road.append("## Как учиться\n\n")
    road.append("1. Открой новый чат и отправь `00-Мастер-промт.md` целиком.\n")
    road.append("2. Отправь файл нужной главы, например `16-RAG.md`.\n")
    road.append("3. Выбери «Темы» или назови номер вопроса. Если номер забыл — посмотри оглавление в мастер-промте.\n")
    road.append("4. После каждого разбора говори «Дальше» или задавай уточнения.\n")
    road.append("5. Когда контекст чата закончился — новый чат, снова мастер-промт и файл главы, номер назови сам.\n\n")

    road.append("## Минимальный маршрут до junior DevOps\n\n")
    road.append("Главы 1–5, 8, 9, 10, 12 — ядро для собеседования. Главы 6, 7, 11, 13 — усиливают и добавляют практику.\n\n")
    road.append("## Маршрут до DevOps + AI\n\n")
    road.append("Ядро выше + главы 14, 15, 16, 17, 18, 19. Главы 20–23 — то, что отличает инженера, который «подключил API», от того, кто умеет это эксплуатировать.\n")
    (OUT_DIR / "00-Роадмап.md").write_text("".join(road), encoding="utf-8")

    # --- README ---
    readme = f"""# Курс: DevOps + AI

Подготовка к собеседованию junior DevOps с ростом в DevOps + AI инженера.
**23 главы, {total} вопросов**, сквозная нумерация 1–{total}.

Учёба рассчитана на телефон: один чат = мастер-промт + один файл главы.

## Структура проекта

~~~
IT-DEVOPS.txt   # полный список: 23 главы, 546 вопросов
тест/           # мастер-промт, роадмап и 23 файла глав
_build/         # сборщик и исходники (не часть курса)
README.md       # этот файл
~~~

## Быстрый старт

1. Открой новый чат с ИИ.
2. Отправь `тест/00-Мастер-промт.md` целиком.
3. Отправь файл нужной главы, например `тест/16-RAG.md`.
4. ИИ покажет название главы и спросит: «Темы или конкретный номер?».
5. Ответь «Темы» или назови номер (например, `412`). Дальше — «Дальше» и уточнения.

## Пример диалога

~~~
Ты:   [тест/00-Мастер-промт.md]
ИИ:   Понял. Пришли файл блока — покажу темы и спрошу, с чего начать.
Ты:   [тест/16-RAG.md]
ИИ:   Глава 16. RAG — вопросы 405–429, 25 штук. Показать темы или начнём с номера?
Ты:   412
ИИ:   [разбор 412] ... Разобрали 412, следующий 413. Жду «Дальше».
~~~

## Команды

| Команда | Что делает |
|---|---|
| «Темы» | краткий список тем главы |
| `412` | разбор конкретного вопроса |
| «Дальше» | следующий вопрос главы |
| «Повтори» | объяснить текущий вопрос иначе |
| «Короче» | сжать ответ до сути |
| «Подробнее» | углубить разбор |
| «Пример» | добавить практический пример |
| «Пропустить» | перейти к следующему вопросу |
| «Стоп» | остановиться |

## Файлы

| Файл | Что внутри |
|---|---|
| `IT-DEVOPS.txt` | полный список вопросов одним файлом |
| `тест/00-Мастер-промт.md` | правила, формат ответа, команды, оглавление |
| `тест/00-Роадмап.md` | главы, цели, навыки, как применить, маршруты, глоссарий |
| `тест/01-Linux.md` … `тест/13-Python-Bash-сценарии.md` | фундамент DevOps |
| `тест/14-LLM-инженерия.md` … `тест/23-AI-FinOps.md` | AI-слой |
| `_build/` | сборщик, новые вопросы и исходники |
| `README.md` | этот файл |

## Карта курса

{toc_text}

## Маршруты

- **Минимум до junior DevOps:** главы 1–5, 8, 9, 10, 12 — ядро собеседования.
- **Усиление:** главы 6, 7, 11, 13 — IaC, облако, GitOps, Python/Bash.
- **DevOps + AI:** ядро + главы 14–19 — LLM, eval, RAG, агенты, harness, проекты.
- **Эксплуатация AI:** главы 20–23 — GPU, observability, безопасность, деньги.

## Глоссарий: где про что

| Термин | Глава |
|---|---|
| Промпт, токены, контекст | 14 |
| Evaluation | 15 |
| RAG | 16 |
| MCP, агенты, A2A | 17 |
| Harness, harness engineering | 18 |
| Большие проекты с ИИ, best practices | 19 |
| GPU, vLLM, инференс | 20 |
| Observability, AIOps | 21 |
| AI Security | 22 |
| AI FinOps | 23 |

## Правила курса

- Вопросы идут по одному, без квизов и тестов.
- Внутри главы порядок: `[БАЗА]` → `[ДЖУН]` → `[МИДЛ]`.
- Нумерация сквозная и не меняется во время обучения.
- Прогресс между чатами не сохраняется — это нормально.
- ИИ общается только на русском.

## Если что-то пошло не так

- **Забыл номер** — открой оглавление в мастер-промте или карту курса выше.
- **Номер из другой главы** — ИИ скажет, какая это глава, и попросит её файл.
- **Контекст чата закончился** — новый чат, снова мастер-промт и файл главы.
- **Ответ слишком длинный** — скажи «Короче».
- **Непонятно** — скажи «Повтори» или «Подробнее».
- **ИИ начал не с того вопроса** — просто назови нужный номер.

## Если хочешь править курс

Файлы `IT-DEVOPS.txt` и папка `тест/` генерируются сборщиком. Менять их вручную можно, но при следующей пересборке правки потеряются.

- Скрипт и новые вопросы: `_build/`
- Памятка для ИИ-агента: `_build/AGENT.md`
- Старые вопросы: `_build/source/`
- Пересборка из корня проекта: `python3 _build/build.py`

## Важно

- `IT-DEVOPS.txt` и `тест/` — генерируемые.
- Исходный список старых вопросов лежит в `_build/source/`.
- `forcopy.txt` и `forsave.yml` — личные файлы, к курсу не относятся.
"""
    (ROOT / "README.md").write_text(readme, encoding="utf-8")

    print(f"OK: {total} вопросов, {len(CHAPTERS)} глав")
    for idx, chapter in enumerate(CHAPTERS, start=1):
        first = chapter["items"][0][0]
        last = chapter["items"][-1][0]
        print(f"{idx:2d}. {chapter['title']}: {first}-{last} ({len(chapter['items'])})")


if __name__ == "__main__":
    build()
