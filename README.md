<div align="center">

<h1>Mehedi Hasan</h1>

<img src="https://readme-typing-svg.demolab.com?font=JetBrains+Mono&weight=500&size=20&duration=3200&pause=1000&color=A78BFA&center=true&vCenter=true&width=640&height=36&lines=Assalamu+Alaikum+%F0%9F%91%8B;AI-Enabled+Product+Engineer;Business+problem+%E2%86%92+shipped+product;Agents%2C+full+stack%2C+safe+to+ship" alt="AI-Enabled Product Engineer"/>

<p>
I turn business problems into working products, with AI where it pays off.<br/>
Senior Software Engineer at <a href="https://www.cloudapper.ai">CloudApper AI</a> · 5+ years · ex <a href="https://vivasoftltd.com/">Vivasoft</a>
</p>

<a href="https://www.linkedin.com/in/m-hasan-ai/"><img src="https://img.shields.io/badge/LinkedIn-0A66C2?style=flat-square&logo=linkedin&logoColor=white" alt="LinkedIn"/></a>
<a href="mailto:m.hasan.pro1@gmail.com"><img src="https://img.shields.io/badge/Email-18181B?style=flat-square&logo=gmail&logoColor=white" alt="Email"/></a>
<a href="https://huggingface.co/MahdiSUST/mt5-large-bn_sum_total_data"><img src="https://img.shields.io/badge/Hugging_Face-18181B?style=flat-square&logo=huggingface&logoColor=FFD21E" alt="Hugging Face"/></a>
<a href="https://drive.google.com/file/d/1xTqFQoLpLsxBPHjFRH0iulZ7DL1yy0Se/view?usp=sharing"><img src="https://img.shields.io/badge/Résumé-7C3AED?style=flat-square&logo=readdotcv&logoColor=white" alt="Resume"/></a>

</div>

## About me

I'm an **AI-enabled product engineer**. I start from the business problem, not the tool. Then I ship the fix end to end: data, back end, AI and UI.

- **How I work:** learn the workflow and where it hurts. Pick the simplest tech that fixes it. Measure the result.
- **AI where it pays off.** What I've shipped to production:
  - **Agentic copilots** that plan and build apps, forms and workflows from a chat. Tool calling, MCP servers and MCP clients.
  - **Code-execution agents** on LangGraph. They write and run code in **gVisor / Firecracker** sandboxes, with human approval and resumable runs.
  - **RAG & memory:** knowledge bases, embeddings and semantic search, plus a knowledge graph as long-term agent memory.
  - **Multi-model setups:** a LiteLLM gateway across OpenAI and Claude. Reasoner and verifier models check the main agent's work.
  - **Safety & quality:** self-checks, policy guardrails, replay tests, evals and approval gates on risky actions.
  - **Cost & context:** prompt caching, context compaction and per-call cost tracking.
  - **Document & media AI:** PDF and image understanding, field extraction, audio and video transcription.
- **End to end:** 5+ years of **C# / .NET** and **Python** back ends, plus front ends in **React**, **Angular** and **Vue**.
- **Domains I've built for:**
  - **HR & payroll:** attendance, leave and payroll for multi-company SaaS.
  - **Healthcare (HIPAA):** multi-agent workflows with PHI checks and audit trails.
  - **Finance ops:** invoice and document parsing with a human review step.
  - **No-code platforms:** an AI copilot that builds apps, forms and workflows from chat.
  - **Legacy modernization:** agents that read COBOL, PL/I, RPG, VB6 and Delphi code and write the specs for a rebuild.
  - **Identity & security:** central SSO, multi-tenant isolation and compliance (HIPAA, SOC 2, GDPR).
- **Open source:** 28 PRs to AI, developer-tool and Islamic-tech projects, including Microsoft and JetBrains.
- **Teaching:** Industry Expert & Mentor for the World Bank-backed **Edge Program**.
- **Ask me about:** turning a manual workflow into an AI product, agent safety, RAG, .NET architecture.

## Impact in numbers

<table>
<tr>
<td align="center" width="33%"><h2>60K+</h2><sub>users on a central SSO service<br/>.NET · Redis</sub></td>
<td align="center" width="33%"><h2>800+</h2><sub>companies on PIHR HR & payroll<br/>50,000+ users</sub></td>
<td align="center" width="33%"><h2>~100K</h2><sub>invoices parsed at 90% accuracy<br/>3,000+ clients</sub></td>
</tr>
<tr>
<td align="center" width="33%"><h2>20–30%</h2><sub>faster APIs<br/>caching · queues · SQL tuning</sub></td>
<td align="center" width="33%"><h2>~2×</h2><sub>accuracy on Bangla summarization<br/>fine-tuned mT5</sub></td>
<td align="center" width="33%"><h2>Top 5%</h2><sub>LinkedIn C# & OOP assessments<br/>1M+ people</sub></td>
</tr>
</table>

## Open-source contributions

**28 PRs across 11 projects** (4 merged so far), including Microsoft, JetBrains and repos with 70K+ stars. Status badges update live from GitHub.

### AI agents & LLM frameworks

| Project | What I fixed | PR |
|:--|:--|:--|
| [**microsoft/agent-framework**](https://github.com/microsoft/agent-framework) <br/> ![stars](https://img.shields.io/github/stars/microsoft/agent-framework?style=flat-square&label=%E2%98%85) | **Bedrock:** a boto3 session set to `eu-west-1` was sent to `us-east-1` when `BEDROCK_REGION` said so. No error was raised. The session's region now wins. | [![#9967](https://img.shields.io/github/pulls/detail/state/microsoft/agent-framework/9967?label=%239967&style=flat-square)](https://github.com/microsoft/agent-framework/pull/9967) |
| | **Mistral:** `service_url` now reports the endpoint of the injected SDK client, not the default URL. | [![#9968](https://img.shields.io/github/pulls/detail/state/microsoft/agent-framework/9968?label=%239968&style=flat-square)](https://github.com/microsoft/agent-framework/pull/9968) |
| | **Gemini:** with an injected `genai.Client`, a bad env value such as `GOOGLE_GENAI_USE_ENTERPRISE` still crashed construction. Those settings are now skipped. | [![#9969](https://img.shields.io/github/pulls/detail/state/microsoft/agent-framework/9969?label=%239969&style=flat-square)](https://github.com/microsoft/agent-framework/pull/9969) |
| [**HKUDS/DeepTutor**](https://github.com/HKUDS/DeepTutor) <br/> ![stars](https://img.shields.io/github/stars/HKUDS/DeepTutor?style=flat-square&label=%E2%98%85) | Lesson prep broke on reasoning models when `<think>` blocks or prose wrapped the JSON. It now finds the JSON and retries once at the right effort level. | [![#2375](https://img.shields.io/github/pulls/detail/state/HKUDS/DeepTutor/2375?label=%232375&style=flat-square)](https://github.com/HKUDS/DeepTutor/pull/2375) |
| [**calesthio/OpenMontage**](https://github.com/calesthio/OpenMontage) <br/> ![stars](https://img.shields.io/github/stars/calesthio/OpenMontage?style=flat-square&label=%E2%98%85) | The ComfyUI video tool reported request defaults as output metadata. It now reports the real values probed from the file. | [![#885](https://img.shields.io/github/pulls/detail/state/calesthio/OpenMontage/885?label=%23885&style=flat-square)](https://github.com/calesthio/OpenMontage/pull/885) |
| [**tryAGI/LangChain**](https://github.com/tryAGI/LangChain) (C#) <br/> ![stars](https://img.shields.io/github/stars/tryAGI/LangChain?style=flat-square&label=%E2%98%85) | `AddDocumentsFrom*` helpers now take several data sources in one call for RAG ingestion. | [![#639](https://img.shields.io/github/pulls/detail/state/tryAGI/LangChain/639?label=%23639&style=flat-square)](https://github.com/tryAGI/LangChain/pull/639) |

### Developer tools

| Project | What I fixed | PR |
|:--|:--|:--|
| [**JetBrains/thinkrail**](https://github.com/JetBrains/thinkrail) <br/> ![stars](https://img.shields.io/github/stars/JetBrains/thinkrail?style=flat-square&label=%E2%98%85) | **Windows:** "Reveal in file manager" opened Explorer in a hidden window, with no error. The folder window now shows. | [![#1158](https://img.shields.io/github/pulls/detail/state/JetBrains/thinkrail/1158?label=%231158&style=flat-square)](https://github.com/JetBrains/thinkrail/pull/1158) |
| | **Performance:** editor lookup scanned a slow WSL `PATH` on the event loop and froze the host for seconds. It now pre-filters folders with async `readdir`. | [![#1159](https://img.shields.io/github/pulls/detail/state/JetBrains/thinkrail/1159?label=%231159&style=flat-square)](https://github.com/JetBrains/thinkrail/pull/1159) |
| [**Nano-Collective/nanocoder**](https://github.com/Nano-Collective/nanocoder) <br/> ![stars](https://img.shields.io/github/stars/Nano-Collective/nanocoder?style=flat-square&label=%E2%98%85) | **Security:** the VS Code chat webview now sanitizes markdown and blocks remote images. This closes an XSS and tracking-pixel path. | [![#1927](https://img.shields.io/github/pulls/detail/state/Nano-Collective/nanocoder/1927?label=%231927&style=flat-square)](https://github.com/Nano-Collective/nanocoder/pull/1927) |
| | A VS Code manifest default hid the `defaultMode` setting. New sessions now start in the configured mode. | [![#1928](https://img.shields.io/github/pulls/detail/state/Nano-Collective/nanocoder/1928?label=%231928&style=flat-square)](https://github.com/Nano-Collective/nanocoder/pull/1928) |
| [**handsome-rich/claude-buddy**](https://github.com/handsome-rich/claude-buddy) | 10 PRs for a Claude Code desktop companion. A floating pet with status badges, tool-permission allow/deny, Windows autostart and a packaged-exe fix. | [#3–#13](https://github.com/handsome-rich/claude-buddy/pulls?q=is%3Apr+author%3AMahdi-Hasan) |
| [**Pienteger/Crow**](https://github.com/Pienteger/Crow) (C#) | 4 PRs for a build-cleanup CLI. `--ig` now protects removal targets, paths with spaces work, test teardown no longer fails, and a one-line installer. | [✅ #2–#5 merged](https://github.com/Pienteger/Crow/pulls?q=is%3Apr+author%3AMahdi-Hasan) |

### Community & Islamic tech

| Project | What I fixed | PR |
|:--|:--|:--|
| [**quran/quran.com-frontend-next**](https://github.com/quran/quran.com-frontend-next) <br/> ![stars](https://img.shields.io/github/stars/quran/quran.com-frontend-next?style=flat-square&label=%E2%98%85) | **Security:** `.env.example` turned off TLS checks by default. New setups now keep TLS verification on. | [![#3362](https://img.shields.io/github/pulls/detail/state/quran/quran.com-frontend-next/3362?label=%233362&style=flat-square)](https://github.com/quran/quran.com-frontend-next/pull/3362) |
| [**DeenTime**](https://github.com/Aaqibhafeezkhan/DeenTime) | The prayer-time engine gave `NaN` or times hours off. I restored the solar math and checked it against `adhan-js`. | [![#69](https://img.shields.io/github/pulls/detail/state/Aaqibhafeezkhan/DeenTime/69?label=%2369&style=flat-square)](https://github.com/Aaqibhafeezkhan/DeenTime/pull/69) |
| | Fixed three tests that failed on `main`. | [![#70](https://img.shields.io/github/pulls/detail/state/Aaqibhafeezkhan/DeenTime/70?label=%2370&style=flat-square)](https://github.com/Aaqibhafeezkhan/DeenTime/pull/70) |
| [**Ansari**](https://github.com/iaser-ai/ansari) | The API's Postgres pool had no `error` listener. A dropped idle connection became an uncaught exception. It is now logged and the dead client is discarded. | [![#349](https://img.shields.io/github/pulls/detail/state/iaser-ai/ansari/349?label=%23349&style=flat-square)](https://github.com/iaser-ai/ansari/pull/349) |
| [**Mihrab**](https://github.com/MihrabHQ/Mihrab) | Arabic home-screen widgets were not RTL. I traced it to widget rows following the phone's locale, not the app's language. The maintainer shipped a fix based on it. | [![#118](https://img.shields.io/github/issues/detail/state/MihrabHQ/Mihrab/118?label=%23118&style=flat-square)](https://github.com/MihrabHQ/Mihrab/issues/118) |

## Experience

<details open>
<summary><b>CloudApper AI</b> (a division of M2SYS Technology) — Software Engineer & AI Architect · <i>Jun 2026 – Present</i></summary>
<br/>

- Built an **AI app-builder copilot**. It plans and builds apps, forms, workflows and dashboards from a chat, then checks its own work. Serves its tools over **MCP** and calls external MCP servers with per-user auth. *(TypeScript, Fastify, Angular, Postgres, Redis)*
- Built a **sandboxed code agent** on LangGraph. It writes and runs code in **gVisor / Firecracker** sandboxes, with human approval, web search and resumable runs. *(Python, FastAPI, Angular)*
- Set up **multi-model routing** through a LiteLLM gateway across OpenAI and Claude. Reasoner and verifier models review risky changes. Prompt caching, context compaction and per-call cost tracking keep spend in check.
- Designed **agent safety and quality gates**: scoped tool wrappers, approval on destructive actions, blast-radius limits, self-evaluation, policy guardrails and replay tests.
- Built **AI connectors** for the no-code platform: RAG knowledge bases, semantic search, field extraction, media transcription and a code-agent plugin. *(.NET)*
- Architected **Legacy → CloudApper Transform**. A Director agent, 4 domain Supervisors and specialist agents read COBOL, PL/I, RPG, VB6 and Delphi code. They produce validated SRS documents. *(.NET 10, Python, Kafka, LiteLLM, GCP)*
- **Red-teamed** a multi-tenant MCP platform for prompt injection, tool-result poisoning and cross-tenant access. Findings led to sandbox isolation, read-only DB fallback, query sandboxing and workload identity.
- Designed a **dynamic agent engine** on Microsoft Agent Framework, with **A2A** collaboration for HIPAA, SOC 2 and GDPR customers. Agents spawn with least-privilege tools, retry on failure, then hand off to a human.

</details>

<details>
<summary><b>Vivasoft Limited</b> — Software Engineer, .NET & AI · <i>Aug 2021 – May 2026</i></summary>
<br/>

- Built **AI agent microservices** with LLMs, RAG, auto SQL generation and vector DBs. They plug into C# .NET Core platforms via **gRPC**.
- Engineered .NET Core microservices (SOA, Clean Architecture, CQRS) for healthcare and HR platforms.
- Built a central **SSO service** with Redis for **60K+ users**.
- Built eval and test setups: golden datasets for LLM evals, k6 load tests, Grafana dashboards.
- Cut latency **~20%** with Redis caching, RabbitMQ background jobs and SQL tuning.
- Ran CI/CD, Docker and Kubernetes (ACA/AKS) with least-privilege IAM.

</details>

## Featured projects

### At CloudApper AI

<table>
<tr>
<td width="50%" valign="top">

### Legacy → CloudApper Transform
*Multi-agent code modernization*

- A **Director** agent leads 4 domain **Supervisors** and specialist agents.
- Reads legacy **COBOL, PL/I, RPG, VB6 and Delphi** codebases.
- Produces validated SRS and requirement models for the rebuild.
- I surveyed DeepWiki, Sourcegraph Cody, AWS Transform, IBM ADDI and EPAM ART to shape the design.

`.NET 10` `Python` `Kafka` `LiteLLM` `GCP`

</td>
<td width="50%" valign="top">

### Secure multi-tenant MCP agent platform
*Agent safety · red-teaming*

- Red-teamed for prompt injection, tool-result poisoning and cross-tenant access.
- Findings led to sandbox isolation and approval gates on destructive tool calls.
- Read-only DB fallback, query sandboxing and workload identity federation.
- Agent code runs in **gVisor** containers with allowlisted tools.

`MCP` `gVisor` `Microsoft Agent Framework` `GCP`

</td>
</tr>
<tr>
<td width="50%" valign="top">

### Dynamic agent engine & A2A swarm
*Agentic workflows · HIPAA, SOC 2, GDPR*

- Spawns agents on demand, each with its own skills and least-privilege tools.
- Failed tasks retry, then go to a human.
- Agents work together over the **A2A** protocol.
- Tool wrappers limit the blast radius of any one agent.

`Microsoft Agent Framework` `A2A` `MCP` `Python`

</td>
<td width="50%" valign="top">

### Enterprise document pipeline
*Human-in-the-loop extraction*

- **Gemini**-based extraction of fields from enterprise documents.
- Human review gate before any result is saved.

`Gemini` `Python` `GCP`

</td>
</tr>
</table>

### Earlier work & side projects

<table>
<tr>
<td width="50%" valign="top">

### Sybil — Multi-agent healthcare AI
*HIPAA-regulated · production*

- 6 agents with **LangGraph** orchestration and **MCP** tools on ACA/AKS.
- **LiteLLM** gateway for routing, fallback and caching. Hybrid RAG on OpenSearch.
- PHI scanners and calibrated **LLM-as-a-Judge**, traced with OpenTelemetry and Langfuse.
- Document parsing at **90%** accuracy on ~100K invoices.

`Python` `LangGraph` `MCP` `.NET` `Azure Doc Intelligence`

</td>
<td width="50%" valign="top">

### [Self-Orbit](https://github.com/Mahdi-Hasan/self-orbit) — Personal intelligence platform
*Open source*

- **.NET 10** services (Clean Architecture, CQRS, DDD) behind a **YARP** gateway.
- Python **FastAPI** AI engine for embeddings and LLM inference, linked over gRPC.
- Turns text and audio into tasks, expenses and summaries.
- Tested with xUnit, Moq and pytest.

`C#` `Python` `gRPC` `Next.js 15` `Kubernetes`

</td>
</tr>
<tr>
<td width="50%" valign="top">

### PIHR — SaaS HR & payroll
*Enterprise · 800+ companies*

- Payroll, attendance and leave microservices for **50,000+ users**.
- RabbitMQ and Redis on AWS. EF Core and Dapper tuning cut query time **~25%**.
- RAG document search, validated with golden datasets.

`C#` `ASP.NET Core` `RabbitMQ` `Redis` `AWS`

</td>
<td width="50%" valign="top">

### [Bangla text summarization](https://huggingface.co/MahdiSUST/mt5-large-bn_sum_total_data)
*Open NLP research*

- Fine-tuned **mT5-large** on a large Bangla corpus.
- **~2×** accuracy over earlier Bangla summarization models.
- Model is public on Hugging Face.

`Python` `PyTorch` `Transformers` `mT5`

</td>
</tr>
<tr>
<td width="50%" valign="top">

### [SafeTravel Bangladesh API](https://github.com/Mahdi-Hasan/SafeTravel-Bangladesh-API)

- Ranks all 64 districts by temperature and PM2.5 air quality.
- **<500 ms p99** from a pre-computed Redis cache with background sync.
- Clean Architecture and CQRS, with unit, integration and E2E tests.

`.NET 10` `Redis` `Hangfire` `xUnit`

</td>
<td width="50%" valign="top">

### [App Insights MCP for Claude](https://github.com/Mahdi-Hasan/sybil-appinsights-mcp)

- An MCP server to query Azure Application Insights in plain English.
- Ask "show me errors from the last 24 hours" inside Claude.

`Node.js` `MCP` `Azure`

</td>
</tr>
</table>

## Tech stack

<p align="center">
  <b>Languages</b><br/>
  <img src="https://skillicons.dev/icons?theme=dark&i=py,cs,ts,js,java,cpp,go,html,css,bash,powershell" alt="Languages"/>
  <br/><br/>
  <b>Back end & front end</b><br/>
  <img src="https://skillicons.dev/icons?theme=dark&i=dotnet,fastapi,nodejs,nextjs,react,angular,vue,tailwind,vite,rabbitmq,kafka" alt="Back end and front end"/>
  <br/><br/>
  <b>Data, AI & ML</b><br/>
  <img src="https://skillicons.dev/icons?theme=dark&i=postgres,sqlite,mongodb,redis,pytorch" alt="Data and AI"/>
  <br/><br/>
  <b>Cloud & DevOps</b><br/>
  <img src="https://skillicons.dev/icons?theme=dark&i=azure,aws,gcp,docker,kubernetes,terraform,githubactions,gitlab,jenkins,grafana,linux" alt="Cloud and DevOps"/>
  <br/><br/>
  <b>Tools</b><br/>
  <img src="https://skillicons.dev/icons?theme=dark&i=git,github,vscode,visualstudio,postman,vercel,pnpm,vitest" alt="Tools"/>
</p>

| Area | Tools |
|:--|:--|
| **Agent frameworks** | Microsoft Agent Framework, LangGraph (checkpointers, interrupts), LangChain (Python & C#), OpenAI SDKs (Python, .NET), MCP TypeScript SDK |
| **Agent protocols** | MCP (servers, clients, per-user auth, tool tiers, deferred tool loading), A2A |
| **LLMs** | OpenAI, Azure OpenAI, Claude, Gemini, Hugging Face Transformers, mT5, PyTorch |
| **LLM ops** | LiteLLM gateway (routing, fallback, caching), multi-model tiers (reasoner, verifier), prompt caching, context compaction, token budgets, cost tracking, SSE streaming |
| **Agent runtime** | gVisor and Firecracker sandboxes, E2B, tool calling (parallel), human-in-the-loop approvals, resumable runs, thread memory, knowledge graphs, web search (Tavily) |
| **RAG & search** | Embeddings, hybrid search, semantic search, OpenSearch, Solr, Milvus, vector DBs, Neo4j graph DB, Postgres full-text search, auto SQL generation |
| **Document & media AI** | Azure Document Intelligence, OCR, Gemini extraction, PDF and image vision, Office file parsing, audio and video transcription, structured output |
| **AI safety & evals** | Approval gates, least-privilege tools, policy guardrails, red-teaming, PHI scanners, LLM-as-a-Judge, self-evaluation, replay tests, golden datasets |
| **Observability** | OpenTelemetry, Langfuse, Azure App Insights, Grafana |
| **.NET** | ASP.NET Core, Web API, EF Core, Dapper, gRPC, YARP, Hangfire, plugin-based connectors |
| **Python** | FastAPI, Pydantic v2, LangGraph, SQLite, pytest, pytest-asyncio, Jupyter |
| **Node.js** | TypeScript, Fastify, Zod, pnpm, Turborepo, Vitest |
| **Front end** | React, Next.js, Angular, Vue, TypeScript, Tailwind CSS, Framer Motion, Radix UI, Nx monorepos |
| **Messaging** | RabbitMQ, Kafka, event-driven systems |
| **Integrations** | Gmail API, plugin connectors for no-code workflows |
| **Databases** | PostgreSQL, SQL Server, SQLite, MongoDB, Redis, Upstash |
| **Cloud** | Azure (ACA, AKS, Functions, App Insights), AWS, GCP, Vercel |
| **DevOps** | Docker, Kubernetes, Terraform, GitHub Actions, GitLab CI, Jenkins |
| **Architecture** | Microservices, SOA, Clean Architecture, CQRS, DDD, event-driven design |
| **Testing** | xUnit, NUnit, Moq, TDD, pytest, Vitest, k6 load testing, contract tests, LLM replay tests |
| **Governance** | OWASP Top 10 for Agentic Apps, NIST AI RMF, EU AI Act, HIPAA, SOC 2, GDPR |

## Recognition & learning

- **Industry Expert & Mentor**, Edge Program (World Bank / Govt. of Bangladesh). Taught Python and back-end deployment.
- **Aspire Leadership Program**, Harvard University.
- **Top 5%** in C# and OOP on LinkedIn (1M+ people).
- HackerRank: Problem Solving, C#, SQL, Java · Docker & Jenkins (KodeKloud) · Machine Learning (Coursera).
- **800+** problems solved on online judges.
- **B.Sc. in Software Engineering**, Shahjalal University of Science & Technology (CGPA 3.61 / 4.00).

<div align="center">

### Let's talk

Open to **AI product engineering**, **agentic AI** and **full-stack** roles.

<a href="https://www.linkedin.com/in/m-hasan-ai/"><img src="https://img.shields.io/badge/Connect_on_LinkedIn-0A66C2?style=flat-square&logo=linkedin&logoColor=white" alt="LinkedIn"/></a>
<a href="mailto:m.hasan.pro1@gmail.com"><img src="https://img.shields.io/badge/Send_an_email-18181B?style=flat-square&logo=gmail&logoColor=white" alt="Email"/></a>

<img src="https://komarev.com/ghpvc/?username=Mahdi-Hasan&style=flat-square&color=7C3AED&label=Profile+views" alt="Profile views"/>

</div>

