# ajaw

[![Pypi 上的版本](https://img.shields.io/pypi/v/ajaw.svg)](https://pypi.org/project/ajaw)

<p style="text-align: center;"><a href="https://pypi.org/project/ajaw/">PyPI</a> | <a href="https://test.pypi.org/project/ajaw/">Test PyPI</a></p>

用于加载 [Python 标准库 argparse 的翻译](https://github.com/DuckDuckStudio/python-argparse-translations)。

## 使用

```bash
pip install ajaw

# Test PyPI
pip install -i https://test.pypi.org/simple/ ajaw
```

```python
import ajaw

# 自动检测
ajaw.load_translations()

# 指定语言
ajaw.load_translations(lang="zh-CN")
```

> [!TIP]  
> 如果你使用 [PyInstaller](https://pyinstaller.org) 打包，请在打包命令中添加 `--collect-data ajaw` 以打包翻译文件（`.mo` 文件）。  
> 该参数的介绍请见 [PyInstaller 文档](https://pyinstaller.org/en/stable/usage.html#cmdoption-collect-data)。

## 许可

本项目采用 [Apache License 2.0](LICENSE.txt) 许可协议。

---

包名称来源: ~~[伟大的圣龙库胡勒阿乔！](https://www.bilibili.com/video/BV1NzLJzpE6R/)~~
