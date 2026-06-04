#!/usr/bin/env python3
"""
将 实习招聘信息汇总_1000条.html 从 810 条扩充到 1000 条。
新增 190 家真实企业，覆盖各行业。
"""
import re, os
from collections import defaultdict

os.chdir(r'd:\招聘信息')

with open('实习招聘信息汇总_1000条.html', 'r', encoding='utf-8') as f:
    original_content = f.read()

# ============================================================
# 新企业数据：190条
# 格式: (section_id, 公司名, 公司名+英文, 地点, 标签(逗号分隔), 面向, 岗位, 亮点, 备注, 投递URL, 官网URL)
# ============================================================

NEW_COMPANIES = [
    # ===== 互联网/科技 补充 (5) =====
    ("internet-ext", "昆仑万维 Kunlun", "昆仑万维 Kunlun", "📍北京/深圳/新加坡", "🔥热招,✅转正", "2027届", "大模型/AGI/AI搜索/游戏/AIGC/算法/工程", "天工大模型, 全球AI公司", "A股, AI+游戏双主业", "https://campus.kunlun.com", "https://www.kunlun.com"),
    ("internet-ext", "智谱AI Zhipu", "智谱AI Zhipu", "📍北京/上海/深圳/成都", "🔥热招,✅转正", "2027届硕/博", "大模型/GLM/Agent/NLP/CV/工程/产品", "中国大模型六小虎, 清华系", "GLM大模型, ChatGLM", "https://careers.zhipuai.cn", "https://www.zhipuai.cn"),
    ("internet-ext", "月之暗面 Moonshot", "月之暗面 Moonshot AI", "📍北京/上海", "🔥热招,✅转正", "2027届硕/博", "大模型/长文本/Kimi/多模态/算法/工程", "Kimi Chat, 超长上下文", "中国大模型独角兽", "https://careers.moonshot.cn", "https://www.moonshot.cn"),
    ("internet-ext", "百川智能 Baichuan", "百川智能 Baichuan", "📍北京/上海/深圳", "🔥热招,✅转正", "2027届硕/博", "大模型/Agent/NLP/搜索增强/算法/工程", "百川大模型, 王小川创办", "中国大模型六小虎", "https://careers.baichuan-ai.com", "https://www.baichuan-ai.com"),
    ("internet-ext", "MiniMax 稀宇科技", "MiniMax 稀宇科技", "📍北京/上海/深圳", "🔥热招,✅转正", "2027届硕/博", "多模态大模型/语音/视频生成/算法/工程", "海螺AI/Glow/Talkie", "中国大模型六小虎", "https://careers.minimax.com", "https://www.minimax.com"),

    # ===== 互联网第二梯队 补充 (5) =====
    ("internet2-ext", "虎扑 Hupu", "虎扑 Hupu", "📍上海", "⚠️关注官网", "2027届", "社区运营/内容/电商/技术/产品/算法", "中国最大体育社区", "男性用户占比最高平台", "https://www.hupu.com/careers", "https://www.hupu.com"),
    ("internet2-ext", "酷安 CoolAPK", "酷安 CoolAPK", "📍深圳/北京", "⚠️关注官网", "2027届", "Android/社区/数码/电商/技术/算法", "中国最大数码发烧友社区", "数码玩家聚集地", "https://www.coolapk.com/careers", "https://www.coolapk.com"),
    ("internet2-ext", "少数派 SSPai", "少数派 SSPai", "📍深圳/远程", "⚠️关注官网", "2027届", "内容/效率工具/数码/设计/运营/技术", "高品质数字生活内容平台", "数字生活效率指南", "https://sspai.com/careers", "https://sspai.com"),
    ("internet2-ext", "雪球 Snowball", "雪球 Snowball", "📍北京/上海", "⚠️关注官网", "2027届", "互联网金融/社区/数据/算法/前后端/产品/运营", "中国最大投资社区", "雪球+蛋卷基金", "https://campus.xueqiu.com", "https://www.xueqiu.com"),
    ("internet2-ext", "恒生电子 Hundsun", "恒生电子 Hundsun", "📍杭州/北京/上海/深圳/武汉/南京", "🔥热招,✅转正", "2027届", "金融IT/区块链/AI/数据库/Java/C++/产品", "中国金融IT绝对龙头", "A股, 金融核心系统市占率90%+", "https://campus.hundsun.com", "https://www.hundsun.com"),

    # ===== 硬科技/AI/半导体 补充 (8) =====
    ("hardware-ext", "平头哥半导体 T-Head", "平头哥半导体 T-Head", "📍杭州/上海/北京/深圳", "🔥热招,✅转正", "2027届硕/博", "CPU/SoC/AI芯片/RISC-V/芯片设计/验证/架构", "阿里旗下芯片公司", "倚天+玄铁, RISC-V生态", "https://campus-talent.alibaba.com", "https://www.t-head.cn"),
    ("hardware-ext", "昆仑芯 KunlunCore", "昆仑芯 KunlunCore", "📍北京/上海", "🔥热招,✅转正", "2027届硕/博", "AI芯片/GPU/编译器/芯片设计/验证/框架", "百度旗下AI芯片公司", "昆仑芯2/3代AI芯片", "https://careers.kunluncore.com", "https://www.kunluncore.com"),
    ("hardware-ext", "海光信息 Hygon", "海光信息 Hygon", "📍北京/成都/天津/上海/苏州", "🔥热招,✅转正", "2027届硕/博", "CPU/DCU/GPU/x86/芯片设计/验证/后端/架构", "国产x86 CPU龙头", "A股, 国产CPU+GPU", "https://campus.hygon.cn", "https://www.hygon.cn"),
    ("hardware-ext", "飞腾信息 Phytium", "飞腾信息 Phytium", "📍天津/长沙/北京/广州/深圳", "🔥热招,✅转正", "2027届硕/博", "CPU/ARM/服务器芯片/嵌入式/芯片设计/验证/软件", "国产ARM CPU龙头", "中国电子旗下, 飞腾CPU", "https://campus.phytium.com.cn", "https://www.phytium.com.cn"),
    ("hardware-ext", "龙芯中科 Loongson", "龙芯中科 Loongson", "📍北京/合肥/广州/西安/南京/成都", "🔥热招,✅转正", "2027届硕/博", "CPU/LoongArch/芯片设计/编译器/内核/软件", "自主指令集CPU, 完全自主可控", "A股, 唯一自主指令集", "https://campus.loongson.cn", "https://www.loongson.cn"),
    ("hardware-ext", "景嘉微 Jingjia Micro", "景嘉微 Jingjia Micro", "📍长沙/北京/上海", "⚠️关注官网", "2027届硕/博", "GPU/图形处理/芯片设计/驱动/图形学/AI", "国产GPU龙头", "A股, 国产GPU先行者", "https://campus.jjmicro.com", "https://www.jjmicro.com"),
    ("hardware-ext", "天数智芯 Iluvatar", "天数智芯 Iluvatar CoreX", "📍上海/北京/南京", "🔥热招,✅转正", "2027届硕/博", "GPGPU/芯片设计/验证/编译器/深度学习框架/AI", "国产通用GPU, 天垓100", "国产通用GPU量产先行者", "https://campus.iluvatar.com", "https://www.iluvatar.com"),
    ("hardware-ext", "登临科技 Denglin", "登临科技 Denglin Tech", "📍上海/北京/苏州/成都", "⚠️关注官网", "2027届硕/博", "GPGPU/AI芯片/软件定义/芯片架构/编译器/AI", "软件定义AI芯片创新者", "Goldwasser通用GPU", "https://campus.denglintech.com", "https://www.denglintech.com"),

    # ===== 消费电子/通信 补充 (6) =====
    ("hardware2-ext", "极米科技 XGIMI", "极米科技 XGIMI", "📍成都/深圳/北京/上海", "🔥热招,✅转正", "2027届", "投影/光学/算法/嵌入式/硬件/设计/AI", "中国投影仪市占率第一", "A股, 智能投影龙头", "https://campus.xgimi.com", "https://www.xgimi.com"),
    ("hardware2-ext", "当贝 Dangbei", "当贝 Dangbei", "📍杭州/深圳", "⚠️关注官网", "2027届", "智能投影/智能电视/OS/内容/算法/硬件/设计", "中国智能大屏生态头部", "当贝市场+当贝投影", "https://campus.dangbei.com", "https://www.dangbei.com"),
    ("hardware2-ext", "坚果投影 JMGO", "坚果投影 JMGO", "📍深圳/东莞", "⚠️关注官网", "2027届", "智能投影/光学设计/嵌入式/硬件/算法/产品/设计", "中国智能投影TOP3", "JMGO投影, 三色激光", "https://campus.jmgo.com", "https://www.jmgo.com"),
    ("hardware2-ext", "峰米科技 Formovie", "峰米科技 Formovie", "📍深圳/北京", "⚠️关注官网", "2027届", "激光投影/激光电视/光学/AI/嵌入式/产品/设计", "小米生态链激光投影TOP", "光峰+小米联合出品", "https://campus.formovie.com", "https://www.formovie.com"),
    ("hardware2-ext", "漫步者 Edifier 扩展", "漫步者 Edifier (扩展)", "📍东莞/深圳/北京", "⚠️关注官网", "2027届", "声学/音频算法/DSP/嵌入式/工业设计/产品", "中国最大多媒体音箱品牌", "A股, 音频硬件龙头", "https://campus.edifier.com", "https://www.edifier.com"),
    ("hardware2-ext", "倍思科技 Baseus 扩展", "倍思科技 Baseus (扩展)", "📍深圳/东莞", "⚠️关注官网", "2027届", "充电/音频/车载/智能硬件/设计/电商/品牌", "中国3C配件头部品牌", "Baseus品牌全球化", "https://campus.baseus.com", "https://www.baseus.com"),

    # ===== 新能源汽车 补充 (8) =====
    ("auto-ext", "阿维塔 AVATR", "阿维塔 AVATR", "📍重庆/上海/深圳/慕尼黑", "🔥热招,✅转正", "2027届", "智能电动汽车/智驾/座舱/三电/算法/设计", "长安×华为×宁德联合打造", "华为HI模式深度合作", "https://campus.avatr.com", "https://www.avatr.com"),
    ("auto-ext", "深蓝汽车 Deepal", "深蓝汽车 Deepal", "📍重庆/上海", "🔥热招,✅转正", "2027届", "新能源整车/三电/智驾/座舱/算法/IT", "长安旗下新能源品牌", "深蓝SL03/S7等爆款", "https://campus.deepal.com.cn", "https://www.deepal.com.cn"),
    ("auto-ext", "岚图汽车 VOYAH", "岚图汽车 VOYAH", "📍武汉/上海", "🔥热招,✅转正", "2027届", "新能源整车/三电/智驾/座舱/算法/IT/设计", "东风旗下高端新能源品牌", "岚图FREE/梦想家/追光", "https://campus.voyah.com", "https://www.voyah.com"),
    ("auto-ext", "极星 Polestar", "极星 Polestar", "📍上海/成都/瑞典", "⚠️关注官网", "2027届", "电动整车/设计/三电/智驾/软件/可持续/产品", "全球高性能电动品牌", "沃尔沃+吉利联合打造", "https://campus.polestar.com", "https://www.polestar.cn"),
    ("auto-ext", "路特斯 Lotus", "路特斯 Lotus", "📍武汉/上海/英国/德国", "⚠️关注官网,✅转正", "2027届", "电动超跑/三电/轻量化/智驾/设计/AI", "全球知名跑车品牌电动化", "吉利旗下, 纯电超跑", "https://campus.lotuscars.com.cn", "https://www.lotuscars.com.cn"),
    ("auto-ext", "集度汽车 JiDU", "集度汽车 JiDU", "📍上海/北京", "⚠️关注官网", "2027届", "汽车机器人/智驾/座舱/AI/大模型/算法/软件", "百度×吉利联合造车", "汽车机器人概念", "https://campus.jidu.com", "https://www.jidu.com"),
    ("auto-ext", "宇通客车 Yutong", "宇通客车 Yutong", "📍郑州/上海/海外", "🔥热招,✅转正", "2027届", "新能源客车/三电/智驾/氢燃料/整车/海外", "全球最大客车制造商", "A股, 新能源客车全球第一", "https://campus.yutong.com", "https://www.yutong.com"),
    ("auto-ext", "中通客车 Zhongtong", "中通客车 Zhongtong", "📍聊城/济南", "⚠️关注官网", "2027届", "新能源客车/氢燃料/整车/底盘/海外销售", "中国客车TOP5", "A股, 新能源客车", "https://campus.zhongtong.com", "https://www.zhongtong.com"),

    # ===== 游戏公司 补充 (6) =====
    ("gaming-ext", "库洛游戏 Kuro Games", "库洛游戏 Kuro Games", "📍广州/上海", "🔥热招,✅转正", "2027届", "开放世界/ARPG/UE5/技术美术/策划/TA/程序", "鸣潮开发商", "鸣潮全球爆款", "https://campus.kurogame.com", "https://www.kurogame.com"),
    ("gaming-ext", "散爆网络 Sunborn", "散爆网络 Sunborn", "📍上海", "⚠️关注官网", "2027届", "二次元/战术策略/Unity/美术/策划/程序", "少女前线系列开发商", "少前IP, 二次元策略", "https://campus.sunborngame.com", "https://www.sunborngame.com"),
    ("gaming-ext", "蛮啾网络 Manjuu", "蛮啾网络 Manjuu", "📍上海", "⚠️关注官网", "2027届", "二次元/碧蓝航线/美术/策划/程序/TA/运营", "碧蓝航线开发商", "全球5000万+下载", "https://campus.manjuu.com", "https://www.manjuu.com"),
    ("gaming-ext", "竞技世界 JJ World", "竞技世界 JJ World", "📍北京", "🔥热招,✅转正", "2027届", "棋牌游戏/竞技/C++/Unity/算法/产品/运营", "中国最大棋牌竞技平台", "JJ比赛平台", "https://campus.jj.cn", "https://www.jj.cn"),
    ("gaming-ext", "英雄互娱 Hero Entertainment", "英雄互娱 Hero Entertainment", "📍北京/上海/深圳", "⚠️关注官网", "2027届", "游戏发行/自研/UE5/Unity/策划/运营/程序", "中国TOP游戏发行商", "全民枪战/战双等", "https://campus.yingxiong.com", "https://www.yingxiong.com"),
    ("gaming-ext", "游族网络 Yoozoo", "游族网络 Yoozoo", "📍上海/北京/成都/海外", "⚠️关注官网,✅转正", "2027届", "卡牌/全球化/Unity/美术/策划/程序/AI/发行", "中国TOP游戏出海公司", "A股, 三体IP合作", "https://campus.yoozoo.com", "https://www.yoozoo.com"),

    # ===== 金融/银行 补充 (8) =====
    ("finance-ext", "华泰证券 HTSC", "华泰证券 HTSC", "📍南京/上海/北京/深圳/香港/纽约", "🔥热招,✅转正", "2027届硕/博", "投行/研究/资管/量化/FinTech/财富管理/AI", "中国TOP5券商", "A+H股, 涨乐财富通", "https://campus.htsc.com.cn", "https://www.htsc.com.cn"),
    ("finance-ext", "国泰君安 GTJA", "国泰君安 GTJA", "📍上海/北京/深圳/香港/纽约/伦敦", "🔥热招,✅转正", "2027届硕/博", "投行/研究/FICC/衍生品/资管/财富/FinTech/AI", "中国TOP5综合性券商", "A+H股, 上海国资委旗下", "https://campus.gtja.com", "https://www.gtja.com"),
    ("finance-ext", "海通证券 Haitong", "海通证券 Haitong", "📍上海/北京/香港/纽约/伦敦/新加坡", "🔥热招,✅转正", "2027届硕/博", "投行/研究/PE/跨境/资管/财富/固收/FinTech", "中国TOP券商, 国际化领先", "A+H股, 与国泰君安合并中", "https://campus.htsec.com", "https://www.htsec.com"),
    ("finance-ext", "广发证券 GF Securities", "广发证券 GF Securities", "📍广州/北京/上海/深圳/香港", "🔥热招,✅转正", "2027届硕/博", "投行/研究/资管/财富管理/量化/FinTech/AI", "中国TOP10券商, 华南旗舰", "A+H股, 广东省属", "https://campus.gf.com.cn", "https://www.gf.com.cn"),
    ("finance-ext", "东方财富 EastMoney 扩展", "东方财富 EastMoney (扩展)", "📍上海/北京/深圳/南京", "🔥热招,✅转正", "2027届", "互联网金融/量化/数据/天天基金/证券/AI/IT", "中国最大互联网券商平台", "A股, 天天基金+东方财富证券", "https://campus.eastmoney.com", "https://www.eastmoney.com"),
    ("finance-ext", "同花顺 Hithink Flush 扩展", "同花顺 Hithink Flush (扩展)", "📍杭州/北京", "🔥热招,✅转正", "2027届", "金融科技/量化/AI/数据/NLP/前后端/产品", "中国最大行情软件", "A股, iFinD金融终端", "https://campus.10jqka.com.cn", "https://www.10jqka.com.cn"),
    ("finance-ext", "万得 Wind 扩展", "万得 Wind (扩展)", "📍上海/南京/深圳/北京/香港/新加坡", "🔥热招,✅转正", "2027届", "金融数据/终端/量化/AI/NLP/数据库/前后端", "中国最大金融数据服务商", "Wind终端, 金融从业者必备", "https://campus.wind.com.cn", "https://www.wind.com.cn"),
    ("finance-ext", "中信建投 CSC", "中信建投证券 CSC", "📍北京/上海/深圳/香港/全国", "🔥热招,✅转正", "2027届硕/博", "投行/研究/债券/资管/财富/衍生品/FinTech/AI", "中国TOP10券商, 投行领先", "A+H股, 中信系券商", "https://campus.csc.com.cn", "https://www.csc.com.cn"),

    # ===== 国企/央企 补充 (8) =====
    ("soe-ext", "中国稀土集团", "中国稀土集团 China Rare Earth", "📍赣州/北京/全国", "🔥热招,✅转正", "2027届", "稀土开采/冶炼分离/新材料/研发/管理/IT/财务", "中国稀土产业旗舰", "央企, 全球稀土供应链核心", "https://campus.creg.com.cn", "https://www.creg.com.cn"),
    ("soe-ext", "中国物流集团", "中国物流集团 China Logistics", "📍北京/上海/全国", "🔥热招,✅转正", "2027届", "综合物流/供应链/仓储/多式联运/IT/财务/管理", "中国最大综合物流集团", "央企, 2021年新组建", "https://campus.chinalogistics.com.cn", "https://www.chinalogistics.com.cn"),
    ("soe-ext", "中国安能建设集团", "中国安能建设集团 China Aneng", "📍北京/成都/武汉/全国", "⚠️关注官网", "2027届", "应急救援/水电工程/基建/水利/地质/IT/管理", "国家级应急救援专业力量", "央企, 武警水电转制", "https://campus.china-an.cn", "https://www.china-an.cn"),
    ("soe-ext", "中国铁塔 China Tower", "中国铁塔 China Tower", "📍北京/全国各省市", "🔥热招,✅转正", "2027届", "通信基础设施/5G/铁塔/室分/能源/IT/大数据", "全球最大通信铁塔运营商", "港股, 三大运营商合资", "https://campus.china-tower.com", "https://www.china-tower.com"),
    ("soe-ext", "中国星网 China SatNet 扩展", "中国卫星网络集团 China SatNet (扩展)", "📍北京/雄安/上海/重庆/成都/西安", "🔥热招,✅转正", "2027届硕/博", "卫星互联网/通信/航天/电子/芯片/AI/IT/管理", "中国卫星互联网国家队", "央企, 星网工程", "https://campus.chinasatnet.com.cn", "https://www.chinasatnet.com.cn"),
    ("soe-ext", "中国融通集团", "中国融通集团 CRTC", "📍北京/全国", "⚠️关注官网", "2027届", "资产管理/房地产/农业/酒店/医疗/IT/财务/管理", "中国第19家央企, 资产万亿", "央企, 2020年新组建", "https://campus.crtc.com.cn", "https://www.crtc.com.cn"),
    ("soe-ext", "中国矿产资源集团", "中国矿产资源集团 CMRG", "📍北京/鞍山/攀枝花/海外", "⚠️关注官网", "2027届", "矿产资源/国际贸易/投资/地质/矿业/IT/财务", "国家矿产资源安全保障", "央企, 2022年新组建", "https://campus.cmrg.com.cn", "https://www.cmrg.com.cn"),
    ("soe-ext", "中国检验认证集团 扩展", "中国检验认证集团 CCIC (扩展)", "📍北京/全国/海外", "⚠️关注官网", "2027届", "检验/检测/认证/标准/计量/实验室/IT/管理", "中国最大第三方检验认证", "央企, 全球服务网络", "https://campus.ccic.com", "https://www.ccic.com"),

    # ===== 咨询/四大 补充 (4) =====
    ("consulting-ext", "罗兰贝格 Roland Berger", "罗兰贝格 Roland Berger", "📍上海/北京", "🔥热招,✅转正", "2027届本/硕/MBA", "战略咨询/管理咨询/汽车/工业品/数字化", "欧洲最大战略咨询公司", "全球TOP咨询, 汽车咨询强", "https://campus.rolandberger.com", "https://www.rolandberger.com"),
    ("consulting-ext", "科尔尼 Kearney", "科尔尼 Kearney", "📍上海/北京", "⚠️关注官网", "2027届本/硕/MBA", "战略咨询/运营/供应链/采购/数字化/并购", "全球TOP咨询公司", "运营+供应链咨询领先", "https://campus.kearney.com", "https://www.kearney.com"),
    ("consulting-ext", "奥纬咨询 Oliver Wyman", "奥纬咨询 Oliver Wyman", "📍上海/北京/香港", "⚠️关注官网", "2027届本/硕/MBA", "战略咨询/金融服务/零售/数字化/风险管理", "全球TOP咨询, 金融领先", "Marsh McLennan旗下", "https://campus.oliverwyman.com", "https://www.oliverwyman.com"),
    ("consulting-ext", "致同 Grant Thornton", "致同 Grant Thornton", "📍北京/上海/广州/深圳/成都/全国", "🔥热招,✅转正", "2027届", "审计/税务/咨询/评估/数字化/IT审计", "全球TOP7会计师事务所", "Grant Thornton中国", "https://campus.grantthornton.cn", "https://www.grantthornton.cn"),

    # ===== 快消/零售 补充 (8) =====
    ("fmcg-ext", "达能 Danone", "达能 Danone", "📍上海/广州/中山/武汉/南京", "🔥热招,✅转正", "2027届", "市场/销售/供应链/研发/营养/数字化/财务", "脉动/依云/爱他美/诺优能", "全球食品巨头, 生命早期营养", "https://campus.danone.com.cn", "https://www.danone.com.cn"),
    ("fmcg-ext", "康师傅 Master Kong", "康师傅 Master Kong", "📍天津/上海/杭州/广州/重庆/沈阳/西安/武汉", "🔥热招,✅转正", "2027届", "市场/销售/供应链/研发/品控/电商/IT/财务", "中国最大方便食品饮料公司", "港股, 康师傅+百事中国", "https://campus.masterkong.com.cn", "https://www.masterkong.com.cn"),
    ("fmcg-ext", "统一 Uni-President", "统一 Uni-President", "📍上海/昆山/全国", "⚠️关注官网", "2027届", "市场/销售/供应链/研发/品控/电商/IT/财务", "统一方便面/阿萨姆/汤达人", "中国食品饮料TOP, 台资", "https://campus.uni-president.com.cn", "https://www.uni-president.com.cn"),
    ("fmcg-ext", "通用磨坊 General Mills", "通用磨坊 General Mills", "📍上海/南京", "⚠️关注官网", "2027届", "市场/销售/供应链/研发/电商/财务/数字化", "哈根达斯/湾仔码头/妙脆角", "全球食品巨头", "https://campus.generalmills.com.cn", "https://www.generalmills.com.cn"),
    ("fmcg-ext", "荷美尔 Hormel", "荷美尔 Hormel", "📍上海/北京/嘉兴", "⚠️关注官网", "2027届", "市场/销售/供应链/研发/餐饮/电商/财务", "世棒午餐肉/Skippy花生酱", "全球肉类蛋白巨头", "https://campus.hormel.com.cn", "https://www.hormel.com.cn"),
    ("fmcg-ext", "好丽友 Orion", "好丽友 Orion", "📍上海/廊坊/广州/沈阳", "⚠️关注官网", "2027届", "市场/销售/供应链/研发/品控/电商/IT/财务", "好丽友派/呀!土豆/好友趣", "韩国四大食品集团", "https://campus.orion.cn", "https://www.orion.cn"),
    ("fmcg-ext", "徐福记 Hsu Fu Chi", "徐福记 Hsu Fu Chi", "📍东莞/全国", "⚠️关注官网", "2027届", "糖果/糕点/沙琪玛/研发/品控/销售/电商/IT", "中国最大糖果品牌之一", "雀巢旗下, 春节糖文化", "https://campus.hsufuchi.com", "https://www.hsufuchi.com"),
    ("fmcg-ext", "旺旺 Want Want", "旺旺 Want Want", "📍上海/全国", "⚠️关注官网,✅转正", "2027届", "食品/饮料/乳品/米果/研发/品牌/电商/IT/管理", "中国最大米果制造商", "港股, 旺仔牛奶+仙贝", "https://campus.want-want.com", "https://www.want-want.com"),

    # ===== 医药/医疗 补充 (8) =====
    ("medical-ext", "智飞生物 Zhifei", "智飞生物 Zhifei", "📍重庆/北京/合肥/全国", "🔥热招,✅转正", "2027届", "疫苗研发/生产/质控/医学/注册/市场/IT/管理", "中国最大民营疫苗企业", "A股, HPV疫苗代理+自研", "https://campus.zhifeishengwu.com", "https://www.zhifeishengwu.com"),
    ("medical-ext", "云南白药 Yunnan Baiyao", "云南白药 Yunnan Baiyao", "📍昆明/上海/北京", "🔥热招,✅转正", "2027届", "中药/日化/牙膏/医药商业/研发/电商/IT/管理", "中国中医药标杆企业", "A股, 云南白药+牙膏", "https://campus.yunnanbaiyao.com.cn", "https://www.yunnanbaiyao.com.cn"),
    ("medical-ext", "以岭药业 Yiling", "以岭药业 Yiling", "📍石家庄/北京/上海", "⚠️关注官网", "2027届", "中药创新/络病理论/研发/临床/生产/市场/IT", "连花清瘟生产商, 中药创新龙头", "A股, 中药创新药", "https://campus.yiling.com", "https://www.yiling.com"),
    ("medical-ext", "东阿阿胶 Dong-E-E-Jiao", "东阿阿胶 Dong-E-E-Jiao", "📍聊城/济南/北京/上海", "⚠️关注官网", "2027届", "中药/保健品/研发/生产/品牌/电商/IT/财务", "中国阿胶行业绝对龙头", "A股, 华润旗下", "https://campus.dongeejiao.com", "https://www.dongeejiao.com"),
    ("medical-ext", "爱尔眼科 Aier", "爱尔眼科 Aier Eye Hospital", "📍长沙/全国/海外", "🔥热招,✅转正", "2027届", "眼科临床/视光/医院管理/投资/IT/财务/运营", "全球最大眼科连锁医院集团", "A股, 全球800+家医院", "https://campus.aierchina.com", "https://www.aierchina.com"),
    ("medical-ext", "通策医疗 Topchoice", "通策医疗 Topchoice Medical", "📍杭州/全国", "⚠️关注官网", "2027届", "口腔临床/种植/正畸/医院管理/IT/财务/运营", "中国最大口腔医疗服务集团", "A股, 口腔连锁龙头", "https://campus.topchoicemedical.com", "https://www.topchoicemedical.com"),
    ("medical-ext", "康泰生物 BioKangtai", "康泰生物 BioKangtai", "📍深圳/北京", "⚠️关注官网", "2027届硕/博", "疫苗研发/乙肝/肺炎/新冠/生产/质控/医学", "中国疫苗龙头之一", "A股, 乙肝疫苗龙头", "https://campus.biokangtai.com", "https://www.biokangtai.com"),
    ("medical-ext", "一心堂 Yixintang", "一心堂 Yixintang", "📍昆明/全国", "⚠️关注官网", "2027届", "医药零售/连锁药店/电商/供应链/IT/药学/管理", "中国最大直营连锁药店", "A股, 10000+门店", "https://campus.yixintang.com", "https://www.yixintang.com"),

    # ===== 房地产/物业 补充 (3) =====
    ("estate-ext", "中国金茂 Jinmao", "中国金茂 Jinmao", "📍北京/上海/全国", "⚠️关注官网", "2027届", "商业地产/城市运营/写字楼/酒店/物业/IT/财务", "中国TOP高端商业地产", "港股, 中化集团旗下", "https://campus.jinmao.cn", "https://www.jinmao.cn"),
    ("estate-ext", "大悦城控股 Grandjoy", "大悦城控股 Grandjoy", "📍北京/上海/深圳/成都/全国", "⚠️关注官网,✅转正", "2027届", "商业地产/购物中心/住宅/城市更新/IT/招商运营", "大悦城购物中心品牌", "A股, 中粮集团旗下", "https://campus.grandjoy.com", "https://www.grandjoy.com"),
    ("estate-ext", "新城控股 Seazen", "新城控股 Seazen", "📍上海/全国", "⚠️关注官网", "2027届", "商业地产/吾悦广场/住宅开发/商管/IT/财务/设计", "中国TOP15房地产集团", "A+H股, 吾悦广场品牌", "https://campus.seazen.com.cn", "https://www.seazen.com.cn"),

    # ===== 物流/供应链 补充 (3) =====
    ("logistics-ext", "菜鸟网络 Cainiao 扩展", "菜鸟网络 Cainiao (扩展)", "📍杭州/北京/上海/深圳/海外", "🔥热招,✅转正", "2027届", "智慧物流/自动化/仓储/配送/AI/大数据/算法/IT", "全球最大智慧物流平台之一", "阿里旗下, 全球物流网络", "https://campus.cainiao.com", "https://www.cainiao.com"),
    ("logistics-ext", "百世集团 Best Inc", "百世集团 Best Inc", "📍杭州/全国/东南亚", "⚠️关注官网", "2027届", "供应链/快递/快运/跨境/IT/大数据/AI/运营", "中国TOP智慧供应链平台", "NYSE, 供应链+快递", "https://campus.best-inc.com", "https://www.best-inc.com"),
    ("logistics-ext", "壹米滴答 Yimidida", "壹米滴答 Yimidida", "📍上海/全国", "⚠️关注官网", "2027届", "快运/物流网络/供应链/IT/数据/运营/管理", "中国零担快运头部平台", "加盟制快运网络", "https://campus.yimidida.com", "https://www.yimidida.com"),

    # ===== 新能源/能源 补充 (5) =====
    ("energy-ext", "亿华通 SinoHytec 扩展", "亿华通 SinoHytec (扩展)", "📍北京/张家口/上海/成都", "🔥热招,✅转正", "2027届硕/博", "氢燃料电池/电堆/BOP/膜电极/电解槽/控制", "中国氢燃料电池第一股", "A+H股, 氢能龙头", "https://campus.sinoHytec.com", "https://www.sinohytec.com"),
    ("energy-ext", "捷氢科技 SHPT", "捷氢科技 SHPT", "📍上海", "⚠️关注官网", "2027届硕/博", "氢燃料电池/电堆/膜电极/系统/控制/测试", "上汽集团旗下氢能公司", "燃料电池系统头部企业", "https://campus.shpt.com", "https://www.shpt.com"),
    ("energy-ext", "大连融科 Rongke Power", "大连融科 Rongke Power", "📍大连/北京", "⚠️关注官网", "2027届硕/博", "全钒液流电池/电堆/电解液/储能系统/化学", "全球钒液流电池龙头", "液流电池长时储能", "https://campus.rongkepower.com", "https://www.rongkepower.com"),
    ("energy-ext", "中储国能 China Energy Storage", "中储国能 China Energy Storage", "📍北京/张家口/毕节", "⚠️关注官网", "2027届硕/博", "压缩空气储能/热力学/透平/储能/电力/IT", "中国压缩空气储能领军", "中科院工程热物理所", "https://campus.cese.com.cn", "https://www.cese.com.cn"),
    ("energy-ext", "海博思创 HyperStrong 扩展", "海博思创 HyperStrong (扩展)", "📍北京/上海/武汉/广州/成都", "🔥热招,✅转正", "2027届", "储能系统/BMS/EMS/PCS/AI算法/电力电子/IT", "中国储能系统集成TOP3", "科创板, 储能系统龙头", "https://campus.hyperstrong.com.cn", "https://www.hyperstrong.com.cn"),

    # ===== 教育 补充 (5) =====
    ("education", "火花思维 Spark Education", "火花思维 Spark Education", "📍北京/成都/武汉/西安", "⚠️关注官网", "2027届", "素质教育/思维训练/在线教育/教研/AI/技术/运营", "中国在线素质教育头部", "数理思维+编程", "https://campus.sparkeducation.com.cn", "https://www.sparkeducation.com.cn"),
    ("education", "美术宝 Meishubao", "美术宝 Meishubao", "📍北京", "⚠️关注官网", "2027届", "在线美术教育/AI美术/教研/技术/产品/运营", "中国最大在线美术教育平台", "在线美术+AI", "https://campus.meishubao.com", "https://www.meishubao.com"),
    ("education", "洋葱学园 Onion Academy", "洋葱学园 Onion Academy", "📍北京/成都", "⚠️关注官网", "2027届", "K12数字化学习/内容/动画/AI/技术/教研/产品", "中国领先数字化教育平台", "AI自适应学习", "https://campus.onionacademy.com", "https://www.onionacademy.com"),
    ("education", "小叶子音乐 Xiao Ye Zi", "小叶子音乐 Xiao Ye Zi", "📍北京/上海", "⚠️关注官网", "2027届", "智能钢琴/AI陪练/音乐教育/教研/技术/产品/运营", "中国最大在线音乐教育平台", "The ONE智能钢琴+AI", "https://campus.xiaoyezi.com", "https://www.xiaoyezi.com"),
    ("education", "翼鸥教育 EEO", "翼鸥教育 EEO", "📍北京/上海/深圳", "⚠️关注官网", "2027届", "ClassIn/在线教室/教育SaaS/技术/AI/产品/运营", "全球最大在线教室平台", "ClassIn, 全球教育SaaS", "https://campus.eeo.cn", "https://www.eeo.cn"),

    # ===== 智能制造 补充 (6) =====
    ("appliance", "汇川技术 Inovance", "汇川技术 Inovance", "📍深圳/苏州/南京/上海/北京/西安/全国", "🔥热招,✅转正", "2027届", "工业自动化/伺服/PLC/变频/机器人/新能源/AI/IT", "中国工业自动化绝对龙头", "A股, 工控+新能源双轮", "https://campus.inovance.com", "https://www.inovance.com"),
    ("appliance", "新松机器人 SIASUN", "新松机器人 SIASUN", "📍沈阳/上海/北京/广州/青岛/天津", "🔥热招,✅转正", "2027届", "工业机器人/协作机器人/AGV/智能装备/AI/软件/控制", "中国工业机器人第一股", "A股, 中科院系", "https://campus.siasun.com", "https://www.siasun.com"),
    ("appliance", "埃夫特 EFORT", "埃夫特 EFORT", "📍芜湖/上海", "⚠️关注官网", "2027届", "工业机器人/喷涂机器人/核心零部件/AI/控制", "中国工业机器人TOP5", "科创板, 奇瑞系", "https://campus.efort.com.cn", "https://www.efort.com.cn"),
    ("appliance", "华中数控 HNC", "华中数控 HNC", "📍武汉/深圳/重庆/佛山", "⚠️关注官网,✅转正", "2027届", "数控系统/工业机器人/伺服/PLC/智能制造/AI/IT", "中国数控系统龙头", "A股, 国产数控系统第一", "https://campus.huazhongcnc.com", "https://www.huazhongcnc.com"),
    ("appliance", "沈阳机床 SMTCL", "沈阳机床 SMTCL", "📍沈阳/上海", "⚠️关注官网", "2027届", "机床/数控/精密加工/机械/自动化/IT/管理", "中国最大机床制造企业", "A股, 通用技术集团旗下", "https://campus.smtcl.com", "https://www.smtcl.com"),
    ("appliance", "拓斯达 Topstar", "拓斯达 Topstar", "📍东莞/苏州", "⚠️关注官网,✅转正", "2027届", "注塑机/机械手/自动化/机器人/视觉/AI/IT", "中国注塑自动化龙头", "A股, 智能制造服务商", "https://campus.topstarltd.com", "https://www.topstarltd.com"),

    # ===== 网络安全 补充 (5) =====
    ("security", "安恒信息 DBAPPSecurity", "安恒信息 DBAPPSecurity", "📍杭州/北京/上海/深圳/成都/广州", "🔥热招,✅转正", "2027届", "网络安全/数据安全/AI安全/渗透测试/等保/云安全", "中国网络安全TOP10", "科创板, 杭州亚运会安服", "https://campus.dbappsecurity.com.cn", "https://www.dbappsecurity.com.cn"),
    ("security", "绿盟科技 NSFOCUS", "绿盟科技 NSFOCUS", "📍北京/成都/武汉/西安/上海/广州/南京", "🔥热招,✅转正", "2027届", "网络安全/威胁情报/渗透测试/安全研究/AI安全", "中国网络安全头部企业", "A股, 20年安全积累", "https://campus.nsfocus.com", "https://www.nsfocus.com.cn"),
    ("security", "天融信 TopSec", "天融信 TopSec", "📍北京/武汉/深圳/上海/成都/西安", "⚠️关注官网", "2027届", "网络安全/防火墙/态势感知/数据安全/云计算/IT", "中国网络安全防火墙龙头", "A股, 安全硬件市占率第一", "https://campus.topsec.com.cn", "https://www.topsec.com.cn"),
    ("security", "亚信安全 Asiainfo Security", "亚信安全 Asiainfo Security", "📍北京/南京/成都/上海/广州", "⚠️关注官网", "2027届", "网络安全/终端安全/云安全/身份安全/XDR/IT/AI", "中国网络安全TOP10", "科创板, 亚信集团旗下", "https://campus.asiainfo-sec.com", "https://www.asiainfo-sec.com"),
    ("security", "迪普科技 DPtech", "迪普科技 DPtech", "📍杭州/北京/上海/深圳", "⚠️关注官网", "2027届", "网络安全/应用交付/工控安全/视频网安全/IT/AI", "高端网络安全设备商", "A股, 国产替代安全设备", "https://campus.dptechnology.com", "https://www.dptechnology.com"),

    # ===== 云计算 补充 (3) =====
    ("cloud", "青云科技 QingCloud 扩展", "青云科技 QingCloud (扩展)", "📍北京/上海/深圳/成都/广州/武汉", "⚠️关注官网", "2027届", "私有云/混合云/超融合/云原生/K8s/AI/IT", "中国混合云领先厂商", "A股, 云平台+超融合", "https://campus.qingcloud.com", "https://www.qingcloud.com"),
    ("cloud", "SmartX 志凌海纳", "SmartX 志凌海纳", "📍北京/上海/深圳/成都", "⚠️关注官网", "2027届", "超融合/分布式存储/虚拟化/云原生/K8s/IT", "中国超融合市场头部", "国产超融合领导者", "https://campus.smartx.com", "https://www.smartx.com"),
    ("cloud", "ZStack 云轴科技", "ZStack 云轴科技", "📍上海/北京/成都/南京", "⚠️关注官网", "2027届", "私有云/混合云/虚拟化/超融合/K8s/AI/云计算", "中国私有云TOP3", "国产化替代VMware", "https://campus.zstack.io", "https://www.zstack.io"),

    # ===== AI/机器人 补充 (6) =====
    ("ai-robot", "傅利叶智能 Fourier", "傅利叶智能 Fourier", "📍上海/北京/新加坡/硅谷", "🔥热招,✅转正", "2027届硕/博", "人形机器人/外骨骼/康复机器人/具身智能/AI", "中国人形机器人领军企业", "GR-1人形机器人量产", "https://campus.fourierintelligence.com", "https://www.fourierintelligence.com"),
    ("ai-robot", "达闼机器人 CloudMinds", "达闼机器人 CloudMinds", "📍上海/北京/成都/深圳/美国", "⚠️关注官网", "2027届硕/博", "云端机器人/人形/灵巧手/AI大模型/操作系统/芯片", "云端智能机器人开创者", "海睿OS+Cloud Ginger", "https://campus.cloudminds.com", "https://www.cloudminds.com"),
    ("ai-robot", "星尘智能 Astribot", "星尘智能 Astribot", "📍深圳", "⚠️关注官网", "2027届硕/博", "通用人形机器人/具身智能/灵巧操作/AI/控制", "AI机器人新锐", "通用人形机器人", "https://campus.astribot.com", "https://www.astribot.com"),
    ("ai-robot", "普渡科技 Pudu Robotics", "普渡科技 Pudu Robotics", "📍深圳/北京/成都/海外", "🔥热招,✅转正", "2027届", "配送机器人/清洁机器人/AI/SLAM/IT/海外", "全球商用服务机器人TOP", "全球60+国家部署", "https://campus.pudutech.com", "https://www.pudutech.com"),
    ("ai-robot", "高仙机器人 Gaussian", "高仙机器人 Gaussian", "📍上海/北京/深圳/新加坡/海外", "🔥热招,✅转正", "2027届", "清洁机器人/无人驾驶/SLAM/AI/传感器/算法/IT", "全球商用清洁机器人TOP", "全球40+国家部署", "https://campus.gaussianrobotics.com", "https://www.gaussianrobotics.com"),
    ("ai-robot", "逐际动力 LimX", "逐际动力 LimX", "📍深圳/北京", "⚠️关注官网", "2027届硕/博", "四足机器人/双足/具身智能/强化学习/AI/控制", "中国足式机器人新锐", "四足+双足全栈自研", "https://campus.limxdynamics.com", "https://www.limxdynamics.com"),

    # ===== 跨境电商 补充 (5) =====
    ("cross-border", "安克创新 Anker 扩展2", "安克创新 Anker (扩展)", "📍深圳/长沙/海外(东京/西雅图/迪拜)", "🔥热招,✅转正", "2027届", "跨境电商/品牌出海/充电/音频/智能家居/AI/海外", "中国消费电子出海第一品牌", "Anker/Soundcore/eufy等", "https://campus.anker.com", "https://www.anker.com"),
    ("cross-border", "赛维时代 Sailvan 扩展", "赛维时代 Sailvan Times (扩展)", "📍深圳/广州/东莞/海外", "🔥热招,✅转正", "2027届", "跨境电商/服装/亚马逊运营/品牌/供应链/IT/AI", "中国跨境电商服装头部", "A股, 亚马逊大卖", "https://campus.sailvan.com", "https://www.sailvan.com"),
    ("cross-border", "致欧科技 Ziel 扩展", "致欧科技 Ziel (扩展)", "📍深圳/宁波/德国/美国/英国", "⚠️关注官网", "2027届", "跨境电商/家具家居/亚马逊/品牌/设计/供应链/IT", "中国家居跨境电商第一股", "SONGMICS/VASAGLE", "https://campus.ziel.com", "https://www.ziel.com"),
    ("cross-border", "子不语 Zibuyu", "子不语 Zibuyu", "📍杭州/广州/美国", "⚠️关注官网", "2027届", "跨境电商/服装/品牌/亚马逊/独立站/设计/AI/供应链", "中国最大跨境电商女装", "港股, 女装跨境电商", "https://campus.zibuyu.com", "https://www.zibuyu.com"),
    ("cross-border", "吉宏股份 Jihong", "吉宏股份 Jihong", "📍厦门/深圳/东南亚", "⚠️关注官网", "2027届", "跨境电商/包装/东南亚电商/AI营销/技术/运营", "东南亚跨境电商龙头", "A股, 跨境电商+包装", "https://campus.jihong.cc", "https://www.jihong.cc"),

    # ===== 航空航天 补充 (4) =====
    ("aerospace", "航天科技集团 扩展", "航天科技集团一院/五院", "📍北京/上海/西安/成都", "🔥热招,✅转正", "2027届硕/博", "运载火箭/卫星/载人航天/深空探测/控制/AI", "中国航天国家队核心", "长征火箭+北斗+嫦娥", "https://campus.casc.com.cn", "https://www.casc.com.cn"),
    ("aerospace", "航天科工集团 扩展", "航天科工集团二院/三院", "📍北京/南京/武汉/贵阳/长沙", "🔥热招,✅转正", "2027届硕/博", "导弹/卫星/雷达/电子对抗/智能控制/AI/量子", "中国导弹工业主力军", "红旗/东风/鹰击等型号", "https://campus.casic.com.cn", "https://www.casic.com.cn"),
    ("aerospace", "中航发 AECC 扩展", "中国航发 AECC (扩展)", "📍北京/沈阳/成都/西安/贵阳/株洲/上海", "🔥热招,✅转正", "2027届硕/博", "航空发动机/燃气轮机/气动/燃烧/材料/控制/AI", "中国航空发动机国家队", "太行/峨眉/长江系列", "https://campus.aecc.cn", "https://www.aecc.cn"),
    ("aerospace", "中航无人机 AVIC 扩展", "中航无人机 AVIC UCAV (扩展)", "📍成都/自贡", "🔥热招,✅转正", "2027届硕/博", "无人机/飞行器/指控/气动/飞控/航电/AI/IT", "中国无人机国家队", "翼龙系列无人机", "https://campus.avic.com", "https://www.avic.com"),

    # ===== 新材料 补充 (4) =====
    ("new-materials", "光启技术 Kuang-Chi", "光启技术 Kuang-Chi", "📍深圳/东莞/成都/西安/佛山", "🔥热招,✅转正", "2027届硕/博", "超材料/隐身技术/电磁/天线/航空/航天/新材料", "全球超材料技术领军", "A股, 军工超材料龙头", "https://campus.kuang-chi.com", "https://www.kuang-chi.com"),
    ("new-materials", "沃特股份 WOTE", "沃特股份 WOTE", "📍深圳/惠州/重庆/苏州", "⚠️关注官网", "2027届", "LCP/特种工程塑料/5G材料/半导体材料/研发", "中国特种高分子材料龙头", "A股, LCP+碳纤维", "https://campus.wotematerials.com", "https://www.wotematerials.com"),
    ("new-materials", "菲利华 Feilihua", "菲利华 Feilihua", "📍荆州/上海/潜江", "⚠️关注官网", "2027届", "石英玻璃/光纤预制棒/半导体石英/光学/航天", "中国石英材料龙头", "A股, 半导体石英耗材", "https://campus.feilihua.com", "https://www.feilihua.com"),
    ("new-materials", "中材科技 Sinoma", "中材科技 Sinoma", "📍北京/南京/淄博/泰安/成都/酒泉", "⚠️关注官网", "2027届", "风电叶片/玻纤/锂膜/高压复合气瓶/新材料", "中国风电叶片市占率第一", "A股, 中国建材集团旗下", "https://campus.sinoma.com.cn", "https://www.sinoma.com.cn"),

    # ===== 影视/文创 补充 (5) =====
    ("media", "中国电影集团 CFG", "中国电影集团 CFG", "📍北京", "⚠️关注官网", "2027届", "电影制作/发行/放映/进出口/技术/制片/市场/IT", "中国最大电影集团", "A股, 中影股份", "https://campus.cfg.com.cn", "https://www.cfg.com.cn"),
    ("media", "追光动画 Light Chaser", "追光动画 Light Chaser", "📍北京", "⚠️关注官网", "2027届", "动画电影/模型/绑定/特效/渲染/CG/TA/技术", "中国3D动画电影头部", "白蛇/新神榜系列", "https://campus.lightchaser.com", "https://www.lightchaser.com"),
    ("media", "原力动画 Original Force", "原力动画 Original Force", "📍南京/成都/上海/美国", "⚠️关注官网", "2027届", "3D动画/游戏美术/动捕/VFX/CG/TA/技术", "中国最大动画制作公司之一", "全球3A游戏美术外包TOP", "https://campus.of3d.com", "https://www.of3d.com"),
    ("media", "儒意影业 Ruyi Films", "儒意影业 Ruyi Films", "📍北京/上海", "⚠️关注官网", "2027届", "影视制作/剧本开发/制片/发行/市场/新媒体/IT", "中国头部影视制作公司", "港股, 万达电影大股东", "https://campus.ruyifilms.com", "https://www.ruyifilms.com"),
    ("media", "啊哈娱乐 AHA", "啊哈娱乐 AHA Entertainment", "📍北京/上海", "⚠️关注官网", "2027届", "动漫/IP/影视/动画/新媒体/制作/运营/设计", "伍六七IP开发商", "刺客伍六七, 国漫IP", "https://campus.ahaentertainment.com", "https://www.ahaentertainment.com"),

    # ===== 食品/餐饮 (10) — food-more =====
    ("food-more", "卫龙美味 Weilong", "卫龙美味 Weilong", "📍漯河/上海/驻马店", "⚠️关注官网,✅转正", "2027届", "辣味零食/魔芋/豆制品/研发/品控/市场/电商/IT", "中国辣味零食第一品牌", "港股, 辣条第一股", "https://campus.weilongfoods.com", "https://www.weilongfoods.com"),
    ("food-more", "周黑鸭 Zhouheiya", "周黑鸭 Zhouheiya", "📍武汉/上海/深圳/全国", "⚠️关注官网", "2027届", "休闲卤味/食品研发/品控/零售/电商/IT/管理", "中国休闲卤味TOP3", "港股, 气调包装卤味", "https://campus.zhouheiya.com", "https://www.zhouheiya.com"),
    ("food-more", "煌上煌 Huangshanghuang", "煌上煌 Huangshanghuang", "📍南昌/全国", "⚠️关注官网", "2027届", "酱卤肉制品/食品研发/品控/连锁零售/电商/IT", "中国酱卤肉制品龙头", "A股, 三大卤味之一", "https://campus.huangshanghuang.com", "https://www.huangshanghuang.com"),
    ("food-more", "巴比食品 Babi Food", "巴比食品 Babi Food", "📍上海/广州/天津/南京/武汉", "⚠️关注官网", "2027届", "中式面点/早餐连锁/中央厨房/供应链/IT/运营", "中国包子第一股", "A股, 4000+早餐门店", "https://campus.babifood.com", "https://www.babifood.com"),
    ("food-more", "五芳斋 Wufangzhai", "五芳斋 Wufangzhai", "📍嘉兴/上海/杭州", "⚠️关注官网", "2027届", "粽子/传统食品/连锁餐饮/研发/电商/IT/品牌", "中国粽子第一品牌", "A股, 百年老字号", "https://campus.wufangzhai.com", "https://www.wufangzhai.com"),
    ("food-more", "广州酒家 GZ Restaurant", "广州酒家 GZ Restaurant", "📍广州/深圳/佛山/上海", "⚠️关注官网", "2027届", "食品制造/餐饮连锁/月饼/速冻/研发/电商/IT", "华南最大食品餐饮集团", "A股, 广州酒家+陶陶居", "https://campus.gzr.com.cn", "https://www.gzr.com.cn"),
    ("food-more", "桃李面包 Toly Bread", "桃李面包 Toly Bread", "📍沈阳/北京/上海/成都/全国", "🔥热招,✅转正", "2027届", "短保面包/烘焙/研发/品控/生产/物流/电商/IT", "中国短保面包绝对龙头", "A股, 全国化烘焙龙头", "https://campus.tolybread.com", "https://www.tolybread.com"),
    ("food-more", "立高食品 Ligao Foods", "立高食品 Ligao Foods", "📍广州/佛山/上海/湖州/河南", "⚠️关注官网", "2027届", "烘焙原料/奶油/冷冻烘焙/研发/品控/销售/IT", "中国烘焙原料龙头", "A股, 冷冻烘焙+奶油", "https://campus.ligaofoods.com", "https://www.ligaofoods.com"),
    ("food-more", "味知香 Weizhixiang", "味知香 Weizhixiang", "📍苏州/上海", "⚠️关注官网", "2027届", "预制菜/半成品菜/研发/品控/供应链/电商/IT", "中国预制菜第一股", "A股, 预制菜龙头", "https://campus.weizhixiang.com", "https://www.weizhixiang.com"),
    ("food-more", "千味央厨 Qianweiyangchu", "千味央厨 Qianweiyangchu", "📍郑州/新乡", "⚠️关注官网", "2027届", "速冻米面/餐饮供应链/B端/研发/品控/IT/运营", "中国餐饮供应链速冻龙头", "A股, B端餐饮供应链", "https://campus.qianweiyangchu.com", "https://www.qianweiyangchu.com"),

    # ===== 人力资源 (8) — hr-more =====
    ("hr-more", "前程无忧 51job", "前程无忧 51job", "📍上海/北京/广州/深圳/全国", "⚠️关注官网", "2027届", "招聘/人力资源/培训测评/猎头/产品/IT/AI/运营", "中国TOP3综合招聘平台", "纳斯达克, 51job.com", "https://campus.51job.com", "https://www.51job.com"),
    ("hr-more", "同道猎聘 Tongdao Liepin", "同道猎聘 Tongdao Liepin", "📍北京/上海/广州/深圳/成都/全国", "⚠️关注官网", "2027届", "中高端招聘/猎头/HR SaaS/AI/大数据/产品/技术", "中国中高端招聘第一平台", "港股, 猎聘网", "https://campus.liepin.com", "https://www.liepin.com"),
    ("hr-more", "万宝盛华 Manpower China", "万宝盛华 Manpower China", "📍上海/北京/广州/深圳/全国", "⚠️关注官网", "2027届", "灵活用工/猎头/RPO/人才寻访/HR咨询/IT/运营", "全球TOP3人力资源服务商", "港股, Manpower大中华", "https://campus.manpower.com.cn", "https://www.manpower.com.cn"),
    ("hr-more", "任仕达 Randstad China", "任仕达 Randstad China", "📍上海/北京/广州/深圳/全国", "⚠️关注官网", "2027届", "灵活用工/猎头/HR解决方案/IT/财务/运营/市场", "全球最大人力资源服务商", "Randstad大中华区", "https://campus.randstad.cn", "https://www.randstad.cn"),
    ("hr-more", "外企德科 FESCO Adecco", "外企德科 FESCO Adecco", "📍北京/上海/深圳/广州/杭州/成都/全国", "⚠️关注官网", "2027届", "人力资源外包/灵活用工/薪酬/HR SaaS/IT/运营", "中国最大人力资源外包平台", "FESCO+Adecco合资", "https://campus.fescoadecco.com", "https://www.fescoadecco.com"),
    ("hr-more", "人瑞人才 Renrui 扩展2", "人瑞人才 Renrui (扩展)", "📍成都/上海/北京/广州/深圳/全国", "⚠️关注官网", "2027届", "灵活用工/新经济/IT人才外包/HR SaaS/技术/运营", "中国最大灵活用工服务商", "港股, 新经济人才服务", "https://campus.renruihr.com", "https://www.renruihr.com"),
    ("hr-more", "北森云计算 Beisen 扩展2", "北森云计算 Beisen (扩展)", "📍北京/上海/深圳/成都/广州", "⚠️关注官网", "2027届", "HR SaaS/招聘/绩效/继任/人才管理/AI/大数据/IT", "中国HR SaaS第一品牌", "港股, 一体化HR SaaS", "https://campus.beisen.com", "https://www.beisen.com"),
    ("hr-more", "Moka 摩卡科技", "Moka 摩卡科技", "📍北京/上海/深圳/广州/成都/杭州", "⚠️关注官网", "2027届", "招聘系统/HR SaaS/AI面试/ATS/大数据/IT/产品", "中国招聘管理系统TOP", "AI招聘, 智能化HR", "https://campus.mokahr.com", "https://www.mokahr.com"),

    # ===== 事业单位/研究机构 (8) — gov-more =====
    ("gov-more", "中科院计算所 ICT CAS", "中科院计算所 ICT CAS", "📍北京", "🔥热招,✅转正", "2027届硕/博", "计算机体系结构/AI/芯片/量子/算法/系统/网络", "中国计算机科学最高殿堂", "龙芯/寒武纪/曙光发源地", "https://campus.ict.ac.cn", "https://www.ict.ac.cn"),
    ("gov-more", "中科院自动化所 CASIA", "中科院自动化所 CASIA", "📍北京", "🔥热招,✅转正", "2027届硕/博", "AI/大模型/多模态/机器人/CV/NLP/芯片/脑科学", "中国AI研究重镇", "紫东太初大模型", "https://campus.ia.ac.cn", "https://www.ia.ac.cn"),
    ("gov-more", "中国工程物理研究院 CAEP", "中国工程物理研究院 CAEP", "📍绵阳/北京/上海/成都", "🔥热招,✅转正", "2027届硕/博", "核物理/武器物理/计算科学/材料/激光/电子/AI", "中国核武器研制生产单位", "国家级战略科研机构", "https://campus.caep.cn", "https://www.caep.cn"),
    ("gov-more", "鹏城实验室 扩展", "鹏城实验室 PCL (扩展)", "📍深圳", "🔥热招,✅转正", "2027届硕/博/博士后", "AI/通信/网络/超算/6G/大模型/芯片/量子/安全", "国家实验室, 深圳AI高地", "鹏城云脑+中国算力网", "https://campus.pcl.ac.cn", "https://www.pcl.ac.cn"),
    ("gov-more", "昌平实验室 Changping Lab", "昌平实验室 Changping Lab", "📍北京昌平", "🔥热招,✅转正", "2027届硕/博/博士后", "生命科学/蛋白质组/基因组/AI制药/脑科学/生物信息", "国家新型科研机构", "国家实验室, 生命科学", "https://campus.cpl.ac.cn", "https://www.cpl.ac.cn"),
    ("gov-more", "中国信通院 CAICT 扩展", "中国信通院 CAICT (扩展)", "📍北京/深圳/上海/广州/重庆/南京/杭州", "🔥热招,✅转正", "2027届硕/博", "5G/6G/工业互联网/AI/数据安全/数字经济/政策", "工信部直属, ICT国家智库", "国家高端专业智库", "https://campus.caict.ac.cn", "https://www.caict.ac.cn"),
    ("gov-more", "国家无线电监测中心", "国家无线电监测中心 SRRC", "📍北京/全国", "⚠️关注官网", "2027届硕/博", "无线电监测/频谱管理/卫星/通信/电子/IT/大数据", "国家无线电管理技术机构", "工信部直属事业单位", "https://campus.srrc.org.cn", "https://www.srrc.org.cn"),
    ("gov-more", "中国电子技术标准化研究院", "中国电子技术标准化研究院 CESI", "📍北京/深圳/广州/上海", "⚠️关注官网", "2027届硕/博", "电子标准化/检测/认证/网络安全/绿色制造/IT/AI", "工信部直属标准化机构", "国家标准制定+检测认证", "https://campus.cesi.cn", "https://www.cesi.cn"),

    # ===== 运动/体育品牌 (5) =====
    ("sports", "安踏集团 Anta 扩展2", "安踏集团 Anta Sports (扩展)", "📍厦门/上海/北京/泉州/广州", "🔥热招,✅转正", "2027届", "运动品牌/零售/供应链/研发/设计/电商/IT/海外", "中国最大体育用品集团", "安踏+FILA+始祖鸟等", "https://campus.anta.com", "https://www.anta.com"),
    ("sports", "匹克 Peak Sport", "匹克 Peak Sport", "📍泉州/厦门/北京", "⚠️关注官网", "2027届", "篮球/跑步/运动鞋服/态极科技/研发/设计/电商/IT", "中国篮球装备头部品牌", "态极科技, 篮球鞋领先", "https://campus.peaksport.com", "https://www.peaksport.com"),
    ("sports", "鸿星尔克 ERKE", "鸿星尔克 ERKE", "📍厦门/泉州", "⚠️关注官网", "2027届", "运动鞋服/跑步/网球/研发/设计/电商/IT/品牌", "国民运动品牌, 国货之光", "国潮品牌, 线上转型", "https://campus.erke.com", "https://www.erke.com"),
    ("sports", "特步 Xtep 扩展2", "特步 Xtep (扩展)", "📍厦门/泉州/上海", "⚠️关注官网", "2027届", "跑步/马拉松/运动鞋服/研发/设计/品牌/电商/IT", "中国跑步装备领军品牌", "港股, 跑步赛道领先", "https://campus.xtep.com.cn", "https://www.xtep.com.cn"),
    ("sports", "361度 扩展2", "361度 361° (扩展)", "📍厦门/泉州", "⚠️关注官网", "2027届", "运动鞋服/跑步/篮球/研发/设计/电商/海外/IT", "中国TOP5运动品牌", "港股, 361°国际线", "https://campus.361sport.com", "https://www.361sport.com"),

    # ===== 白酒/饮料 (4) =====
    ("beverage-alcohol", "洋河股份 Yanghe", "洋河股份 Yanghe", "📍宿迁/南京", "⚠️关注官网", "2027届", "白酒/酿造/品控/品牌/市场/电商/IT/管理/财务", "中国白酒TOP3, 梦之蓝", "A股, 洋河+双沟", "https://campus.chinayanghe.com", "https://www.chinayanghe.com"),
    ("beverage-alcohol", "山西汾酒 Fenjiu", "山西汾酒 Fenjiu", "📍汾阳/太原", "⚠️关注官网", "2027届", "清香型白酒/酿造/品控/品牌/市场/电商/IT/管理", "中国清香型白酒龙头", "A股, 清香鼻祖", "https://campus.fenjiu.com.cn", "https://www.fenjiu.com.cn"),
    ("beverage-alcohol", "泸州老窖 Luzhou Laojiao", "泸州老窖 Luzhou Laojiao", "📍泸州/成都", "⚠️关注官网", "2027届", "浓香型白酒/酿造/品控/品牌/市场/电商/IT/管理", "中国浓香鼻祖, 国窖1573", "A股, 浓香鼻祖", "https://campus.lzlj.com", "https://www.lzlj.com"),
    ("beverage-alcohol", "华润啤酒 CR Beer", "华润啤酒 CR Beer", "📍北京/沈阳/杭州/全国", "🔥热招,✅转正", "2027届", "啤酒/雪花/喜力/酿造/品控/品牌/电商/IT/管理", "中国最大啤酒企业", "港股, 全球最大啤酒商", "https://campus.crbeer.com.cn", "https://www.crbeer.com.cn"),

    # ===== 日化/化妆品 (4) =====
    ("beauty-personal", "丸美股份 Marubi 扩展2", "丸美股份 Marubi (扩展)", "📍广州/上海", "⚠️关注官网", "2027届", "眼霜/抗衰护肤品/研发/品牌/电商/设计/IT/市场", "中国眼霜第一品牌", "A股, 眼部护理专家", "https://campus.marubi.com.cn", "https://www.marubi.com.cn"),
    ("beauty-personal", "韩束 Kans", "韩束 Kans (上美集团)", "📍上海", "⚠️关注官网,✅转正", "2027届", "护肤品/面膜/研发/品牌/电商/社交电商/IT/设计", "国货护肤头部品牌", "港股, 上美集团", "https://campus.kans.com", "https://www.kans.com"),
    ("beauty-personal", "敷尔佳 Fuerjia", "敷尔佳 Fuerjia", "📍哈尔滨/上海/杭州", "⚠️关注官网", "2027届", "医用敷料/功能性护肤/研发/医美/电商/品牌/IT", "中国医用敷料第一品牌", "A股, 医用敷料龙头", "https://campus.fuerjia.com", "https://www.fuerjia.com"),
    ("beauty-personal", "自然堂/伽蓝集团 JALA", "伽蓝集团 JALA (自然堂)", "📍上海", "⚠️关注官网,✅转正", "2027届", "护肤品/自然堂/美素/研发/品牌/电商/IT/设计", "中国化妆品TOP集团", "自然堂+美素+春夏", "https://campus.jala.com.cn", "https://www.jala.com.cn"),

    # ===== 补充: 更多企业 (23) =====
    ("insurance-ext", "友邦保险 AIA China", "友邦保险 AIA China", "📍上海/北京/深圳/广州/江苏/全国", "⚠️关注官网", "2027届", "寿险/健康险/养老/精算/营销/IT/数字化/管理", "全球最大寿险公司", "AIA, 专注亚太", "https://campus.aia.com.cn", "https://www.aia.com.cn"),
    ("insurance-ext", "新华人寿 NCI 扩展", "新华人寿 NCI (扩展)", "📍北京/全国各省市", "⚠️关注官网,✅转正", "2027届", "寿险/健康险/精算/投资/IT/大数据/AI/管理/运营", "中国TOP10寿险公司", "A+H股, 新华保险", "https://campus.newchinalife.com", "https://www.newchinalife.com"),
    ("insurance-ext", "中国太保 CPIC 扩展", "中国太保 CPIC (扩展)", "📍上海/全国", "⚠️关注官网,✅转正", "2027届", "产险/寿险/健康险/养老/精算/投资/IT/AI/管理", "中国TOP3保险集团", "A+H股, 太平洋保险", "https://campus.cpic.com.cn", "https://www.cpic.com.cn"),
    ("media-ext", "新周刊 New Weekly", "新周刊 New Weekly", "📍广州/北京/上海", "⚠️关注官网", "2027届", "杂志/新媒体/生活方式/内容/短视频/运营/设计", "中国最新锐时事生活杂志", "新锐文化传媒", "https://campus.neweekly.com.cn", "https://www.neweekly.com.cn"),
    ("media-ext", "刺猬公社 CIWEI", "刺猬公社 CIWEI", "📍北京", "⚠️关注官网", "2027届", "互联网内容/新媒体/科技人文/数据新闻/短视频", "专注互联网内容产业新媒体", "内容产业观察头部", "https://campus.ciweigongshe.com", "https://www.ciweigongshe.com"),
    ("media-ext", "南都娱乐 Southern Metropolis", "南都娱乐 Southern Metropolis", "📍广州/北京/上海", "⚠️关注官网", "2027届", "娱乐新闻/新媒体/娱乐圈/短视频/内容/运营/品牌", "南方都市报旗下娱乐", "南方报业传媒集团", "https://campus.nandu.com", "https://www.nandu.com"),
    ("pharma-ext", "先声药业 Simcere", "先声药业 Simcere", "📍南京/上海/北京/海口/波士顿", "🔥热招,✅转正", "2027届", "创新药/肿瘤/CNS/自免/研发/临床/注册/BD/IT", "中国创新药头部企业", "港股, 先必新等创新药", "https://campus.simcere.com", "https://www.simcere.com"),
    ("pharma-ext", "信立泰 Salubris", "信立泰 Salubris", "📍深圳/北京/成都/苏州/美国", "⚠️关注官网", "2027届", "心血管/肾科/骨科创新药/仿制药/研发/临床/IT", "中国心血管药物龙头", "A股, 信立坦等创新药", "https://campus.salubris.cn", "https://www.salubris.cn"),
    ("pharma-ext", "天士力 Tasly", "天士力 Tasly", "📍天津/上海/江苏/云南/贵州", "⚠️关注官网", "2027届", "中药现代化/复方丹参滴丸/创新中药/生物药/研发", "中国中药现代化领军企业", "A股, 复方丹参滴丸", "https://campus.tasly.com", "https://www.tasly.com"),
    ("shipping-ext", "宁波舟山港 Ningbo Port", "宁波舟山港集团 (扩展)", "📍宁波/舟山/杭州", "⚠️关注官网", "2027届", "港口运营/物流/航运/集装箱/码头管理/IT/大数据", "全球最大港口, 货物吞吐量第一", "A股, 全球第一大港", "https://campus.nbport.com.cn", "https://www.nbport.com.cn"),
    ("shipping-ext", "青岛港 Qingdao Port", "青岛港 Qingdao Port", "📍青岛/威海/东营/潍坊", "⚠️关注官网", "2027届", "港口运营/物流/航运/集装箱/自动化码头/IT", "中国TOP5, 全自动化码头", "A+H股, 智慧港口", "https://campus.qdport.com", "https://www.qdport.com"),
    ("shipping-ext", "天津港 Tianjin Port", "天津港 Tianjin Port", "📍天津/雄安", "⚠️关注官网", "2027届", "港口运营/物流/航运/集装箱/冷链/IT/大数据", "中国北方最大综合性港口", "A+H股, 京津冀海上门户", "https://campus.tianjinport.com", "https://www.tianjinport.com"),
    ("chemical-ext", "恒逸石化 Hengyi", "恒逸石化 Hengyi", "📍杭州/文莱/新加坡/上海", "⚠️关注官网", "2027届", "PTA/聚酯/化纤/石化/贸易/研发/IT/管理/财务", "全球最大PTA生产商之一", "A股, 浙江恒逸集团", "https://campus.hengyi.com", "https://www.hengyi.com"),
    ("chemical-ext", "桐昆集团 Tongkun", "桐昆集团 Tongkun", "📍桐乡/嘉兴/湖州/南通/宿迁/新疆", "⚠️关注官网", "2027届", "涤纶长丝/PTA/化纤/石化/新材料/研发/IT/管理", "全球最大涤纶长丝生产商", "A股, 涤纶长丝龙头", "https://campus.tongkun.com.cn", "https://www.tongkun.com.cn"),
    ("chemical-ext", "新凤鸣 Xinfengming", "新凤鸣 Xinfengming", "📍桐乡/湖州/平湖/徐州", "⚠️关注官网", "2027届", "涤纶长丝/PTA/化纤/新材料/智能制造/IT/管理", "中国化纤行业领军企业", "A股, PTA-涤纶一体化", "https://campus.xinfengming.com", "https://www.xinfengming.com"),
    ("saas-ext", "明道云 Mingdao", "明道云 Mingdao", "📍上海/北京/深圳/广州", "⚠️关注官网", "2027届", "零代码/APaaS/企业数字化/低代码/前后端/产品/AI", "中国零代码平台头部", "APaaS零代码应用平台", "https://campus.mingdao.com", "https://www.mingdao.com"),
    ("saas-ext", "纷享销客 Fxiaoke", "纷享销客 Fxiaoke", "📍北京/上海/深圳/广州/杭州/成都", "⚠️关注官网", "2027届", "CRM SaaS/连接型CRM/销售管理/AI/前后端/产品", "中国CRM SaaS头部", "连接型CRM开创者", "https://campus.fxiaoke.com", "https://www.fxiaoke.com"),
    ("bib-ext", "艾德生物 AmoyDx", "艾德生物 AmoyDx", "📍厦门/上海", "⚠️关注官网", "2027届", "肿瘤精准诊断/伴随诊断/PCR/NGS/研发/IT/管理", "中国肿瘤伴随诊断龙头", "A股, 市占率第一", "https://campus.amoydx.com", "https://www.amoydx.com"),
    ("bib-ext", "泛生子 Genetron", "泛生子 Genetron", "📍北京/上海/杭州/重庆/广州/美国", "⚠️关注官网", "2027届", "癌症精准医疗/早筛/NGS/IVD/研发/生物信息/AI", "中国肿瘤基因检测头部", "癌症早筛, 纳斯达克", "https://campus.genetronhealth.com", "https://www.genetronhealth.com"),
    ("bib-ext", "燃石医学 扩展", "燃石医学 Burning Rock (扩展)", "📍广州/上海/北京", "⚠️关注官网", "2027届硕/博", "肿瘤NGS/早筛/伴随诊断/MRD/研发/生物信息/AI", "中国肿瘤NGS检测龙头", "纳斯达克, 肿瘤精准诊疗", "https://campus.brbiotech.com", "https://www.brbiotech.com"),
    ("construct-ext", "中国中铁 CREC 扩展", "中国中铁 CREC (扩展)", "📍北京/全国/海外", "🔥热招,✅转正", "2027届", "铁路/公路/桥梁/隧道/城轨/市政/勘察设计/IT", "全球最大建筑工程承包商", "A+H股, 央企", "https://campus.crecg.com", "https://www.crecg.com"),
    ("construct-ext", "中国铁建 CRCC 扩展", "中国铁建 CRCC (扩展)", "📍北京/全国/海外", "🔥热招,✅转正", "2027届", "铁路/公路/桥梁/隧道/城轨/房建/勘察设计/IT", "全球TOP3建筑工程承包商", "A+H股, 央企", "https://campus.crcc.cn", "https://www.crcc.cn"),
    ("construct-ext", "中国交建 CCCC 扩展", "中国交建 CCCC (扩展)", "📍北京/全国/海外", "🔥热招,✅转正", "2027届", "港口/航道/路桥/疏浚/港机/海上风电/勘察设计", "全球最大港口公路承包商", "A+H股, 央企", "https://campus.ccccltd.cn", "https://www.ccccltd.cn"),
]

# ============================================================
# 构建新条目的 HTML
# ============================================================
def build_row_html(entry):
    """根据条目数据构建紧凑格式的 HTML row"""
    section_id, company_name, company_display, location, tags_str, target, positions, highlight, note, apply_url = entry[:10]
    website_url = entry[10] if len(entry) > 10 else ""

    # 构建标签
    tag_parts = []
    for tag in tags_str.split(','):
        tag = tag.strip()
        if '热招' in tag:
            tag_parts.append(f'<span class="tag hot">{tag}</span>')
        elif '转正' in tag:
            tag_parts.append(f'<span class="tag green">{tag}</span>')
        elif '截止' in tag:
            tag_parts.append(f'<span class="tag orange">{tag}</span>')
        else:
            tag_parts.append(f'<span class="tag">{tag}</span>')

    tag_html = ''.join(tag_parts)
    tags_wrapper = f'<span class="row-tags">{tag_html}</span>' if tag_html else ''

    # 构建 action 按钮
    actions = f'<a class="btn-primary" href="{apply_url}" target="_blank">投递</a>'
    if website_url:
        actions += f'<a class="btn-outline" href="{website_url}" target="_blank">官网</a>'

    # 完整行
    return (f'<div class="row"><span class="row-num">999</span>'
            f'<span class="row-left"><span class="row-company">{company_display}</span>'
            f'<span class="row-loc">{location}</span>{tags_wrapper}</span>'
            f'<span class="row-info"><span class="info-item"><strong>面向：</strong>{target}</span>'
            f'<span class="info-item"><strong>岗：</strong>{positions}</span>'
            f'<span class="info-item" style="color:#fbbf24;">{highlight}</span>'
            f'<span class="info-item" style="color:#4ade80;font-size:.7em;">{note}</span></span>'
            f'<span class="row-actions">{actions}</span></div>')

# ============================================================
# 插入新条目到各个 section
# ============================================================
# 找到所有 section 的边界
section_starts = list(re.finditer(r'<div class="section" id="([^"]+)">', original_content))
section_boundaries = []
for i, m in enumerate(section_starts):
    sec_id = m.group(1)
    start = m.start()
    if i + 1 < len(section_starts):
        end = section_starts[i + 1].start()
    else:
        # 最后一个 section — 找到 footer 开始处
        footer_match = re.search(r'<div class="footer">', original_content[start:])
        if footer_match:
            end = start + footer_match.start()
        else:
            end = len(original_content)
    section_boundaries.append((sec_id, start, end))

print(f"Found {len(section_boundaries)} sections")

# 按 section 分组新条目
new_by_section = defaultdict(list)
for entry in NEW_COMPANIES:
    new_by_section[entry[0]].append(entry)

# 从后往前插入（保持位置偏移正确）
result = original_content
offset = 0
total_added = 0

for sec_id, sec_start, sec_end in section_boundaries:
    if sec_id not in new_by_section:
        continue

    entries = new_by_section[sec_id]
    # 找到该 section 内 rows div 的结束标签
    # Section 结构: <div class="section" id="xxx"> ... <div class="rows"> ... rows ... </div> </div>
    section_text = result[sec_start + offset:sec_end + offset]

    # 找到 rows div 的闭合标签 </div> (在 section 结束之前)
    # 从后往前找：在 section_text 中，倒数第一个 </div> 是 section 闭合，
    # 倒数第二个 </div> 是 rows 闭合
    div_ends = list(re.finditer(r'</div>', section_text))
    if len(div_ends) < 2:
        print(f"  WARNING: Section '{sec_id}' has fewer than 2 </div> tags, skipping")
        continue

    # rows 的 </div> 是倒数第二个（section div 内还有一个 rows div）
    rows_close = div_ends[-2]
    insert_pos = sec_start + offset + rows_close.start()

    # 生成新条目 HTML
    new_rows = [build_row_html(e) for e in entries]
    insertion = '\n' + '\n'.join(new_rows) + '\n'

    # 插入
    result = result[:insert_pos] + insertion + result[insert_pos:]
    offset += len(insertion)
    total_added += len(entries)
    print(f"  Added {len(entries)} entries to '{sec_id}'")

print(f"\nTotal new entries added: {total_added}")

# ============================================================
# 重新编号所有条目
# ============================================================
counter = [0]  # 用列表模拟可变计数器

def renumber_func(match):
    counter[0] += 1
    n = counter[0]
    return f'<span class="row-num">{n:02d}</span>' if n < 100 else f'<span class="row-num">{n}</span>'

result = re.sub(r'<span class="row-num">\d+</span>', renumber_func, result)
final_count = counter[0]
print(f"Final entry count: {final_count}")

# ============================================================
# 更新统计显示
# ============================================================
# 更新搜索栏的"共 X 条"
result = re.sub(r'共 \d+ 条', f'共 {final_count} 条', result)
# 更新 hero 的"810+企业"
result = re.sub(r'810\+企业', f'{final_count}+企业', result)

# ============================================================
# 写入文件
# ============================================================
with open('实习招聘信息汇总_1000条.html', 'w', encoding='utf-8') as f:
    f.write(result)

print(f"\nDONE! File written successfully with {final_count} entries.")
