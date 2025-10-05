"""
微信公众号 Markdown 转换器

核心转换功能，将 Markdown 转换为适合微信公众号的 HTML 格式。
"""

import re
import markdown2
from bs4 import BeautifulSoup
import pyperclip
from .styles import BASE_STYLE, HTML_TEMPLATE, WECHAT_INLINE_STYLE


class WeChatFormatter:
    """微信公众号格式化器"""
    
    def __init__(self):
        """初始化格式化器"""
        self.markdown_extras = [
            'fenced-code-blocks',
            'tables',
            'strike',
            'task_list',
            'footnotes',
            'cuddled-lists',
            'metadata',
            'code-friendly'
        ]
    
    def convert(self, markdown_text: str, inline_style: bool = False) -> str:
        """
        转换 Markdown 文本为微信公众号 HTML
        
        Args:
            markdown_text: Markdown 文本
            inline_style: 是否使用内联样式（用于复制到剪切板）
            
        Returns:
            转换后的 HTML 文本
        """
        # 预处理 Markdown 文本
        processed_text = self._preprocess_markdown(markdown_text)
        
        # 转换为 HTML
        html = markdown2.markdown(processed_text, extras=self.markdown_extras)
        
        # 后处理 HTML
        html = self._postprocess_html(html, inline_style)
        
        if inline_style:
            return html
        else:
            return HTML_TEMPLATE.format(style=BASE_STYLE, content=html)
    
    def convert_file(self, file_path: str, inline_style: bool = False) -> str:
        """
        转换 Markdown 文件为微信公众号 HTML
        
        Args:
            file_path: Markdown 文件路径
            inline_style: 是否使用内联样式
            
        Returns:
            转换后的 HTML 文本
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                markdown_text = f.read()
            return self.convert(markdown_text, inline_style)
        except FileNotFoundError:
            raise FileNotFoundError(f"文件不存在: {file_path}")
        except Exception as e:
            raise Exception(f"读取文件失败: {e}")
    
    def copy_to_clipboard(self, content: str) -> bool:
        """
        将内容复制到剪切板（富文本格式）
        
        Args:
            content: 要复制的HTML内容
            
        Returns:
            是否复制成功
        """
        try:
            # 在Windows上使用win32clipboard来复制富文本
            import platform
            if platform.system() == 'Windows':
                return self._copy_html_windows(content)
            else:
                # 其他系统回退到纯文本复制
                pyperclip.copy(content)
                return True
        except Exception as e:
            print(f"复制失败: {e}")
            return False
    
    def _copy_html_windows(self, html_content: str) -> bool:
        """
        在Windows上复制HTML富文本格式
        """
        try:
            import win32clipboard
            
            # HTML格式的注册格式ID
            CF_HTML = win32clipboard.RegisterClipboardFormat("HTML Format")
            
            # 准备HTML格式的剪切板数据
            # 为了修复微信公众号复制格式问题，需要确保HTML结构紧凑
            # 移除不必要的换行符，防止内容被拆分成单独行
            cleaned_html = html_content.replace('\n', '').replace('\r', '')
            
            html_format = f"""Version:0.9
StartHTML:0000000000
EndHTML:0000000000
StartFragment:0000000000
EndFragment:0000000000
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
body {{ margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", "Helvetica Neue", Helvetica, Arial, sans-serif; }}
</style>
</head>
<body>
<!--StartFragment-->{cleaned_html}<!--EndFragment-->
</body>
</html>"""
            
            # 计算偏移量
            start_html = html_format.find('<!DOCTYPE')
            end_html = len(html_format)
            start_fragment = html_format.find('<!--StartFragment-->') + len('<!--StartFragment-->')
            end_fragment = html_format.find('<!--EndFragment-->')
            
            # 更新偏移量
            html_format = html_format.replace('StartHTML:0000000000', f'StartHTML:{start_html:010d}')
            html_format = html_format.replace('EndHTML:0000000000', f'EndHTML:{end_html:010d}')
            html_format = html_format.replace('StartFragment:0000000000', f'StartFragment:{start_fragment:010d}')
            html_format = html_format.replace('EndFragment:0000000000', f'EndFragment:{end_fragment:010d}')
            
            # 复制到剪切板
            win32clipboard.OpenClipboard()
            win32clipboard.EmptyClipboard()
            win32clipboard.SetClipboardData(CF_HTML, html_format.encode('utf-8'))
            win32clipboard.CloseClipboard()
            
            return True
        except ImportError as e:
            print(f"导入win32clipboard失败: {e}")
            # 如果没有win32clipboard，回退到pyperclip
            pyperclip.copy(html_content)
            return True
        except Exception as e:
            print(f"Windows复制失败: {e}")
            return False
    
    def convert_and_copy(self, markdown_text: str) -> tuple[str, bool]:
        """
        转换 Markdown 并复制到剪切板
        
        Args:
            markdown_text: Markdown 文本
            
        Returns:
            (转换后的HTML, 是否复制成功)
        """
        html = self.convert(markdown_text, inline_style=True)
        success = self.copy_to_clipboard(html)
        return html, success
    
    def convert_file_and_copy(self, file_path: str) -> tuple[str, bool]:
        """
        转换 Markdown 文件并复制到剪切板
        
        Args:
            file_path: Markdown 文件路径
            
        Returns:
            (转换后的HTML, 是否复制成功)
        """
        html = self.convert_file(file_path, inline_style=True)
        success = self.copy_to_clipboard(html)
        return html, success
    
    def _preprocess_markdown(self, text: str) -> str:
        """
        预处理 Markdown 文本
        
        Args:
            text: 原始 Markdown 文本
            
        Returns:
            处理后的 Markdown 文本
        """
        # 处理注音符号（日语假名和汉语拼音）
        text = self._process_furigana(text)
        
        # 处理特殊标记
        text = self._process_special_marks(text)
        
        return text
    
    def _process_furigana(self, text: str) -> str:
        """
        处理注音符号
        
        支持格式：
        - 世界【せかい】
        - 世界{せかい}
        - 上海【Shàng・hǎi】
        """
        # 处理【】格式的注音
        text = re.sub(
            r'([^\s]+)【([^\]]+)】',
            r'<ruby>\1<rt>\2</rt></ruby>',
            text
        )
        
        # 处理{}格式的注音
        text = re.sub(
            r'([^\s]+)\{([^}]+)\}',
            r'<ruby>\1<rt>\2</rt></ruby>',
            text
        )
        
        return text
    
    def _process_special_marks(self, text: str) -> str:
        """
        处理特殊标记
        """
        # 处理高亮标记 ==text==
        text = re.sub(
            r'==([^=]+)==',
            r'<span class="wechat-highlight">\1</span>',
            text
        )
        
        # 处理提示框 :::tip 内容 :::
        text = re.sub(
            r':::tip\s*\n(.*?)\n:::',
            r'<div class="wechat-box">\1</div>',
            text,
            flags=re.DOTALL
        )
        
        return text
    
    def _postprocess_html(self, html: str, inline_style: bool = False) -> str:
        """
        后处理 HTML
        
        Args:
            html: 原始 HTML
            inline_style: 是否使用内联样式
            
        Returns:
            处理后的 HTML
        """
        soup = BeautifulSoup(html, 'html.parser')
        
        if inline_style:
            # 添加内联样式
            self._add_inline_styles(soup)
        
        # 处理链接（外部链接转为脚注）
        self._process_links(soup)
        
        # 处理表格
        self._process_tables(soup)
        
        # 处理代码块
        self._process_code_blocks(soup)
        
        return str(soup)
    
    def _add_inline_styles(self, soup: BeautifulSoup):
        """添加内联样式"""
        for tag_name, style in WECHAT_INLINE_STYLE.items():
            for tag in soup.find_all(tag_name):
                existing_style = tag.get('style', '')
                if existing_style:
                    tag['style'] = f"{existing_style}; {style}"
                else:
                    tag['style'] = style
    
    def _process_links(self, soup: BeautifulSoup):
        """处理链接，外部链接转为脚注"""
        links = soup.find_all('a')
        footnotes = []
        
        for i, link in enumerate(links, 1):
            href = link.get('href', '')
            if href.startswith('http'):
                # 外部链接转为脚注
                link_text = link.get_text()
                link.replace_with(f"{link_text}[{i}]")
                footnotes.append(f"[{i}] {link_text}: {href}")
        
        # 添加脚注
        if footnotes:
            footnote_section = soup.new_tag('div', style='margin-top: 2em; padding-top: 1em; border-top: 1px solid #ddd; font-size: 14px; color: #666;')
            footnote_section.string = '\n'.join(footnotes)
            soup.append(footnote_section)
    
    def _process_tables(self, soup: BeautifulSoup):
        """处理表格样式"""
        for table in soup.find_all('table'):
            # 为奇偶行添加不同背景色
            rows = table.find_all('tr')
            for i, row in enumerate(rows):
                if i > 0 and i % 2 == 0:  # 跳过表头，偶数行
                    row['style'] = row.get('style', '') + '; background-color: #f8f9fa;'
    
    def _process_code_blocks(self, soup: BeautifulSoup):
        """处理代码块"""
        for pre in soup.find_all('pre'):
            code = pre.find('code')
            if code:
                # 添加代码块样式
                pre['style'] = 'background-color: #2c3e50; color: #ecf0f1; padding: 1em; border-radius: 5px; overflow-x: auto; margin: 1em 0;'
                code['style'] = 'background-color: transparent; color: inherit; font-family: "SFMono-Regular", Consolas, monospace;'


# 便捷函数
def convert_markdown(text: str, inline_style: bool = False) -> str:
    """
    便捷函数：转换 Markdown 文本
    
    Args:
        text: Markdown 文本
        inline_style: 是否使用内联样式
        
    Returns:
        转换后的 HTML
    """
    formatter = WeChatFormatter()
    return formatter.convert(text, inline_style)


def convert_file(file_path: str, inline_style: bool = False) -> str:
    """
    便捷函数：转换 Markdown 文件
    
    Args:
        file_path: 文件路径
        inline_style: 是否使用内联样式
        
    Returns:
        转换后的 HTML
    """
    formatter = WeChatFormatter()
    return formatter.convert_file(file_path, inline_style)


def convert_and_copy(text: str) -> bool:
    """
    便捷函数：转换并复制到剪切板
    
    Args:
        text: Markdown 文本
        
    Returns:
        是否复制成功
    """
    formatter = WeChatFormatter()
    _, success = formatter.convert_and_copy(text)
    return success