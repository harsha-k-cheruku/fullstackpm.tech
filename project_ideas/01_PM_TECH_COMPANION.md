# Project Idea: PM Tech Companion

**Status:** Early Stage Concept
**Created:** 2026-02-14
**Owner:** Harsha Cheruku

---

## The Problem

PMs face a knowledge gap when building products:

- **Writing specs without technical literacy** — They describe features without understanding the engineering effort, database complexity, or infrastructure needs
- **Miscommunicating with engineers** — Vague timelines, unclear scope, surprises during implementation
- **Making bad trade-offs** — Choosing features without understanding the technical debt or architectural implications
- **Slow decision-making** — Every technical question requires an engineer to explain, blocking progress
- **Scaling uncertainty** — Building for 10 users looks nothing like building for 1M users, but PMs often don't know which constraints matter

**The insight:** Most PMs would make better decisions if they understood the technical story behind their feature—not to *become* engineers, but to **orient themselves in the technical landscape**.

---

## The Solution: PM Tech Companion

An AI-powered tool that translates PM intent into technical architecture. A PM describes what they want to build, provides their tech stack, and the tool responds with:

1. **Technical Breakdown** — What needs to be built, why, and how components connect
2. **Multiple Build Paths** — MVP (2 weeks), Scalable (6 weeks), Enterprise (3+ months)
3. **Effort Estimates** — Side-by-side: "SDE Team" vs "Full Stack PM + AI"
4. **Architecture Narrative** — A story explaining *why* each component is needed
5. **Trade-off Analysis** — What you gain/lose with each approach
6. **Risk & Mitigation** — What could go wrong and how to prevent it
7. **Testing & Deployment Strategy** — How to ship with confidence

**The format:** Conversational, visual, detailed but digestible. Like a technical design doc, but written *for* PMs, not *by* engineers.

---

## Why This Matters

### For Product Teams
- **Faster decisions** — Technical understanding at decision-making speed
- **Better estimates** — Timelines are tied to technical reality, not wishful thinking
- **Aligned teams** — Engineers and PMs speak the same language
- **Fewer surprises** — Technical debt is visible upfront, not discovered mid-sprint

### For Full Stack PMs
- **Prototype with confidence** — Understand what's realistic to build yourself vs delegate
- **Learn by doing** — See how real architectures solve real problems
- **Build in public** — Explain your decisions to stakeholders, investors, teams

### For Non-Technical Founders
- **Raise from a position of knowledge** — Understand your tech story before pitching
- **Hire smarter** — Ask engineers better questions
- **Build faster** — Make technical decisions without constant consulting

### For PM Communities
- A reference library of "how to build X" across different tech stacks
- Open-source patterns and architectures
- Crowdsourced wisdom on trade-offs

---

## How It Works

### Input
A PM provides:

```
Feature/Epic: "Allow sellers to upload bulk listings via CSV"

Current Tech Stack:
- Backend: Python + FastAPI
- Database: PostgreSQL
- Frontend: React + TypeScript
- Infrastructure: AWS (EC2, S3)
- Queue: None (synchronous only)

Constraints:
- Timeline: 4 weeks
- Team: 2 engineers
- Scale: 10K sellers max (for now)
- Performance: Uploads should take <30 seconds

Integration Points:
- Already have Stripe integration
- Existing seller notification system
- SQL database with seller schema defined

What matters most?
- Speed of delivery
- Data reliability (no lost listings)
- Seller experience (clear feedback on errors)
```

### Output

The tool generates a comprehensive technical narrative:

---

## Example Output: "Bulk CSV Upload for Sellers"

### 1️⃣ The Problem (Restated)
Sellers currently add listings one-by-one. For a seller with 1,000 products, this is 1,000 form submissions. We want to let them upload via CSV, validate data, and batch-insert into the database.

### 2️⃣ Architecture Overview

```
┌─────────────────┐
│   React App     │  (Frontend)
│  - File picker  │
│  - CSV upload   │
│  - Progress bar │
└────────┬────────┘
         │
         ▼
┌─────────────────────────┐
│   FastAPI Upload API    │
│  - File validation      │
│  - CSV parsing          │
│  - Error handling       │
└────────┬────────────────┘
         │
         ▼
┌──────────────────┐     ┌──────────────────┐
│  PostgreSQL DB   │     │  S3 (file store) │
│  - Listings      │     │  - CSV uploads   │
│  - Upload logs   │     │  - Backup        │
└──────────────────┘     └──────────────────┘
         ▲
         │
    ┌────┴──────────┐
    │ Seller email  │
    │ notification  │
    └───────────────┘
```

### 3️⃣ Component Breakdown

#### Frontend: CSV File Picker + Progress Indicator
**What:** React component for file selection and upload status
**Why:** Users need to see upload progress and validation errors in real-time
**Trade-offs:**
- ✅ Direct feedback keeps sellers engaged
- ⚠️ Adds complexity to error state management

**Estimate:**
- SDE: 2-3 days (design component, handle errors, test)
- Full Stack PM + Claude: 1 day (use Claude to generate component, iterate on UX)

#### Backend: CSV Parser + Validator
**What:** FastAPI endpoint that:
1. Receives CSV file (multipart form)
2. Parses into rows
3. Validates each row (required fields, data types, business rules)
4. Returns success/error list

**Why:** Validation on the server ensures data quality and security
**Trade-offs:**
- ✅ Prevents bad data from reaching database
- ✅ Consistent validation rules (client + server)
- ⚠️ Slower user experience (validation takes time)

**Solutions to the speed problem:**
- Option A: Validate in background job (async) — Seller sees "Upload queued, check back in 5 min" (takes longer overall, better UX)
- Option B: Validate synchronously — Seller waits but knows immediately if data is bad (faster, worse UX during large uploads)
- Recommendation: Option A with progress notifications via WebSocket or polling

**Estimate:**
- SDE: 3-4 days (CSV parsing, validation logic, error handling, testing)
- Full Stack PM + Claude: 2 days (Claude writes validation logic, you iterate rules)

#### Database: New Tables + Schema
**What:**
```sql
CREATE TABLE bulk_uploads (
  id UUID PRIMARY KEY,
  seller_id UUID,
  created_at TIMESTAMP,
  status VARCHAR (pending|processing|success|failed),
  total_rows INT,
  successful_rows INT,
  failed_rows INT
);

CREATE TABLE upload_errors (
  id UUID PRIMARY KEY,
  upload_id UUID,
  row_number INT,
  field_name VARCHAR,
  error_message VARCHAR
);

-- Add to listings table:
ALTER TABLE listings ADD upload_id UUID;
```

**Why:** Track uploads separately from listings so sellers can see what happened
**Trade-offs:**
- ✅ Audit trail and debugging
- ✅ Sellers can understand failures
- ⚠️ Extra tables = more complex queries

**Estimate:**
- SDE: 1 day (schema design, migrations, testing)
- Full Stack PM + Claude: 2 hours (Claude suggests schema, you review)

#### Error Feedback System
**What:** When validation fails, seller sees:
- Row number
- Field name
- What went wrong (e.g., "Price must be > 0")
- Suggestion (e.g., "Did you mean 19.99?")

**Why:** Vague errors like "Invalid data" waste seller time
**Trade-offs:**
- ✅ Better UX, faster fix cycles
- ⚠️ Error messages need careful copywriting

**Estimate:**
- SDE: 2 days (error message generation, formatting, display)
- Full Stack PM + Claude: 1 day (Claude writes error messages, you refine)

#### Notifications + Status Tracking
**What:**
- Email: "Your bulk upload of 500 listings is complete. 498 successful, 2 failed. [View details]"
- In-app: Notification badge + upload history page
- Webhook: Send upload status to their CRM/system if they want

**Why:** Sellers need to know the outcome without polling the dashboard
**Trade-offs:**
- ✅ Asynchronous workflow feels faster
- ⚠️ Needs reliable email/notification system

**Estimate:**
- SDE: 2 days (notification logic, email templates, testing)
- Full Stack PM + Claude: 1 day (Claude writes email template, you design notification UX)

---

### 4️⃣ Three Build Paths

#### Path A: MVP (2 weeks, ~80 hours SDE)
**Goal:** Proof of concept that CSV upload works

**What's included:**
- Basic file picker (HTML file input)
- CSV parser (synchronous)
- Validation (basic: required fields, types)
- Success/error page (simple list)
- Email notification (on completion)

**What's NOT included:**
- Real-time progress
- Error suggestions
- Upload history
- Webhook/integration

**When to choose this:**
- You need to validate the feature quickly
- Low volume (100s of listings max)
- You're OK with sellers waiting during validation

**Estimate:** 2 engineers × 1 week

#### Path B: Scalable (6 weeks, ~240 hours SDE)
**Goal:** Production-ready, handles thousands of sellers

**What's included:**
- Everything from MVP
- Async validation (queue-based)
- WebSocket progress updates
- Rich error messages with suggestions
- Upload history + status page
- Duplicate detection (don't create duplicate listings)
- Retry logic (failed rows can be re-uploaded)

**What's NOT included:**
- Webhooks to external systems
- Advanced duplicate detection (ML-based)
- Rate limiting per seller

**When to choose this:**
- You're shipping to users (not MVP)
- You want to handle growth without rearchitecting
- You care about seller experience

**Estimate:** 2-3 engineers × 3-4 weeks

#### Path C: Enterprise (3+ months, 600+ hours SDE)
**Goal:** Highly available, auditable, integrable

**What's included:**
- Everything from Path B
- Webhook callbacks (notify their systems)
- Rate limiting + quota management
- Audit logging (compliance)
- Data lineage (track where each listing came from)
- Advanced duplicate detection (fuzzy matching)
- Backup/restore functionality
- Integration with data warehouse

**When to choose this:**
- Large enterprise customers require webhooks
- Compliance matters (audit trails)
- You're building a platform business

**Estimate:** 4-6 engineers × 6+ weeks

---

### 5️⃣ Effort Estimates: SDE Team vs Full Stack PM

| Task | SDE Team | Full Stack PM + AI |
|------|----------|-------------------|
| File picker UI | 2-3 days | 1 day (Claude generates) |
| CSV parser | 3-4 days | 1.5 days (Claude writes, you test) |
| Validation logic | 2-3 days | 1 day (Claude parameterizes) |
| Database schema | 1 day | 2 hours (Claude suggests) |
| Error messages | 2 days | 3 hours (Claude writes, you edit) |
| Async queue setup | 3-4 days | 2-3 days (more complex, needs testing) |
| WebSocket updates | 3-4 days | 2-3 days (Claude scaffolds, you integrate) |
| Email notifications | 2 days | 1 day (Claude templates, you send) |
| Testing + QA | 5-7 days | 3-4 days (Claude helps write tests) |
| **Total MVP (Path A)** | **80 hours** | **40-50 hours** |
| **Total Scalable (Path B)** | **240 hours** | **120-150 hours** |

**Key insight:** 50-60% faster with AI, especially on:
- Boilerplate (CSV parsing, error handling)
- Code generation (endpoints, models, queries)
- Documentation and testing

**Bottleneck:** Architecture decisions, integration testing, production debugging still need humans.

---

### 6️⃣ Trade-off Analysis

#### Synchronous vs Asynchronous Validation

| | Synchronous | Asynchronous |
|---|---|---|
| **User sees errors in** | 5-10 seconds | 30-60 seconds (in background) |
| **Max file size** | 1-5 MB (limited by request timeout) | 100+ MB (queue handles it) |
| **Server load** | Spiky (all validation at once) | Smooth (spread over time) |
| **Cost** | Lower (no extra services) | Higher (queue + worker servers) |
| **Complexity** | Simple | Medium |
| **When to use** | MVP, low volume | Production, 10K+ sellers |

**Recommendation:** Start synchronous (Path A), migrate to async at Path B.

#### SQL vs NoSQL for Upload History

| | PostgreSQL | MongoDB |
|---|---|---|
| **Query patterns** | Fixed (upload history, error list) | Flexible |
| **Consistency** | ACID (guaranteed correctness) | Eventual |
| **You already have** | ✅ (using it for listings) | ❌ (adds complexity) |
| **Cost** | Lower (single database) | Higher (manage two systems) |

**Recommendation:** Stay with PostgreSQL.

#### File Storage: Database vs S3

| | Store in DB | Store in S3 |
|---|---|---|
| **Query speed** | Slower (large BLOB) | Fast (separate storage) |
| **Cost** | Higher DB storage | Lower, but S3 retrieval costs |
| **Compliance** | Everything in one place | Distributed (audit harder) |
| **Scalability** | Database can bloat | Scales independently |

**Recommendation:** For MVP, store metadata in DB, CSV file in S3. Keeps database lean.

---

### 7️⃣ Risks & Mitigation

| Risk | Impact | Probability | Mitigation |
|---|---|---|---|
| **Malformed CSV crashes parser** | Upload fails for all sellers | High | Validate file before parsing, add error handling, test with 100+ CSV variations |
| **Duplicate listings created** | Data inconsistency | High | Check if listing exists before insert, add unique constraint on (seller_id, sku) |
| **Large file uploads timeout** | Seller loses data | Medium | Implement chunked uploads, add progress tracking |
| **Validation too strict** | Sellers can't upload valid data | Medium | Use fuzzy matching for fields, provide clear error messages |
| **Database migration breaks** | Old listings become orphaned | Low | Run migrations in background, add rollback plan |
| **Performance degrades with scale** | 10K sellers = slow uploads | Medium | Test with production-scale data, add indexes on seller_id and created_at |

---

### 8️⃣ Testing Strategy

**Unit Tests** (Claude can help write these):
- CSV parser: valid/invalid rows, edge cases (empty file, 1M rows, special characters)
- Validation rules: required fields, type checks, business logic
- Error formatting: message clarity, field names

**Integration Tests**:
- End-to-end: upload → validate → insert → confirm email sent
- Database: verify listings created, errors logged, upload_id linked
- Edge cases: duplicate file upload, concurrent uploads from same seller

**Load Tests**:
- Can system handle 100 concurrent uploads?
- What's the latency at different file sizes (100 rows, 1K, 10K)?
- Database query performance under load?

**Estimate:** 30-40% of development time

---

### 9️⃣ Deployment Strategy

**Stage 1: Internal Testing** (1 week)
- You + 1 engineer test with real CSV files
- Catch bugs, refine error messages
- Test with edge cases (empty files, special characters, 100K rows)

**Stage 2: Beta** (1 week)
- Invite 10-20 power sellers
- Collect feedback on UX
- Monitor for errors
- Measure upload latency

**Stage 3: Gradual Rollout** (2-4 weeks)
- Enable for 10% of sellers
- Monitor error rates, performance
- Increase to 50%, then 100%
- Keep rollback plan ready

**Monitoring:**
- Upload success rate (target: >98%)
- Average upload time (target: <1 minute for 500 listings)
- Error rate by type (duplicates, validation, system)
- Customer feedback (seller satisfaction)

---

## 10️⃣ Why Each Component is Needed

| Component | Why | What fails without it |
|---|---|---|
| **File picker UI** | Sellers need an intuitive way to upload | Manual integration (copy-paste into form) |
| **CSV parser** | Standardized format, easy to use | Sellers have to convert to JSON or API calls |
| **Validation** | Catch errors before database | Bad data pollutes database, manual cleanup |
| **Error feedback** | Sellers know what's wrong | Support tickets ("It didn't work") |
| **Async processing** | Handle large files without timeout | Uploads fail for 1K+ rows |
| **Upload history** | Sellers audit what they uploaded | No visibility into past uploads |
| **Notifications** | Sellers know when it's done | They leave page, forget about upload |
| **Database indexes** | Keep queries fast at scale | Performance degrades as data grows |

---

## Why Build This Tool (PM Tech Companion)

This feature (bulk CSV upload) is a **perfect example** of what PMs need to understand:

- **Scope ambiguity** — "Bulk upload" sounds simple but has 10+ hidden decisions
- **Technical trade-offs** — Synchronous vs async, database schema, file storage
- **Estimation unpredictability** — Why does it take 2 weeks for engineers to explain what you thought would take 2 days?
- **Team alignment** — When everyone understands the architecture, scope creep is easier to spot

**PM Tech Companion solves this by making architectural thinking visible and accessible.**

---

## Next Steps

**Questions to answer before building:**
1. How many sellers will use this monthly? (10? 1000?)
2. What's the typical file size? (100 rows? 10K?)
3. What's the timeline? (2 weeks? 2 months?)
4. Do sellers need real-time progress or is "check back in 5 min" OK?
5. Will we integrate with external systems (CRM, data warehouse)?

**Recommendation:** Start with Path A (MVP), ship in 2 weeks, gather feedback, iterate to Path B.

---

## Key Takeaway

This is not just a technical spec. **It's a story about why the feature matters, what could go wrong, and how to ship with confidence.** This is what PMs need to understand building.

