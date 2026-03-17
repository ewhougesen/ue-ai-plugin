# LLM Model Policy

## Prerequisite: Open Source & Small Models

**All additional LLM models used in this project MUST be:**

1. **Open Source** - No proprietary, closed-source models
2. **VERY Small** - Must run locally on:
   - User's Mac (M-series chip)
   - Docker container
   - Minimal RAM requirements (< 4GB)

---

## Approved Model Sources

| Source | Models | Size | Notes |
|--------|--------|------|-------|
| **Ollama** | Llama 3.2 (1B/3B), Phi-3, Gemma 2 (2B) | ~1-4GB | Recommended |
| **llama.cpp** | Quantized models | ~500MB-2GB | Fastest |
| **GPT4All** | Multiple small models | ~1-3GB | Easy setup |

---

## Primary Model Configuration

**z.ai API** (already configured):
- Main model: `glm-4.7` (Sonnet equivalent)
- Fallback: `glm-5` (Opus equivalent)
- Lightweight: `glm-4.5-air` (Haiku equivalent)

---

## Local Model Integration (When Needed)

For tasks requiring local models:

```python
# Example: Ollama integration
OLLAMA_BASE_URL = "http://localhost:11434"
LOCAL_MODEL = "llama3.2:1b"  # Only 1GB!
```

---

## Size Limits

| Use Case | Max Model Size |
|----------|----------------|
| **Local inference** | 2GB (quantized) |
| **Docker container** | 3GB (including dependencies) |
| **API-based (z.ai)** | No limit (runs on their servers) |

---

## Prohibited

❌ **NOT ALLOWED:**
- Proprietary models (unless via API like z.ai)
- Large local models (> 4GB)
- Models requiring enterprise hardware
- Models with restrictive licenses

---

**When in doubt: Use z.ai API or Ollama with < 2GB models.**
