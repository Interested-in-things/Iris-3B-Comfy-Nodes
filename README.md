# Iris-3B Comfy Nodes

ComfyUI nodes for [Iris-3B](https://huggingface.co/speridlabs/iris-3b), a 3B pixel-space text-to-image model from Sperid Labs, plus its 4x upscaler. Iris has no VAE, so everything goes straight to IMAGE.

Tested on an AMD RX 9060 XT (16 GB, ROCm on Windows). It should work the same on NVIDIA.

## Install

Search for **Iris-3B** in ComfyUI-Manager, or clone into `ComfyUI/custom_nodes`:

```
git clone https://github.com/bani4kaskashka/Iris-3B-Comfy-Nodes
```

Nothing else to install. It needs transformers 4.57 or newer, which recent ComfyUI already has.

## Workflows

Download one and drag it into ComfyUI, or open it from Templates once the pack is installed.

- [Iris-3B Text to Image (Simple)](example_workflows/Iris-3B%20Text%20to%20Image%20%28Simple%29.json): resolution and quality presets
- [Iris-3B Text to Image (Advanced)](example_workflows/Iris-3B%20Text%20to%20Image%20%28Advanced%29.json): every sampler setting
- [Iris-3B Upscale 4x](example_workflows/Iris-3B%20Upscale%204x.json): 4x upscale of any image

Both text-to-image workflows end with a 4x upscale group (1024 to 4096) that's bypassed by default. Select the group and press Ctrl+B to turn it on.

## Models

When a workflow opens with a model missing, ComfyUI lists it under Missing Models with a Download button. The loaders also download anything still missing on first run (about 32 GB in total), so the workflows run as-is either way.

```
models/diffusion_models/iris-3b.safetensors            text to image (12 GB)
models/diffusion_models/iris-3b-upscaler.safetensors   4x upscaler (12 GB)
models/text_encoders/Qwen3-VL-4B-Instruct/             text encoder, the whole HF repo (8.3 GB)
```

To get them yourself, the two Iris files are `model.safetensors` and `upscaler/model.safetensors` from [speridlabs/iris-3b](https://huggingface.co/speridlabs/iris-3b), renamed as above. The configs come with this pack.

```
hf download Qwen/Qwen3-VL-4B-Instruct --local-dir models/text_encoders/Qwen3-VL-4B-Instruct
```

The text encoder has to be the original HF folder. Single-file or fp8 Qwen3-VL text encoders won't work, because Iris reads 12 hidden layers from it.

## Nodes

- **Load Iris-3B Model**: loads the DiT. `bf16` uses 6 GB of VRAM. `fp32` is the shipped precision but needs a lot more than 16 GB.
- **Load Iris Text Encoder (Qwen3-VL-4B)**: lists HF folders in `text_encoders`.
- **Iris Text Encode**: positive and negative prompt. Leave the negative empty to use the null prompt the model was trained with.
- **Iris Sampler (Simple)**: dropdowns for resolution (1 MP sizes from 21:9 to 9:21), quality (fast = 30 steps, balanced = 50, best = 100) and prompt adherence (cfg 2, 3 or 4.5), plus seed and batch size.
- **Iris Sampler (Advanced)**: every setting: steps, cfg, seed, batch size, shift, solver order, CFG interval, any width/height in multiples of 16, and keep_model_on_gpu.
- **Load Iris Upscaler** and **Iris Upscale**: Iris fine-tuned for restoration and 4x upscaling. It's a single pass per 1024 px tile with overlapping tiles and a wavelet color fix. It works on any IMAGE, not just Iris output. With `limit_input_size` on, big inputs are shrunk first (short side 512, long side 1024), so the output stays at or under 2048x4096. Turn it off for a full 4x of any size.

Both samplers use DPM-Solver++ on the flow schedule. The defaults match the model card (cfg 3, shift 4). Live previews follow ComfyUI's preview setting and cost nothing, since Iris predicts pixels directly.

## VRAM and speed

Each model visits the GPU only for its own step and sits in system RAM otherwise, so peak VRAM is about 8 GB. Expect to need around 22 GB of free system RAM with all three models loaded.

On a 9060 XT, a 1024x1024 image takes about 1.8 s per step. 4x upscaling 1024x1024 to 4096x4096 is 49 tiles.

On AMD, start ComfyUI the normal way (`main.py`), which turns on the AOTriton flash attention kernels. Without them attention falls back to a slow path.

## Credits

The model code in `vendor/iris3b` is from [speridlabs/iris-3b](https://github.com/speridlabs/iris-3b) (Apache-2.0, see `vendor/LICENSE` and `vendor/NOTICE`). Only the inference parts are included. This pack is also Apache-2.0.
