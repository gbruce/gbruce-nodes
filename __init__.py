# gbruce_nodes package
# Minimal package exposing the custom node(s).
__version__ = "0.1.0"

from .minimal_node import EchoNode, VersionNode

__all__ = ["EchoNode", "VersionNode"]
