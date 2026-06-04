#!/usr/bin/env python3
"""
Clean up index.html:
1. Remove search chips: ONLY 即将截止 and 清除
2. Expand 地区 row with ALL cities, one row + expandable
3. Remove only 即将截止 JS filter logic
"""
import re, sys, io, shutil
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# ====== 1. Extract ALL unique cities from data rows ======
all_locs = re.findall(r'<span class="row-loc">📍([^<]*)</span>', content)
from collections import Counter
city_freq = Counter()
for loc in all_locs:
    loc_clean = loc.replace('📍', '').strip()
    for part in loc_clean.split('/'):
        p = part.strip()
        if p:
            city_freq[p] += 1

city_set = set(city_freq.keys())

# Top cities for the visible row (12 most common)
top_cities = ['北京','上海','深圳','广州','成都','杭州','武汉','南京','西安','苏州','重庆','天津']
top_cities = [c for c in top_cities if c in city_set]

# All other cities (sorted by frequency)
other_cities = sorted(city_set - set(top_cities), key=lambda x: (-city_freq[x], x))

print(f"Top cities (visible row): {top_cities}")
print(f"Other cities (hidden): {len(other_cities)}")

# ====== 2. Build new 地区 section ======
top_chips = '\n        '.join(
    f'<span class="search-chip" data-cat="loc" onclick="chipClick(this,\x27{c}\x27)">{c}</span>'
    for c in top_cities
)

hidden_chips = '\n        '.join(
    f'<span class="search-chip" data-cat="loc" onclick="chipClick(this,\x27{c}\x27)">{c}</span>'
    for c in other_cities
)

new_location_section = f'''<!-- 第一行：地区 -->
        <div class="search-chips-row" id="locRow1">
          <span class="search-chip-cat">📍 地区</span>
          {top_chips}
          <span class="search-chip" onclick="toggleMoreCities()" id="moreCitiesBtn" style="color:#7c3aed;border-color:#7c3aed;font-weight:600;">更多城市 ▾</span>
        </div>
        <div class="search-chips-row" id="locRow2" style="display:none;flex-wrap:wrap;">
          <span class="search-chip-cat"></span>
          {hidden_chips}
        </div>'''

# ====== 3. Replace 地区 section ======
old_loc_pattern = re.compile(
    r'<!-- 第一行：地区 -->\s*<div class="search-chips-row">\s*<span class="search-chip-cat">📍 地区</span>.*?</div>',
    re.DOTALL
)
content = re.sub(old_loc_pattern, new_location_section, content, count=1)
print("Replaced 地区 section with expanded cities")

# ====== 4. Remove ONLY 即将截止 + 清除 row ======
old_deadline_row = re.compile(
    r'<!-- 第四行：即将截止 \+ 清除 -->\s*<div class="search-chips-row">\s*<span class="search-chip hot-chip".*?</div>',
    re.DOTALL
)
content = re.sub(old_deadline_row, '', content, count=1)
print("Removed 即将截止/清除 row")

# ====== 5. Remove only 即将截止 JS filter block (keep 热招中 and 可转正) ======
old_js_deadline = re.compile(
    r"(\s*)else if \(kwl === '⏰即将截止'\) \{\s*"
    r"if \(allTags\.includes\('截止'\)\) \{ matchTag = true; break; \}\s*"
    r"\}",
    re.DOTALL
)
content = re.sub(old_js_deadline, '', content)
print("Removed 即将截止 JS filter (kept 热招中/可转正)")

# ====== 6. Add toggleMoreCities function ======
toggle_js = '''
      function toggleMoreCities() {
        const row2 = document.getElementById('locRow2');
        const btn = document.getElementById('moreCitiesBtn');
        if (row2.style.display === 'none' || row2.style.display === '') {
          row2.style.display = 'flex';
          row2.style.flexWrap = 'wrap';
          btn.textContent = '收起 ▲';
        } else {
          row2.style.display = 'none';
          btn.textContent = '更多城市 ▾';
        }
      }
'''
content = content.replace(
    'function clearSearch() {',
    toggle_js + '\n      function clearSearch() {',
)

print("\nAll modifications complete!")
print(f"Top cities visible: {len(top_cities)}")
print(f"Hidden expandable cities: {len(other_cities)}")

# Backup
shutil.copy('index.html', 'index_backup_before_clean.html')
print("\nBackup saved to index_backup_before_clean.html")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("index.html updated!")
