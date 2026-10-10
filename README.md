# Iris-3B Comfy Nodes

ComfyUI nodes for [Iris-3B](https://huggingface.co/speridlabs/iris-3b), a 3B pixel-space text-to-image model from Sperid Labs, plus its 4x upscaler. Iris has no VAE, so everything goes straight to IMAGE.

Tested on an AMD RX 9060 XT (16 GB, ROCm on Windows). It should work the same on NVIDIA.

## Install

Search for **Iris-3B** in ComfyUI-Manager once it is on the Comfy Registry, or clone into `ComfyUI/custom_nodes`:

```
git clone https://github.com/bani4kaskashka/Iris-3B-Comfy-Nodes
```

No extra pip installs are needed. The pack uses torch, transformers (4.57 or newer), omegaconf, safetensors and huggingface_hub, which ComfyUI already ships.

## Workflows

Drag one of these into ComfyUI. They also show up under Templates.

- [`example_workflows/iris3b_text_to_image.json`](example_workflows/iris3b_text_to_image.json): Simple sampler
- [`example_workflows/iris3b_text_to_image_advanced.json`](example_workflows/iris3b_text_to_image_advanced.json): Advanced sampler
- [`example_workflows/iris3b_upscale.json`](example_workflows/iris3b_upscale.json): 4x upscale of any image

Both text-to-image workflows end with a 4x upscale node that's bypassed by default. Select it and press Ctrl+B to turn it on.

## Models

The loaders download anything that's missing on first run (about 32 GB in total), so the workflows run as-is. To get the files yourself instead:

```
hf download speridlabs/iris-3b --exclude "depth/*" --local-dir models/diffusion_models/iris-3b
hf download Qwen/Qwen3-VL-4B-Instruct --local-dir models/text_encoders/Qwen3-VL-4B-Instruct
```

That gives you:

```
models/diffusion_models/iris-3b/model.safetensors, config.yaml       text to image (12 GB)
models/diffusion_models/iris-3b/upscaler/                            4x upscaler (12 GB)
models/text_encoders/Qwen3-VL-4B-Instruct/                           text encoder (8.3 GB)
```

The text encoder has to be the original HF folder. Single-file or fp8 Qwen3-VL text encoders won't work, because Iris reads 12 hidden layers from it.

## Nodes

- **Load Iris-3B Model**: loads the DiT. `bf16` uses 6 GB of VRAM. `fp32` is the shipped precision but needs a lot more than 16 GB.
- **Load Iris Text Encoder (Qwen3-VL-4B)**: lists HF folders in `text_encoders`.
- **Iris Text Encode**: positive and negative prompt. Leave the negative empty to use the null prompt the model was trained with.
- **Iris Sampler (Simple)**: dropdowns for resolution (1 MP sizes from 21:9 to 9:21), quality (fast = 30 steps, balanced = 50, best = 100) and prompt adherence (cfg 2, 3 or 4.5), plus seed and batch size.
- **Iris Sampler (Advanced)**: every setting: steps, cfg, seed, batch size, shift, solver order, CFG interval, any width/height in multiples of 16, and keep_model_on_gpu.
- **Load Iris Upscaler** and **Iris Upscale**: Iris fine-tuned for restoration and 4x upscaling. It's a single pass per 1024 px tile with overlapping tiles and a wavelet color fix. It works on any IMAGE, not just Iris output.

Both samplers use DPM-Solver++ on the flow schedule. The defaults match the model card (cfg 3, shift 4). Live previews follow ComfyUI's preview setting and cost nothing, since Iris predicts pixels directly.

## VRAM and speed

Each model visits the GPU only for its own step and sits in system RAM otherwise, so peak VRAM is about 8 GB. Expect to need around 22 GB of free system RAM with all three models loaded.

On a 9060 XT, a 1024x1024 image takes about 1.8 s per step. 4x upscaling 1024x1024 to 4096x4096 is 49 tiles.

On AMD, start ComfyUI the normal way (`main.py`), which turns on the AOTriton flash attention kernels. Without them attention falls back to a slow path.

## Credits

The model code in `vendor/iris3b` is from [speridlabs/iris-3b](https://github.com/speridlabs/iris-3b) (Apache-2.0, see `vendor/LICENSE` and `vendor/NOTICE`). Only the inference parts are included. This pack is also Apache-2.0.
