# VulnoraIQ assistant model — training pipeline

Train a small instruction-tuned model for the VulnoraIQ assistant.

## Quick start

```bash
# 1. Install training deps
pip install -r vulnoraiq/model/requirements-train.txt

# 2. Generate dataset from OWASP docs
python vulnoraiq/model/prepare_dataset.py

# 3. Train (QLoRA, ~20-40 min on 16 GB GPU)
python vulnoraiq/model/train.py
```

The script creates `./assistant-output/` with:
- `adapter/` — LoRA adapter weights
- `merged/` — full merged model in HF format (convert this to GGUF, see below)

Test it with:

```bash
VULNORAIQ_ASSISTANT_MODEL_PATH=./assistant-output/nora-1.5b-Q6_K.gguf \
    python -c "from webui.assistant_llm import LocalAssistantModel; \
    m = LocalAssistantModel.instance(); \
    print(m.generate([{'role':'user','content':'What is prompt injection?'}], temperature=0.2, max_tokens=256))"
```

## Evaluation

Validate behaviour against a held-out, hand-written eval set (`eval_dataset.jsonl`)
that is phrased unlike the templated training data — an honest signal of whether the
model generalises. Cases assert behaviour (identity, refusal-to-fix, no CVE
fabrication, grounding, safe framing, CVE-reference use), not exact text.

```bash
# verify the harness logic (no model needed)
python model/evaluate.py --selftest

# score a model, then compare old vs new by running twice
VULNORAIQ_ASSISTANT_MODEL_PATH=model/assistant-output/nora-1.5b-Q6_K.gguf \
    python model/evaluate.py
```

## Assistant identity and tools (Nora)

The model is "Nora", the VulnoraIQ assistant (display name `nora-assistant`). It is
trained to ground answers in supplied **reference material** and to never invent CVE
ids/CVSS scores. The runtime injects that reference material from:

- `docs/owasp/` + `model/knowledge/` (the extracted OWASP PDFs) via bag-of-words RAG;
- authoritative CVE/CVSS records fetched from NVD for any CVE id named in the prompt
  (`assistant_tools.cve_reference_lookup`);
- `web_fetch` of a public security URL the user provides.

> After changing the model name, rebuild the WebUI bundle (`webui/console`) so the
> served frontend picks up `nora-assistant`; the committed `webui/static` bundle is
> generated, not hand-edited.

## Options

| Flag | Default | Description |
|------|---------|-------------|
| `--base` | Qwen/Qwen2.5-1.5B-Instruct | Base model (0.5B = smaller/faster, 3B = best quality; stay in the Qwen family to keep the ChatML template) |
| `--dataset` | auto (from OWASP docs) | Custom JSONL dataset path |
| `--epochs` | 2 | Training epochs (early stopping on eval_loss also enabled) |
| `--lr` | 2e-4 | Peak learning rate |
| `--batch-size` | 2 | Per-device batch size |
| `--grad-accum` | 4 | Gradient accumulation steps |
| `--max-seq-len` | 2048 | Max sequence length |
| `--lora-r` | 16 | LoRA rank |
| `--gguf-quant` | q4_k_m | GGUF quantization type |
| `--upload-to-hf` | — | Upload adapter to HuggingFace repo |

## Dataset format

JSONL with `messages` key (OpenAI chat format):

```jsonl
{"messages": [{"role": "system", "content": "..."}, {"role": "user", "content": "..."}, {"role": "assistant", "content": "..."}]}
```

Run `prepare_dataset.py` to generate from OWASP docs. Add your own examples by appending to the output JSONL.

## Model recommendations

| Model | Params | VRAM | GGUF (Q6_K) | Notes |
|-------|--------|------|-------------|-------|
| **Qwen2.5-1.5B-Instruct** | 1.5B | ~6 GB | ~1.3 GB | **Default.** Best quality/effort balance; Apache-2.0; drop-in ChatML. |
| Qwen2.5-0.5B-Instruct | 0.5B | ~4 GB | ~0.5 GB | Smaller/faster; leans hardest on RAG. |
| Qwen2.5-3B-Instruct | 3B | ~8 GB | ~2.5 GB | Highest quality on a 16 GB GPU. |
| Llama-3.2-1B-Instruct | 1B | ~5 GB | ~1.0 GB | Fallback only — needs ChatML retemplating + Llama license. |

Nora's job is grounding on injected reference material, so larger models mainly buy
better synthesis and fewer degenerate/off-template outputs. Measure any base change
with `evaluate.py` rather than assuming.

## Distributing Nora (model file, not a hosted service)

Hosting the GGUF on HuggingFace distributes the **weights file** — it does *not*
stand up a public Nora anyone can chat with. Each VulnoraIQ instance auto-downloads
the GGUF and runs Nora **locally, in-process** (llama-cpp) on the user's own hardware.

After training and converting to GGUF (e.g. `nora-1.5b-Q6_K.gguf`):

```bash
# upload the GGUF to a HuggingFace repo you own
huggingface-cli upload youruser/nora-assistant nora-1.5b-Q6_K.gguf
```

Users point their instance at it:

```
VULNORAIQ_ASSISTANT_MODEL_REPO=youruser/nora-assistant
VULNORAIQ_ASSISTANT_MODEL_FILE=nora-1.5b-Q6_K.gguf
```

The first-run autodownload fetches it automatically. Notes:

- The repo must be **public** — the auto-download uses a plain URL with no token, so
  a private/gated repo would 401.
- Redistribution is fine on a **Qwen** base (Apache-2.0); a Llama base adds license
  conditions.
- A public, browser-accessible Nora is a *separate* deployment of the WebUI itself —
  add auth and a privacy review first, since findings can contain sensitive target
  data and Nora has web/CVE lookup.

## GGUF conversion

`train.py` stops at the merged HF model; convert it to GGUF with llama.cpp:

```bash
git clone https://github.com/ggerganov/llama.cpp
python llama.cpp/convert_hf_to_gguf.py assistant-output/merged \
    --outtype q6_k -o assistant-output/nora-1.5b-Q6_K.gguf
```

Size is no longer constrained, so `q6_k` (~1.3 GB for 1.5B) is a good quality/size
balance; use `q8_0` for maximum fidelity or `q4_k_m` for the smallest file.
