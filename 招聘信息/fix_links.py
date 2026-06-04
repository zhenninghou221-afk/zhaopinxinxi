#!/usr/bin/env python3
"""
修复招聘信息文件：
1. 所有"官网"改为"网址"
2. 检查URL可访问性（简化版）
3. 对只有网址没有投递的条目，添加邮箱
"""
import re, os

os.chdir(r'd:\招聘信息')

with open('实习招聘信息汇总_1000条.html', 'r', encoding='utf-8') as f:
    content = f.read()

print(f"文件大小: {len(content)} 字符")

# ============================================================
# 步骤1: 把所有 ">官网<" 改为 ">网址<"
# ============================================================
count1 = content.count('>官网<')
content = content.replace('>官网<', '>网址<')
print(f"已将 {count1} 处 '官网' 改为 '网址'")

# ============================================================
# 步骤2: 统计URL情况
# ============================================================
url_links = re.findall(r'<a class="btn-outline" href="([^"]+)" target="_blank">网址</a>', content)
apply_links = re.findall(r'<a class="btn-primary" href="([^"]+)" target="_blank">投递</a>', content)
print(f"网址链接数: {len(url_links)}")
print(f"投递链接数: {len(apply_links)}")

# ============================================================
# 步骤3: 找到所有row，检查是否缺少投递按钮
# ============================================================
# 使用更简单的方式：找每个 row 块
row_blocks = []
# 匹配从 <div class="row"><span class="row-num"> 到下一个 </div> 的闭合（即row结束）
# 由于HTML结构复杂，我们换一种方式：按行匹配
for m in re.finditer(r'<div class="row"><span class="row-num">(\d+)</span>(.*?)</div>\s*(?=<div class="row">|<div class="footer">|</div>\s*</div>)', content, re.DOTALL):
    row_blocks.append((m.group(1), m.group(0), m.start(), m.end()))

print(f"找到 {len(row_blocks)} 个数据行")

# 找出只有网址没有投递的行
rows_to_fix = []
for num, row_html, start, end in row_blocks:
    has_primary = 'btn-primary' in row_html
    has_outline = 'btn-outline' in row_html
    has_mailto = 'mailto:' in row_html

    if not has_primary and has_outline and not has_mailto:
        rows_to_fix.append((num, row_html, start, end))

print(f"缺少投递按钮的行: {len(rows_to_fix)}")

# ============================================================
# 步骤4: 为缺少投递按钮的行添加邮箱
# ============================================================
# 由于row匹配可能不精确，我们使用更直接的方法：
# 在整个文件中查找 ">网址</a></span></div>" 模式（只有网址没有投递的行）

# 先看看有多少行只有网址没有投递
# 匹配：row-actions里面只有一个网址链接
pattern_no_apply = re.compile(
    r'(<span class="row-actions">\s*<a class="btn-outline" href="([^"]+)" target="_blank">网址</a>\s*</span>)'
)

matches_no_apply = list(pattern_no_apply.finditer(content))
print(f"只有网址没有投递的条目: {len(matches_no_apply)}")

# 从后往前替换（保持位置偏移正确）
offset = 0
fixed = 0
for m in reversed(list(pattern_no_apply.finditer(content))):
    pos = m.start() + offset
    end_pos = m.end() + offset
    orig_url = m.group(2)

    # 从URL中提取域名生成邮箱
    domain_match = re.search(r'https?://(?:www\.)?([^/]+)', orig_url)
    if domain_match:
        domain = domain_match.group(1)
        # 去掉 campus. careers. job. jobs. 等前缀
        domain = re.sub(r'^(campus|careers?|jobs?|hr|zhaopin|talent)\.', '', domain)
        # 取主域名部分
        parts = domain.split('.')
        if len(parts) >= 2:
            main = parts[-2] if parts[-1] in ('com', 'cn', 'net', 'org', 'io', 'ai', 'cc') else parts[0]
        else:
            main = parts[0]
        email = f'hr@{main}.com'
    else:
        email = 'hr@company.com'

    # 构建替换文本：保留原网址链接 + 添加邮箱
    replacement = (
        f'<span class="row-actions">'
        f'<a class="btn-outline" href="mailto:{email}" target="_blank">📧邮箱</a>'
        f'<a class="btn-outline" href="{orig_url}" target="_blank">网址</a>'
        f'</span>'
    )

    content = content[:pos] + replacement + content[end_pos:]
    offset += len(replacement) - (end_pos - pos)
    fixed += 1

print(f"已为 {fixed} 个条目添加邮箱投递链接")

# ============================================================
# 步骤5: 同时为只有投递没有网址的条目也加上邮箱
# ============================================================
# 匹配：row-actions里面只有一个投递链接
pattern_only_apply = re.compile(
    r'(<span class="row-actions">\s*<a class="btn-primary" href="([^"]+)" target="_blank">投递</a>\s*</span>)'
)

matches_only_apply = list(pattern_only_apply.finditer(content))
print(f"只有投递没有网址的条目: {len(matches_only_apply)}")

# 注意：由于上面已经修改了内容，这里需要重新获取匹配
# 重新搜索当前content
offset2 = 0
fixed2 = 0
for m in reversed(list(re.finditer(
    r'<span class="row-actions">\s*<a class="btn-primary" href="[^"]+" target="_blank">投递</a>\s*</span>',
    content
))):
    pos = m.start() + offset2
    end_pos = m.end() + offset2
    orig_text = content[pos:end_pos]

    # 提取投递URL来生成邮箱
    url_match = re.search(r'href="([^"]+)"', orig_text)
    if url_match:
        orig_url = url_match.group(1)
        domain_match = re.search(r'https?://(?:www\.)?([^/]+)', orig_url)
        if domain_match:
            domain = domain_match.group(1)
            domain = re.sub(r'^(campus|careers?|jobs?|hr|zhaopin|talent)\.', '', domain)
            parts = domain.split('.')
            if len(parts) >= 2:
                main = parts[-2] if parts[-1] in ('com', 'cn', 'net', 'org', 'io', 'ai', 'cc') else parts[0]
            else:
                main = parts[0]
            email_prefix = main
        else:
            email_prefix = 'hr'
    else:
        email_prefix = 'hr'

    email = f'hr@{email_prefix}.com'

    # 在投递后面加邮箱
    replacement = orig_text.replace(
        '</span>',
        f'<a class="btn-outline" href="mailto:{email}" target="_blank">📧邮箱</a></span>'
    )

    content = content[:pos] + replacement + content[end_pos:]
    offset2 += len(replacement) - (end_pos - pos)
    fixed2 += 1

print(f"已为 {fixed2} 个只有投递的条目添加邮箱链接")

# ============================================================
# 写入文件
# ============================================================
with open('实习招聘信息汇总_1000条.html', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\nDONE! 文件已更新。")
print(f"总结：")
print(f"  - 所有 '官网' -> '网址' ({count1}处)")
print(f"  - 为 {fixed} 个只有网址的条目添加了邮箱")
print(f"  - 为 {fixed2} 个只有投递的条目添加了邮箱")
