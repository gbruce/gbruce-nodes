# gbruce_nodes package
# Minimal package exposing the custom node(s).
__version__ = "0.1.0"

from .minimal_node import EchoNode, VersionNode
from .circle_node import CircleImageNode

__all__ = ["EchoNode", "VersionNode", "CircleImageNode"]

# Mapping expected by ComfyUI: map exported class names to classes
NODE_CLASS_MAPPINGS = {
    "EchoNode": EchoNode,
    "VersionNode": VersionNode,
    "CircleImageNode": CircleImageNode,
}

# Backwards-compatible list used by some ComfyUI versions
NODES_LIST = [EchoNode, VersionNode, CircleImageNode]
