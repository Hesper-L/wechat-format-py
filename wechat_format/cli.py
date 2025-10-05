"""
微信公众号格式化工具 - 命令行接口

提供简单易用的命令行工具，支持文件转换和剪切板操作。
"""

import os
import sys
import click
from pathlib import Path
from .converter import WeChatFormatter


@click.group()
@click.version_option(version='1.0.0', prog_name='wechat-format')
def cli():
    """微信公众号 Markdown 格式化工具
    
    将 Markdown 文件转换为适合微信公众号的 HTML 格式，
    支持一键复制到剪切板。
    """
    pass


@cli.command()
@click.argument('input_file', type=click.Path(exists=True))
@click.option('-o', '--output', type=click.Path(), help='输出文件路径（可选）')
@click.option('-c', '--copy', is_flag=True, help='转换后复制到剪切板')
@click.option('--inline', is_flag=True, help='使用内联样式（适合复制到微信后台）')
@click.option('--preview', is_flag=True, help='在浏览器中预览结果')
def convert(input_file, output, copy, inline, preview):
    """转换 Markdown 文件为微信公众号格式
    
    示例:
        wechat-format convert article.md
        wechat-format convert article.md -o output.html
        wechat-format convert article.md --copy
        wechat-format convert article.md --copy --inline
    """
    try:
        formatter = WeChatFormatter()
        
        # 转换文件
        click.echo(f"正在转换文件: {input_file}")
        html = formatter.convert_file(input_file, inline_style=inline or copy)
        
        # 保存到文件
        if output:
            with open(output, 'w', encoding='utf-8') as f:
                f.write(html)
            click.echo(f"✅ 转换完成，已保存到: {output}")
        
        # 复制到剪切板
        if copy:
            success = formatter.copy_to_clipboard(html)
            if success:
                click.echo("✅ 已复制到剪切板，可直接粘贴到微信公众号后台")
            else:
                click.echo("❌ 复制到剪切板失败")
        
        # 预览
        if preview:
            preview_file = _create_preview_file(html, input_file)
            click.echo(f"📖 预览文件已生成: {preview_file}")
            _open_in_browser(preview_file)
        
        # 如果没有指定输出选项，显示帮助信息
        if not output and not copy and not preview:
            click.echo("💡 提示: 使用 --copy 复制到剪切板，或 -o 保存到文件")
            
    except Exception as e:
        click.echo(f"❌ 转换失败: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.argument('input_file', type=click.Path(exists=True))
def copy(input_file):
    """快速转换并复制到剪切板
    
    这是 'convert --copy --inline' 的快捷方式
    
    示例:
        wechat-format copy article.md
    """
    try:
        formatter = WeChatFormatter()
        
        click.echo(f"正在转换文件: {input_file}")
        html, success = formatter.convert_file_and_copy(input_file)
        
        if success:
            click.echo("✅ 转换完成并已复制到剪切板")
            click.echo("📋 现在可以直接粘贴到微信公众号后台")
        else:
            click.echo("❌ 复制到剪切板失败")
            
    except Exception as e:
        click.echo(f"❌ 转换失败: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.option('-p', '--port', default=5000, help='Web 服务器端口 (默认: 5000)')
@click.option('--debug', is_flag=True, help='启用调试模式')
def serve(port, debug):
    """启动 Web 界面服务器
    
    提供实时预览和转换功能的 Web 界面
    
    示例:
        wechat-format serve
        wechat-format serve -p 8080
    """
    try:
        from .web import create_app
        
        app = create_app()
        
        click.echo(f"🚀 启动 Web 服务器...")
        click.echo(f"📱 访问地址: http://localhost:{port}")
        click.echo(f"💡 按 Ctrl+C 停止服务器")
        
        app.run(host='0.0.0.0', port=port, debug=debug)
        
    except ImportError:
        click.echo("❌ Web 界面功能需要安装 Flask")
        click.echo("💡 运行: pip install flask")
        sys.exit(1)
    except Exception as e:
        click.echo(f"❌ 启动服务器失败: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.argument('input_file', type=click.Path(exists=True))
def preview(input_file):
    """在浏览器中预览转换结果
    
    示例:
        wechat-format preview article.md
    """
    try:
        formatter = WeChatFormatter()
        
        click.echo(f"正在生成预览: {input_file}")
        html = formatter.convert_file(input_file, inline_style=False)
        
        preview_file = _create_preview_file(html, input_file)
        click.echo(f"📖 预览文件已生成: {preview_file}")
        
        _open_in_browser(preview_file)
        
    except Exception as e:
        click.echo(f"❌ 生成预览失败: {e}", err=True)
        sys.exit(1)


@cli.command()
def demo():
    """生成示例 Markdown 文件
    
    创建一个包含各种格式的示例文件，用于测试转换效果
    """
    demo_content = """# 微信公众号格式化工具示例

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
"""
    
    demo_file = "wechat_demo.md"
    
    try:
        with open(demo_file, 'w', encoding='utf-8') as f:
            f.write(demo_content)
        
        click.echo(f"✅ 示例文件已生成: {demo_file}")
        click.echo("💡 现在可以运行: wechat-format copy wechat_demo.md")
        
    except Exception as e:
        click.echo(f"❌ 生成示例文件失败: {e}", err=True)


def _create_preview_file(html: str, input_file: str) -> str:
    """创建预览文件"""
    input_path = Path(input_file)
    preview_file = input_path.with_suffix('.preview.html')
    
    with open(preview_file, 'w', encoding='utf-8') as f:
        f.write(html)
    
    return str(preview_file)


def _open_in_browser(file_path: str):
    """在浏览器中打开文件"""
    import webbrowser
    import urllib.parse
    
    file_url = 'file://' + urllib.parse.quote(os.path.abspath(file_path))
    webbrowser.open(file_url)


if __name__ == '__main__':
    cli()