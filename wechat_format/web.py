"""
微信公众号格式化工具 - Web 界面

提供实时预览和转换功能的 Web 界面。
"""

from flask import Flask, render_template, request, jsonify
from .converter import WeChatFormatter
import os


def create_app():
    """创建 Flask 应用"""
    app = Flask(__name__)
    
    # 配置
    app.config['SECRET_KEY'] = 'wechat-format-secret-key'
    
    # 初始化格式化器
    formatter = WeChatFormatter()
    
    @app.route('/')
    def index():
        """主页"""
        return render_template('index.html')
    
    @app.route('/api/convert', methods=['POST'])
    def api_convert():
        """转换 API"""
        try:
            data = request.get_json()
            markdown_text = data.get('markdown', '')
            inline_style = data.get('inline', False)
            
            if not markdown_text.strip():
                return jsonify({
                    'success': False,
                    'error': 'Markdown 内容不能为空'
                })
            
            # 转换
            html = formatter.convert(markdown_text, inline_style=inline_style)
            
            return jsonify({
                'success': True,
                'html': html
            })
            
        except Exception as e:
            return jsonify({
                'success': False,
                'error': str(e)
            })
    
    @app.route('/api/copy', methods=['POST'])
    def api_copy():
        """复制到剪切板 API（富文本格式）"""
        try:
            data = request.get_json()
            markdown_text = data.get('markdown', '')
            
            if not markdown_text.strip():
                return jsonify({
                    'success': False,
                    'error': 'Markdown 内容不能为空'
                })
            
            # 转换并复制
            html, success = formatter.convert_and_copy(markdown_text)
            
            return jsonify({
                'success': success,
                'html': html,
                'message': '已复制到剪切板，可直接粘贴到微信公众号编辑器' if success else '复制失败，请手动复制'
            })
            
        except Exception as e:
            return jsonify({
                'success': False,
                'error': str(e)
            })
    
    return app


# 模板文件内容
TEMPLATE_INDEX = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>微信公众号格式化工具</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 12px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }
        
        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        
        .header p {
            font-size: 1.1em;
            opacity: 0.9;
        }
        
        .main {
            display: flex;
            min-height: 600px;
        }
        
        .editor-panel, .preview-panel {
            flex: 1;
            padding: 20px;
        }
        
        .editor-panel {
            border-right: 1px solid #eee;
        }
        
        .panel-title {
            font-size: 1.2em;
            font-weight: 600;
            margin-bottom: 15px;
            color: #333;
        }
        
        #markdown-input {
            width: 100%;
            height: 500px;
            border: 1px solid #ddd;
            border-radius: 8px;
            padding: 15px;
            font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
            font-size: 14px;
            line-height: 1.5;
            resize: vertical;
            outline: none;
            transition: border-color 0.3s;
        }
        
        #markdown-input:focus {
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }
        
        .preview-content {
            border: 1px solid #ddd;
            border-radius: 8px;
            padding: 20px;
            height: 500px;
            overflow-y: auto;
            background: #fafafa;
        }
        
        .toolbar {
            padding: 20px;
            background: #f8f9fa;
            border-top: 1px solid #eee;
            display: flex;
            gap: 15px;
            justify-content: center;
            flex-wrap: wrap;
        }
        
        .btn {
            padding: 12px 24px;
            border: none;
            border-radius: 6px;
            font-size: 14px;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.3s;
            text-decoration: none;
            display: inline-flex;
            align-items: center;
            gap: 8px;
        }
        
        .btn-primary {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        
        .btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.3);
        }
        
        .btn-secondary {
            background: #6c757d;
            color: white;
        }
        
        .btn-secondary:hover {
            background: #5a6268;
            transform: translateY(-2px);
        }
        
        .btn-success {
            background: #28a745;
            color: white;
        }
        
        .btn-success:hover {
            background: #218838;
            transform: translateY(-2px);
        }
        
        .status {
            padding: 10px 15px;
            border-radius: 6px;
            margin: 10px 0;
            font-size: 14px;
            display: none;
        }
        
        .status.success {
            background: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }
        
        .status.error {
            background: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }
        
        .demo-content {
            color: #666;
            font-style: italic;
            line-height: 1.6;
        }
        
        @media (max-width: 768px) {
            .main {
                flex-direction: column;
            }
            
            .editor-panel {
                border-right: none;
                border-bottom: 1px solid #eee;
            }
            
            .toolbar {
                flex-direction: column;
                align-items: center;
            }
            
            .btn {
                width: 100%;
                max-width: 300px;
                justify-content: center;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 微信公众号格式化工具</h1>
            <p>将 Markdown 转换为适合微信公众号的 HTML 格式，支持一键复制</p>
        </div>
        
        <div class="main">
            <div class="editor-panel">
                <div class="panel-title">📝 Markdown 编辑器</div>
                <textarea id="markdown-input" placeholder="在这里输入你的 Markdown 内容...

# 示例标题

这是一个**粗体**文本和*斜体*文本的示例。

## 功能特色

- ✅ 支持 Markdown 语法
- ✅ 实时预览
- ✅ 一键复制到剪切板
- ✅ 微信公众号样式优化

## 代码示例

```python
print('Hello, WeChat!')
```

> 这是一个引用块

| 功能 | 支持 |
|------|------|
| 表格 | ✅ |
| 代码 | ✅ |"></textarea>
            </div>
            
            <div class="preview-panel">
                <div class="panel-title">👀 实时预览</div>
                <div id="preview-content" class="preview-content">
                    <div class="demo-content">
                        在左侧输入 Markdown 内容，这里会实时显示转换后的效果。<br><br>
                        💡 提示：转换后的内容已经过微信公众号样式优化，可以直接复制使用。
                    </div>
                </div>
            </div>
        </div>
        
        <div class="toolbar">
            <button id="convert-btn" class="btn btn-primary">
                🔄 转换预览
            </button>
            <button id="copy-btn" class="btn btn-success">
                📋 复制到剪切板
            </button>
            <button id="demo-btn" class="btn btn-secondary">
                📄 加载示例
            </button>
        </div>
        
        <div id="status" class="status"></div>
    </div>

    <script>
        const markdownInput = document.getElementById('markdown-input');
        const previewContent = document.getElementById('preview-content');
        const convertBtn = document.getElementById('convert-btn');
        const copyBtn = document.getElementById('copy-btn');
        const demoBtn = document.getElementById('demo-btn');
        const status = document.getElementById('status');
        
        let convertTimeout;
        
        // 实时转换（防抖）
        markdownInput.addEventListener('input', function() {
            clearTimeout(convertTimeout);
            convertTimeout = setTimeout(convertMarkdown, 500);
        });
        
        // 转换按钮
        convertBtn.addEventListener('click', convertMarkdown);
        
        // 复制按钮
        copyBtn.addEventListener('click', copyToClipboard);
        
        // 示例按钮
        demoBtn.addEventListener('click', loadDemo);
        
        function convertMarkdown() {
            const markdown = markdownInput.value;
            
            if (!markdown.trim()) {
                previewContent.innerHTML = '<div class="demo-content">在左侧输入 Markdown 内容，这里会实时显示转换后的效果。</div>';
                return;
            }
            
            fetch('/api/convert', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    markdown: markdown,
                    inline: false
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    previewContent.innerHTML = data.html;
                } else {
                    showStatus('转换失败: ' + data.error, 'error');
                }
            })
            .catch(error => {
                showStatus('网络错误: ' + error.message, 'error');
            });
        }
        
        function copyToClipboard() {
            const markdown = markdownInput.value;
            
            if (!markdown.trim()) {
                showStatus('请先输入 Markdown 内容', 'error');
                return;
            }
            
            fetch('/api/copy', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    markdown: markdown
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    showStatus('✅ 已复制到剪切板，可直接粘贴到微信公众号后台', 'success');
                } else {
                    showStatus('复制失败: ' + (data.error || data.message), 'error');
                }
            })
            .catch(error => {
                showStatus('网络错误: ' + error.message, 'error');
            });
        }
        
        function loadDemo() {
            const demoContent = `# 🎯 微信公众号格式化工具示例

## 功能特色

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

\`\`\`python
from wechat_format import WeChatFormatter

formatter = WeChatFormatter()
html = formatter.convert_file('article.md')
formatter.copy_to_clipboard(html)
\`\`\`

## 🔥 重要提示

> 使用本工具，让你的微信公众号文章更加**专业**和**美观**！

---

*现在点击"复制到剪切板"按钮试试吧！*`;
            
            markdownInput.value = demoContent;
            convertMarkdown();
            showStatus('示例内容已加载', 'success');
        }
        
        function showStatus(message, type) {
            status.textContent = message;
            status.className = 'status ' + type;
            status.style.display = 'block';
            
            setTimeout(() => {
                status.style.display = 'none';
            }, 3000);
        }
        
        // 初始转换
        convertMarkdown();
    </script>
</body>
</html>"""


def setup_templates():
    """设置模板文件"""
    import os
    from pathlib import Path
    
    # 获取包目录
    package_dir = Path(__file__).parent
    templates_dir = package_dir / 'templates'
    
    # 创建模板目录
    templates_dir.mkdir(exist_ok=True)
    
    # 写入模板文件
    template_file = templates_dir / 'index.html'
    with open(template_file, 'w', encoding='utf-8') as f:
        f.write(TEMPLATE_INDEX)


# 确保模板文件存在
setup_templates()