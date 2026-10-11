"""Iris-3B text-to-image for ComfyUI. The model code in vendor/bucky_iris3b is upstream's iris3b
package (Apache-2.0), renamed so it can't clash with other Iris packs that bundle their own copy."""

import os
import sys

_vendor = os.path.join(os.path.dirname(os.path.abspath(__file__)), "vendor")
if _vendor not in sys.path:
    sys.path.insert(0, _vendor)

from .nodes import NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS  # noqa: E402

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]
