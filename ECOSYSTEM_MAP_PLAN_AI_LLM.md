# Ecosystem Map Plan: AI Product / LLM Ecosystem

**For:** Code Puppy | **Priority:** Tier 2 | **Build time:** 4-5 hours
**PM hiring relevance:** Anthropic, OpenAI, Cohere, Google DeepMind, plus every AI-native product company

---

## Why This Is a Map

The AI landscape changes fast but has a stable architecture: model providers → inference → fine-tuning → orchestration → applications. PMs at AI-native companies need to understand all layers. No PM-focused visual reference exists.

---

## Diagrams to Build (5 diagrams)

### Diagram 1: LLM Infrastructure Stack
**Section ID:** `#stack`
**Type:** Layered architecture

```
┌─────────────────────────────────────────────────────┐
│  APPLICATION LAYER                                    │
│  ChatGPT, Claude.ai, Perplexity, Cursor, Copilot    │
│  Custom apps built on APIs                           │
├─────────────────────────────────────────────────────┤
│  ORCHESTRATION / FRAMEWORK                            │
│  LangChain, LlamaIndex, Vercel AI SDK, Semantic      │
│  Kernel, Agents (MCP, tool use, function calling)    │
├─────────────────────────────────────────────────────┤
│  API / INFERENCE LAYER                                │
│  Anthropic API, OpenAI API, Google Vertex AI,         │
│  Together AI, Groq, Fireworks AI, AWS Bedrock        │
├─────────────────────────────────────────────────────┤
│  MODEL LAYER                                          │
│  Frontier: Claude, GPT-4, Gemini                     │
│  Open: Llama, Mistral, DeepSeek, Qwen               │
│  Specialized: Code (Codex), Image (DALL-E, Midjourney)│
├─────────────────────────────────────────────────────┤
│  FINE-TUNING & CUSTOMIZATION                          │
│  RLHF, DPO, LoRA, full fine-tuning                   │
│  Training providers: Scale AI, Surge, RLHF vendors   │
├─────────────────────────────────────────────────────┤
│  COMPUTE / INFRASTRUCTURE                             │
│  GPUs: NVIDIA (H100, B200), AMD (MI300X)             │
│  Cloud: AWS, GCP, Azure, CoreWeave, Lambda           │
│  Training clusters: custom hardware, networking      │
├─────────────────────────────────────────────────────┤
│  DATA LAYER                                           │
│  Training data: Common Crawl, Books, Code (GitHub)   │
│  Vector DBs: Pinecone, Weaviate, Chroma, pgvector   │
│  Evaluation: MMLU, HumanEval, Arena rankings         │
└─────────────────────────────────────────────────────┘
```

**Content per layer:**
- **Application:** End-user products. Chat interfaces, code assistants, search engines, creative tools. This is where users interact.
- **Orchestration:** Frameworks that glue models to tools, data, and workflows. Agents that can take actions. MCP for tool connectivity.
- **API/Inference:** The delivery layer. Model providers serve predictions via API. Inference optimization (batching, caching, speculative decoding) critical for cost/latency.
- **Model:** Foundation models. Frontier (Claude, GPT-4) vs open-source (Llama, Mistral). Trade-off: capability vs cost vs control.
- **Fine-tuning:** Customize models for specific tasks. RLHF (human feedback), DPO (preference optimization), LoRA (efficient fine-tuning). Scale AI provides training data.
- **Compute:** GPUs are the bottleneck. NVIDIA dominance (H100 $30K each, 12-month waitlists). Cloud providers offer GPU-as-a-service.
- **Data:** Training data (web crawl, books, code). Vector databases for RAG retrieval. Evaluation benchmarks for comparing models.

---

### Diagram 2: AI Product Architecture Patterns
**Section ID:** `#patterns`
**Type:** 4 architecture cards (like TSM business models)

1. **Thin Wrapper**
   - Architecture: UI → API call to frontier model → display response
   - Example: Many early "GPT wrappers" (Jasper v1, Copy.ai v1)
   - Moat: None (anyone can call the same API)
   - Cost: Low (just API fees)
   - PM lesson: Thin wrappers die when the model provider adds the feature natively

2. **RAG-Powered Application**
   - Architecture: UI → query → retrieve relevant docs from vector DB → inject context → LLM generates answer
   - Example: Perplexity (search), Notion AI (workspace context), customer support bots
   - Moat: Proprietary data (your documents, your knowledge base)
   - Cost: Medium (embedding + storage + inference)
   - PM lesson: Data quality determines output quality. RAG garbage in = garbage out.

3. **Agent / Autonomous System**
   - Architecture: User goal → LLM plans steps → executes tools (APIs, code, browser) → validates → returns result
   - Example: Claude Code, Devin (coding), AutoGPT, Operator (web tasks)
   - Moat: Tool ecosystem + reliability engineering
   - Cost: High (multiple LLM calls per task, tool execution)
   - PM lesson: Agents need robust error handling. One wrong tool call cascades.

4. **Fine-Tuned / Custom Model**
   - Architecture: Train specialized model on domain data → serve via own infrastructure
   - Example: Bloomberg GPT (finance), Med-PaLM (healthcare), code models
   - Moat: Domain expertise + training data
   - Cost: Very high (training $1M+, inference infrastructure)
   - PM lesson: Only fine-tune if you have proprietary data AND the frontier model can't do it well enough.

---

### Diagram 3: RAG Pipeline
**Section ID:** `#rag`
**Type:** Flow diagram (animated if possible, like deep dive S2)

```
Documents → Chunking → Embedding → Vector DB (Index)
                                        ↓
User Query → Query Embedding → Similarity Search → Top-K Chunks Retrieved
                                                          ↓
                                    Prompt Assembly (system prompt + retrieved context + user query)
                                                          ↓
                                              LLM Generates Response
                                                          ↓
                                        Post-processing (citations, formatting)
                                                          ↓
                                              Display to User
```

**For each step, explain:**
- **Chunking:** Split documents into 500-2000 token chunks. Overlap by 10-20%. Too small = no context. Too large = noise.
- **Embedding:** Convert text to vector (numerical representation). Models: OpenAI text-embedding-3, Cohere embed, open-source (BGE, E5).
- **Vector DB:** Store embeddings for fast similarity search. Options: Pinecone (managed), Weaviate (open), pgvector (PostgreSQL extension).
- **Similarity Search:** Find chunks most similar to user query. Algorithm: cosine similarity, ANN (approximate nearest neighbor).
- **Prompt Assembly:** Combine system instructions + retrieved chunks + user question into one prompt.
- **Generation:** LLM reads full prompt, generates answer grounded in retrieved context.
- **Post-processing:** Add citations (link to source chunks), format response, filter hallucinations.

**Key callout:** "RAG doesn't eliminate hallucinations — it reduces them. The model can still ignore the retrieved context or confabulate details. Evaluation (checking if the answer is grounded in the sources) is the unsolved hard problem."

---

### Diagram 4: Build vs Buy Decision Map
**Section ID:** `#buildvsbuy`
**Type:** Decision tree / comparison grid

**When to use Frontier Model API (Claude, GPT-4):**
- ✅ General-purpose tasks (summarization, Q&A, writing)
- ✅ Rapid prototyping (ship in days, not months)
- ✅ You don't have proprietary training data
- ✅ Quality matters more than cost
- ❌ Latency-sensitive (API call = 1-10 seconds)
- ❌ Privacy-critical (data sent to third party)

**When to use Fine-Tuned Model:**
- ✅ Consistent style/format needed (e.g., always output JSON)
- ✅ You have 1000+ high-quality examples
- ✅ Domain-specific terminology/knowledge
- ✅ Cost matters at scale (smaller fine-tuned model cheaper than large frontier)
- ❌ You want general capability (fine-tuning narrows, doesn't broaden)
- ❌ Your data changes frequently (retraining is expensive)

**When to use Open-Source Model (Llama, Mistral):**
- ✅ Data privacy required (runs on your infrastructure)
- ✅ Cost optimization at very high volume
- ✅ Customization needed (modify architecture, training)
- ✅ Offline/edge deployment
- ❌ You need frontier-level capability (open-source trails by 6-12 months)
- ❌ You don't have ML engineering team

**When to use RAG (Retrieval-Augmented Generation):**
- ✅ You have proprietary documents (knowledge base, docs, policies)
- ✅ Answers must be grounded/cited
- ✅ Content changes frequently (update docs, not retrain model)
- ✅ You want to use frontier model + your data
- ❌ Your data is unstructured/messy (garbage in = garbage out)

---

### Diagram 5: AI Business Models
**Section ID:** `#bizmodels`
**Type:** Grid cards (like HealthTech models)

1. **API Consumption Pricing**
   - How: Charge per token (input + output). Price per 1M tokens.
   - Example: Anthropic ($3-15/MTok), OpenAI ($2.50-15/MTok), Google ($1.25-5/MTok)
   - Pros: Usage-aligned, scales with value
   - Cons: Unpredictable costs for customer, race to zero on price
   - PM metric: Revenue per token, cost per token, margin

2. **Seat-Based SaaS (AI-Enhanced)**
   - How: Monthly subscription per user, AI features included
   - Example: Notion AI ($10/user/month), GitHub Copilot ($10-39/user/month), Cursor ($20/month)
   - Pros: Predictable revenue, familiar billing model
   - Cons: Heavy users subsidized by light users, margin pressure from inference costs
   - PM metric: AI feature adoption rate, inference cost per user

3. **Outcome-Based Pricing**
   - How: Charge per successful outcome (resolved ticket, generated lead, completed task)
   - Example: Intercom AI ($0.99/resolution), some coding agents charge per PR
   - Pros: Aligned with customer value, easy ROI story
   - Cons: Hard to define "successful outcome," margin unpredictable
   - PM metric: Cost per outcome, outcome success rate

4. **Embedded AI (Co-Pilot Model)**
   - How: AI embedded in existing product as premium tier
   - Example: Salesforce Einstein, Adobe Firefly, Canva Magic
   - Pros: Upsell existing customers, high switching costs
   - Cons: Must justify price increase, customers expect AI "for free" eventually
   - PM metric: Upsell conversion rate, AI feature stickiness

5. **Infrastructure / Platform**
   - How: Sell compute, tools, infrastructure for others to build AI
   - Example: AWS Bedrock, Vercel AI, Pinecone, Scale AI
   - Pros: Pick-and-shovel play (sell to gold miners), platform effects
   - Cons: Commoditization risk, low margins at scale
   - PM metric: Developer adoption, API call volume, retention

---

## Color Palette

```css
:root {
  /* Models (Purple) */
  --ai-model-bg: #faf5ff;
  --ai-model-border: #d8b4fe;
  --ai-model-text: #7e22ce;

  /* Inference/API (Blue) */
  --ai-api-bg: #eff6ff;
  --ai-api-border: #93c5fd;
  --ai-api-text: #1e40af;

  /* Application (Green) */
  --ai-app-bg: #f0fdf4;
  --ai-app-border: #86efac;
  --ai-app-text: #15803d;

  /* Data (Amber) */
  --ai-data-bg: #fffbeb;
  --ai-data-border: #fcd34d;
  --ai-data-text: #b45309;

  /* Compute (Rose) */
  --ai-compute-bg: #fff1f2;
  --ai-compute-border: #fda4af;
  --ai-compute-text: #9f1239;

  /* Orchestration (Indigo) */
  --ai-orch-bg: #eef2ff;
  --ai-orch-border: #a5b4fc;
  --ai-orch-text: #3730a3;

  /* Neutral */
  --ai-card-bg: #ffffff;
  --ai-card-border: #e2e8f0;
  --ai-heading: #0f172a;
  --ai-body: #475569;
}
```

---

## Files to Create (8 files)

| File | Purpose |
|------|---------|
| `code/app/static/css/ai-llm-ecosystem.css` | CSS with `--ai-*` variables |
| `code/app/templates/resources/ai_llm_ecosystem.html` | Main template |
| `code/app/templates/resources/partials/ai_subnav.html` | 5-section subnav |
| `code/app/templates/resources/partials/ai_diagram_stack.html` | Diagram 1: LLM infrastructure stack |
| `code/app/templates/resources/partials/ai_diagram_patterns.html` | Diagram 2: Architecture patterns (4 cards) |
| `code/app/templates/resources/partials/ai_diagram_rag.html` | Diagram 3: RAG pipeline |
| `code/app/templates/resources/partials/ai_diagram_buildvsbuy.html` | Diagram 4: Build vs buy |
| `code/app/templates/resources/partials/ai_diagram_bizmodels.html` | Diagram 5: Business models |

## Files to Modify

| File | Change |
|------|--------|
| `code/app/routers/resources.py` | Add route: `/resources/ecosystem-maps/ai-llm-ecosystem` |
| `code/app/templates/resources/ecosystem_maps.html` | Add AI/LLM card to gallery |

## Verification

- [ ] All 5 diagrams render
- [ ] RAG pipeline shows clear flow from docs → chunking → embedding → retrieval → generation
- [ ] Build vs buy decision map is a clear decision tree
- [ ] Business models cover 5 distinct monetization patterns
- [ ] Dark mode + mobile responsive

