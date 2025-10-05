# 微信公众号格式化工具示例

## 🎯 功能特色

这是一个**强大**的微信公众号格式化工具，支持：

- ✅ Markdown 转 HTML
- ✅ 一键复制到剪切板  
- ✅ 微信公众号样式优化
- ✅ 表格和代码块支持

## 📊 功能对比

| 功能 | 本工具 | 其他工具 |
|------|--------|----------|
| Python 支持 | ✅ | ❌ |
| 命令行工具 | ✅ | 部分 |
| 一键复制 | ✅ | 部分 |
| 样式优化 | ✅ | 一般 |

## 💻 代码示例

```python
from wechat_format import WeChatFormatter

formatter = WeChatFormatter()
html = formatter.convert_file('article.md')
formatter.copy_to_clipboard(html)
```

## 🔥 高亮文本

==这是高亮文本==，非常醒目！

## 📝 提示框

:::tip
这是一个提示框，用于重要信息提醒。
:::

## 🌟 总结

使用本工具，让你的微信公众号文章更加**专业**和**美观**！

---

*本示例展示了工具的主要功能，更多用法请参考文档。*
