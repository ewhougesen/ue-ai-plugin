# AI Trading Assistant - System Design Document

**Date:** 2025-03-20
**Status:** Approved
**Version:** 1.0

## Executive Summary

A browser-activated stock trading assistant with optional auto-trading capabilities. The system validates strategies via backtesting and paper trading before enabling live trading. Built with risk-first principles, multi-source data verification, and comprehensive audit logging.

**Key Features:**
- Real-time market data ingestion (Polygon.io)
- Paper trading validation (Alpaca Paper API)
- Live trading with enhanced safeguards
- Momentum and Mean Reversion strategies
- Three-tier profit-based risk model
- Browser extension + web dashboard control
- Comprehensive audit logging

**Non-Negotiable Constraints:**
- Never claim 100% correctness
- Multi-source data verification
- Fail closed, not open
- All logic traceable and auditable
- Paper trading before live trading
- Auto-trading must be opt-in

---

## 1. System Architecture

```
┌──────────────────────────────────────────────────────────────────────┐
│ USER LAYER                                                             │
│ Browser Extension + Web Dashboard                                     │
└────────────┬─────────────────────────────────────────────────────────┘
             │ HTTPS/WebSocket
             ▼
┌──────────────────────────────────────────────────────────────────────┐
│ API GATEWAY (Fastify + TypeScript)                                   │
└─────┬───────────────┬────────────────────────┬──────────────────────┘
      │               │                        │
      ▼               ▼                        ▼
┌──────────┐  ┌──────────────┐      ┌─────────────────┐
│ Data     │  │ Strategy     │      │ Execution       │
│ Layer    │  │ Engine       │      │ Layer           │
│ Polygon  │  │ Momentum     │      │ Alpaca API      │
│ Redis    │  │ Mean Rev.    │      │ Order Mgmt      │
│ Postgres │  │ Scoring      │      │ Position Track  │
└──────────┘  └──────────────┘      └─────────────────┘
                    │
                    ▼
           ┌────────────────┐
           │ Risk Engine    │
           │ 3-Tier Model   │
           │ Kill Switch    │
           └────────────────┘
```

---

## 2. Technology Stack

### Frontend
- **Browser Extension:** React + TypeScript + TailwindCSS + Plasmo
- **Web Dashboard:** React + TypeScript + TailwindCSS + Socket.io

### Backend
- **API:** Node.js + TypeScript + Fastify
- **WebSocket:** Socket.io
- **Database:** PostgreSQL (primary) + Redis (cache)

### External Services
- **Market Data:** Polygon.io
- **Execution:** Alpaca (Paper → Live)

### Development
- **Testing:** Jest + Playwright
- **Containers:** Docker + Docker Compose
- **Build:** TypeScript compiler

---

## 3. Database Schema

### Key Tables

**users**
```sql
id UUID PRIMARY KEY
email VARCHAR(255) UNIQUE
password_hash VARCHAR(255)
alpaca_api_key VARCHAR(255) ENCRYPTED
alpaca_secret_key VARCHAR(255) ENCRYPTED
polygon_api_key VARCHAR(255) ENCRYPTED
base_capital DECIMAL(10,2)
current_capital DECIMAL(10,2)
risk_mode VARCHAR(20)
```

**sessions**
```sql
id UUID PRIMARY KEY
user_id UUID REFERENCES users(id)
budget DECIMAL(10,2)
risk_mode VARCHAR(20)
status VARCHAR(20) -- running, stopped, emergency
start_time TIMESTAMP
end_time TIMESTAMP NULLABLE
starting_capital DECIMAL(10,2)
ending_capital DECIMAL(10,2) NULLABLE
total_pnl DECIMAL(10,2) NULLABLE
```

**signals**
```sql
id UUID PRIMARY KEY
session_id UUID REFERENCES sessions(id)
symbol VARCHAR(10)
strategy VARCHAR(50)
action VARCHAR(10) -- buy, sell
confidence_score DECIMAL(3,2)
risk_score DECIMAL(3,2)
reward_ratio DECIMAL(3,1)
entry DECIMAL(10,2)
stop_loss DECIMAL(10,2)
take_profit DECIMAL(10,2)
position_size DECIMAL(10,2)
reason TEXT
executed BOOLEAN DEFAULT FALSE
```

**orders**
```sql
id UUID PRIMARY KEY
signal_id UUID REFERENCES signals(id)
alpaca_order_id VARCHAR(50)
symbol VARCHAR(10)
side VARCHAR(10)
qty INTEGER
price DECIMAL(10,2)
order_type VARCHAR(20)
status VARCHAR(20) -- pending, submitted, filled, cancelled, rejected
submitted_at TIMESTAMP
filled_at TIMESTAMP NULLABLE
filled_price DECIMAL(10,2) NULLABLE
```

**positions**
```sql
id UUID PRIMARY KEY
user_id UUID REFERENCES users(id)
symbol VARCHAR(10)
qty INTEGER
avg_entry_price DECIMAL(10,2)
current_price DECIMAL(10,2)
unrealized_pnl DECIMAL(10,2)
realized_pnl DECIMAL(10,2) DEFAULT 0
stop_loss DECIMAL(10,2)
take_profit DECIMAL(10,2)
opened_at TIMESTAMP
closed_at TIMESTAMP NULLABLE
status VARCHAR(20) -- open, closed
```

**audit_log** (Immutable)
```sql
id UUID PRIMARY KEY
user_id UUID REFERENCES users(id)
session_id UUID REFERENCES sessions(id)
event_type VARCHAR(50)
event_data JSONB
timestamp TIMESTAMP
ip_address VARCHAR(45)
```

### Redis Cache
```
market_data:{symbol} → Hash (price, volume, timestamp)
signals:queue → List
session:{id}:state → Hash
rate_limit:{user_id}:{action} → String
kill_switch → String
```

---

## 4. API Endpoints

### Authentication
```
POST /api/auth/register
POST /api/auth/login
POST /api/auth/logout
```

### Sessions
```
POST /api/sessions
GET /api/sessions/:id
PUT /api/sessions/:id/stop
DELETE /api/sessions/:id (emergency)
```

### Trading
```
GET /api/trading/signals
GET /api/trading/positions
POST /api/trading/override
GET /api/trading/performance
```

### Market Data
```
GET /api/market/quote/:symbol
GET /api/market/snapshot
GET /api/market/screener
```

### Configuration
```
GET /api/config/user
PUT /api/config/user
POST /api/config/keys
```

### WebSocket Events

**Server → Client**
```
market:update
signal:generated
signal:executed
order:submitted
order:filled
order:rejected
position:opened
position:closed
position:updated
risk:warning
risk:limit_hit
session:update
error
```

**Client → Server**
```
session:start
session:stop
session:emergency
subscribe:market
unsubscribe:market
```

---

## 5. Strategy Scoring Model

### Momentum Strategy

**Signal Conditions:**
1. Price breaks above 20-day high
2. Volume > 1.5x average volume
3. RSI(14) between 50-70
4. Price > SMA(50)

**Scoring (0-100 points):**
- Breakout strength: 30 points
- Volume confirmation: 25 points
- Trend alignment: 20 points
- RSI condition: 15 points
- Price consistency: 10 points

**Output:**
```typescript
{
  symbol: "AAPL",
  action: "buy",
  confidence: 0.96,
  risk_score: 0.32,
  reward_ratio: 2.5,
  entry: 178.50,
  stop_loss: 174.93, // -2%
  take_profit: 187.42, // +5%
  position_size: calculated_by_risk_engine,
  reason: "Breakout +5% above 20-day high with 2.0x volume..."
}
```

### Mean Reversion Strategy

**Signal Conditions:**
1. Price drops below 20-day low
2. RSI(14) < 30 (oversold)
3. Volume spikes (panic selling)
4. Price deviates > 2% from SMA(20)

**Scoring (0-100 points):**
- Oversold magnitude: 30 points
- RSI oversold: 25 points
- Volume panic: 20 points
- Deviation from mean: 15 points
- Support level: 10 points

---

## 6. Risk Rules

### Three-Tier Profit-Based Position Sizing

**Tier 1: Base Capital (Protected)**
- Original deposit: Always 2% max risk
- Never increases regardless of profits

**Tier 2: Accumulated Profits ($0-$500)**
- Can risk up to 50%

**Tier 3: Excess Profits (above $500)**
- Can risk up to 75%

**Example:**
```
Base: $1,000 → Tier 1 risk: $20 (always)
Profits: $2,000 → Tier 2 risk: $250 (50% of $500)
                → Tier 3 risk: $1,125 (75% of $1,500)
Total per trade: $1,395
```

### Risk Limits by Mode

| Mode | Max Per Trade | Daily Loss | Max Positions | SL | TP | Ratio |
|------|--------------|------------|---------------|-----|-----|-------|
| Conservative | 2% | 5% | 3 | -2% | +4% | 2:1 |
| Balanced | 5% | 10% | 5 | -2% | +5% | 2.5:1 |
| Aggressive | 10% | 20% | 8 | -3% | +9% | 3:1 |

### Kill Switch Triggers
- Emergency button clicked
- Daily loss limit hit
- API connection lost >30 seconds
- Market data stale >30 seconds
- Broker rejects order
- 5 consecutive losses

---

## 7. Trading Flows

### Paper Trading Flow
1. User initiates paper session (budget: $100 paper money)
2. System connects to Polygon (real data) + Alpaca Paper API
3. Strategy engine scans for opportunities
4. Risk engine validates signals
5. Orders placed via Alpaca Paper API
6. Positions monitored and tracked
7. Session ends → Report generated

### Live Trading Flow
1. User must complete paper trading profitably
2. System displays risk warnings
3. User explicitly acknowledges risks
4. Enhanced pre-trade validations (API health, market status, etc.)
5. User confirmation required (5-second countdown)
6. Orders placed via Alpaca Live API
7. Enhanced monitoring and kill switch always available
8. Comprehensive audit logging

---

## 8. Security Model

### API Key Storage
- AES-256-GCM encryption at rest
- TLS 1.3+ in transit
- Separate encryption keys from data
- Hardware security module (production)

### Authentication
- JWT tokens (15-minute expiry)
- Refresh tokens (httpOnly cookie)
- Password hashing (bcrypt)
- Rate limiting (5 attempts per 15 min)
- 2FA optional

### Audit Logging
Every action logged:
- Session start/stop
- Signal generation
- Order submission/fill
- Position changes
- Risk events
- API access
- Errors

Logs are:
- Immutable
- Append-only
- Retained 7 years
- Monitored for anomalies

### Failure Modes
**FAIL CLOSED:**
- API lost → Stop trading
- Data stale → Stop trading
- Risk limit → Stop trading
- Validation fail → Skip trade

---

## 9. Test Plan

### Unit Tests (60%) - Jest
- Strategy scoring logic
- Risk engine calculations
- Technical indicators
- Service methods

### Integration Tests (30%)
- API endpoints
- External API calls (mocked)
- Database operations
- WebSocket events

### E2E Tests (10%)
- Paper trading flow
- Risk limit flow
- Emergency stop flow
- Market data failure flow

### Coverage Targets
- Strategy logic: 90%+
- Risk engine: 95%+
- Services: 80%+
- Overall: 75%+

---

## 10. Repository Structure

```
trading-assistant/
├── backend/              # Fastify + TypeScript API
├── web-dashboard/        # React web UI
├── browser-extension/    # Browser extension
├── shared/              # Shared types/utils
├── docs/                # Documentation
└── scripts/             # Setup/build/test scripts
```

---

## 11. Deployment

### Development
- Docker Compose locally
- Mock external APIs
- Hot reload

### Staging
- Cloud VPS
- Alpaca Paper Trading
- Polygon free tier
- SSL certificates

### Production
- Managed Kubernetes
- Managed PostgreSQL + Redis
- CDN for static assets
- DDoS protection
- Secrets manager
- Monitoring & alerting

---

## 12. Next Steps

1. Create implementation plan
2. Set up repository structure
3. Implement backend services
4. Build frontend interfaces
5. Integrate external APIs
6. Implement strategies
7. Add risk engine
8. Write comprehensive tests
9. Deploy to staging
10. Validate with paper trading

---

**End of Design Document**
