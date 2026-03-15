# Copilot Instructions

## What this repo is

`gbruce_nodes` is a ComfyUI custom nodes package. It is installed by placing the `gbruce_nodes/` folder inside a ComfyUI installation's `custom_nodes/` directory. ComfyUI discovers and loads it at startup via the `NODE_CLASS_MAPPINGS` / `NODE_DISPLAY_NAME_MAPPINGS` dicts exported from `__init__.py`.

## ComfyUI node conventions

Every node is a plain Python class. The following class-level attributes are required by ComfyUI:

- `INPUT_TYPES(cls)` — classmethod returning a dict with `"required"` and/or `"optional"` keys mapping input names to `(TYPE,)` tuples (or `(TYPE, options_dict)` tuples).
- `RETURN_TYPES` — tuple of output type strings, e.g. `("STRING",)`.
- `CATEGORY` — string shown in the node browser; use `"gbruce-nodes"` for nodes in this package.
- `FUNCTION` — name of the instance method ComfyUI calls to execute the node.

The execute method must return a tuple, even for a single output.

Nodes are registered in `__init__.py` by being exported — ComfyUI reads `NODE_CLASS_MAPPINGS` if present, or falls back to scanning for node classes. Add new nodes to the `from .module import NodeClass` imports and `__all__`.

## Package layout

```
gbruce_nodes/
  __init__.py       # version, imports, __all__
  minimal_node.py   # EchoNode, VersionNode
```

Add new node modules as peer files to `minimal_node.py` and import them in `__init__.py`.

## Version

Version is defined once in `__init__.py` as `__version__` and imported by node modules via `from . import __version__`. Keep it as the single source of truth.

## Installation / testing

There is no automated test suite. To test manually:
1. Ensure `gbruce_nodes/` is symlinked or copied into `ComfyUI/custom_nodes/`.
2. Start ComfyUI and verify the `gbruce-nodes` category appears in the node browser.
3. For quick import checks without a running ComfyUI: `python -c "from gbruce_nodes import EchoNode, VersionNode; print('OK')"` from the parent directory.
