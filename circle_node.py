from . import __version__
from PIL import Image, ImageDraw
import numpy as np
try:
    import torch
except Exception:
    torch = None


class _NumpyImageWrapper:
    """Wrap a numpy HxWxC uint8 array and present a .cpu().numpy() float HxWxC (0..1) API

    ComfyUI often calls image.cpu().numpy(); if numpy arrays are returned directly that lacks .cpu().
    This wrapper provides cpu() and numpy() so both code paths work consistently.
    """
    def __init__(self, arr_uint8):
        # store float32 array in 0..1 range, HxWxC
        self._arr = arr_uint8.astype('float32') / 255.0

    def cpu(self):
        return self

    def numpy(self):
        return self._arr

    # common torch-like convenience methods
    def detach(self):
        return self

    def to(self, *args, **kwargs):
        return self

class CircleImageNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {"width": ("INT",), "height": ("INT",), "batch_size": ("INT",)}}

    RETURN_TYPES = ("IMAGE",)
    CATEGORY = "gbruce-nodes"
    FUNCTION = "generate"
    VERSION = __version__

    def _clamp(self, v, lo, hi):
        return max(lo, min(hi, int(v)))

    def generate(self, width=256, height=256, batch_size=1):
        width = self._clamp(width, 8, 8192)
        height = self._clamp(height, 8, 8192)
        batch_size = self._clamp(batch_size, 1, 64)

        size = (width, height)
        radius = min(width, height) // 2
        margin = max(2, min(4, radius // 16))
        bbox = [ (width//2) - radius + margin,
                 (height//2) - radius + margin,
                 (width//2) + radius - margin,
                 (height//2) + radius - margin ]

        images = []
        for _ in range(batch_size):
            img = Image.new("RGB", size, "black")
            draw = ImageDraw.Draw(img)
            draw.ellipse(bbox, fill="white")
            arr = np.array(img, dtype=np.uint8)
            # Normalize channels to HxWx3
            if arr.ndim == 2:
                arr = np.stack([arr, arr, arr], axis=-1)
            elif arr.ndim == 3 and arr.shape[2] == 1:
                arr = np.concatenate([arr, arr, arr], axis=2)
            elif arr.ndim == 3 and arr.shape[2] >= 4:
                # If there is an alpha channel or unexpected extra channels, take first 3
                arr = arr[:, :, :3]

            # If torch is available, convert to float CHW tensor in 0..1 range (expected by ComfyUI)
            if torch is not None:
                try:
                    t = torch.from_numpy(arr.astype('float32') / 255.0).permute(2, 0, 1).contiguous()
                    images.append(t)
                except Exception:
                    images.append(_NumpyImageWrapper(arr))
            else:
                # Wrap numpy arrays so callers can call .cpu().numpy() safely
                images.append(_NumpyImageWrapper(arr))

        # Return a tuple containing the list of image tensors/wrappers as expected by ComfyUI
        return (images,)
