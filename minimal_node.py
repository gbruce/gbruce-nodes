"""
Minimal ComfyUI custom node: EchoNode

This node provides a single STRING input and a single STRING output.
Place the gbruce_nodes folder in ComfyUI's custom nodes directory (e.g., ComfyUI/custom_nodes/) and restart ComfyUI.
"""

class EchoNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {"text": ("STRING",)}}

    RETURN_TYPES = ("STRING",)
    CATEGORY = "gbruce-nodes"
    FUNCTION = "echo"

    def echo(self, text="Hello from gbruce-nodes"):
        # Simple passthrough/echo implementation
        return (str(text),)
