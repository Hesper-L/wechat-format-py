"""
微信公众号样式定义

基于原版 wechat-format 项目的样式，针对微信公众号优化。
"""

# 基础样式
BASE_STYLE = """
<style>
.markdown-body {
    box-sizing: border-box;
    min-width: 200px;
    max-width: 980px;
    margin: 0 auto;
    padding: 45px;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", "Helvetica Neue", Helvetica, Arial, sans-serif;
    font-size: 16px;
    line-height: 1.6;
    word-wrap: break-word;
    color: #333;
}

/* 标题样式 */
.markdown-body h1 {
    font-size: 24px;
    font-weight: bold;
    color: #2c3e50;
    margin: 1.5em 0 1em 0;
    padding-bottom: 0.3em;
    border-bottom: 2px solid #3498db;
}

.markdown-body h2 {
    font-size: 20px;
    font-weight: bold;
    color: #34495e;
    margin: 1.3em 0 0.8em 0;
    padding-left: 10px;
    border-left: 4px solid #3498db;
}

.markdown-body h3 {
    font-size: 18px;
    font-weight: bold;
    color: #2c3e50;
    margin: 1.2em 0 0.6em 0;
}

.markdown-body h4 {
    font-size: 16px;
    font-weight: bold;
    color: #34495e;
    margin: 1em 0 0.5em 0;
}

/* 段落样式 */
.markdown-body p {
    margin: 0.8em 0;
    line-height: 1.8;
}

/* 强调样式 */
.markdown-body strong {
    font-weight: bold;
    color: #e74c3c;
}

.markdown-body em {
    font-style: italic;
    color: #8e44ad;
}

/* 链接样式 */
.markdown-body a {
    color: #3498db;
    text-decoration: none;
    border-bottom: 1px solid #3498db;
}

/* 列表样式 */
.markdown-body ul, .markdown-body ol {
    margin: 0.8em 0;
    padding-left: 2em;
}

.markdown-body li {
    margin: 0.3em 0;
    line-height: 1.6;
}

/* 引用样式 */
.markdown-body blockquote {
    margin: 1em 0;
    padding: 0.8em 1em;
    background-color: #f8f9fa;
    border-left: 4px solid #3498db;
    color: #555;
    font-style: italic;
}

/* 代码样式 */
.markdown-body code {
    background-color: #f1f2f6;
    color: #e74c3c;
    padding: 2px 4px;
    border-radius: 3px;
    font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, Courier, monospace;
    font-size: 0.9em;
}

.markdown-body pre {
    background-color: #2c3e50;
    color: #ecf0f1;
    padding: 1em;
    border-radius: 5px;
    overflow-x: auto;
    margin: 1em 0;
}

.markdown-body pre code {
    background-color: transparent;
    color: inherit;
    padding: 0;
}

/* 表格样式 */
.markdown-body table {
    width: 100%;
    border-collapse: collapse;
    margin: 1em 0;
    font-size: 14px;
}

.markdown-body th, .markdown-body td {
    border: 1px solid #ddd;
    padding: 8px 12px;
    text-align: left;
}

.markdown-body th {
    background-color: #3498db;
    color: white;
    font-weight: bold;
}

.markdown-body tr:nth-child(even) {
    background-color: #f8f9fa;
}

/* 分割线样式 */
.markdown-body hr {
    border: none;
    height: 2px;
    background: linear-gradient(to right, transparent, #3498db, transparent);
    margin: 2em 0;
}

/* 图片样式 */
.markdown-body img {
    max-width: 100%;
    height: auto;
    border-radius: 5px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    margin: 1em 0;
}

/* 微信公众号特殊样式 */
.wechat-highlight {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 0.2em 0.5em;
    border-radius: 3px;
    font-weight: bold;
}

.wechat-box {
    background-color: #f8f9fa;
    border: 1px solid #e9ecef;
    border-radius: 8px;
    padding: 1em;
    margin: 1em 0;
    position: relative;
}

.wechat-box::before {
    content: "💡";
    position: absolute;
    top: -10px;
    left: 15px;
    background-color: #fff;
    padding: 0 5px;
}
</style>
"""

# HTML 模板
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>微信公众号文章</title>
    {style}
</head>
<body>
    <div class="markdown-body">
        {content}
    </div>
</body>
</html>
"""

# 微信公众号专用样式（用于复制到剪切板）
WECHAT_INLINE_STYLE = {
    'h1': 'font-size: 24px; font-weight: bold; color: #2c3e50; margin: 1.5em 0 1em 0; padding-bottom: 0.3em; border-bottom: 2px solid #3498db;',
    'h2': 'font-size: 20px; font-weight: bold; color: #34495e; margin: 1.3em 0 0.8em 0; padding-left: 10px; border-left: 4px solid #3498db;',
    'h3': 'font-size: 18px; font-weight: bold; color: #2c3e50; margin: 1.2em 0 0.6em 0;',
    'h4': 'font-size: 16px; font-weight: bold; color: #34495e; margin: 1em 0 0.5em 0;',
    'p': 'margin: 0.8em 0; line-height: 1.8; font-size: 16px; color: #333;',
    'strong': 'font-weight: bold; color: #e74c3c;',
    'em': 'font-style: italic; color: #8e44ad;',
    'code': 'background-color: #f1f2f6; color: #e74c3c; padding: 2px 4px; border-radius: 3px; font-family: monospace; font-size: 0.9em;',
    'blockquote': 'margin: 1em 0; padding: 0.8em 1em; background-color: #f8f9fa; border-left: 4px solid #3498db; color: #555; font-style: italic;',
    'ul': 'margin: 0.8em 0; padding-left: 2em;',
    'ol': 'margin: 0.8em 0; padding-left: 2em;',
    'li': 'margin: 0.3em 0; line-height: 1.6;',
    'table': 'width: 100%; border-collapse: collapse; margin: 1em 0; font-size: 14px;',
    'th': 'border: 1px solid #ddd; padding: 8px 12px; background-color: #3498db; color: white; font-weight: bold;',
    'td': 'border: 1px solid #ddd; padding: 8px 12px;',
    'img': 'max-width: 100%; height: auto; border-radius: 5px; margin: 1em 0;',
    'hr': 'border: none; height: 2px; background: linear-gradient(to right, transparent, #3498db, transparent); margin: 2em 0;'
}