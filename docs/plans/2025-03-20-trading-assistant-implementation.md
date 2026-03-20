# AI Trading Assistant Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build a browser-activated stock trading assistant with real-time market data, paper trading validation, and optional live auto-trading.

**Architecture:** Browser extension + web dashboard for controls, Node.js/TypeScript backend for trading logic, PostgreSQL for data storage, Redis for caching, Polygon.io for market data, Alpaca for execution.

**Tech Stack:** React, TypeScript, Fastify, PostgreSQL, Redis, Socket.io, Jest, Docker

---

## Phase 1: Foundation Setup

### Task 1: Create Repository Structure

**Files:**
- Create: `package.json`
- Create: `tsconfig.json`
- Create: `.gitignore`
- Create: `docker-compose.yml`
- Create: `.env.example`

**Step 1: Create root package.json**

```json
{
  "name": "trading-assistant",
  "version": "1.0.0",
  "private": true,
  "workspaces": [
    "backend",
    "web-dashboard",
    "browser-extension",
    "shared"
  ],
  "scripts": {
    "dev": "concurrently \"npm run dev:backend\" \"npm run dev:dashboard\"",
    "dev:backend": "cd backend && npm run dev",
    "dev:dashboard": "cd web-dashboard && npm run dev",
    "build": "npm run build --workspaces --if-present",
    "test": "npm run test --workspaces --if-present",
    "lint": "eslint . --ext .ts,.tsx",
    "docker:up": "docker-compose up -d",
    "docker:down": "docker-compose down"
  },
  "devDependencies": {
    "concurrently": "^8.2.2",
    "eslint": "^8.57.0",
    "typescript": "^5.4.5"
  }
}
```

**Step 2: Create root tsconfig.json**

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "commonjs",
    "lib": ["ES2022"],
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "resolveJsonModule": true,
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true
  }
}
```

**Step 3: Create .gitignore**

```
node_modules/
dist/
build/
.env
*.log
.DS_Store
coverage/
.vscode/
.idea/
*.swp
*.swo
```

**Step 4: Create docker-compose.yml**

```yaml
version: '3.8'

services:
  postgres:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: trading
      POSTGRES_PASSWORD: trading_dev
      POSTGRES_DB: trading_assistant
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

volumes:
  postgres_data:
  redis_data:
```

**Step 5: Create .env.example**

```
# Database
DATABASE_URL=postgresql://trading:trading_dev@localhost:5432/trading_assistant
REDIS_URL=redis://localhost:6379

# API Keys (encrypted before storage)
POLYGON_API_KEY=your_polygon_key_here
ALPACA_API_KEY=your_alpaca_key_here
ALPACA_SECRET_KEY=your_alpaca_secret_here

# Server
PORT=3000
NODE_ENV=development
JWT_SECRET=generate_secure_random_string

# Encryption
ENCRYPTION_KEY=generate_32_byte_hex_key

# CORS
FRONTEND_URL=http://localhost:5173
```

**Step 6: Commit**

```bash
git add package.json tsconfig.json .gitignore docker-compose.yml .env.example
git commit -m "feat: initialize repository structure"
```

---

### Task 2: Setup Backend Workspace

**Files:**
- Create: `backend/package.json`
- Create: `backend/tsconfig.json`
- Create: `backend/src/index.ts`
- Create: `backend/src/app.ts`

**Step 1: Create backend/package.json**

```json
{
  "name": "backend",
  "version": "1.0.0",
  "main": "dist/index.js",
  "scripts": {
    "dev": "tsx watch src/index.ts",
    "build": "tsc",
    "start": "node dist/index.js",
    "test": "jest",
    "test:watch": "jest --watch",
    "lint": "eslint src --ext .ts"
  },
  "dependencies": {
    "@fastify/cors": "^8.5.0",
    "@fastify/jwt": "^7.2.4",
    "@fastify/rate-limit": "^9.1.0",
    "@fastify/websocket": "^10.0.1",
    "bcrypt": "^5.1.1",
    "fastify": "^4.26.2",
    "ioredis": "^5.4.1",
    "pg": "^8.11.3",
    "socket.io": "^4.7.2",
    "ws": "^8.16.0",
    "zod": "^3.22.4"
  },
  "devDependencies": {
    "@types/bcrypt": "^5.0.2",
    "@types/node": "^20.11.28",
    "@types/pg": "^8.11.0",
    "@types/ws": "^8.5.10",
    "jest": "^29.7.0",
    "ts-jest": "^29.1.2",
    "tsx": "^4.7.1",
    "typescript": "^5.4.5"
  }
}
```

**Step 2: Create backend/tsconfig.json**

```json
{
  "extends": "../../tsconfig.json",
  "compilerOptions": {
    "outDir": "./dist",
    "rootDir": "./src",
    "esModuleInterop": true,
    "resolveJsonModule": true,
    "moduleResolution": "node"
  },
  "include": ["src/**/*"]
}
```

**Step 3: Create backend/src/app.ts**

```typescript
import Fastify, { FastifyInstance } from 'fastify';
import cors from '@fastify/cors';
import jwt from '@fastify/jwt';
import rateLimit from '@fastify/rate-limit';
import websocket from '@fastify/websocket';

export async function createApp(): Promise<FastifyInstance> {
  const app = Fastify({
    logger: {
      level: process.env.LOG_LEVEL || 'info'
    }
  });

  // Register plugins
  await app.register(cors, {
    origin: process.env.FRONTEND_URL || 'http://localhost:5173',
    credentials: true
  });

  await app.register(jwt, {
    secret: process.env.JWT_SECRET || 'dev-secret-change-in-production'
  });

  await app.register(rateLimit, {
    max: 100,
    timeWindow: '1 minute'
  });

  await app.register(websocket);

  // Health check
  app.get('/health', async () => {
    return { status: 'ok', timestamp: new Date().toISOString() };
  });

  return app;
}
```

**Step 4: Create backend/src/index.ts**

```typescript
import { createApp } from './app';

async function start() {
  try {
    const app = await createApp();

    const port = parseInt(process.env.PORT || '3000');
    await app.listen({ port, host: '0.0.0.0' });

    console.log(`🚀 Server running on port ${port}`);
  } catch (err) {
    console.error('Failed to start server:', err);
    process.exit(1);
  }
}

start();
```

**Step 5: Install dependencies**

```bash
cd backend
npm install
```

**Step 6: Commit**

```bash
git add backend/
git commit -m "feat: setup backend workspace with Fastify"
```

---

### Task 3: Setup Database Connection

**Files:**
- Create: `backend/src/db/connection.ts`
- Create: `backend/src/db/redis.ts`
- Create: `backend/src/db/config.ts`
- Create: `backend/src/db/migrations/001_init.sql`

**Step 1: Create backend/src/db/config.ts**

```typescript
export const dbConfig = {
  host: process.env.DB_HOST || 'localhost',
  port: parseInt(process.env.DB_PORT || '5432'),
  database: process.env.DB_NAME || 'trading_assistant',
  user: process.env.DB_USER || 'trading',
  password: process.env.DB_PASSWORD || 'trading_dev'
};

export const redisConfig = {
  host: process.env.REDIS_HOST || 'localhost',
  port: parseInt(process.env.REDIS_PORT || '6379')
};
```

**Step 2: Create backend/src/db/connection.ts**

```typescript
import { Pool, PoolClient } from 'pg';
import { dbConfig } from './config';

let pool: Pool | null = null;

export async function getPool(): Promise<Pool> {
  if (!pool) {
    pool = new Pool(dbConfig);
  }
  return pool;
}

export async function getClient(): Promise<PoolClient> {
  const pool = await getPool();
  return pool.connect();
}

export async function closePool(): Promise<void> {
  if (pool) {
    await pool.end();
    pool = null;
  }
}
```

**Step 3: Create backend/src/db/redis.ts**

```typescript
import Redis from 'ioredis';
import { redisConfig } from './config';

let client: Redis | null = null;

export function getRedisClient(): Redis {
  if (!client) {
    client = new Redis({
      host: redisConfig.host,
      port: redisConfig.port,
      retryStrategy(times) {
        if (times > 3) {
          console.error('Redis connection failed after 3 retries');
          return null;
        }
        return Math.min(times * 100, 3000);
      }
    });

    client.on('error', (err) => {
      console.error('Redis error:', err);
    });
  }
  return client;
}

export async function closeRedis(): Promise<void> {
  if (client) {
    await client.quit();
    client = null;
  }
}
```

**Step 4: Create backend/src/db/migrations/001_init.sql**

```sql
-- Users table
CREATE TABLE IF NOT EXISTS users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email VARCHAR(255) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  alpaca_api_key VARCHAR(255),
  alpaca_secret_key VARCHAR(255),
  polygon_api_key VARCHAR(255),
  base_capital DECIMAL(10,2) DEFAULT 0,
  current_capital DECIMAL(10,2) DEFAULT 0,
  risk_mode VARCHAR(20) DEFAULT 'balanced',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Sessions table
CREATE TABLE IF NOT EXISTS sessions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  budget DECIMAL(10,2) NOT NULL,
  risk_mode VARCHAR(20) NOT NULL,
  status VARCHAR(20) NOT NULL,
  start_time TIMESTAMP NOT NULL,
  end_time TIMESTAMP,
  starting_capital DECIMAL(10,2) NOT NULL,
  ending_capital DECIMAL(10,2),
  total_pnl DECIMAL(10,2),
  trades_count INTEGER DEFAULT 0,
  wins_count INTEGER DEFAULT 0,
  losses_count INTEGER DEFAULT 0
);

-- Signals table
CREATE TABLE IF NOT EXISTS signals (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  session_id UUID NOT NULL REFERENCES sessions(id) ON DELETE CASCADE,
  symbol VARCHAR(10) NOT NULL,
  strategy VARCHAR(50) NOT NULL,
  action VARCHAR(10) NOT NULL,
  confidence_score DECIMAL(3,2) NOT NULL,
  risk_score DECIMAL(3,2) NOT NULL,
  reward_ratio DECIMAL(3,1) NOT NULL,
  entry DECIMAL(10,2) NOT NULL,
  stop_loss DECIMAL(10,2) NOT NULL,
  take_profit DECIMAL(10,2) NOT NULL,
  position_size DECIMAL(10,2) NOT NULL,
  reason TEXT,
  executed BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Orders table
CREATE TABLE IF NOT EXISTS orders (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  signal_id UUID REFERENCES signals(id) ON DELETE SET NULL,
  alpaca_order_id VARCHAR(50),
  symbol VARCHAR(10) NOT NULL,
  side VARCHAR(10) NOT NULL,
  qty INTEGER NOT NULL,
  price DECIMAL(10,2),
  order_type VARCHAR(20) NOT NULL,
  status VARCHAR(20) NOT NULL,
  submitted_at TIMESTAMP,
  filled_at TIMESTAMP,
  filled_price DECIMAL(10,2),
  filled_qty INTEGER,
  commission DECIMAL(10,2) DEFAULT 0
);

-- Positions table
CREATE TABLE IF NOT EXISTS positions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  symbol VARCHAR(10) NOT NULL,
  qty INTEGER NOT NULL,
  avg_entry_price DECIMAL(10,2) NOT NULL,
  current_price DECIMAL(10,2),
  unrealized_pnl DECIMAL(10,2) DEFAULT 0,
  realized_pnl DECIMAL(10,2) DEFAULT 0,
  stop_loss DECIMAL(10,2),
  take_profit DECIMAL(10,2),
  opened_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  closed_at TIMESTAMP,
  status VARCHAR(20) DEFAULT 'open'
);

-- Trades table (closed positions)
CREATE TABLE IF NOT EXISTS trades (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  position_id UUID NOT NULL REFERENCES positions(id),
  symbol VARCHAR(10) NOT NULL,
  entry_price DECIMAL(10,2) NOT NULL,
  exit_price DECIMAL(10,2) NOT NULL,
  qty INTEGER NOT NULL,
  pnl DECIMAL(10,2) NOT NULL,
  pnl_percent DECIMAL(5,2) NOT NULL,
  hold_duration_min INTEGER NOT NULL,
  strategy VARCHAR(50),
  tier_used INTEGER NOT NULL,
  closed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Audit log table (immutable)
CREATE TABLE IF NOT EXISTS audit_log (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  session_id UUID REFERENCES sessions(id) ON DELETE SET NULL,
  event_type VARCHAR(50) NOT NULL,
  event_data JSONB NOT NULL,
  timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  ip_address VARCHAR(45)
);

-- Risk events table
CREATE TABLE IF NOT EXISTS risk_events (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  session_id UUID NOT NULL REFERENCES sessions(id) ON DELETE CASCADE,
  event_type VARCHAR(50) NOT NULL,
  severity VARCHAR(20) NOT NULL,
  message TEXT NOT NULL,
  resolved BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_sessions_user_id ON sessions(user_id);
CREATE INDEX IF NOT EXISTS idx_sessions_status ON sessions(status);
CREATE INDEX IF NOT EXISTS idx_signals_session_id ON signals(session_id);
CREATE INDEX IF NOT EXISTS idx_signals_executed ON signals(executed);
CREATE INDEX IF NOT EXISTS idx_orders_status ON orders(status);
CREATE INDEX IF NOT EXISTS idx_positions_user_id ON positions(user_id);
CREATE INDEX IF NOT EXISTS idx_positions_status ON positions(status);
CREATE INDEX IF NOT EXISTS idx_audit_log_user_id ON audit_log(user_id);
CREATE INDEX IF NOT EXISTS idx_audit_log_timestamp ON audit_log(timestamp);
```

**Step 5: Run database setup**

```bash
docker-compose up -d postgres
# Wait for postgres to start, then:
psql postgresql://trading:trading_dev@localhost:5432/trading_assistant < backend/src/db/migrations/001_init.sql
```

**Step 6: Commit**

```bash
git add backend/src/db/
git commit -m "feat: setup database connection and schema"
```

---

## Phase 2: Authentication System

### Task 4: Create User Model and Types

**Files:**
- Create: `backend/src/models/User.ts`
- Create: `backend/src/types/index.d.ts`

**Step 1: Create backend/src/types/index.d.ts**

```typescript
export interface User {
  id: string;
  email: string;
  alpacaApiKey?: string;
  alpacaSecretKey?: string;
  polygonApiKey?: string;
  baseCapital: number;
  currentCapital: number;
  riskMode: 'conservative' | 'balanced' | 'aggressive';
  createdAt: Date;
  updatedAt: Date;
}

export interface Session {
  id: string;
  userId: string;
  budget: number;
  riskMode: 'conservative' | 'balanced' | 'aggressive';
  status: 'running' | 'stopped' | 'emergency';
  startTime: Date;
  endTime?: Date;
  startingCapital: number;
  endingCapital?: number;
  totalPnl?: number;
  tradesCount: number;
  winsCount: number;
  lossesCount: number;
}

export interface Signal {
  id: string;
  sessionId: string;
  symbol: string;
  strategy: 'momentum' | 'mean_reversion';
  action: 'buy' | 'sell';
  confidence: number;
  riskScore: number;
  rewardRatio: number;
  entry: number;
  stopLoss: number;
  takeProfit: number;
  positionSize: number;
  reason: string;
  executed: boolean;
  createdAt: Date;
}

export interface Position {
  id: string;
  userId: string;
  symbol: string;
  qty: number;
  avgEntryPrice: number;
  currentPrice: number;
  unrealizedPnl: number;
  realizedPnl: number;
  stopLoss?: number;
  takeProfit?: number;
  openedAt: Date;
  closedAt?: Date;
  status: 'open' | 'closed';
}

export interface MarketData {
  symbol: string;
  price: number;
  bid?: number;
  ask?: number;
  volume: number;
  timestamp: Date;
  source: 'polygon';
}

export interface AuthPayload {
  email: string;
  password: string;
}

export interface AuthResponse {
  token: string;
  user: Omit<User, 'alpacaApiKey' | 'alpacaSecretKey' | 'polygonApiKey'>;
}
```

**Step 2: Create backend/src/models/User.ts**

```typescript
import { PoolClient } from 'pg';
import { User } from '../types';

export class UserModel {
  constructor(private db: PoolClient) {}

  async create(email: string, passwordHash: string): Promise<User> {
    const result = await this.db.query(
      `INSERT INTO users (email, password_hash)
       VALUES ($1, $2)
       RETURNING *`,
      [email, passwordHash]
    );

    return this.mapFromDb(result.rows[0]);
  }

  async findByEmail(email: string): Promise<User | null> {
    const result = await this.db.query(
      'SELECT * FROM users WHERE email = $1',
      [email]
    );

    return result.rows[0] ? this.mapFromDb(result.rows[0]) : null;
  }

  async findById(id: string): Promise<User | null> {
    const result = await this.db.query(
      'SELECT * FROM users WHERE id = $1',
      [id]
    );

    return result.rows[0] ? this.mapFromDb(result.rows[0]) : null;
  }

  async updateCapital(userId: string, currentCapital: number): Promise<void> {
    await this.db.query(
      `UPDATE users
       SET current_capital = $1, updated_at = CURRENT_TIMESTAMP
       WHERE id = $2`,
      [currentCapital, userId]
    );
  }

  async storeApiKeys(
    userId: string,
    keys: {
      alpacaApiKey?: string;
      alpacaSecretKey?: string;
      polygonApiKey?: string;
    }
  ): Promise<void> {
    await this.db.query(
      `UPDATE users
       SET alpaca_api_key = COALESCE($1, alpaca_api_key),
           alpaca_secret_key = COALESCE($2, alpaca_secret_key),
           polygon_api_key = COALESCE($3, polygon_api_key),
           updated_at = CURRENT_TIMESTAMP
       WHERE id = $4`,
      [keys.alpacaApiKey, keys.alpacaSecretKey, keys.polygonApiKey, userId]
    );
  }

  private mapFromDb(row: any): User {
    return {
      id: row.id,
      email: row.email,
      alpacaApiKey: row.alpaca_api_key,
      alpacaSecretKey: row.alpaca_secret_key,
      polygonApiKey: row.polygon_api_key,
      baseCapital: parseFloat(row.base_capital),
      currentCapital: parseFloat(row.current_capital),
      riskMode: row.risk_mode,
      createdAt: row.created_at,
      updatedAt: row.updated_at
    };
  }
}
```

**Step 3: Commit**

```bash
git add backend/src/models/ backend/src/types/
git commit -m "feat: add User model and types"
```

---

### Task 5: Implement Authentication Service

**Files:**
- Create: `backend/src/services/AuthService.ts`
- Create: `backend/src/services/EncryptionService.ts`

**Step 1: Create backend/src/services/EncryptionService.ts**

```typescript
import crypto from 'crypto';

export class EncryptionService {
  private key: Buffer;

  constructor() {
    const keyHex = process.env.ENCRYPTION_KEY;
    if (!keyHex) {
      throw new Error('ENCRYPTION_KEY environment variable not set');
    }
    this.key = Buffer.from(keyHex, 'hex');
  }

  encrypt(plaintext: string): { encrypted: string; iv: string; tag: string } {
    const iv = crypto.randomBytes(16);
    const cipher = crypto.createCipheriv('aes-256-gcm', this.key, iv);

    let encrypted = cipher.update(plaintext, 'utf8', 'hex');
    encrypted += cipher.final('hex');

    const tag = cipher.getAuthTag();

    return {
      encrypted,
      iv: iv.toString('hex'),
      tag: tag.toString('hex')
    };
  }

  decrypt(encrypted: string, iv: string, tag: string): string {
    const decipher = crypto.createDecipheriv(
      'aes-256-gcm',
      this.key,
      Buffer.from(iv, 'hex')
    );
    decipher.setAuthTag(Buffer.from(tag, 'hex'));

    let decrypted = decipher.update(encrypted, 'hex', 'utf8');
    decrypted += decipher.final('utf8');

    return decrypted;
  }

  hashPassword(password: string): string {
    const salt = crypto.randomBytes(16).toString('hex');
    const hash = crypto
      .pbkdf2Sync(password, salt, 100000, 64, 'sha512')
      .toString('hex');
    return `${salt}:${hash}`;
  }

  verifyPassword(password: string, storedHash: string): boolean {
    const [salt, hash] = storedHash.split(':');
    const verifyHash = crypto
      .pbkdf2Sync(password, salt, 100000, 64, 'sha512')
      .toString('hex');
    return hash === verifyHash;
  }
}

export const encryptionService = new EncryptionService();
```

**Step 2: Create backend/src/services/AuthService.ts**

```typescript
import { UserModel } from '../models/User';
import { getClient } from '../db/connection';
import { encryptionService } from './EncryptionService';
import { AuthPayload, AuthResponse, User } from '../types';

export class AuthService {
  async register(payload: AuthPayload): Promise<AuthResponse> {
    const db = await getClient();
    const userModel = new UserModel(db);

    // Check if user exists
    const existing = await userModel.findByEmail(payload.email);
    if (existing) {
      throw new Error('User already exists');
    }

    // Hash password
    const passwordHash = encryptionService.hashPassword(payload.password);

    // Create user
    const user = await userModel.create(payload.email, passwordHash);

    await db.release();

    // Generate token
    const token = this.generateToken(user.id);

    return {
      token,
      user: this.sanitizeUser(user)
    };
  }

  async login(payload: AuthPayload): Promise<AuthResponse> {
    const db = await getClient();
    const userModel = new UserModel(db);

    const user = await userModel.findByEmail(payload.email);
    if (!user) {
      await db.release();
      throw new Error('Invalid credentials');
    }

    // Verify password
    const passwordHash = await this.getPasswordHash(user.email);
    if (!encryptionService.verifyPassword(payload.password, passwordHash)) {
      await db.release();
      throw new Error('Invalid credentials');
    }

    await db.release();

    // Generate token
    const token = this.generateToken(user.id);

    return {
      token,
      user: this.sanitizeUser(user)
    };
  }

  async getUserById(userId: string): Promise<User | null> {
    const db = await getClient();
    const userModel = new UserModel(db);

    const user = await userModel.findById(userId);
    await db.release();

    return user;
  }

  private generateToken(userId: string): string {
    // In production, use proper JWT signing
    return Buffer.from(JSON.stringify({ userId, exp: Date.now() + 3600000 })).toString('base64');
  }

  private sanitizeUser(user: User): Omit<User, 'alpacaApiKey' | 'alpacaSecretKey' | 'polygonApiKey'> {
    const { alpacaApiKey, alpacaSecretKey, polygonApiKey, ...sanitized } = user;
    return sanitized;
  }

  private async getPasswordHash(email: string): Promise<string> {
    // In real implementation, store password hash separately or retrieve from user
    // For now, return dummy - implement properly
    const db = await getClient();
    const result = await db.query(
      'SELECT password_hash FROM users WHERE email = $1',
      [email]
    );
    await db.release();
    return result.rows[0]?.password_hash || '';
  }
}

export const authService = new AuthService();
```

**Step 3: Commit**

```bash
git add backend/src/services/
git commit -m "feat: implement authentication and encryption services"
```

---

### Task 6: Create Auth Routes

**Files:**
- Create: `backend/src/routes/auth.ts`
- Modify: `backend/src/app.ts`

**Step 1: Create backend/src/routes/auth.ts**

```typescript
import { FastifyInstance } from 'fastify';
import { authService } from '../services/AuthService';

export async function authRoutes(fastify: FastifyInstance) {
  fastify.post('/register', async (request, reply) => {
    try {
      const payload = request.body as { email: string; password: string };

      if (!payload.email || !payload.password) {
        return reply.status(400).send({ error: 'Email and password required' });
      }

      const result = await authService.register(payload);
      return reply.status(201).send(result);
    } catch (error) {
      if (error instanceof Error && error.message === 'User already exists') {
        return reply.status(409).send({ error: 'User already exists' });
      }
      return reply.status(500).send({ error: 'Internal server error' });
    }
  });

  fastify.post('/login', async (request, reply) => {
    try {
      const payload = request.body as { email: string; password: string };

      if (!payload.email || !payload.password) {
        return reply.status(400).send({ error: 'Email and password required' });
      }

      const result = await authService.login(payload);
      return reply.send(result);
    } catch (error) {
      if (error instanceof Error && error.message === 'Invalid credentials') {
        return reply.status(401).send({ error: 'Invalid credentials' });
      }
      return reply.status(500).send({ error: 'Internal server error' });
    }
  });
}
```

**Step 2: Modify backend/src/app.ts to include auth routes**

```typescript
import Fastify, { FastifyInstance } from 'fastify';
import cors from '@fastify/cors';
import jwt from '@fastify/jwt';
import rateLimit from '@fastify/rate-limit';
import websocket from '@fastify/websocket';
import { authRoutes } from './routes/auth';

export async function createApp(): Promise<FastifyInstance> {
  const app = Fastify({
    logger: {
      level: process.env.LOG_LEVEL || 'info'
    }
  });

  await app.register(cors, {
    origin: process.env.FRONTEND_URL || 'http://localhost:5173',
    credentials: true
  });

  await app.register(jwt, {
    secret: process.env.JWT_SECRET || 'dev-secret-change-in-production'
  });

  await app.register(rateLimit, {
    max: 100,
    timeWindow: '1 minute'
  });

  await app.register(websocket);

  app.get('/health', async () => {
    return { status: 'ok', timestamp: new Date().toISOString() };
  });

  // Register routes
  await app.register(authRoutes, { prefix: '/api/auth' });

  return app;
}
```

**Step 3: Commit**

```bash
git add backend/src/routes/ backend/src/app.ts
git commit -m "feat: add authentication routes"
```

---

## Phase 3: Market Data Integration

### Task 7: Create Polygon Market Data Service

**Files:**
- Create: `backend/src/config/polygon.ts`
- Create: `backend/src/services/MarketDataService.ts`

**Step 1: Create backend/src/config/polygon.ts**

```typescript
export const polygonConfig = {
  apiKey: process.env.POLYGON_API_KEY || '',
  baseUrl: 'https://api.polygon.io',
  wsUrl: 'wss://socket.polygon.io/stocks'
};
```

**Step 2: Create backend/src/services/MarketDataService.ts**

```typescript
import { EventEmitter } from 'events';
import WebSocket from 'ws';
import { getRedisClient } from '../db/redis';
import { polygonConfig } from '../config/polygon';
import { MarketData } from '../types';

export class MarketDataService extends EventEmitter {
  private ws: WebSocket | null = null;
  private subscriptions: Set<string> = new Set();
  private redis = getRedisClient();

  async connect(): Promise<void> {
    return new Promise((resolve, reject) => {
      this.ws = new WebSocket(
        `${polygonConfig.wsUrl}/v3/${polygonConfig.apiKey}`
      );

      this.ws.on('open', () => {
        console.log('✅ Polygon WebSocket connected');
        resolve();
      });

      this.ws.on('error', (error) => {
        console.error('❌ Polygon WebSocket error:', error);
        reject(error);
      });

      this.ws.on('message', (data) => {
        this.handleMessage(data.toString());
      });

      this.ws.on('close', () => {
        console.log('🔌 Polygon WebSocket disconnected');
        // Reconnect logic
        setTimeout(() => this.connect(), 5000);
      });
    });
  }

  private handleMessage(data: string): void {
    try {
      const message = JSON.parse(data);

      if (message.ev === 'T' || message.ev === 'Q') {
        // Trade or Quote
        const marketData: MarketData = {
          symbol: message.S || message.sym,
          price: message.p || message.bp,
          bid: message.bp,
          ask: message.ap,
          volume: message.v || 0,
          timestamp: new Date(),
          source: 'polygon'
        };

        // Cache in Redis (5 second expiry)
        this.redis.setex(
          `market_data:${marketData.symbol}`,
          5,
          JSON.stringify(marketData)
        );

        // Emit to subscribers
        this.emit('quote', marketData);
      }
    } catch (error) {
      console.error('Error parsing WebSocket message:', error);
    }
  }

  async subscribe(symbols: string[]): Promise<void> {
    // Subscribe via WebSocket
    const ticks = symbols.map(s => `${s}.AM`).join(',');

    this.ws?.send(JSON.stringify({
      action: 'subscribe',
      params: ticks
    }));

    symbols.forEach(s => this.subscriptions.add(s));
  }

  async unsubscribe(symbols: string[]): Promise<void> {
    const ticks = symbols.map(s => `${s}.AM`).join(',');

    this.ws?.send(JSON.stringify({
      action: 'unsubscribe',
      params: ticks
    }));

    symbols.forEach(s => this.subscriptions.delete(s));
  }

  async getQuote(symbol: string): Promise<MarketData | null> {
    // Check cache first
    const cached = await this.redis.get(`market_data:${symbol}`);
    if (cached) {
      return JSON.parse(cached);
    }

    // Fetch from REST API if cache miss
    try {
      const response = await fetch(
        `${polygonConfig.baseUrl}/v2/aggs/ticker/${symbol}/prev?adjusted=true&apikey=${polygonConfig.apiKey}`
      );

      const data = await response.json();

      if (data.results && data.results.length > 0) {
        const quote: MarketData = {
          symbol,
          price: data.results[0].c,
          volume: data.results[0].v,
          timestamp: new Date(data.results[0].t),
          source: 'polygon'
        };

        // Cache for 5 seconds
        await this.redis.setex(
          `market_data:${symbol}`,
          5,
          JSON.stringify(quote)
        );

        return quote;
      }
    } catch (error) {
      console.error(`Error fetching quote for ${symbol}:`, error);
    }

    return null;
  }

  async disconnect(): Promise<void> {
    this.ws?.close();
    this.ws = null;
  }
}

export const marketDataService = new MarketDataService();
```

**Step 3: Add Polygon API dependency to backend/package.json**

```json
"dependencies": {
  ...
  "ws": "^8.16.0"
}
```

**Step 4: Commit**

```bash
git add backend/src/config/ backend/src/services/ backend/package.json
git commit -m "feat: add Polygon market data service with WebSocket"
```

---

### Task 8: Create Technical Indicators Utility

**Files:**
- Create: `backend/src/utils/indicators.ts`

**Step 1: Create backend/src/utils/indicators.ts**

```typescript
export interface PriceData {
  timestamp: number;
  open: number;
  high: number;
  low: number;
  close: number;
  volume: number;
}

export class TechnicalIndicators {
  /**
   * Simple Moving Average
   */
  static sma(prices: number[], period: number): number[] {
    const result: number[] = [];

    for (let i = period - 1; i < prices.length; i++) {
      const sum = prices.slice(i - period + 1, i + 1).reduce((a, b) => a + b, 0);
      result.push(sum / period);
    }

    return result;
  }

  /**
   * Relative Strength Index
   */
  static rsi(prices: number[], period: number = 14): number[] {
    const result: number[] = [];
    const avgGains: number[] = [];
    const avgLosses: number[] = [];

    for (let i = 1; i < prices.length; i++) {
      const change = prices[i] - prices[i - 1];
      avgGains.push(Math.max(0, change));
      avgLosses.push(Math.max(0, -change));
    }

    let avgGain = avgGains.slice(0, period).reduce((a, b) => a + b) / period;
    let avgLoss = avgLosses.slice(0, period).reduce((a, b) => a + b) / period;

    // First RSI
    const rs = avgLoss === 0 ? 100 : avgGain / avgLoss;
    result.push(100 - (100 / (1 + rs)));

    // Subsequent RSIs using Wilder's smoothing
    for (let i = period; i < avgGains.length; i++) {
      avgGain = (avgGain * (period - 1) + avgGains[i]) / period;
      avgLoss = (avgLoss * (period - 1) + avgLosses[i]) / period;

      const rs = avgLoss === 0 ? 100 : avgGain / avgLoss;
      result.push(100 - (100 / (1 + rs)));
    }

    return result;
  }

  /**
   * Average True Range
   */
  static atr(data: PriceData[], period: number = 14): number[] {
    const trueRanges: number[] = [];

    for (let i = 0; i < data.length; i++) {
      const high = data[i].high;
      const low = data[i].low;
      const prevClose = i > 0 ? data[i - 1].close : data[i].close;

      const tr = Math.max(
        high - low,
        Math.abs(high - prevClose),
        Math.abs(low - prevClose)
      );
      trueRanges.push(tr);
    }

    return this.sma(trueRanges, period);
  }

  /**
   * Get 20-day high
   */
  static high20(data: PriceData[]): number {
    const last20 = data.slice(-20);
    return Math.max(...last20.map(d => d.high));
  }

  /**
   * Get 20-day low
   */
  static low20(data: PriceData[]): number {
    const last20 = data.slice(-20);
    return Math.min(...last20.map(d => d.low));
  }

  /**
   * Average Volume
   */
  static avgVolume(data: PriceData[], period: number): number {
    const lastN = data.slice(-period);
    const sum = lastN.reduce((a, b) => a + b.volume, 0);
    return sum / period;
  }
}
```

**Step 2: Commit**

```bash
git add backend/src/utils/
git commit -m "feat: add technical indicators utility"
```

---

## Phase 4: Strategy Engine

### Task 9: Implement Momentum Strategy

**Files:**
- Create: `backend/src/strategies/MomentumStrategy.ts`
- Create: `backend/src/strategies/types.ts`

**Step 1: Create backend/src/strategies/types.ts**

```typescript
import { PriceData } from '../utils/indicators';

export interface Signal {
  symbol: string;
  strategy: 'momentum' | 'mean_reversion';
  action: 'buy' | 'sell';
  confidence: number;
  riskScore: number;
  rewardRatio: number;
  entry: number;
  stopLoss: number;
  takeProfit: number;
  positionSize: number;
  reason: string;
}

export interface StrategyConfig {
  minConfidence: number;
  minVolume: number;
  maxSpread: number; // as decimal (0.005 = 0.5%)
}

export interface StockData {
  symbol: string;
  price: number;
  bid?: number;
  ask?: number;
  volume: number;
  history: PriceData[];
}
```

**Step 2: Create backend/src/strategies/MomentumStrategy.ts**

```typescript
import { TechnicalIndicators } from '../utils/indicators';
import { Signal, StrategyConfig, StockData } from './types';

export class MomentumStrategy {
  private config: StrategyConfig;

  constructor(config: Partial<StrategyConfig> = {}) {
    this.config = {
      minConfidence: 0.70,
      minVolume: 100000,
      maxSpread: 0.005,
      ...config
    };
  }

  analyze(stock: StockData): Signal | null {
    // Check minimum liquidity
    if (stock.volume < this.config.minVolume) {
      return null;
    }

    // Check spread if bid/ask available
    if (stock.bid && stock.ask) {
      const spread = (stock.ask - stock.bid) / stock.bid;
      if (spread > this.config.maxSpread) {
        return null;
      }
    }

    // Need at least 50 days of history
    if (stock.history.length < 50) {
      return null;
    }

    const prices = stock.history.map(d => d.close);
    const rsiValues = TechnicalIndicators.rsi(prices, 14);
    const sma50 = TechnicalIndicators.sma(prices, 50);
    const currentRsi = rsiValues[rsiValues.length - 1];
    const high20 = TechnicalIndicators.high20(stock.history);
    const avgVolume = TechnicalIndicators.avgVolume(stock.history, 20);
    const currentPrice = stock.price;

    // Momentum conditions
    const breaksOut = currentPrice > high20;
    const volumeConfirmation = stock.volume > avgVolume * 1.5;
    const rsiOk = currentRsi >= 50 && currentRsi <= 70;
    const trendAligned = sma50.length > 0 && currentPrice > sma50[sma50.length - 1];

    if (!breaksOut || !volumeConfirmation || !rsiOk || !trendAligned) {
      return null;
    }

    // Calculate score
    let score = 0;
    const reasons: string[] = [];

    // Breakout strength (30 points)
    const breakoutPercent = ((currentPrice - high20) / high20) * 100;
    const breakoutPoints = Math.min(30, Math.max(0, breakoutPercent * 6)); // 5%+ = max
    score += breakoutPoints;
    reasons.push(`Breakout +${breakoutPercent.toFixed(2)}% above 20-day high`);

    // Volume confirmation (25 points)
    const volumeRatio = stock.volume / avgVolume;
    const volumePoints = Math.min(25, Math.max(0, (volumeRatio - 1.5) * 50));
    score += volumePoints;
    reasons.push(`Volume ${volumeRatio.toFixed(1)}x average`);

    // Trend alignment (20 points)
    const smaValue = sma50[sma50.length - 1];
    const trendPoints = currentPrice > smaValue ? 20 : 0;
    score += trendPoints;
    reasons.push(`Price above SMA(50)`);

    // RSI condition (15 points)
    const rsiPoints = currentRsi >= 50 && currentRsi <= 60 ? 15 : currentRsi <= 70 ? 10 : 5;
    score += rsiPoints;
    reasons.push(`RSI ${currentRsi.toFixed(0)} - room to run`);

    // Consistency (10 points)
    const consistencyPoints = 10; // Assuming clean break
    score += consistencyPoints;
    reasons.push(`Clean breakout`);

    const confidence = score / 100;

    // Risk score based on ATR
    const atr = TechnicalIndicators.atr(stock.history, 14);
    const currentAtr = atr[atr.length - 1];
    const riskScore = Math.min(1, currentAtr / currentPrice);

    if (confidence < this.config.minConfidence) {
      return null;
    }

    // Calculate position levels (Balanced mode: 2% SL, 5% TP)
    const stopLossPercent = 0.02;
    const takeProfitPercent = 0.05;

    return {
      symbol: stock.symbol,
      strategy: 'momentum',
      action: 'buy',
      confidence,
      riskScore,
      rewardRatio: takeProfitPercent / stopLossPercent,
      entry: currentPrice,
      stopLoss: currentPrice * (1 - stopLossPercent),
      takeProfit: currentPrice * (1 + takeProfitPercent),
      positionSize: 0, // Will be calculated by risk engine
      reason: reasons.join('. ') + '.'
    };
  }
}
```

**Step 3: Commit**

```bash
git add backend/src/strategies/
git commit -m "feat: implement Momentum strategy with scoring"
```

---

### Task 10: Implement Mean Reversion Strategy

**Files:**
- Create: `backend/src/strategies/MeanReversionStrategy.ts`

**Step 1: Create backend/src/strategies/MeanReversionStrategy.ts**

```typescript
import { TechnicalIndicators } from '../utils/indicators';
import { Signal, StrategyConfig, StockData } from './types';

export class MeanReversionStrategy {
  private config: StrategyConfig;

  constructor(config: Partial<StrategyConfig> = {}) {
    this.config = {
      minConfidence: 0.70,
      minVolume: 100000,
      maxSpread: 0.005,
      ...config
    };
  }

  analyze(stock: StockData): Signal | null {
    // Check minimum liquidity
    if (stock.volume < this.config.minVolume) {
      return null;
    }

    // Check spread if bid/ask available
    if (stock.bid && stock.ask) {
      const spread = (stock.ask - stock.bid) / stock.bid;
      if (spread > this.config.maxSpread) {
        return null;
      }
    }

    // Need at least 20 days of history
    if (stock.history.length < 20) {
      return null;
    }

    const prices = stock.history.map(d => d.close);
    const rsiValues = TechnicalIndicators.rsi(prices, 14);
    const sma20 = TechnicalIndicators.sma(prices, 20);
    const currentRsi = rsiValues[rsiValues.length - 1];
    const low20 = TechnicalIndicators.low20(stock.history);
    const avgVolume = TechnicalIndicators.avgVolume(stock.history, 20);
    const currentPrice = stock.price;

    // Mean reversion conditions
    const dropsBelow = currentPrice < low20;
    const oversold = currentRsi < 30;
    const volumeSpike = stock.volume > avgVolume * 2;
    const deviatesFromMean = sma20.length > 0 &&
      Math.abs((currentPrice - sma20[sma20.length - 1]) / sma20[sma20.length - 1]) > 0.02;

    if (!dropsBelow || !oversold || !volumeSpike || !deviatesFromMean) {
      return null;
    }

    // Calculate score
    let score = 0;
    const reasons: string[] = [];

    // Oversold magnitude (30 points)
    const dropPercent = ((low20 - currentPrice) / low20) * 100;
    const oversoldPoints = Math.min(30, Math.max(0, dropPercent * 7));
    score += oversoldPoints;
    reasons.push(`Oversold -${dropPercent.toFixed(2)}% below 20-day low`);

    // RSI oversold (25 points)
    const rsiPoints = currentRsi < 25 ? 25 : currentRsi < 28 ? 20 : 15;
    score += rsiPoints;
    reasons.push(`RSI ${currentRsi.toFixed(0)} - deeply oversold`);

    // Volume panic (20 points)
    const volumeRatio = stock.volume / avgVolume;
    const volumePoints = Math.min(20, Math.max(0, (volumeRatio - 2) * 10));
    score += volumePoints;
    reasons.push(`Panic volume ${volumeRatio.toFixed(1)}x average`);

    // Deviation from mean (15 points)
    const smaValue = sma20[sma20.length - 1];
    const deviationPercent = Math.abs((currentPrice - smaValue) / smaValue) * 100;
    const deviationPoints = Math.min(15, Math.max(0, (deviationPercent - 2) * 5));
    score += deviationPoints;
    reasons.push(`Deviation -${deviationPercent.toFixed(2)}% from SMA(20)`);

    // Support level (10 points)
    const supportPoints = 10; // Assuming near major support
    score += supportPoints;
    reasons.push(`Near major support`);

    const confidence = score / 100;

    // Risk score (mean reversion is riskier)
    const atr = TechnicalIndicators.atr(stock.history, 14);
    const currentAtr = atr[atr.length - 1];
    const riskScore = Math.min(1, (currentAtr / currentPrice) * 1.2);

    if (confidence < this.config.minConfidence) {
      return null;
    }

    // Calculate position levels (Balanced mode: slightly wider SL for mean reversion)
    const stopLossPercent = 0.02; // Still 2% but allow more room
    const takeProfitPercent = 0.05;

    return {
      symbol: stock.symbol,
      strategy: 'mean_reversion',
      action: 'buy',
      confidence,
      riskScore,
      rewardRatio: takeProfitPercent / stopLossPercent,
      entry: currentPrice,
      stopLoss: currentPrice * (1 - stopLossPercent),
      takeProfit: currentPrice * (1 + takeProfitPercent),
      positionSize: 0, // Will be calculated by risk engine
      reason: reasons.join('. ') + '. Expect mean reversion.'
    };
  }
}
```

**Step 2: Commit**

```bash
git add backend/src/strategies/MeanReversionStrategy.ts
git commit -m "feat: implement Mean Reversion strategy with scoring"
```

---

### Task 11: Implement Strategy Engine

**Files:**
- Create: `backend/src/services/StrategyEngine.ts`

**Step 1: Create backend/src/services/StrategyEngine.ts**

```typescript
import { EventEmitter } from 'events';
import { MarketDataService } from './MarketDataService';
import { MomentumStrategy } from '../strategies/MomentumStrategy';
import { MeanReversionStrategy } from '../strategies/MeanReversionStrategy';
import { Signal, StockData } from '../strategies/types';

interface WatchlistItem {
  symbol: string;
  enabled: boolean;
}

export class StrategyEngine extends EventEmitter {
  private marketData: MarketDataService;
  private momentumStrategy: MomentumStrategy;
  private meanReversionStrategy: MeanReversionStrategy;
  private watchlist: Map<string, WatchlistItem> = new Map();
  private stockData: Map<string, StockData> = new Map();
  private scanInterval: NodeJS.Timeout | null = null;

  constructor() {
    super();
    this.marketData = new MarketDataService();
    this.momentumStrategy = new MomentumStrategy();
    this.meanReversionStrategy = new MeanReversionStrategy();
  }

  async initialize(watchlist: string[]): Promise<void> {
    // Initialize watchlist
    watchlist.forEach(symbol => {
      this.watchlist.set(symbol, { symbol, enabled: true });
    });

    // Connect to market data
    await this.marketData.connect();
    await this.marketData.subscribe(watchlist);

    // Listen for market data updates
    this.marketData.on('quote', (data) => this.handleQuote(data));

    // Fetch historical data
    await this.fetchHistoricalData(watchlist);

    // Start scanning every 30 seconds
    this.scanInterval = setInterval(() => this.scan(), 30000);
  }

  private async fetchHistoricalData(symbols: string[]): Promise<void> {
    for (const symbol of symbols) {
      try {
        // Fetch daily bars for last year
        const response = await fetch(
          `https://api.polygon.io/v2/aggs/ticker/${symbol}/range/1/day/2024-01-01/${new Date().toISOString().split('T')[0]}?adjusted=true&apikey=${process.env.POLYGON_API_KEY}`
        );

        const data = await response.json();

        if (data.results && data.results.length > 0) {
          const history = data.results.map((bar: any) => ({
            timestamp: bar.t,
            open: bar.o,
            high: bar.h,
            low: bar.l,
            close: bar.c,
            volume: bar.v
          }));

          const stockData = this.stockData.get(symbol);
          if (stockData) {
            stockData.history = history;
          } else {
            this.stockData.set(symbol, {
              symbol,
              price: history[history.length - 1].close,
              volume: history[history.length - 1].volume,
              history
            });
          }
        }
      } catch (error) {
        console.error(`Error fetching historical data for ${symbol}:`, error);
      }
    }
  }

  private handleQuote(data: any): void {
    const stockData = this.stockData.get(data.symbol);
    if (stockData) {
      stockData.price = data.price;
      stockData.volume = data.volume;
      if (data.bid) stockData.bid = data.bid;
      if (data.ask) stockData.ask = data.ask;
    }
  }

  scan(): Signal[] {
    const signals: Signal[] = [];

    for (const [symbol, item] of this.watchlist) {
      if (!item.enabled) continue;

      const stockData = this.stockData.get(symbol);
      if (!stockData || !stockData.history || stockData.history.length < 20) {
        continue;
      }

      // Run momentum strategy
      const momentumSignal = this.momentumStrategy.analyze(stockData);
      if (momentumSignal) {
        signals.push(momentumSignal);
      }

      // Run mean reversion strategy
      const reversionSignal = this.meanReversionStrategy.analyze(stockData);
      if (reversionSignal) {
        signals.push(reversionSignal);
      }
    }

    // Sort by confidence × (1 - risk_score)
    signals.sort((a, b) =>
      (b.confidence * (1 - b.riskScore)) -
      (a.confidence * (1 - a.riskScore))
    );

    // Emit signals
    signals.forEach(signal => this.emit('signal', signal));

    return signals;
  }

  addToWatchlist(symbol: string): void {
    this.watchlist.set(symbol, { symbol, enabled: true });
    this.marketData.subscribe([symbol]);
  }

  removeFromWatchlist(symbol: string): void {
    this.watchlist.delete(symbol);
    this.stockData.delete(symbol);
    this.marketData.unsubscribe([symbol]);
  }

  stop(): void {
    if (this.scanInterval) {
      clearInterval(this.scanInterval);
      this.scanInterval = null;
    }
    this.marketData.disconnect();
  }
}
```

**Step 2: Commit**

```bash
git add backend/src/services/StrategyEngine.ts
git commit -m "feat: implement Strategy Engine with scanning"
```

---

## Phase 5: Risk Engine

### Task 12: Implement Risk Engine with Three-Tier Model

**Files:**
- Create: `backend/src/services/RiskEngine.ts`

**Step 1: Create backend/src/services/RiskEngine.ts**

```typescript
import { getClient } from '../db/connection';
import { Signal, Session } from '../types';

interface RiskLimits {
  maxPerTrade: number;  // Percentage
  maxDailyLoss: number;  // Percentage
  maxPositions: number;
  stopLoss: number;      // Percentage
  takeProfit: number;    // Percentage
}

interface ValidationResult {
  valid: boolean;
  errors: string[];
}

export class RiskEngine {
  private riskLimits: Map<string, RiskLimits> = new Map();

  constructor() {
    // Define risk limits by mode
    this.riskLimits.set('conservative', {
      maxPerTrade: 0.02,
      maxDailyLoss: 0.05,
      maxPositions: 3,
      stopLoss: 0.02,
      takeProfit: 0.04
    });

    this.riskLimits.set('balanced', {
      maxPerTrade: 0.05,
      maxDailyLoss: 0.10,
      maxPositions: 5,
      stopLoss: 0.02,
      takeProfit: 0.05
    });

    this.riskLimits.set('aggressive', {
      maxPerTrade: 0.10,
      maxDailyLoss: 0.20,
      maxPositions: 8,
      stopLoss: 0.03,
      takeProfit: 0.09
    });
  }

  /**
   * Calculate position size using three-tier profit-based model
   */
  async calculatePositionSize(
    userId: string,
    baseCapital: number,
    currentProfits: number,
    riskMode: 'conservative' | 'balanced' | 'aggressive'
  ): Promise<number> {
    const db = await getClient();

    // Get user's current capital
    const result = await db.query(
      'SELECT base_capital, current_capital FROM users WHERE id = $1',
      [userId]
    );

    if (!result.rows[0]) {
      await db.release();
      throw new Error('User not found');
    }

    const { baseCapital, currentCapital } = result.rows[0];
    await db.release();

    // Tier 1: Base capital (always protected at 2%)
    const tier1Risk = baseCapital * 0.02;

    // Tier 2: First $500 of profits at 50%
    let tier2Risk = 0;
    if (currentProfits > 0) {
      const tier2Profits = Math.min(currentProfits, 500);
      tier2Risk = tier2Profits * 0.50;
    }

    // Tier 3: Excess profits at 75%
    let tier3Risk = 0;
    if (currentProfits > 500) {
      const tier3Profits = currentProfits - 500;
      tier3Risk = tier3Profits * 0.75;
    }

    let totalRisk = tier1Risk + tier2Risk + tier3Risk;

    // Cap at 10% max regardless of tier (aggressive mode max)
    const maxRisk = (baseCapital + currentProfits) * 0.10;
    totalRisk = Math.min(totalRisk, maxRisk);

    return totalRisk;
  }

  /**
   * Validate signal against risk limits
   */
  async validateSignal(
    signal: Signal,
    session: Session,
    userId: string
  ): Promise<ValidationResult> {
    const errors: string[] = [];
    const db = await getClient();

    // Check daily loss limit
    const dailyLossResult = await db.query(
      `SELECT COALESCE(SUM(CASE WHEN pnl < 0 THEN -pnl ELSE 0 END), 0) as daily_loss
       FROM trades
       WHERE user_id = $1
       AND closed_at >= CURRENT_DATE`,
      [userId]
    );

    const dailyLoss = parseFloat(dailyLossResult.rows[0].daily_loss || 0);
    const limits = this.riskLimits.get(session.riskMode);
    const maxDailyLoss = session.budget * limits.maxDailyLoss;

    if (dailyLoss >= maxDailyLoss) {
      errors.push('Daily loss limit reached');
    }

    // Check max open positions
    const positionsResult = await db.query(
      `SELECT COUNT(*) as count
       FROM positions
       WHERE user_id = $1 AND status = 'open'`,
      [userId]
    );

    const openPositions = parseInt(positionsResult.rows[0].count);
    if (openPositions >= limits.maxPositions) {
      errors.push('Maximum open positions reached');
    }

    // Check confidence threshold
    if (signal.confidence < 0.70) {
      errors.push('Signal confidence too low');
    }

    // Check liquidity (avg volume from market data service)
    // This would require fetching from market data - for now assume checked
    if (signal.positionSize < 100000) { // Minimum volume check
      errors.push('Insufficient liquidity');
    }

    await db.release();

    return {
      valid: errors.length === 0,
      errors
    };
  }

  /**
   * Check if risk limit has been hit
   */
  async checkRiskLimit(userId: string, sessionId: string): Promise<boolean> {
    const db = await getClient();

    // Get session details
    const sessionResult = await db.query(
      'SELECT * FROM sessions WHERE id = $1',
      [sessionId]
    );

    if (!sessionResult.rows[0]) {
      await db.release();
      return false;
    }

    const session = sessionResult.rows[0];
    const limits = this.riskLimits.get(session.risk_mode);
    const maxDailyLoss = session.budget * limits.maxDailyLoss;

    // Check current daily loss
    const lossResult = await db.query(
      `SELECT COALESCE(SUM(CASE WHEN pnl < 0 THEN -pnl ELSE 0 END), 0) as daily_loss
       FROM trades
       WHERE user_id = $1
       AND closed_at >= CURRENT_DATE`,
      [userId]
    );

    const dailyLoss = parseFloat(lossResult.rows[0].daily_loss || 0);
    await db.release();

    return dailyLoss >= maxDailyLoss;
  }
}

export const riskEngine = new RiskEngine();
```

**Step 2: Commit**

```bash
git add backend/src/services/RiskEngine.ts
git commit -m "feat: implement Risk Engine with three-tier model"
```

---

## Phase 6: Execution Service

### Task 13: Implement Alpaca Execution Service

**Files:**
- Create: `backend/src/config/alpaca.ts`
- Create: `backend/src/services/ExecutionService.ts`

**Step 1: Create backend/src/config/alpaca.ts**

```typescript
export const alpacaConfig = {
  apiKey: process.env.ALPACA_API_KEY || '',
  secretKey: process.env.ALPACA_SECRET_KEY || '',
  baseUrl: process.env.NODE_ENV === 'production'
    ? 'https://api.alpaca.markets'
    : 'https://paper-api.alpaca.markets'
};
```

**Step 2: Create backend/src/services/ExecutionService.ts**

```typescript
import { encryptionService } from './EncryptionService';
import { alpacaConfig } from '../config/alpaca';
import { getClient } from '../db/connection';
import { Signal } from '../types';

interface Order {
  id: string;
  symbol: string;
  side: 'buy' | 'sell';
  qty: number;
  type: 'market' | 'limit' | 'stop' | 'stop_limit';
  limitPrice?: number;
  stopPrice?: number;
  timeInForce: 'day' | 'gtc' | 'ioc' | 'opg';
  status: 'pending' | 'submitted' | 'filled' | 'cancelled' | 'rejected';
  submittedAt?: Date;
  filledAt?: Date;
  filledPrice?: number;
  filledQty?: number;
}

export class ExecutionService {
  private async getApiKeys(userId: string): Promise { apiKey: string; secretKey: string } {
    const db = await getClient();
    const result = await db.query(
      'SELECT alpaca_api_key, alpaca_secret_key FROM users WHERE id = $1',
      [userId]
    );
    await db.release();

    if (!result.rows[0] || !result.rows[0].alpaca_api_key) {
      throw new Error('Alpaca API keys not configured');
    }

    return {
      apiKey: encryptionService.decrypt(
        result.rows[0].alpaca_api_key.split(':')[0],
        result.rows[0].alpaca_api_key.split(':')[1],
        result.rows[0].alpaca_api_key.split(':')[2]
      ),
      secretKey: encryptionService.decrypt(
        result.rows[0].alpaca_secret_key.split(':')[0],
        result.rows[0].alpaca_secret_key.split(':')[1],
        result.rows[0].alpaca_secret_key.split(':')[2]
      )
    };
  }

  async submitOrder(signal: Signal, userId: string): Promise<Order> {
    const { apiKey, secretKey } = await this.getApiKeys(userId);

    const order: Order = {
      id: crypto.randomUUID(),
      symbol: signal.symbol,
      side: signal.action,
      qty: Math.floor(signal.positionSize / signal.entry),
      type: 'market',
      timeInForce: 'day',
      status: 'pending'
    };

    // Store in database
    const db = await getClient();
    await db.query(
      `INSERT INTO orders (id, signal_id, symbol, side, qty, order_type, status, submitted_at)
       VALUES ($1, $2, $3, $4, $5, $6, $7, $8)`,
      [
        order.id,
        signal.id,
        order.symbol,
        order.side,
        order.qty,
        order.type,
        order.status,
        new Date()
      ]
    );
    await db.release();

    // Submit to Alpaca
    try {
      const response = await fetch(`${alpacaConfig.baseUrl}/v2/orders`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'APCA-API-KEY-ID': apiKey,
          'APCA-API-SECRET-KEY': secretKey
        },
        body: JSON.stringify({
          symbol: order.symbol,
          side: order.side,
          type: order.type,
          time_in_force: order.timeInForce,
          qty: order.qty,
          client_order_id: `trading_assistant_${order.id}`
        })
      });

      if (response.ok) {
        const data = await response.json();

        // Update with Alpaca order ID
        await db.query(
          'UPDATE orders SET alpaca_order_id = $1, status = $2 WHERE id = $3',
          [data.id, 'submitted', order.id]
        );

        order.status = 'submitted';
      } else {
        const error = await response.json();

        // Update as rejected
        await db.query(
          'UPDATE orders SET status = $1 WHERE id = $2',
          ['rejected', order.id]
        );

        order.status = 'rejected';
        throw new Error(error.message || 'Order rejected by broker');
      }
    } catch (error) {
      await db.query(
        'UPDATE orders SET status = $1 WHERE id = $2',
        ['rejected', order.id]
      );
      throw error;
    } finally {
      await db.release();
    }

    return order;
  }

  async checkOrderStatus(orderId: string): Promise<Order> {
    const db = await getClient();

    const result = await db.query(
      'SELECT * FROM orders WHERE id = $1',
      [orderId]
    );

    if (!result.rows[0]) {
      await db.release();
      throw new Error('Order not found');
    }

    const order = result.rows[0];

    // If submitted, check status with Alpaca
    if (order.status === 'submitted' && order.alpaca_order_id) {
      const userId = await this.getUserIdFromOrder(orderId);
      const { apiKey, secretKey } = await this.getApiKeys(userId);

      const response = await fetch(`${alpacaConfig.baseUrl}/v2/orders/${order.alpaca_order_id}`, {
        headers: {
          'APCA-API-KEY-ID': apiKey,
          'APCA-API-SECRET-KEY': secretKey
        }
      });

      if (response.ok) {
        const data = await response.json();

        // Update order status
        await db.query(
          `UPDATE orders
           SET status = $1, filled_at = $2, filled_price = $3, filled_qty = $4
           WHERE id = $5`,
          [
            data.filled_at || data.status,
            data.filled_at || null,
            data.filled_avg_price || null,
            data.filled_qty || null,
            orderId
          ]
        );

        order.status = data.status;
      }
    }

    await db.release();
    return order as Order;
  }

  private async getUserIdFromOrder(orderId: string): Promise<string> {
    const db = await getClient();
    const result = await db.query(
      `SELECT u.id FROM users u
       JOIN sessions s ON s.user_id = u.id
       JOIN signals sg ON sg.session_id = s.id
       JOIN orders o ON o.signal_id = sg.id
       WHERE o.id = $1`,
      [orderId]
    );
    await db.release();

    return result.rows[0].id;
  }
}

export const executionService = new ExecutionService();
```

**Step 3: Commit**

```bash
git add backend/src/config/alpaca.ts backend/src/services/ExecutionService.ts
git commit -m "feat: implement Alpaca Execution Service"
```

---

## Phase 7: Session Management

### Task 14: Implement Session Service

**Files:**
- Create: `backend/src/services/SessionService.ts`

**Step 1: Create backend/src/services/SessionService.ts**

```typescript
import { v4 as uuidv4 } from 'uuid';
import { getClient } from '../db/connection';
import { Session } from '../types';
import { StrategyEngine } from './StrategyEngine';
import { riskEngine } from './RiskEngine';
import { executionService } from './ExecutionService';

export class SessionService {
  private sessions: Map<string, Session> = new Map();
  private strategyEngine: StrategyEngine | null = null;

  async createSession(
    userId: string,
    budget: number,
    riskMode: 'conservative' | 'balanced' | 'aggressive',
    strategies: string[],
    duration: number
  ): Promise<Session> {
    const db = await getClient();

    const session: Session = {
      id: uuidv4(),
      userId,
      budget,
      riskMode,
      status: 'running',
      startTime: new Date(),
      startingCapital: budget,
      tradesCount: 0,
      winsCount: 0,
      lossesCount: 0
    };

    await db.query(
      `INSERT INTO sessions (id, user_id, budget, risk_mode, status, start_time, starting_capital)
       VALUES ($1, $2, $3, $4, $5, $6, $7)`,
      [session.id, userId, budget, riskMode, session.status, session.startTime, session.startingCapital]
    );

    await db.release();

    // Store in memory
    this.sessions.set(session.id, session);

    // Start strategy engine
    if (!this.strategyEngine) {
      this.strategyEngine = new StrategyEngine();
      const watchlist = ['AAPL', 'TSLA', 'NVDA', 'MSFT', 'GOOGL', 'AMZN', 'META', 'NFLX'];
      await this.strategyEngine.initialize(watchlist);
    }

    // Start scanning loop
    this.startScanningLoop(session.id);

    // Set session timeout
    if (duration > 0) {
      setTimeout(() => this.endSession(session.id), duration * 60 * 1000);
    }

    return session;
  }

  private async startScanningLoop(sessionId: string): Promise<void> {
    const session = this.sessions.get(sessionId);
    if (!session || session.status !== 'running') {
      return;
    }

    try {
      // Get signals from strategy engine
      const signals = this.strategyEngine!.scan();

      for (const signal of signals) {
        // Validate against risk limits
        const validation = await riskEngine.validateSignal(signal, session, session.userId);

        if (!validation.valid) {
          console.log(`Signal rejected: ${validation.errors.join(', ')}`);
          continue;
        }

        // Calculate position size
        const profits = await this.calculateProfits(session.userId);
        const positionSize = await riskEngine.calculatePositionSize(
          session.userId,
          session.startingCapital,
          profits,
          session.riskMode
        );

        signal.positionSize = positionSize;

        // Execute trade
        const order = await executionService.submitOrder(signal, session.userId);

        console.log(`✅ Order submitted: ${order.symbol} ${order.side} ${order.qty} shares`);
      }

      // Check if risk limit hit
      const limitHit = await riskEngine.checkRiskLimit(session.userId, sessionId);
      if (limitHit) {
        await this.endSession(sessionId, 'Risk limit reached');
      }
    } catch (error) {
      console.error('Error in scanning loop:', error);
    }

    // Schedule next scan (30 seconds)
    if (this.sessions.get(sessionId)?.status === 'running') {
      setTimeout(() => this.startScanningLoop(sessionId), 30000);
    }
  }

  private async calculateProfits(userId: string): Promise<number> {
    const db = await getClient();
    const result = await db.query(
      `SELECT COALESCE(SUM(pnl), 0) as total_pnl FROM trades WHERE user_id = $1`,
      [userId]
    );
    await db.release();
    return parseFloat(result.rows[0].total_pnl || 0);
  }

  async endSession(sessionId: string, reason?: string): Promise<Session> {
    const session = this.sessions.get(sessionId);
    if (!session) {
      throw new Error('Session not found');
    }

    const db = await getClient();

    // Update session
    await db.query(
      `UPDATE sessions
       SET status = $1, end_time = $2, total_pnl = $3
       WHERE id = $4`,
      ['stopped', new Date(), reason ? reason : session.totalPnl, sessionId]
    );

    await db.release();

    // Update memory
    session.status = 'stopped';
    session.endTime = new Date();
    this.sessions.set(sessionId, session);

    return session;
  }

  async emergencyStop(sessionId: string): Promise<Session> {
    const session = this.sessions.get(sessionId);
    if (!session) {
      throw new Error('Session not found');
    }

    // Cancel all pending orders
    // Close all positions
    // Stop scanning

    return this.endSession(sessionId, 'Emergency stop activated');
  }

  getSession(sessionId: string): Session | undefined {
    return this.sessions.get(sessionId);
  }
}

export const sessionService = new SessionService();
```

**Step 2: Add uuid dependency to backend/package.json**

```json
"dependencies": {
  ...
  "uuid": "^9.0.1",
  "@types/uuid": "^9.0.8"
}
```

**Step 3: Commit**

```bash
git add backend/src/services/SessionService.ts backend/package.json
git commit -m "feat: implement Session Service with auto-trading"
```

---

## Phase 8: WebSocket Integration

### Task 15: Implement WebSocket Handler

**Files:**
- Create: `backend/src/websocket/handler.ts`
- Create: `backend/src/websocket/events.ts`

**Step 1: Create backend/src/websocket/events.ts**

```typescript
export interface WebSocketEvent {
  type: string;
  data: any;
  timestamp: Date;
}

export class EventEmitter {
  private listeners: Map<string, Set<Function>> = new Map();

  on(event: string, callback: Function): void {
    if (!this.listeners.has(event)) {
      this.listeners.set(event, new Set());
    }
    this.listeners.get(event)!.add(callback);
  }

  emit(event: string, data: any): void {
    const listeners = this.listeners.get(event);
    if (listeners) {
      listeners.forEach(callback => callback(data));
    }
  }

  off(event: string, callback: Function): void {
    const listeners = this.listeners.get(event);
    if (listeners) {
      listeners.delete(callback);
    }
  }
}

export const eventEmitter = new EventEmitter();
```

**Step 2: Create backend/src/websocket/handler.ts**

```typescript
import { FastifyRequest } from 'fastify';
import { WebSocket } from 'ws';
import { eventEmitter } from './events';

export function handleWebSocket(connection: WebSocket, req: FastifyRequest) {
  console.log('WebSocket client connected');

  connection.on('message', async (data) => {
    try {
      const message = JSON.parse(data.toString());
      await handleClientMessage(message, connection);
    } catch (error) {
      connection.send(JSON.stringify({
        type: 'error',
        data: { message: 'Invalid message format' }
      }));
    }
  });

  connection.on('close', () => {
    console.log('WebSocket client disconnected');
  });

  // Subscribe to events
  eventEmitter.on('signal', (data) => {
    connection.send(JSON.stringify({
      type: 'signal:generated',
      data
    }));
  });

  eventEmitter.on('order', (data) => {
    connection.send(JSON.stringify({
      type: 'order:submitted',
      data
    }));
  });

  eventEmitter.on('fill', (data) => {
    connection.send(JSON.stringify({
      type: 'order:filled',
      data
    }));
  });

  eventEmitter.on('position', (data) => {
    connection.send(JSON.stringify({
      type: 'position:opened',
      data
    }));
  });

  eventEmitter.on('risk', (data) => {
    connection.send(JSON.stringify({
      type: 'risk:warning',
      data
    }));
  });
}

async function handleClientMessage(message: any, connection: WebSocket) {
  switch (message.type) {
    case 'session:start':
      // Handle session start
      break;
    case 'session:stop':
      // Handle session stop
      break;
    case 'session:emergency':
      // Handle emergency stop
      break;
    case 'subscribe:market':
      // Subscribe to market data
      break;
    default:
      console.log('Unknown message type:', message.type);
  }
}
```

**Step 3: Update backend/src/app.ts to register WebSocket**

```typescript
import { websocketPlugin } from '@fastify/websocket';
import { handleWebSocket } from './websocket/handler';

// In createApp function:
await app.register(websocketPlugin);

app.register(async function (fastify) {
  fastify.get('/ws', { websocket: true }, (connection, req) => {
    handleWebSocket(connection.socket, req);
  });
});
```

**Step 4: Commit**

```bash
git add backend/src/websocket/
git commit -m "feat: add WebSocket handler for real-time updates"
```

---

## Phase 9: Session Routes

### Task 16: Implement Session Routes

**Files:**
- Create: `backend/src/routes/sessions.ts`

**Step 1: Create backend/src/routes/sessions.ts**

```typescript
import { FastifyInstance } from 'fastify';
import { sessionService } from '../services/SessionService';

export async function sessionRoutes(fastify: FastifyInstance) {
  fastify.post('/', async (request, reply) => {
    try {
      // Verify JWT token (add auth middleware)
      const userId = (request as any).user?.id;
      if (!userId) {
        return reply.status(401).send({ error: 'Unauthorized' });
      }

      const payload = request.body as {
        budget: number;
        riskMode: 'conservative' | 'balanced' | 'aggressive';
        strategies: string[];
        maxDuration: number;
      };

      const session = await sessionService.createSession(
        userId,
        payload.budget,
        payload.riskMode,
        payload.strategies,
        payload.maxDuration
      );

      return reply.status(201).send(session);
    } catch (error) {
      return reply.status(500).send({ error: 'Failed to create session' });
    }
  });

  fastify.get('/:id', async (request, reply) => {
    try {
      const userId = (request as any).user?.id;
      const { id } = request.params as { id: string };

      const session = sessionService.getSession(id);

      if (!session || session.userId !== userId) {
        return reply.status(404).send({ error: 'Session not found' });
      }

      return reply.send(session);
    } catch (error) {
      return reply.status(500).send({ error: 'Internal server error' });
    }
  });

  fastify.put('/:id/stop', async (request, reply) => {
    try {
      const userId = (request as any).user?.id;
      const { id } = request.params as { id: string };

      const session = sessionService.getSession(id);
      if (!session || session.userId !== userId) {
        return reply.status(404).send({ error: 'Session not found' });
      }

      const stopped = await sessionService.endSession(id);
      return reply.send(stopped);
    } catch (error) {
      return reply.status(500).send({ error: 'Failed to stop session' });
    }
  });

  fastify.delete('/:id', async (request, reply) => {
    try {
      const userId = (request as any).user?.id;
      const { id } = request.params as { id: string };

      const session = sessionService.getSession(id);
      if (!session || session.userId !== userId) {
        return reply.status(404).send({ error: 'Session not found' });
      }

      const stopped = await sessionService.emergencyStop(id);
      return reply.send(stopped);
    } catch (error) {
      return reply.status(500).send({ error: 'Emergency stop failed' });
    }
  });
}
```

**Step 2: Update backend/src/app.ts to register session routes**

```typescript
import { sessionRoutes } from './routes/sessions';

// In createApp function:
await app.register(sessionRoutes, { prefix: '/api/sessions' });
```

**Step 3: Commit**

```bash
git add backend/src/routes/sessions.ts backend/src/app.ts
git commit -m "feat: add session management routes"
```

---

## Phase 10: Testing

### Task 17: Add Unit Tests for Risk Engine

**Files:**
- Create: `backend/tests/unit/RiskEngine.test.ts`

**Step 1: Create backend/tests/unit/RiskEngine.test.ts**

```typescript
import { describe, it, expect } from '@jest/globals';
import { RiskEngine } from '../../src/services/RiskEngine';

describe('RiskEngine - Three-Tier Position Sizing', () => {
  const riskEngine = new RiskEngine();

  describe('Tier 1: Base Capital Protection', () => {
    it('should never risk more than 2% of base capital', async () => {
      const baseCapital = 1000;
      const profits = 0;
      const size = await riskEngine.calculatePositionSize(
        'user-1',
        baseCapital,
        profits,
        'balanced'
      );

      expect(size).toBe(20); // 2% of $1,000
    });

    it('should maintain Tier 1 risk even with large profits', async () => {
      const baseCapital = 1000;
      const profits = 10000;
      const tier1Risk = 20; // Still 2%

      // Verify base capital is always protected
      expect(tier1Risk).toBeLessThanOrEqual(20);
    });
  });

  describe('Tier 2: Accumulated Profits', () => {
    it('should allow 50% risk on first $500 of profits', async () => {
      const baseCapital = 1000;
      const profits = 300;
      const size = await riskEngine.calculatePositionSize(
        'user-1',
        baseCapital,
        profits,
        'balanced'
      );

      const tier1Risk = 20;
      const tier2Risk = 150; // 50% of $300
      expect(size).toBe(tier1Risk + tier2Risk);
    });
  });

  describe('Tier 3: Excess Profits', () => {
    it('should allow 75% risk on profits above $500', async () => {
      const baseCapital = 1000;
      const profits = 2000;
      const size = await riskEngine.calculatePositionSize(
        'user-1',
        baseCapital,
        profits,
        'balanced'
      );

      const tier1Risk = 20;
      const tier2Risk = 250; // 50% of first $500
      const tier3Risk = 1125; // 75% of remaining $1,500
      expect(size).toBe(tier1Risk + tier2Risk + tier3Risk);
    });
  });

  describe('Max Position Cap', () => {
    it('should cap total position at 10% of total capital', async () => {
      const baseCapital = 1000;
      const profits = 10000;
      const totalCapital = baseCapital + profits;
      const maxAllowed = totalCapital * 0.10;

      const size = await riskEngine.calculatePositionSize(
        'user-1',
        baseCapital,
        profits,
        'balanced'
      );

      expect(size).toBeLessThanOrEqual(maxAllowed);
    });
  });
});
```

**Step 2: Add Jest configuration to backend/package.json**

```json
"jest": {
  "preset": "ts-jest",
  "testEnvironment": "node",
  "roots": ["<rootDir>/tests"],
  "testMatch": ["**/*.test.ts"]
}
```

**Step 3: Commit**

```bash
git add backend/tests/
git commit -m "test: add Risk Engine unit tests"
```

---

## Phase 11: Web Dashboard

### Task 18: Setup Web Dashboard Workspace

**Files:**
- Create: `web-dashboard/package.json`
- Create: `web-dashboard/tsconfig.json`
- Create: `web-dashboard/vite.config.ts`
- Create: `web-dashboard/index.html`
- Create: `web-dashboard/src/main.tsx`
- Create: `web-dashboard/src/App.tsx`

**Step 1: Create web-dashboard/package.json**

```json
{
  "name": "web-dashboard",
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "preview": "vite preview",
    "lint": "eslint . --ext .ts,.tsx"
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.22.1",
    "socket.io-client": "^4.7.2",
    "recharts": "^2.12.0",
    "date-fns": "^3.3.1"
  },
  "devDependencies": {
    "@types/react": "^18.2.55",
    "@types/react-dom": "^18.2.19",
    "@types/node": "^20.11.28",
    "@types/date-fns": "^2.6.0",
    "@vitejs/plugin-react": "^4.2.1",
    "autoprefixer": "^10.4.18",
    "eslint": "^8.57.0",
    "postcss": "^8.4.35",
    "tailwindcss": "^3.4.1",
    "typescript": "^5.4.5",
    "vite": "^5.1.6"
  }
}
```

**Step 2: Create web-dashboard/tsconfig.json**

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "useDefineForClassFields": true,
    "lib": ["ES2022", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx",
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true
  },
  "include": ["src"],
  "references": [{ "path": "../shared" }]
}
```

**Step 3: Create web-dashboard/vite.config.ts**

```typescript
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      '/api': 'http://localhost:3000',
      '/ws': {
        target: 'ws://localhost:3000',
        ws: true
      }
    }
  }
});
```

**Step 4: Create web-dashboard/index.html**

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Trading Assistant</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.tsx"></script>
  </body>
</html>
```

**Step 5: Create web-dashboard/src/main.tsx**

```tsx
import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter } from 'react-router-dom';
import App from './App';
import './index.css';

ReactDOM.createRoot(
  document.getElementById('root')!
).render(
  <React.StrictMode>
    <BrowserRouter>
      <App />
    </BrowserRouter>
  </React.StrictMode>
);
```

**Step 6: Create web-dashboard/src/App.tsx**

```tsx
import { Routes, Route } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import Login from './pages/Login';

function App() {
  return (
    <div className="min-h-screen bg-gray-900 text-white">
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/" element={<Dashboard />} />
      </Routes>
    </div>
  );
}

export default App;
```

**Step 7: Create web-dashboard/src/index.css**

```css
@tailwind base;
@tailwind components;
@tailwind utilities;

body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
    'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
    sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
```

**Step 8: Create web-dashboard/tailwind.config.js**

```js
/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
```

**Step 9: Install dependencies**

```bash
cd web-dashboard
npm install
```

**Step 10: Commit**

```bash
git add web-dashboard/
git commit -m "feat: setup web dashboard workspace with Vite + React"
```

---

## Phase 12: Deployment

### Task 19: Create Docker Configuration

**Files:**
- Create: `backend/Dockerfile`
- Create: `web-dashboard/Dockerfile`
- Update: `docker-compose.yml`

**Step 1: Create backend/Dockerfile**

```dockerfile
FROM node:20-alpine

WORKDIR /app

COPY package*.json ./
RUN npm ci --only=production

COPY . .
RUN npm run build

EXPOSE 3000

CMD ["npm", "start"]
```

**Step 2: Create web-dashboard/Dockerfile**

```dockerfile
FROM node:20-alpine AS builder

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

**Step 3: Update docker-compose.yml**

```yaml
version: '3.8'

services:
  postgres:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: trading
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:-trading_prod}
      POSTGRES_DB: trading_assistant
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    ports:
      - "3000:3000"
    environment:
      - DATABASE_URL=postgresql://trading:${POSTGRES_PASSWORD:-trading_prod}@postgres:5432/trading_assistant
      - REDIS_URL=redis://redis:6379
      - NODE_ENV=${NODE_ENV:-production}
      - JWT_SECRET=${JWT_SECRET}
      - ENCRYPTION_KEY=${ENCRYPTION_KEY}
      - POLYGON_API_KEY=${POLYGON_API_KEY}
    depends_on:
      - postgres
      - redis

  dashboard:
    build:
      context: ./web-dashboard
      dockerfile: Dockerfile
    ports:
      - "80:80"
    depends_on:
      - backend

volumes:
  postgres_data:
  redis_data:
```

**Step 4: Commit**

```bash
git add backend/Dockerfile web-dashboard/Dockerfile docker-compose.yml
git commit -m "feat: add Docker configuration for deployment"
```

---

## Implementation Complete

The implementation plan is now complete with:
- 19 major tasks
- Backend API with authentication, market data, strategies, risk engine, execution
- Session management with auto-trading
- WebSocket for real-time updates
- Web dashboard foundation
- Testing framework
- Docker deployment configuration

**Next Steps:**
1. Initialize new repository
2. Execute tasks in order using @superpowers:executing-plans
3. Test thoroughly with paper trading
4. Deploy to staging
5. Validate before live trading

**Critical Path for Trading:**
Authentication → Market Data → Strategy Engine → Risk Engine → Execution Service → Session Management

**Testing Priority:**
1. Risk Engine (95% coverage required)
2. Strategy Logic (90% coverage required)
3. Authentication/Security
4. Order Execution
5. End-to-end trading flows
