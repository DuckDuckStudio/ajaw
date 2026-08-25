"""
# ajaw

为 Python 标准库 `argparse` 模块提供翻译。

翻译文件（`.mo`）来源于 [DuckDuckStudio/python-argparse-translations](https://github.com/DuckDuckStudio/python-argparse-translations)。

## 使用

```python
import argparse
import ajaw

ajaw.load_translations()
```
"""

from .loader import BUNDLED_LANGUAGES, load_translations

__all__ = ["BUNDLED_LANGUAGES", "load_translations"]
