#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Extract all story nodes + endings + routing from index.html into a readable txt.
"""
import re
import sys

with open('E:/smallgame/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Extract script block
script = re.search(r'<script>([\s\S]*?)</script>', content).group(1)

# Find STORY block boundaries
story_start = script.find('const STORY = {')
story_end = script.find('};', story_start) + 2
story = script[story_start:story_end]

# Extract nodes block
nodes_match = re.search(r'nodes:\s*\{([\s\S]*?)\n  \},\s*\n\s*endings:', story)
nodes_block = nodes_match.group(1) if nodes_match else ''

# Extract endings block
endings_match = re.search(r'endings:\s*\{([\s\S]*?)\n  \}\s*\n\}', story)
endings_block = endings_match.group(1) if endings_match else ''


def extract_top_level_objects(block):
    """Parse top-level NodeID: { ... } entries by tracking brace depth."""
    objects = []
    i = 0
    while i < len(block):
        # Find next ID: { at line start (4 spaces indent)
        m = re.search(r'\n    (\w+):\s*\{', block[i:])
        if not m:
            break
        id_start = i + m.start() + 1  # skip leading \n
        name = m.group(1)
        brace_start = i + m.end() - 1  # position of {
        # Walk to matching }
        depth = 1
        j = brace_start + 1
        in_str = None  # track ' " ` for strings
        in_template_expr = 0
        in_line_comment = False
        in_block_comment = False
        while j < len(block) and depth > 0:
            c = block[j]
            prev = block[j-1] if j > 0 else ''
            if in_line_comment:
                if c == '\n':
                    in_line_comment = False
            elif in_block_comment:
                if c == '*' and j+1 < len(block) and block[j+1] == '/':
                    in_block_comment = False
                    j += 1
            elif in_str:
                if c == '\\':
                    j += 1  # skip escape
                elif c == in_str:
                    in_str = None
                elif in_str == '`' and c == '$' and j+1 < len(block) and block[j+1] == '{':
                    in_template_expr += 1
                    j += 1
            else:
                if c == '/' and j+1 < len(block) and block[j+1] == '/':
                    in_line_comment = True
                    j += 1
                elif c == '/' and j+1 < len(block) and block[j+1] == '*':
                    in_block_comment = True
                    j += 1
                elif c in ('"', "'", '`'):
                    in_str = c
                elif c == '{':
                    depth += 1
                elif c == '}':
                    depth -= 1
            j += 1
        # j is one past the closing }
        body = block[brace_start:j]
        objects.append((name, body))
        i = j
    return objects


def extract_field(body, field):
    """Extract a top-level field's raw value."""
    # field: value pattern at depth 1
    # Use brace-tracking starting after `field:`
    pattern = re.compile(rf'\n      {re.escape(field)}:\s*')
    m = pattern.search(body)
    if not m:
        return None
    start = m.end()
    # Determine value type
    rest = body[start:]
    if rest.startswith('`'):
        # template literal
        end = 1
        while end < len(rest):
            if rest[end] == '\\':
                end += 2
                continue
            if rest[end] == '`':
                return rest[1:end]
            end += 1
        return rest[1:]
    elif rest.startswith('"'):
        end = 1
        while end < len(rest):
            if rest[end] == '\\':
                end += 2
                continue
            if rest[end] == '"':
                return rest[1:end]
            end += 1
        return rest[1:]
    elif rest.startswith('{'):
        depth = 1
        j = 1
        in_str = None
        while j < len(rest) and depth > 0:
            c = rest[j]
            if in_str:
                if c == '\\': j += 2; continue
                if c == in_str: in_str = None
            else:
                if c in ('"', "'", '`'): in_str = c
                elif c == '{': depth += 1
                elif c == '}': depth -= 1
            j += 1
        return rest[:j]
    elif rest.startswith('['):
        depth = 1
        j = 1
        in_str = None
        while j < len(rest) and depth > 0:
            c = rest[j]
            if in_str:
                if c == '\\': j += 2; continue
                if c == in_str: in_str = None
            else:
                if c in ('"', "'", '`'): in_str = c
                elif c == '[': depth += 1
                elif c == ']': depth -= 1
            j += 1
        return rest[:j]
    elif rest.startswith('function'):
        # body: function(state) { ... } · 提取函数体为可读片段
        idx = rest.find('{')
        depth = 1
        j = idx + 1
        in_str = None
        while j < len(rest) and depth > 0:
            c = rest[j]
            if in_str:
                if c == '\\': j += 2; continue
                if c == in_str: in_str = None
            else:
                if c in ('"', "'", '`'): in_str = c
                elif c == '{': depth += 1
                elif c == '}': depth -= 1
            j += 1
        # extract all `...` template literals and their conditions
        fn_body = rest[idx:j]
        # find all parts.push(`...`) blocks + their preceding if/else
        templates = re.findall(r'(?:if\s*\([^)]*\)\s*\{|else\s+if\s*\([^)]*\)\s*\{|else\s*\{|return\s*)\s*(?:parts\.push\()?`([^`]*)`', fn_body)
        # find conditions
        condition_template_pairs = []
        # Iterate through fn_body and pair conditions to template literals
        idx2 = 0
        while idx2 < len(fn_body):
            # Find next condition or template
            cond_match = re.search(r'(if|else if)\s*\((s\.[^)]+)\)\s*\{|else\s*\{|return\s', fn_body[idx2:])
            if not cond_match:
                break
            cond = cond_match.group(2) if cond_match.group(2) else cond_match.group(0).strip()
            # Find next ` after this
            tmpl_start = fn_body.find('`', idx2 + cond_match.end())
            if tmpl_start < 0:
                break
            tmpl_end = tmpl_start + 1
            while tmpl_end < len(fn_body):
                if fn_body[tmpl_end] == '\\':
                    tmpl_end += 2; continue
                if fn_body[tmpl_end] == '`':
                    break
                tmpl_end += 1
            template = fn_body[tmpl_start+1:tmpl_end]
            condition_template_pairs.append((cond, template))
            idx2 = tmpl_end + 1
        # format
        out = ['<<这是 body-as-function · 按状态条件分支动态拼接>>']
        if condition_template_pairs:
            for i, (cond, tmpl) in enumerate(condition_template_pairs):
                out.append('')
                out.append(f'━━ 分支 #{i+1}:  if {cond}  ━━')
                out.append(tmpl.replace('\\n', '\n').replace('\\\'', '\'').replace('\\\\', '\\'))
        else:
            # fallback · 直接抽出所有 ` ... ` 模板字符串作为模块
            templates_raw = re.findall(r'`((?:[^`\\]|\\.)*)`', fn_body)
            # 同时找 if 条件
            if_conditions = re.findall(r'if\s*\((s\.[^)]+)\)', fn_body)
            out.append('')
            out.append(f'<<NT1 模块化 7 段拼接 · 按 flag 状态选择展示哪些段>>')
            out.append('')
            for i, tmpl in enumerate(templates_raw):
                cond = if_conditions[i] if i < len(if_conditions) else '(共通模块 · 总是出现)'
                out.append(f'━━ 模块 #{i+1}:  {cond}  ━━')
                out.append(tmpl.replace('\\n', '\n').replace('\\\'', '\'').replace('\\\\', '\\'))
                out.append('')
        return '\n'.join(out)
    else:
        # primitive
        m2 = re.match(r'([^,\n]+)', rest)
        return m2.group(1).strip() if m2 else None


def parse_choices(choices_str):
    """Parse choices array from string `[...]`."""
    if not choices_str:
        return []
    inner = choices_str.strip()
    if inner.startswith('['): inner = inner[1:]
    if inner.endswith(']'): inner = inner[:-1]
    # Split top-level objects
    choices = []
    depth = 0
    cur = ''
    in_str = None
    i = 0
    while i < len(inner):
        c = inner[i]
        if in_str:
            cur += c
            if c == '\\' and i+1 < len(inner):
                cur += inner[i+1]
                i += 2
                continue
            if c == in_str:
                in_str = None
        else:
            if c in ('"', "'", '`'):
                in_str = c
                cur += c
            elif c == '{':
                depth += 1
                cur += c
            elif c == '}':
                depth -= 1
                cur += c
                if depth == 0 and cur.strip().startswith('{'):
                    choices.append(cur.strip())
                    cur = ''
            elif c == ',' and depth == 0:
                cur = ''  # reset between choice objects
            else:
                cur += c
        i += 1
    return choices


def extract_choice_field(choice_str, field):
    """Extract field from a choice object string."""
    # field: value (no nesting beyond simple types)
    m = re.search(rf'\b{re.escape(field)}:\s*', choice_str)
    if not m:
        return None
    start = m.end()
    rest = choice_str[start:]
    if rest.startswith('"'):
        end = 1
        while end < len(rest):
            if rest[end] == '\\': end += 2; continue
            if rest[end] == '"': return rest[1:end]
            end += 1
    elif rest.startswith("'"):
        end = 1
        while end < len(rest):
            if rest[end] == '\\': end += 2; continue
            if rest[end] == "'": return rest[1:end]
            end += 1
    elif rest.startswith('`'):
        end = 1
        while end < len(rest):
            if rest[end] == '\\': end += 2; continue
            if rest[end] == '`': return rest[1:end]
            end += 1
    elif rest.startswith('{'):
        depth = 1
        j = 1
        while j < len(rest) and depth > 0:
            if rest[j] == '{': depth += 1
            elif rest[j] == '}': depth -= 1
            j += 1
        return rest[:j]
    elif rest.startswith('s =>'):
        # condition function
        # take until `,` or `}` at top depth
        depth = 0
        j = 0
        in_str = None
        while j < len(rest):
            c = rest[j]
            if in_str:
                if c == '\\': j += 2; continue
                if c == in_str: in_str = None
            else:
                if c in ('"', "'", '`'): in_str = c
                elif c == '(': depth += 1
                elif c == ')': depth -= 1
                elif depth == 0 and c in (',', '}'):
                    return rest[:j].strip()
            j += 1
        return rest[:j].strip()
    else:
        m2 = re.match(r'([^,}]+)', rest)
        return m2.group(1).strip() if m2 else None


def render_node(name, body):
    out = []
    out.append('═' * 70)
    out.append(f'节点 · {name}')
    out.append('═' * 70)

    chapter = extract_field(body, 'chapter')
    title = extract_field(body, 'title')
    summary = extract_field(body, 'summary')
    weight = extract_field(body, 'weight')

    if chapter: out.append(f'章节: {chapter}')
    if title: out.append(f'标题: {title}')
    if summary: out.append(f'Summary: {summary}')
    if weight: out.append(f'权重: {weight}')
    out.append('')

    # preludes (by previous node + choice)
    preludes = extract_field(body, 'preludes')
    if preludes:
        out.append('【入场 prelude · 按上一节点/选项分支】')
        # Parse each key — 严格匹配:行首 + 缩进 + ASCII key + `:` + 反引号/双引号
        # 避免误判 prelude body 内的中文/英文 + 冒号(如 "微信你:" / "open to dialogue:")
        keys = re.findall(r'(?:^|\n)[\t ]+([A-Za-z_][A-Za-z0-9_]*):\s*[`"]', preludes)
        for k in keys:
            val = extract_choice_field(preludes, k)
            if val:
                out.append(f'  ◆ {k}:')
                for line in val.replace('\\n', '\n').split('\n'):
                    out.append(f'      {line}')
                out.append('')

    # preludesByFlag
    preludes_by_flag = extract_field(body, 'preludesByFlag')
    if preludes_by_flag:
        out.append('【入场 prelude · 按 flag/item 分支(可叠加)】')
        keys = re.findall(r'(?:^|\n)[\t ]+([A-Za-z_][A-Za-z0-9_]*):\s*[`"]', preludes_by_flag)
        for k in keys:
            val = extract_choice_field(preludes_by_flag, k)
            if val:
                out.append(f'  ◆ if has [{k}]:')
                for line in val.replace('\\n', '\n').split('\n'):
                    out.append(f'      {line}')
                out.append('')

    # body
    body_field = extract_field(body, 'body')
    if body_field:
        out.append('【主文 BODY】')
        for line in body_field.replace('\\n', '\n').split('\n'):
            out.append(f'  {line}')
        out.append('')

    # choices
    choices_str = extract_field(body, 'choices')
    if choices_str:
        out.append('【选项】')
        for ch in parse_choices(choices_str):
            key = extract_choice_field(ch, 'key')
            text = extract_choice_field(ch, 'text')
            effects = extract_choice_field(ch, 'effects')
            flag = extract_choice_field(ch, 'flag')
            item = extract_choice_field(ch, 'item')
            nxt = extract_choice_field(ch, 'next')
            cond = extract_choice_field(ch, 'condition')

            out.append(f'  ┃ 选项 {key}:')
            if text:
                txt_clean = text.replace('\\n', '\n      ').replace('\\"', '"')
                out.append(f'      文字: {txt_clean}')
            if effects: out.append(f'      维度: {effects}')
            if flag: out.append(f'      flag: {flag}')
            if item: out.append(f'      item: {item}')
            if cond: out.append(f'      条件: {cond}')
            if nxt: out.append(f'      → 跳转: {nxt}')
            out.append('')

    # totalAccount / label / bossView (for endings)
    total_account = extract_field(body, 'totalAccount')
    label = extract_field(body, 'label')
    if label:
        out.append(f'【label】 {label}')
    if total_account:
        out.append(f'【总账】 {total_account}')
    out.append('')

    return '\n'.join(out)


# Build output
output = []
output.append('=' * 70)
output.append('《运营修罗场》v2.2 + v3 · 全剧情 + 跳转图')
output.append('导出时间: 2026-04-26')
output.append('=' * 70)
output.append('')
output.append('【路径总览 · v3 final · 17 节点 + 5 结局】')
output.append('')
output.append('  N01 (周一09:59 HR邮件+阿布微信)')
output.append('   → N02A (10:05 心理评估问卷)')
output.append('   → N03 (14:00 Aurora 15人名单·缺6人)')
output.append('   → N04B (5点半的办公室·按N03分A/B/C/D不同时间结束)')
output.append('   → NT1A (周二09:30 站会本体·阿布分活·mid-meeting 4选项)         ← v3 拆分')
output.append('   → NT1B (09:42 米拉抱箱走过+Seraphine路过+9:44散会)              ← v3 拆分')
output.append('   → NT2 (10:30 米拉余韵+12封询价邮件)')
output.append('   → NT3 (16:30 客户改brief第2次·三蟹一体 [新增E:AI助手反生成])    ← v3 加 E 选项')
output.append('   → N_TUE_NIGHT (周二23:30 望京回家路·煎饼摊+闹钟·过渡节点)       ← v3 新增')
output.append('   → NW1 (周三11:00 Sam审名单·三炸·Cohort Member邮件)')
output.append('   → NW2 (16:30 OA故障+Gordon反问+Emma 18W突袭)')
output.append('   → N04 (周四09:30 米拉工位真空+客户老板异动)')
output.append('   → N06C (17:00-19:00 KaptainK双重灾难 [新增E:§4.2法务反制])      ← v3 加 E 选项')
output.append('   → N_THU_NIGHT (周四22:00 公司打车回家·Sam第一次直接wechat你)    ← v3 新增')
output.append('   → N07 (周五11:00 凌晨brief+Emma脚本+EOD三件事)')
output.append('   → N08 (15:00 Mirror数据表 [双层叠加:6列科幻+5项mapping])        ← v3 改写')
output.append('   → ENDING_GATE (18:00 EOD)')
output.append('       → 决高·共中·规高·险低 → E_NORMAL · 上岸者')
output.append('       → 决高·共低·险高     → E_BLADE  · 执剑人')
output.append('       → 共高·决中           → E_PLANB  · Plan B 在身')
output.append('       → 默认                  → E_NUMB   · 装糊涂大师')
output.append('       → 觉察道具≥4 (优先)    → E_PM14   · 未命名')
output.append('')
output.append('=' * 70)
output.append('【核心规则】')
output.append('')
output.append('维度: 决/共/规/险 · 累积影响结局判定')
output.append('暗线钥匙: hr_email_screenshot (N01 D 选项 · 截 ^_^ 邮件)')
output.append('暗线池: 10 项觉察道具 · 任意持有 ≥ 4 项触发隐藏结局 E_PM14')
output.append('   1. vivian_quote               (Vivian "都是哄婴儿"金句)')
output.append('   2. vivian_quote_overheard     (NT2 D · 茶水间 Jasper 偷听)')
output.append('   3. bcc_awareness_header       (NW2 D · HR 系统 BCC 头)')
output.append('   4. saw_mirror_auth            (NW1 D · OA 角落 Mirror Auth v14)')
output.append('   5. mila_termination_metadata  (N04 D · 飞书字段编辑者 seraphine)')
output.append('   6. director_endorsement       (N06C D · Vivian 工位主动等)')
output.append('   7. brief_engine_watermark     (N07 D · brief 底 Powered by PM-14)')
output.append('   8. mirror_screenshot          (N08 B · 数据表全表)')
output.append('   9. mila_data_row              (N08 C · Mila 数据行特写)')
output.append('  10. gordon_confront            (N08 D · Gordon "你早点知道也好")')
output.append('')
output.append('反制武器(不计入觉察池 · 但走 ending bias):')
output.append('  · contract_clause_screenshot (N06C E · §4.2 Sole Sourcing 截图)')
output.append('')
output.append('沟通渠道严格分场:')
output.append('  · 内部团队 (阿布/Jasper/Vivian/Gordon/Seraphine/米拉) = 微信')
output.append('  · 客户对接 (Nolan) = 微信项目群 (Sam 不进群 · 通过 Nolan 转)')
output.append('  · 海外 KOL = 邮件 + WhatsApp 单对单')
output.append('  · 飞书表 = agency 内部 + Nolan 协作 (KOL 不在飞书)')
output.append('')
output.append('v3 三大新机制:')
output.append('  · 双过渡节点 = N_TUE_NIGHT / N_THU_NIGHT · 给玩家"下班路上"喘息')
output.append('  · 玩家反制选项 = NT3 E (AI 助手) + N06C E (§4.2 法务) · 爽点+代价+行业讽刺')
output.append('  · PM-14 数据表双层叠加 = 学术黑话表头 + 底部 office 荒诞 mapping')
output.append('')
output.append('=' * 70)
output.append('')
output.append('⚠️ 关于 function body 节点(NT1A / NT1B / N04B / N_TUE_NIGHT)')
output.append('   这些节点的 body 是 JS function · 内部按 state.flags 拼接多个 module。')
output.append('   下方 BODY 段只输出函数源码 · 看到的 if/else 分支是动态条件 ·')
output.append('   实际游戏会按玩家状态选其中一支或拼接多段 ·')
output.append('   完整渲染后的剧情请打开 index.html 浏览器实际跑各 path。')
output.append('')
output.append('=' * 70)
output.append('')
output.append('### 节点详情 ###')
output.append('')

nodes = extract_top_level_objects(nodes_block)
for name, body in nodes:
    output.append(render_node(name, body))

output.append('=' * 70)
output.append('### 结局详情 ###')
output.append('=' * 70)
output.append('')

endings = extract_top_level_objects(endings_block)
for name, body in endings:
    output.append(render_node(name, body))

# Write
with open('E:/smallgame/全剧情_v22.txt', 'w', encoding='utf-8', newline='') as f:
    f.write('\n'.join(output))

print(f'Exported {len(nodes)} nodes + {len(endings)} endings.')
print(f'File: E:/smallgame/全剧情_v22.txt')
print(f'Total bytes: {sum(len(s) for s in output)}')
