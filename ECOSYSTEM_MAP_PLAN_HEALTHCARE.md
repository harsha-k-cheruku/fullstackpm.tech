# Ecosystem Map Plan: US Healthcare Ecosystem

**For:** Code Puppy | **Priority:** Tier 2 | **Build time:** 4-5 hours
**PM hiring relevance:** Oscar Health, Hims, Teladoc, Epic, Veeva, Change Healthcare, Waystar

---

## Why This Is a Map

The US healthcare system is genuinely incomprehensible to outsiders. The payer-provider-PBM triangle, prior auth, claims rails, and value-based care models all reward a visual architecture over prose. Almost no PM-focused visual reference exists.

---

## Diagrams to Build (5 diagrams)

### Diagram 1: Healthcare Participant Map
**Section ID:** `#participants`
**Type:** Layered architecture (concentric or stacked)

```
┌─────────────────────────────────────────────────┐
│  PATIENTS / CONSUMERS                            │
│  Individuals, Families, Employers                │
├─────────────────────────────────────────────────┤
│  PROVIDERS                                       │
│  Hospitals, Clinics, Physicians, Labs, Pharmacy  │
├─────────────────────────────────────────────────┤
│  PAYERS (INSURANCE)                              │
│  Commercial (UHC, Anthem, Cigna, Aetna)         │
│  Government (Medicare, Medicaid, VA, Tricare)    │
├─────────────────────────────────────────────────┤
│  PHARMACY BENEFIT MANAGERS (PBMs)                │
│  Express Scripts, CVS Caremark, OptumRx          │
├─────────────────────────────────────────────────┤
│  INFRASTRUCTURE                                  │
│  EHR (Epic, Cerner), Claims (Change Healthcare) │
│  Standards (HL7/FHIR), Clearinghouses            │
├─────────────────────────────────────────────────┤
│  PHARMA & DEVICE MANUFACTURERS                   │
│  Drug manufacturers, Medical device companies    │
├─────────────────────────────────────────────────┤
│  REGULATORS                                      │
│  FDA, CMS, HHS, State DOI                        │
└─────────────────────────────────────────────────┘
```

**Content per layer:**
- **Patients:** End consumers. Pay premiums, copays, deductibles. Mostly don't choose their insurer (employer does).
- **Providers:** Deliver care. Bill insurers. Must navigate complex coding (ICD-10, CPT). Hospital systems consolidating rapidly.
- **Payers:** Pay claims. Set reimbursement rates. Negotiate with providers. Commercial (employer-sponsored) vs Government (Medicare/Medicaid).
- **PBMs:** Middlemen for pharmacy benefits. Negotiate drug prices with pharma, manage formularies. Top 3 control ~80% of market. Controversial (opaque pricing).
- **Infrastructure:** EHR systems (Epic has ~35% market share), claims clearinghouses (Change Healthcare processes ~15B claims/year), standards (HL7 FHIR for interoperability).
- **Pharma:** Manufacture drugs/devices. Set list prices. Negotiate rebates with PBMs. Direct-to-consumer advertising (US is one of two countries that allows it).
- **Regulators:** FDA (drug approval), CMS (Medicare/Medicaid rules), HHS (HIPAA privacy), State DOI (insurance regulation).

---

### Diagram 2: Claims Flow — How a Medical Bill Gets Paid
**Section ID:** `#claims`
**Type:** Sequence diagram (like FE Loan Flow)

**Participants (6 columns):** Patient, Provider, Clearinghouse, Payer, PBM (for Rx), Bank

| Step | Actor | Action |
|------|-------|--------|
| 1 | Patient | Visits doctor, receives care |
| 2 | Provider | Documents encounter in EHR (diagnosis + procedure codes) |
| 3 | Provider | Submits claim (CMS-1500 or UB-04 form) to clearinghouse |
| 4 | Clearinghouse | Scrubs claim (validates codes, checks formatting), forwards to payer |
| 5 | Payer | Adjudicates: checks eligibility, applies benefits, calculates allowed amount |
| 6 | Payer | Applies member cost-sharing (deductible, copay, coinsurance) |
| 7 | Payer | Sends EOB (Explanation of Benefits) to patient |
| 8 | Payer | Sends remittance (ERA/835) to provider |
| 9 | Provider | Posts payment, bills patient for remaining balance |
| 10 | Patient | Pays provider (or gets sent to collections) |

**For pharmacy claims (toggle/tab):**
| Step | Actor | Action |
|------|-------|--------|
| 1 | Patient | Presents prescription at pharmacy |
| 2 | Pharmacy | Submits real-time claim to PBM (NCPDP standard) |
| 3 | PBM | Checks formulary, applies copay tier, adjudicates in ~2 seconds |
| 4 | PBM | Returns copay amount to pharmacy |
| 5 | Patient | Pays copay at counter |
| 6 | PBM | Reimburses pharmacy (net of rebates from manufacturer) |

**Key callout:** "Medical claims take 30-90 days to settle. Pharmacy claims settle in 2 seconds. This difference drives entirely different product architectures."

---

### Diagram 3: Prior Authorization Sequence
**Section ID:** `#priorauth`
**Type:** Flow diagram with decision nodes

```
Provider orders treatment/procedure
  │
  ├── Is prior auth required? (check payer rules)
  │     │
  │     ├── NO → Proceed with treatment → Submit claim normally
  │     │
  │     └── YES → Submit prior auth request to payer
  │           │
  │           ├── Payer reviews (clinical criteria, medical necessity)
  │           │     │
  │           │     ├── APPROVED → Proceed with treatment
  │           │     │
  │           │     ├── DENIED → Provider can:
  │           │     │     ├── Accept denial (patient pays or doesn't get treatment)
  │           │     │     ├── Appeal (peer-to-peer review with payer medical director)
  │           │     │     └── External review (independent review organization)
  │           │     │
  │           │     └── PENDING (more info needed) → Provider submits clinical docs
  │           │           └── Average wait: 3-14 days (!!!!)
  │           │
  │           └── Urgent/emergency → Expedited review (24-72 hours)
```

**Key stats to display:**
- 34% of prior auths are initially denied (AMA survey 2024)
- 82% of denials are eventually overturned on appeal
- Average delay: 7 business days
- Prior auth contributes to ~25% of care delays

**Callout:** "Prior auth is one of the most hated processes in healthcare. 82% of initial denials are overturned — meaning the process mostly delays care that should have been approved in the first place."

---

### Diagram 4: Fee-for-Service vs Value-Based Care
**Section ID:** `#ffs-vbc`
**Type:** Two-panel comparison (like adtech advertiser vs publisher)

**Left: Fee-for-Service (FFS)**
- How it works: Provider bills for each service rendered. More services = more revenue.
- Incentive: Volume. Do more procedures, order more tests, see more patients.
- Payment: Per visit, per procedure, per test. Payer reimburses at negotiated rate.
- Quality signal: None built in. Provider gets paid same whether outcome is good or bad.
- Risk holder: Payer (insurer) bears all financial risk.
- Dominance: Still ~60% of US healthcare payments.
- Problem: Misaligned incentives → over-treatment, unnecessary procedures, cost inflation.

**Right: Value-Based Care (VBC)**
- How it works: Provider paid based on outcomes (patient health, cost reduction, quality metrics).
- Incentive: Quality. Keep patients healthy, reduce readmissions, manage chronic conditions.
- Payment models: Shared savings (split cost reduction with payer), bundled payments (one price for full episode), capitation (fixed $ per patient per month).
- Quality signal: Core to payment (HEDIS measures, readmission rates, patient satisfaction).
- Risk holder: Provider bears some/all financial risk.
- Adoption: Growing (~40% of payments), pushed by CMS (Medicare).
- Challenge: Requires population health management, data infrastructure, risk adjustment.

**Between panels:** Spectrum showing the shift:
```
FFS (volume) ←——————————————→ VBC (outcomes)
  │                                    │
  Pay-per-visit   Shared savings   Bundled   Capitation   Global budget
```

---

### Diagram 5: HealthTech Business Models
**Section ID:** `#healthtech`
**Type:** Grid cards (4-6 cards, like TSM Business Models)

1. **D2C Telehealth**
   - Model: Direct-to-consumer (Hims, Ro, Cerebral)
   - Revenue: Subscription or per-visit fee
   - Payer: Patient (often cash-pay, some accept insurance)
   - Value prop: Convenience, privacy, speed
   - Challenge: Clinical quality, regulation, customer acquisition cost

2. **B2B2C Health Platform**
   - Model: Sell to employers/payers, serve their members (Livongo, Omada, Virta)
   - Revenue: Per-employee-per-month (PEPM) fee
   - Payer: Employer or insurer
   - Value prop: Reduce employer healthcare costs via chronic disease management
   - Challenge: Long sales cycle, proving ROI, clinical evidence

3. **Digital Therapeutics (DTx)**
   - Model: FDA-regulated software as treatment (Pear Therapeutics, Akili)
   - Revenue: Per prescription (like a drug), billed to insurance
   - Payer: Insurance (requires formulary placement)
   - Value prop: Clinically proven, prescription-grade
   - Challenge: FDA approval (2+ years), insurance coverage, prescription workflow

4. **EHR / Infrastructure**
   - Model: Software for providers (Epic, Cerner/Oracle Health, athenahealth)
   - Revenue: License fees + implementation + maintenance
   - Payer: Provider organization (hospital, clinic)
   - Value prop: Clinical workflow, billing, compliance
   - Challenge: Switching costs massive (Epic implementations take 2+ years, cost $1B+ for large systems)

5. **Claims & Revenue Cycle**
   - Model: Automate billing/claims for providers (Waystar, Change Healthcare, Availity)
   - Revenue: Per-claim processing fee or subscription
   - Payer: Provider organization
   - Value prop: Faster payment, fewer denials, reduced admin cost
   - Challenge: Integration complexity, regulatory compliance, consolidation pressure

6. **Health Data & Analytics**
   - Model: Aggregate de-identified health data for pharma/payers (Flatiron, Komodo Health, Truveta)
   - Revenue: Data licensing, analytics subscriptions
   - Payer: Pharma companies, payers, researchers
   - Value prop: Real-world evidence, population insights
   - Challenge: Privacy (HIPAA), data quality, patient consent

---

## Color Palette

```css
:root {
  /* Patient (Blue) */
  --hc-patient-bg: #eff6ff;
  --hc-patient-border: #93c5fd;
  --hc-patient-text: #1e40af;

  /* Provider (Green) */
  --hc-provider-bg: #f0fdf4;
  --hc-provider-border: #86efac;
  --hc-provider-text: #15803d;

  /* Payer (Purple) */
  --hc-payer-bg: #faf5ff;
  --hc-payer-border: #d8b4fe;
  --hc-payer-text: #7e22ce;

  /* PBM (Orange) */
  --hc-pbm-bg: #fff7ed;
  --hc-pbm-border: #fdba74;
  --hc-pbm-text: #9a3412;

  /* Infrastructure (Slate) */
  --hc-infra-bg: #f1f5f9;
  --hc-infra-border: #cbd5e1;
  --hc-infra-text: #334155;

  /* Pharma (Rose) */
  --hc-pharma-bg: #fff1f2;
  --hc-pharma-border: #fda4af;
  --hc-pharma-text: #9f1239;

  /* Neutral */
  --hc-card-bg: #ffffff;
  --hc-card-border: #e2e8f0;
  --hc-heading: #0f172a;
  --hc-body: #475569;
  --hc-muted: #64748b;
}
```

---

## Files to Create (8 files)

| File | Purpose |
|------|---------|
| `code/app/static/css/healthcare-ecosystem.css` | CSS with `--hc-*` variables |
| `code/app/templates/resources/healthcare_ecosystem.html` | Main template |
| `code/app/templates/resources/partials/hc_subnav.html` | 5-section subnav |
| `code/app/templates/resources/partials/hc_diagram_participants.html` | Diagram 1 |
| `code/app/templates/resources/partials/hc_diagram_claims.html` | Diagram 2 (tabbed: medical vs pharmacy) |
| `code/app/templates/resources/partials/hc_diagram_priorauth.html` | Diagram 3 |
| `code/app/templates/resources/partials/hc_diagram_ffs_vbc.html` | Diagram 4 |
| `code/app/templates/resources/partials/hc_diagram_healthtech.html` | Diagram 5 |

## Files to Modify

| File | Change |
|------|--------|
| `code/app/routers/resources.py` | Add route: `/resources/ecosystem-maps/healthcare-ecosystem` |
| `code/app/templates/resources/ecosystem_maps.html` | Add Healthcare card to gallery |

## Route

```python
@router.get("/resources/ecosystem-maps/healthcare-ecosystem", response_class=HTMLResponse)
async def healthcare_ecosystem(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        "resources/healthcare_ecosystem.html",
        _ctx(request, title="US Healthcare Ecosystem — PM Visual Guide | fullstackpm.tech",
             current_page="/resources/ecosystem-maps"),
    )
```

## Verification

- [ ] All 5 diagrams render
- [ ] Claims flow is tabbed (medical vs pharmacy)
- [ ] Prior auth shows decision tree with stats
- [ ] FFS vs VBC comparison is clear
- [ ] HealthTech models are 6 distinct cards
- [ ] Dark mode + mobile responsive
- [ ] Gallery updated

