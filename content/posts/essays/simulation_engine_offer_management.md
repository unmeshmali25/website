
---
title: "Simulation Engine & Offer Management System"
date: 2025-12-27T00:00:00+05:30
draft: false
---

## Overview

Implemented a complete simulation engine for testing offer management workflows with persona-based shopping agents. The system enables accelerated time simulation (1 real hour = 1 week simulated time) to model long-term offer lifecycle effects.

## High-Level Architecture Overview (LangGraph + LangSmith)

```
┌─────────────────────────────────────────────────────────────────┐
│                   SimulationOrchestrator (New)                   │
│        Coordinates time advancement + runs LangGraph agents      │
└──────────────────────────┬──────────────────────────────────────┘
                           │
           ┌───────────────┼───────────────┐
           │               │               │
           ▼               ▼               ▼
┌──────────────────┐ ┌────────────────────────────────────────┐
│  OfferScheduler  │ │     LangGraph StateGraph (per agent)   │
│   (Existing)     │ │                                        │
│                  │ │ [decide_shop] ──▶ [browse_products]    │
│ - Time advance   │ │       │                 │              │
│ - Cycle mgmt     │ │    (skip)          [add_to_cart]       │
│ - Offer refresh  │ │       │                 │              │
└──────────────────┘ │       │          [view_coupons]        │
                     │       │                 │              │
                     │       │         [decide_checkout]      │
                     │       │           /         \          │
                     │       │    [complete]    [abandon]     │
                     │       ▼           \         /          │
                     │     [END] ◀───────────────             │
                     └────────────────────────────────────────┘
                           │
                           ▼
              ┌───────────────────────────┐
              │   LangSmith Tracing       │
              │   (Automatic per node)    │
              └───────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                     PostgreSQL Database                          │
│   agents | users | shopping_sessions | shopping_session_events   │
│   user_coupons | offer_cycles | simulation_state                 │
└─────────────────────────────────────────────────────────────────┘
```

# Simulation Layer-Specific Architecture Overview

## Layer 1: Application & API

```
FastAPI Application (app/main.py)

  ┌──────────────────┐      ┌──────────────────────────────────┐
  │ Auth Verification │─────▶│  SIMULATION MODE BYPASS          │
  │ (Supabase JWT)   │      │  Bearer dev:<agent_id>           │
  └──────────────────┘      └──────────────────────────────────┘
           │                              │
           ▼                              ▼
  ┌──────────────────┐      ┌──────────────────────────────────┐
  │ Production Paths │      │  Simulation Paths                 │
  └──────────────────┘      └──────────────────────────────────┘
           │                              │
           ▼                              ▼
  ┌──────────────────┐      ┌──────────────────────────────────┐
  │ Routes:          │      │  Offer Engine Routes              │
  │  • cart          │      │  • /cycles (GET/POST)             │
  │  • orders        │      │  • /cycles/{id}                    │
  │  • stores        │      │  • /refresh/user/{user_id}        │
  └──────────────────┘      │  • /time/advance                   │
                           └──────────────────────────────────┘
```

---

## Layer 2: Simulation Orchestrator

```
SimulationOrchestrator (app/simulation/orchestrator.py)

  ┌────────────────────────────────────────────────────────────────┐
  │  Rich Dashboard (Terminal UI)                                   │
  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐                │
  │  │ Statistics  │ │ Agent List  │ │ Event Log  │                │
  │  │ • Cycles    │ │ • Status    │ │ • Actions  │                │
  │  │ • Checkouts │ │ • Store     │ │ • Errors   │                │
  │  │ • Offers    │ │ • Cart      │ │             │                │
  │  └─────────────┘ └─────────────┘ └─────────────┘                │
  └────────────────────────────────────────────────────────────────┘

  ┌────────────────────────────────────────────────────────────────┐
  │  Time Service                                                   │
  │  • Real Time ───────────────────┐                               │
  │  • Simulated Time ────────▶ 1 hour = 168 hours (1 week)        │
  │  • Coordinate Conversion     │                               │
  └────────────────────────────────┼───────────────────────────────┘
                                    │
  ┌────────────────────────────────▼────────────────────────────────┐
  │  Offer Engine Scheduler                                          │
  │  ┌──────────────────┐  ┌──────────────────┐  ┌───────────────┐  │
  │  │ Cycle Manager    │  │ Expiration      │  │ Offer Assigner│  │
  │  │ • Create cycles  │──▶│ Handler         │──▶│ • Distribute  │  │
  │  │ • Track windows │  │ • Mark expired  │  │   to wallets  │  │
  │  └──────────────────┘  └──────────────────┘  └───────────────┘  │
  └────────────────────────────────────────────────────────────────┘
```

---

## Layer 3: Agent Simulation

```
Agent Pool (Multiple Persona-Based Agents)

  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐
  │ Agent 1  │  │ Agent 2  │  │ Agent 3  │  │ Agent N  │
  │ (Excel   │  │ (Excel   │  │ (Excel   │  │ (Excel   │
  │  Persona)│  │  Persona)│  │  Persona)│  │  Persona)│
  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘
       │             │             │             │
       ▼             ▼             ▼             ▼

  ┌────────────────────────────────────────────────────────────────┐
  │  Agent State (28 Persona Attributes)                            │
  │  • Demographics: age, income, location                        │
  │  • Shopping: frequency, basket_size, impulsivity               │
  │  • Preferences: categories, brands, days_of_week                │
  │  • Psychology: discount_sensitivity, price_consciousness       │
  └────────────────────────────────────────────────────────────────┘
       │             │             │             │
       └─────────────┴─────────────┴─────────────┘
                     │
                     ▼

  ┌────────────────────────────────────────────────────────────────┐
  │  LangGraph Shopping Graph (Decision Workflow)                   │
  │                                                                 │
  │                      ┌──────────┐                                │
  │                      │  Start   │                                │
  │                      └────┬─────┘                                │
  │                           │                                       │
  │                           ▼                                       │
  │                    ┌─────────────┐                               │
  │                    │decide_shop │                               │
  │                    └─────┬───────┘                               │
  │                    Yes│      │No                                │
  │                       ▼      ▼                                   │
  │              ┌────────────┐  ┌────┐                              │
  │              │browse_    │  │END │                              │
  │              │products   │  └────┘                              │
  │              └─────┬──────┘                                       │
  │                   │                                             │
  │                   ▼                                             │
  │           ┌───────────────┐                                     │
  │           │  add_to_cart  │                                     │
  │           └───────┬───────┘                                     │
  │                   │                                             │
  │                   ▼                                             │
  │           ┌───────────────┐                                     │
  │           │ view_coupons  │                                     │
  │           └───────┬───────┘                                     │
  │                   │                                             │
  │                   ▼                                             │
  │         ┌─────────────────┐                                     │
  │         │  decide_checkout│                                     │
  │         └────┬───────┬───┘                                     │
  │              │       │                                         │
  │         Yes  │       │  No                                      │
  │              ▼       ▼                                         │
  │     ┌────────────┐  ┌────┐                                    │
  │     │complete_   │  │END │                                    │
  │     │checkout    │  └────┘                                    │
  │     └────────────┘                                            │
  │                                                                 │
  └────────────────────────────────────────────────────────────────┘
                           │
                           ▼

  ┌────────────────────────────────────────────────────────────────┐
  │  Shopping Actions (Database Operations)                          │
  │  • create_session()      • browse_products()                      │
  │  • add_to_cart()         • apply_coupon()                         │
  │  • view_coupon()         • complete_checkout()                     │
  │  • abandon_session()     • create_event() (ML training data)     │
  └────────────────────────────────────────────────────────────────┘
```

---

## Layer 4: Database Schema

```
NEW TABLES (Migration 007)

┌─────────────────────┐  ┌─────────────────────┐
│ offer_cycles        │  │ user_offer_cycles   │
├─────────────────────┤  ├─────────────────────┤
│ id                  │  │ user_id → users(id) │
│ cycle_number        │  │ current_cycle_id    │
│ started_at          │  │ last_refresh_at     │
│ ends_at             │  │ next_refresh_at     │
│ simulated_start_date│  │ is_simulation       │
│ simulated_end_date  │  └─────────────────────┘
│ is_simulation       │
└─────────────────────┘

┌─────────────────────┐
│ simulation_state    │
├─────────────────────┤
│ simulated_date      │
│ real_start_time     │
│ cycle_number        │
└─────────────────────┘


MODIFIED TABLES

┌─────────────────────────────┐    ┌───────────────────────────────┐
│ user_coupons                 │    │ orders                        │
├─────────────────────────────┤    ├───────────────────────────────┤
│ + status (active/expired/)   │    │ + is_simulated                │
│ + offer_cycle_id             │    │ + simulated_at                │
│ + is_simulation              │    │                               │
└─────────────────────────────┘    └───────────────────────────────┘


EXISTING TABLES (Used by Simulation)

users, agents, products, shopping_sessions,
shopping_session_events, cart_items, coupons
```

---

## Layer 5: Tooling & Utilities

```
┌────────────────────────────────────┐  ┌──────────────────────────────┐
│ seed_simulation_agents.py           │  │ check_db.py                  │
│ • Load Excel personas              │  │ • List tables & row counts   │
│ • Create users & agents            │  │ • Inspect sample data        │
│ • --test flag for quick testing    │  │ • Validate schema            │
└────────────────────────────────────┘  └──────────────────────────────┘
```

---

## Data Flows

```
1. TIME ADVANCEMENT
   Orchestrator ──▶ TimeService ──▶ SimulationState (DB)
                          │
                          └──▶ Coordinate Conversion
                              Real Time ↔ Simulated Time
                              (1 hour = 168 hours = 1 week)

2. OFFER CYCLE MANAGEMENT
   Scheduler ──▶ CycleManager ──▶ OfferAssigner ──▶ user_coupons
                │                │
                │                └─▶ Distribute to wallets
                │                   • frontstore: 2/cycle
                │                   • category-brand: 30/cycle
                └─▶ ExpirationHandler
                    └─▶ Mark expired offers

3. AGENT EXECUTION
   Orchestrator ──▶ ShoppingGraph (LangGraph)
                  │
                  ├─▶ decide_shop
                  ├─▶ browse_products
                  ├─▶ add_to_cart
                  ├─▶ view_coupons
                  ├─▶ decide_checkout
                  └─▶ complete_checkout / abandon_session
                         │
                         ▼
                  Actions ──▶ Database
                         │
                         ├─▶ shopping_sessions
                         └─▶ shopping_session_events (ML training data)

4. AUTHENTICATION FLOW
   HTTP Request ──▶ verify_token()
                      │
         ┌────────────┴────────────┐
         ▼                         ▼
    Production                 Simulation
    (Supabase JWT)              (dev:<agent_id>)
         │                         │
         └───────────┬─────────────┘
                     ▼
               User Context
               (user_id, email)
```

## Core Components

### 1. Offer Engine (Simulation-Only)

**Location:** [`app/offer_engine/`](app/offer_engine/)

- **Scheduler:** Manages 7-day offer cycles with configurable refresh logic
- **Time Service:** Handles simulated time advancement and coordinate conversion
- **Expiration Handler:** Tracks and expires offers based on cycle boundaries
- **Cycle Manager:** Creates new cycles and manages per-cycle coupon allocation
- **Offer Assigner:** Distributes coupons to user wallets (frontstore: 2/cycle, category-brand: 30/cycle)
- **REST API:** Routes for manual cycle management and debugging

### 2. Agent Simulation System

**Location:** [`app/simulation/`](app/simulation/)

- **Shopping Graph:** LangGraph-based workflow with 6 decision nodes:
  - [`decide_shop`](decide_shop) - Shop frequency based on persona (frequent/regular/occasional/rare)
  - [`browse_products`](browse_products) - View products by category preference
  - [`add_to_cart`](add_to_cart) - Add items based on impulsivity score
  - [`view_coupons`](view_coupons) - Check available wallet offers
  - [`decide_checkout`](decide_checkout) - Complete or abandon based on discount sensitivity
  - [`complete_checkout`](complete_checkout)/[`abandon_session`](abandon_session) - Final transaction or cart abandonment
- **Agent Actions:** Database operations for all shopping behaviors
- **State Management:** Tracks persona attributes (28 structured columns from Excel)
- **Orchestrator:** Multi-agent coordinator with rich terminal dashboard (stats, logs, agent status)

### 3. Database Schema

**Migrations:** [`007_offer_engine.sql`](007_offer_engine.sql), [`008_add_simulation_columns_to_orders.sql`](008_add_simulation_columns_to_orders.sql)

**Tables Added:**
- `offer_cycles` - Cycle metadata (start/end, simulated dates)
- `user_offer_cycles` - Per-user cycle tracking with refresh windows
- `simulation_state` - Global simulation calendar/time tracking

**Tables Modified:**
- `user_coupons` - Added `status`, `offer_cycle_id`, `is_simulation` columns
- `orders` - Added `is_simulated`, `simulated_at` columns

### 4. Authentication Enhancement

**File:** [`app/main.py`](app/main.py:291)

Lines 291-304: Added simulation mode bypass. When `SIMULATION_MODE=true`, accepts `Bearer dev:<agent_id>` tokens for agent authentication without Supabase JWT.

## Tooling

[`scripts/seed_simulation_agents.py`](scripts/seed_simulation_agents.py)
- Loads personas from Excel (28 columns: demographics, preferences, shopping habits)
- Creates user entries in `users` table
- Creates agent entries with full persona data
- Supports `--test` flag for 2 test agents or `--count N` for limited seeding

[`scripts/check_db.py`](scripts/check_db.py)
- Database inspection utility
- Lists tables, row counts, and sample data

## Key Features

- ✅ Non-intrusive: Only activates when `SIMULATION_MODE=true`
- ✅ Accelerated simulation: Configurable time scaling (default: 168x)
- ✅ Persona-driven agents: 28 attributes per agent for realistic behavior
- ✅ Rich monitoring: Live dashboard with statistics and agent logs
- ✅ LangGraph integration: Traced decision paths for analysis
- ✅ ML-ready: All shopping events recorded for training data

## Testing Status

- ✅ End-to-end simulation tested with 2 agents
- ✅ Offer cycle creation and refresh working
- ✅ Shopping flow functional (browse → cart → checkout/abandon)
- ⚠️ Agent behavior tuning needed to increase checkout rates

## Environment Variables

```bash
SIMULATION_MODE=true
TIME_SCALE=168
OFFER_CYCLE_DAYS=7
OFFER_EXPIRATION_DAYS=14
MAX_WALLET_CAPACITY=32
FRONTSTORE_PER_CYCLE=2
CATEGORY_BRAND_PER_CYCLE=30
```

{{< collapse maxHeight="800" title="Simulation Test QA, Assumptions, Blindspots, Checklist & Priority Order" >}}

### Q1: What constitutes "agent behavior" for the initial 6-hour test?

**Context**: The offer engine handles coupon assignment/expiration, but agents need to "do something" (shop, browse, redeem coupons) for meaningful data generation.

| Option | Description | Recommendation |
|--------|-------------|----------------|
| **A. Minimal: Offer cycling only** | Agents exist, offers get assigned/expire on schedule | Easy to test, validates offer engine |
| **B. Basic shopping: Random product browsing** | Agents browse products, add to cart based on persona traits | Moderate complexity, generates shopping_session_events |
| **C. Full shopping: Complete checkout flow** | Agents browse, add to cart, apply coupons, checkout | Most realistic but complex |

**Recommended**: Option B for initial 6-hour test. This validates both offer engine AND generates meaningful shopping data without the complexity of checkout/payment flows.

---

### Q2: What does "watch agent behaviors via LangSmith" mean specifically?

**Context**: LangSmith is designed for tracing LLM calls. Current offer engine uses NO LLM calls (pure rules-based).

| Option | Description | Recommendation |
|--------|-------------|----------------|
| **A. LangSmith for LLM persona decisions** | Add LLM calls for 10% of shopping decisions, trace them | Adds cost, complexity |
| **B. Custom logging + dashboard** | Rich terminal dashboard showing real-time stats | No external dependency |
| **C. Database + Supabase dashboard** | Store events in DB, view via Supabase or custom UI | Persistent, queryable |
| **D. LangSmith for future LangGraph rewrite** | Skip for v1, plan for v2 | Pragmatic approach |

**Recommended**: Option C (Database events) + Option B (Rich dashboard) for v1. Reserve LangSmith for v2 LangGraph integration.

---

### Q3: What time scale should the 6-hour test use?

**Context**: Original plan uses 168x compression (1 real hour = 1 simulated week). For a 6-hour test:
- 168x: 6 hours = 6 weeks simulated = ~42 offer cycles
- Lower scale allows finer observation

| Option | Description | Recommendation |
|--------|-------------|----------------|
| **A. Full 168x compression** | 6 hours = 6 weeks = 42 daily shopping opportunities per agent | Tests full speed |
| **B. 24x compression** | 6 hours = 6 days = ~6 shopping opportunities per agent | More observable |
| **C. Real-time (1x)** | 6 hours = 6 hours = likely 0-1 shopping events | Too slow |
| **D. Configurable** | Allow adjustment during test | Most flexible |

**Recommended**: Option D (Configurable), starting with 24x for the first test run to observe behaviors clearly, then scaling up.

---

### Q4: What database should agents interact with?

**Context**: Simulation data needs to be isolated from production.

| Option | Description | Recommendation |
|--------|-------------|----------------|
| **A. Same DB with is_simulated flags** | Use existing schema with filtering | Already implemented in migration |
| **B. Separate simulation database** | Completely isolated | Extra setup |
| **C. In-memory/SQLite for testing** | Fast, disposable | Not persistent |

**Recommended**: Option A - already implemented. `is_simulated=true` flags exist on users, orders, user_coupons.

---

### Q5: How should agent shopping behavior be determined?

**Context**: The Rules Engine is NOT implemented. Need to decide complexity level.

| Option | Description | Recommendation |
|--------|-------------|----------------|
| **A. Random with persona weights** | Simple probability based on shopping_frequency, price_sensitivity | Fast to implement |
| **B. Full rules engine** | Complete implementation of should_shop_today(), time_patterns, etc. | More realistic but longer |
| **C. Hybrid: Core rules only** | Implement shopping_frequency and time_of_day only | Balanced approach |

**Recommended**: Option C - implement core rules (shopping frequency, time preferences) for v1 test. Add full churn model, seasonal modifiers later.

---

## Implicit Assumptions

### A1: Agents are already seeded in the database
**Assumption**: The `agents` table has at least 2 agents with valid `user_id` references.
**Risk**: If not seeded, simulation will fail immediately.
**Validation**: Run `SELECT COUNT(*) FROM agents WHERE is_active = true` before starting.

### A2: Coupons pool is populated
**Assumption**: `coupons` table has at least 50 frontstore + 150 category/brand coupons.
**Risk**: Offer assignment will fail or assign nothing.
**Validation**: Run coupon counts query before starting.

### A3: Products table has sufficient data
**Assumption**: `products` table has products across multiple categories for agents to "shop".
**Risk**: Shopping behavior will have no items to select.
**Validation**: Check products count and category distribution.

### A4: Database migrations are applied
**Assumption**: Migration 007 (offer_engine.sql) has been run.
**Risk**: Missing tables will cause immediate failures.
**Validation**: Check for offer_cycles, user_offer_cycles, simulation_state tables.

### A5: SIMULATION_MODE environment variable
**Assumption**: `SIMULATION_MODE=true` will be set before running.
**Risk**: All offer engine endpoints return "simulation_mode_disabled".
**Validation**: Environment check at startup.

---

## Potential Blindspots

### B1: Offer Engine Never Tested
**Issue**: The entire offer engine has been implemented but never run against real database.
**Risk**: Unknown bugs in cycle creation, offer assignment, expiration handling.
**Mitigation**: Create a test script that exercises each component before full simulation.

### B2: No Agent Execution Loop
**Issue**: There's no code that actually "runs" agents. OfferScheduler handles offers, but nothing makes agents shop.
**Risk**: Simulation will only rotate offers, not generate shopping data.
**Mitigation**: Need to implement `AgentRunner` or `SimulationLoop` that:
1. Gets all active agents
2. For each simulated day, decides who shops
3. Executes shopping behavior for each agent

### B3: No Checkpointing/Resume
**Issue**: 6-hour run can fail. No checkpoint mechanism exists.
**Risk**: Lose all progress on crash.
**Mitigation**: Implement checkpoint every N minutes to `simulation_state` table.

### B4: No Shopping Session Events
**Issue**: Agents need to create `shopping_session_events` records for ML training data.
**Risk**: Even if offers rotate, no user behavior data is generated.
**Mitigation**: Implement minimal action executor that creates:
- `shopping_sessions` records
- `shopping_session_events` (view_product, cart_add_item, etc.)

### B5: Time Service Persistence
**Issue**: `TimeService.save_state()` exists but unclear if called regularly.
**Risk**: On crash, simulation time resets to beginning.
**Mitigation**: Verify state is saved after each time advance.

### B6: No Error Handling for Agent Failures
**Issue**: If one agent fails, unclear if others continue.
**Risk**: Single agent error could halt entire simulation.
**Mitigation**: Wrap agent execution in try/catch, log errors, continue.

### B7: Database Connection Pool Exhaustion
**Issue**: Running 300 agents with concurrent DB operations.
**Risk**: Connection pool (size=5) exhausted.
**Mitigation**: For 2-agent test, fine. For 300 agents, need async connection pooling or batched operations.

### B8: Metrics/Observability Gap
**Issue**: No way to see what's happening during the 6-hour run.
**Risk**: "Black box" execution, only see results at end.
**Mitigation**: Implement real-time statistics endpoint or dashboard.

---

## Pre-flight Checklist

Before running the 6-hour simulation:

1. [ ] Verify at least 2 agents exist in `agents` table
2. [ ] Verify agents have valid `user_id` references in `users` table
3. [ ] Verify coupons table has 50+ frontstore and 150+ category/brand coupons
4. [ ] Verify products table has products across categories
5. [ ] Verify migration 007 applied (check for offer_cycles table)
6. [ ] Set `SIMULATION_MODE=true` in environment
7. [ ] Test offer engine endpoints manually (start, advance, status)
8. [ ] Run offer assignment for 1 agent manually
9. [ ] Verify logging is working
10. [ ] Set up monitoring dashboard or logging output

---

## Recommended Priority Order

1. **Test offer engine** - Verify existing code works
2. **Implement minimal agent runner** - Loop that advances time and makes agents "shop"
3. **Add basic shopping behavior** - Random product browsing based on persona
4. **Add observability** - Rich dashboard or DB stats queries
5. **Run 6-hour test** - 2 agents at 24x time scale
6. **Review data** - Query shopping_session_events, user_coupons, orders
7. **Fix issues** - Based on data review
8. **Scale up** - Increase time scale, add more agents

{{< /collapse >}}
