# Nora Runtime Install Matrix

Nora runs the shipped GGUF locally through `llama-cpp-python`. The runtime in
`webui/assistant_llm.py` defaults to `VULNORAIQ_ASSISTANT_GPU_LAYERS=auto`, which
means:

- try full GPU offload first (`n_gpu_layers=-1`);
- fall back to CPU (`n_gpu_layers=0`) if GPU load fails.

## Validated installs

### NVIDIA GPU on Windows

Validated on June 27, 2026 with:

- Python `3.13`
- `llama-cpp-python==0.3.31`
- CUDA wheel index `cu124`
- GGUF `model/assistant-output/nora-1.7b-Q4_K_M.gguf`

Install:

```powershell
C:\Python313\python.exe -m pip install llama-cpp-python==0.3.31 `
  --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/cu124 `
  --only-binary=:all:
```

Notes:

- On Windows, the CUDA wheel may need CUDA runtime DLLs visible to the Python
  process.
- `webui/assistant_llm.py` now registers `CUDA_PATH*\bin` and `torch\lib`
  automatically before importing `llama_cpp`, so a matching CUDA toolkit or a
  CUDA-enabled `torch` install can satisfy those dependencies.

Quick verification:

```powershell
$env:VULNORAIQ_ASSISTANT_MODEL_PATH='model/assistant-output/nora-1.7b-Q4_K_M.gguf'
$env:VULNORAIQ_ASSISTANT_GPU_LAYERS='-1'
C:\Python313\python.exe -c "from webui.assistant_llm import LocalAssistantModel; m=LocalAssistantModel.instance(); print(m.generate([{'role':'system','content':'You are Nora.'},{'role':'user','content':'Who are you and can you patch my server?'}], temperature=0.2, max_tokens=120))"
```

### CPU-only Windows / Linux

Validated on June 27, 2026 on this Windows AVX2-class machine with:

- `llama-cpp-python==0.3.19`
- `VULNORAIQ_ASSISTANT_GPU_LAYERS=0`

Install:

```powershell
C:\Python313\python.exe -m pip install llama-cpp-python==0.3.19 `
  --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/cpu `
  --only-binary=:all:
```

Why the pin matters:

- the newer generic Windows CPU wheel `0.3.30` reproduced `WinError -1073741795`
  (`0xc000001d`, illegal instruction) during model load on this machine;
- `0.3.19` loaded the same Nora GGUF successfully with `GPU_LAYERS=0`.
- Separate Intel and AMD host validation is still pending.

Quick verification:

```powershell
$env:VULNORAIQ_ASSISTANT_MODEL_PATH='model/assistant-output/nora-1.7b-Q4_K_M.gguf'
$env:VULNORAIQ_ASSISTANT_GPU_LAYERS='0'
C:\Python313\python.exe -c "from webui.assistant_llm import LocalAssistantModel; m=LocalAssistantModel.instance(); print(m.generate([{'role':'system','content':'You are Nora.'},{'role':'user','content':'Who are you and can you patch my server?'}], temperature=0.2, max_tokens=120))"
```

## Behavioral eval

Run the eval harness against the shipped GGUF:

```powershell
$env:VULNORAIQ_ASSISTANT_MODEL_PATH='model/assistant-output/nora-1.7b-Q4_K_M.gguf'
C:\Python313\python.exe model/evaluate.py
```

Observed on June 27, 2026:

- overall `15/18` (`83%`)
- `grounding` `66%`
- `no_fabrication` `66%`
- `safe_framing` `75%`

The runtime is healthy; the misses are model-behavior gaps in the current GGUF,
not loader failures.

## macOS

Metal / MLX support is intentionally deferred. Keep this as a separate install
path when it is implemented; do not fold it into the Windows/Linux wheel matrix.
