
---
title: "Simulation Engine & Offer Management System"
date: 2025-12-27T00:00:00+05:30
draft: false
---

## Overview

Implemented a complete simulation engine for testing offer management workflows with persona-based shopping agents. The system enables accelerated time simulation (1 real hour = 1 week simulated time) to model long-term offer lifecycle effects.

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