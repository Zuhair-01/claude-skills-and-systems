---
name: gpu-model-squeeze
description: "Setup + safety playbook for running quantized local models (LLM/image/video) that exceed or barely fit the RTX 4060 8GB laptop GPU via CPU/RAM offload. Use before pulling or running: Qwen3.8-27B abliterated, Flux.1-dev abliterated, Wan2.2-14B Rapid-AIO-NSFW. Extends local-llm-expert with the offload/safety-net layer that skill doesn't cover."
---

# GPU Squeeze Playbook (8GB VRAM, 32GB RAM, i7-13650HX 20T)

Companion to `local-llm-expert` (quant format theory) — this is the practical
setup + safety net for models that need CPU/RAM offload to fit.

## Hardware ceiling (confirmed 2026-09-21)
- GPU: RTX 4060 Laptop, 8188 MiB VRAM, no eGPU possible (no Thunderbolt/USB4 on this Dell G15)
- RAM: 32GB total, but often only 8-10GB free with normal apps open — **check free RAM before any offloaded run**, not just VRAM
- CPU: i7-13650HX, 14C/20T — offload target for spillover, not fast but usable

## Pre-flight checklist (every model, every run)
1. `python D:\AI_Models\gpu_lock.py status` — don't run if another job holds the GPU
2. Check free RAM: PowerShell `Get-CimInstance Win32_OperatingSystem | Select FreePhysicalMemory` (KB) — need free RAM ≥ (offloaded GB × 1.3) headroom, or the OS starts swapping and everything stalls, not just the model
3. Check disk free on D: — model files are large, verify space before pulling, not after
4. Acquire GPU lock as this job's owner name before loading; release in a finally/trap so a crash doesn't strand the lock

## Runtime install (do first, before any model pull)
- **LLM runtime: LM Studio** — already installed (`~/.lmstudio`), loads pre-quantized GGUF directly with a GPU-offload slider. No separate llama.cpp setup needed.
- **Image + video runtime: ComfyUI** — NOT installed yet. Both Flux and Wan2.2 GGUF workflows need it; considered SwarmUI (just wraps ComfyUI, no real alternative) and Forge (image-only, no video support) — neither replaces it, don't split into two UIs for no VRAM benefit.
  - Install portable Windows build to `D:\AI_Models\ComfyUI` (~5GB)
  - Required custom node: `city96/ComfyUI-GGUF` (`git clone` into `custom_nodes/`, then `pip install -r requirements.txt` via ComfyUI's bundled python) — this is what makes the GGUF Unet Loader node exist at all
  - Model placement: `.gguf` UNet files → `models/unet/`, text encoders → `models/clip/`, VAE → `models/vae/`
  - No "soup" quantization tool exists (checked GitHub thoroughly) — `mlfoundations/model-soups` is a different technique (weight-averaging fine-tunes for accuracy, not compression). Don't confuse the two.

## Per-model setup

### Qwen3.8-27B-abliterated (huihui-ai), IQ3_XXS quant
- Runtime: llama.cpp / Ollama (once GGUF imported via Modelfile) or LM Studio
- Offload flag: llama.cpp `-ngl N` — start high, drop N until it loads without OOM; ~2.5GB must land on CPU/RAM at this quant
- Safety net: **run one throwaway prompt first** to confirm it loads and produces coherent text before treating it as production-ready — abliterated models occasionally degrade the model's factual/reasoning behavior more than advertised, verify before relying on it for real work
- Content check: abliterated = refusal-removed, not truth-removed — it will comply with more requests including ones a stock model refuses; treat outputs as unvetted, same review bar as any other local model output

### Flux.1-dev-abliterated-V2 (t8star), Q4_K_M
- Runtime: ComfyUI (standard for GGUF diffusion models)
- Required companion files: T5 text encoder (run in fp8, ~2.5GB) + VAE (~300MB) — these are separate downloads, not bundled in the UNet GGUF, factor into total download size
- Safety net: **set text encoder device to CPU in the ComfyUI node** (`CLIPLoader` device override) — this is what makes the 6.8GB UNet actually fit; forgetting this step is the #1 way this OOMs
- Verify: generate 1 test image at low step count before a real batch — abliterated FLUX merges sometimes drift on prompt adherence vs stock FLUX

### Wan2.2-14B-Rapid-AIO-NSFW (DoorZekor), Q4_K_S
- Runtime: ComfyUI video workflow (Wan2.2 native nodes)
- "Rapid"/distilled = fewer sampling steps needed (check the repo's README for the exact recommended step count — using stock Wan step counts on a distilled model wastes time or degrades output)
- Safety net: test on a short/low-res clip first — video models fail expensively (minutes wasted) if VRAM is misjudged; don't queue a long batch untested
- This is a NSFW-tuned checkpoint — treat its output review bar like any generated content the user will use: verify before shipping anywhere client-facing (same standard as [[feedback_voice_must_not_sound_ai]] approval-before-use pattern, applied to visual output)

## Rollback / don't-lose-progress rule
- All pulls go through `uv`'s cache (`D:\AI_Models\.uv_cache`) or HF's local cache — both resume partial downloads on retry, confirmed working across 4 retries on 2026-09-21's OmniVoice install (wifi drops mid-download, no re-download of completed bytes)
- Never delete a cache dir mid-troubleshooting to "start clean" — that's exactly the progress-loss the resumability exists to avoid
