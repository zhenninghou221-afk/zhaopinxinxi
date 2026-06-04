#!/usr/bin/env python3
"""
重构招聘信息文件：
1. 删除所有分类大标题和section分组 -> 扁平化列表
2. 保留关键词搜索功能
3. 白底纯白背景
4. 官网 -> 网址
5. 增加地区与面向之间的间距
6. 100+ -> 1000+
"""
import re, os

os.chdir(r'd:\招聘信息')

with open('实习招聘信息汇总_1000条.html', 'r', encoding='utf-8') as f:
    content = f.read()

print("原始文件大小:", len(content))

# ============================================================
# 步骤1: 提取所有数据行（row）
# ============================================================
# 匹配所有数据row（有row-num的，排除header-row）
data_rows = []
for m in re.finditer(r'<div class="row"><span class="row-num">(\d+)</span>(.*?)</div>\s*(?=<div class="row">|</div>\s*</div>|<div class="footer">|$)', content, re.DOTALL):
    row_num = m.group(1)
    row_html = m.group(0)
    # 排除 header-row
    if 'header-row' not in row_html:
        data_rows.append(row_html)

print(f"提取到 {len(data_rows)} 个数据行")

# ============================================================
# 步骤2: 重新编号
# ============================================================
def renumber_row(row, new_num):
    # 替换 row-num
    row = re.sub(r'<span class="row-num">\d+</span>',
                 f'<span class="row-num">{new_num:02d}</span>' if new_num < 100 else f'<span class="row-num">{new_num}</span>',
                 row)
    return row

renumbered_rows = [renumber_row(row, i+1) for i, row in enumerate(data_rows)]
print(f"重新编号完成: 1-{len(renumbered_rows)}")

# ============================================================
# 步骤3: 构建新的HTML
# ============================================================

new_html = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>2027-2029届毕业生实习招聘信息汇总 (2026暑期)</title>
<style>
  :root { --bg:#ffffff; --card-bg:#ffffff; --text:#1a1a2e; --text2:#64748b; --accent:#2563eb; --accent2:#7c3aed; --border:#e2e8f0; --tag-bg:#eff6ff; --tag-text:#2563eb; --row-hover:#f0f4ff; }
  * { margin:0; padding:0; box-sizing:border-box; }
  body { font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC","Microsoft YaHei",sans-serif; background:var(--bg); color:var(--text); line-height:1.5; }
  .hero { background:#ffffff; padding:44px 20px; text-align:center; border-bottom:1px solid var(--border); }
  .hero h1 { font-size:2em; background:linear-gradient(135deg,var(--accent),var(--accent2)); -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text; margin-bottom:6px; }
  .hero .subtitle { color:var(--text2); font-size:.95em; }
  .hero .update { display:inline-block; margin-top:10px; background:var(--tag-bg); color:var(--tag-text); padding:5px 18px; border-radius:20px; font-size:.82em; border:1px solid #bfdbfe; }
  .stats-row { display:flex; justify-content:center; gap:32px; margin-top:18px; flex-wrap:wrap; }
  .stat-item { text-align:center; }
  .stat-item .num { font-size:1.7em; font-weight:800; background:linear-gradient(135deg,#f59e0b,#ef4444); -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text; }
  .stat-item .label { color:var(--text2); font-size:.78em; }
  .container { max-width:1400px; margin:0 auto; padding:12px 20px; }
  .rows { display:flex; flex-direction:column; gap:5px; }
  .row { background:var(--card-bg); border:1px solid var(--border); border-radius:8px; padding:10px 16px; display:flex; align-items:center; gap:24px; transition:all .18s; min-height:48px; box-shadow:0 1px 2px rgba(0,0,0,.03); }
  .row:hover { border-color:var(--accent); background:var(--row-hover); box-shadow:0 2px 8px rgba(37,99,235,.08); }
  .row-num { width:26px; height:26px; border-radius:5px; background:#f1f5f9; color:var(--text2); display:flex; align-items:center; justify-content:center; font-size:.72em; font-weight:700; flex-shrink:0; }
  .row-left { display:flex; flex-direction:column; gap:3px; min-width:160px; max-width:240px; flex-shrink:0; }
  .row-company { font-weight:700; color:#0f172a; font-size:.9em; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }
  .row-loc { font-size:.74em; color:#d97706; white-space:nowrap; font-weight:500; }
  .row-tags { display:flex; flex-wrap:wrap; gap:3px; }
  .tag { font-size:.66em; padding:2px 7px; border-radius:8px; background:var(--tag-bg); color:var(--tag-text); white-space:nowrap; border:1px solid #bfdbfe; }
  .tag.hot { background:#fef2f2; color:#dc2626; border-color:#fecaca; }
  .tag.green { background:#f0fdf4; color:#16a34a; border-color:#bbf7d0; }
  .tag.orange { background:#fff7ed; color:#ea580c; border-color:#fed7aa; }
  .tag.purple { background:#f5f3ff; color:#7c3aed; border-color:#ddd6fe; }
  .row-info { flex:1; display:flex; flex-wrap:wrap; gap:6px 18px; font-size:.78em; color:var(--text2); align-items:center; min-width:0; padding-left:4px; }
  .row-info .info-item { white-space:nowrap; }
  .row-info .info-item strong { color:#334155; font-weight:600; }
  .row-actions { display:flex; gap:6px; flex-shrink:0; flex-wrap:wrap; align-items:center; }
  .row-actions a { display:inline-block; padding:5px 12px; border-radius:6px; font-size:.76em; font-weight:600; text-decoration:none; transition:all .2s; white-space:nowrap; }
  .btn-primary { background:var(--accent); color:#fff; }
  .btn-primary:hover { background:#1d4ed8; }
  .btn-outline { border:1px solid var(--border); color:var(--text); background:#fff; }
  .btn-outline:hover { border-color:var(--accent); color:var(--accent); background:#f8faff; }
  .row.header-row { background:transparent; border:none; padding:5px 16px; font-size:.74em; color:var(--text2); font-weight:600; min-height:auto; box-shadow:none; }
  .row.header-row:hover { background:transparent; border-color:transparent; box-shadow:none; }
  .row.header-row .row-left { visibility:hidden; }
  .row.hidden { display:none; }
  .no-result { text-align:center; padding:40px; color:var(--text2); font-size:.9em; }
  /* Search Bar */
  .search-bar-wrap { position:sticky; top:0; z-index:100; background:rgba(255,255,255,.97); backdrop-filter:blur(10px); padding:12px 20px 8px; border-bottom:1px solid var(--border); display:flex; flex-direction:column; gap:8px; align-items:center; box-shadow:0 1px 3px rgba(0,0,0,.04); }
  .search-input-row { display:flex; gap:8px; width:100%; max-width:700px; align-items:center; }
  .search-input-row input { flex:1; background:#f8fafc; border:1px solid var(--border); border-radius:20px; padding:9px 18px; color:#0f172a; font-size:.88em; outline:none; transition:border .2s; }
  .search-input-row input:focus { border-color:var(--accent); background:#fff; }
  .search-input-row input::placeholder { color:#94a3b8; }
  .search-result-count { font-size:.78em; color:var(--text2); white-space:nowrap; }
  .search-chips { display:flex; gap:6px; flex-wrap:wrap; justify-content:center; max-width:900px; }
  .search-chip { font-size:.72em; padding:5px 13px; border-radius:14px; border:1px solid var(--border); background:#fff; color:var(--text2); cursor:pointer; transition:all .18s; white-space:nowrap; user-select:none; }
  .search-chip:hover { border-color:var(--accent); color:var(--accent); background:#f8faff; }
  .search-chip.active { background:var(--accent); color:#fff; border-color:var(--accent); font-weight:600; }
  .search-chip.hot-chip { border-color:#ef4444; color:#dc2626; }
  .search-chip.hot-chip:hover,.search-chip.hot-chip.active { background:#ef4444; color:#fff; }
  .alert { border-radius:8px; padding:12px 18px; margin:12px 0; font-size:.82em; }
  .alert.tips { background:#f0fdf4; border:1px solid #bbf7d0; color:#166534; }
  .alert h3 { margin-bottom:5px; font-size:.92em; }
  .footer { text-align:center; padding:26px 20px; color:var(--text2); font-size:.74em; border-top:1px solid var(--border); margin-top:24px; }
  .footer a { color:var(--accent); }
  @media (max-width:800px) {
    .hero h1 { font-size:1.3em; }
    .row { flex-wrap:wrap; gap:8px; padding:10px 12px; }
    .row-left { min-width:110px; max-width:100%; }
    .row-info { flex-direction:column; align-items:flex-start; gap:3px; }
    .row-actions { width:100%; }
    .stats-row { gap:14px; }
    .row-num { display:none; }
  }
</style>
</head>
<body>

<!-- ============ HERO ============ -->
<div class="hero">
  <h1>🎯 2027–2029届 实习招聘信息大全</h1>
  <p class="subtitle">覆盖23大行业 · 1000+企业 · 2026年暑期实习 · 持续更新</p>
  <span class="update">📅 更新于 2026年6月4日 | 信息来源：企业官网、24365平台、高校就业网</span>
  <div class="stats-row">
    <div class="stat-item"><div class="num">1000+</div><div class="label">收录企业</div></div>
    <div class="stat-item"><div class="num">1000</div><div class="label">招聘条目</div></div>
    <div class="stat-item"><div class="num">15万+</div><div class="label">实习岗位</div></div>
    <div class="stat-item"><div class="num">50%+</div><div class="label">平均转正率</div></div>
  </div>
</div>

<!-- ============ 搜索栏 ============ -->
<div class="search-bar-wrap" id="searchBar">
  <div class="search-input-row">
    <input type="text" id="searchInput" placeholder="🔍 输入公司名、城市、行业、岗位关键词筛选…" oninput="doSearch()" autofocus>
    <span class="search-result-count" id="resultCount">共 ''' + str(len(renumbered_rows)) + ''' 条</span>
  </div>
  <div class="search-chips" id="searchChips">
    <span class="search-chip" onclick="chipClick(this,'🔥热招中')">🔥 热招中</span>
    <span class="search-chip" onclick="chipClick(this,'✅可转正')">✅ 可转正</span>
    <span class="search-chip" onclick="chipClick(this,'北京')">📍 北京</span>
    <span class="search-chip" onclick="chipClick(this,'上海')">📍 上海</span>
    <span class="search-chip" onclick="chipClick(this,'深圳')">📍 深圳</span>
    <span class="search-chip" onclick="chipClick(this,'广州')">📍 广州</span>
    <span class="search-chip" onclick="chipClick(this,'杭州')">📍 杭州</span>
    <span class="search-chip" onclick="chipClick(this,'成都')">📍 成都</span>
    <span class="search-chip" onclick="chipClick(this,'武汉')">📍 武汉</span>
    <span class="search-chip" onclick="chipClick(this,'南京')">📍 南京</span>
    <span class="search-chip" onclick="chipClick(this,'AI/大模型')">🤖 AI/大模型</span>
    <span class="search-chip" onclick="chipClick(this,'算法')">🧮 算法</span>
    <span class="search-chip" onclick="chipClick(this,'芯片')">💾 芯片</span>
    <span class="search-chip" onclick="chipClick(this,'产品')">📦 产品</span>
    <span class="search-chip" onclick="chipClick(this,'自动驾驶')">🚗 自动驾驶</span>
    <span class="search-chip" onclick="chipClick(this,'金融/银行')">🏦 金融/银行</span>
    <span class="search-chip" onclick="chipClick(this,'快消')">🛍️ 快消</span>
    <span class="search-chip" onclick="chipClick(this,'新能源')">⚡ 新能源</span>
    <span class="search-chip" onclick="chipClick(this,'医药')">🏥 医药</span>
    <span class="search-chip" onclick="chipClick(this,'游戏')">🎮 游戏</span>
    <span class="search-chip" onclick="chipClick(this,'国企/央企')">🏛️ 国企/央企</span>
    <span class="search-chip hot-chip" onclick="chipClick(this,'⏰即将截止')">⏰ 即将截止</span>
    <span class="search-chip" onclick="clearSearch()" style="border-color:#ef4444;color:#dc2626;">✕ 清除</span>
  </div>
</div>

<div class="container">

<div class="alert tips">
  <h3>💡 使用说明</h3>
  <p>① 每行是一家企业的完整招聘信息（企业名→工作地区→岗位→投递按钮）；② 📍橙色文字 = 工作城市；③ 标签：🔥=热招中/⏰=即将截止/✅=可转正/⚠️=关注官网；④ <strong>2027届是主力</strong>，2028/2029届部分项目开放；⑤ 使用搜索栏输入关键词快速筛选目标企业。</p>
</div>

<div class="rows">
<div class="row header-row"><span class="row-num">#</span><span class="row-left">企业 / 工作地区</span><span class="row-info">面向对象 / 岗位方向</span><span class="row-actions">投递</span></div>
'''

# 添加所有数据行
# 先做 官网->网址 替换
for i, row in enumerate(renumbered_rows):
    row = row.replace('>官网<', '>网址<')
    new_html += row + '\n'

# 添加结尾
new_html += '''</div>

<div class="footer">
  <p>📅 更新于 2026年6月4日 | 信息来源：企业官网·24365平台·高校就业网·牛客网等公开渠道</p>
  <p>⚠️ 投递前请在各企业官网确认最新信息（截止日期、岗位状态可能有变动） | <a href="#">↑ 返回顶部</a></p>
</div>

</div>

<script>
  // ===== 搜索 & 筛选 =====
  let activeKeyword = '';
  function doSearch() {
    const q = document.getElementById('searchInput').value.trim().toLowerCase();
    const rows = document.querySelectorAll('.row:not(.header-row)');
    let visibleCount = 0;

    rows.forEach(row => {
      const text = row.textContent.toLowerCase();
      const company = (row.querySelector('.row-company')?.textContent || '').toLowerCase();
      const loc = (row.querySelector('.row-loc')?.textContent || '').toLowerCase();
      const allTags = Array.from(row.querySelectorAll('.tag')).map(t => t.textContent).join(' ').toLowerCase();
      const combined = company + ' ' + loc + ' ' + allTags + ' ' + text;

      let show = true;

      // 输入框关键词匹配
      if (q) {
        show = combined.includes(q);
      }

      // 芯片关键词匹配
      if (activeKeyword && show) {
        const kw = activeKeyword.toLowerCase();
        if (kw === '✅可转正') {
          show = allTags.includes('转正') || allTags.includes('留用') || allTags.includes('offer');
        } else if (kw === '⏰即将截止') {
          show = allTags.includes('截止');
        } else if (kw === 'ai/大模型') {
          show = combined.includes('ai') || combined.includes('大模型') || combined.includes('llm');
        } else if (kw === '金融/银行') {
          show = combined.includes('银行') || combined.includes('金融') || combined.includes('券商') || combined.includes('保险');
        } else if (kw === '新能源') {
          show = combined.includes('新能源') || combined.includes('电池') || combined.includes('储能') || combined.includes('光伏') || combined.includes('风电');
        } else if (kw === '医药') {
          show = combined.includes('医药') || combined.includes('医疗') || combined.includes('药') || combined.includes('生物');
        } else if (kw === '游戏') {
          show = combined.includes('游戏') || combined.includes('互娱');
        } else if (kw === '国企/央企') {
          show = combined.includes('央企') || combined.includes('国企') || combined.includes('国资委');
        } else if (kw === '芯片') {
          show = combined.includes('芯片') || combined.includes('ic') || combined.includes('cpu') || combined.includes('gpu') || combined.includes('半导体');
        } else if (kw === '自动驾驶') {
          show = combined.includes('自动驾驶') || combined.includes('智能驾驶') || combined.includes('智驾');
        } else if (kw === '🔥热招中') {
          show = allTags.includes('热招');
        } else if (kw === '快消') {
          show = combined.includes('快消') || combined.includes('零售') || combined.includes('食品') || combined.includes('饮料') || combined.includes('化妆品');
        } else {
          show = combined.includes(kw);
        }
      }

      if (show) {
        row.classList.remove('hidden');
        visibleCount++;
      } else {
        row.classList.add('hidden');
      }
    });

    document.getElementById('resultCount').textContent = q || activeKeyword ? '匹配 ' + visibleCount + ' 条' : '共 ' + rows.length + ' 条';

    // 高亮当前激活的芯片
    document.querySelectorAll('.search-chip').forEach(c => {
      c.classList.remove('active');
      if (c.textContent.includes(activeKeyword)) c.classList.add('active');
    });
  }

  function chipClick(el, keyword) {
    if (el.classList.contains('active')) {
      activeKeyword = '';
      document.getElementById('searchInput').value = '';
    } else {
      activeKeyword = keyword;
    }
    doSearch();
    document.querySelectorAll('.search-chip').forEach(c => c.classList.remove('active'));
    if (activeKeyword) el.classList.add('active');
  }

  function clearSearch() {
    activeKeyword = '';
    document.getElementById('searchInput').value = '';
    document.querySelectorAll('.search-chip').forEach(c => c.classList.remove('active'));
    doSearch();
    document.getElementById('searchInput').focus();
  }

  // 键盘快捷键：ESC清除搜索
  document.addEventListener('keydown', e => {
    if (e.key === 'Escape') { clearSearch(); }
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
      e.preventDefault();
      document.getElementById('searchInput').focus();
    }
  });
</script>
</body>
</html>'''

# ============================================================
# 写入文件
# ============================================================
with open('实习招聘信息汇总_1000条.html', 'w', encoding='utf-8') as f:
    f.write(new_html)

print(f"\nDONE! 文件已重构。")
print(f"  - 删除了所有分类标题和section分组")
print(f"  - 所有条目扁平化排列")
print(f"  - 保留关键词搜索功能")
print(f"  - 纯白背景")
print(f"  - 官网 -> 网址")
print(f"  - 总条目数: {len(renumbered_rows)}")
print(f"  - 新文件大小: {len(new_html)} 字符")
