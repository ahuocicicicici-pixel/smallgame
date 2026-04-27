"""
v3.1 全路径一致性检查
"""
import re
import sys
import io

# 强制 stdout UTF-8 输出 · 避开 Windows GBK 默认
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

OK = "[OK]"
NG = "[FAIL]"

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. 提取所有节点
nodes_section = re.search(r'nodes:\s*\{(.*?)\n  \},\s*endings:', html, re.DOTALL).group(1)
# 末尾加一个 sentinel 让 lookahead 能匹配最后一个节点
nodes_section_with_sentinel = nodes_section + "\n    __SENTINEL__: {"
node_pat = re.compile(r'^    ([A-Z_0-9]+):\s*\{(.*?)(?=^    [A-Z_0-9]+:\s*\{)', re.MULTILINE | re.DOTALL)

nodes = {}
for m in node_pat.finditer(nodes_section_with_sentinel):
    nid = m.group(1)
    if nid == '__SENTINEL__': continue
    body = m.group(2)

    # choices block (between choices: [ and the matching ])
    cm = re.search(r'choices:\s*\[(.*?)\]\s*\n    \},?\s*$', body, re.DOTALL)
    if not cm:
        cm = re.search(r'choices:\s*\[(.*?)\]', body, re.DOTALL)

    choices = []
    if cm:
        choices_block = cm.group(1)
        depth = 0
        start = 0
        in_str = None
        BS = chr(92)  # backslash
        for i, c in enumerate(choices_block):
            if in_str:
                if c == BS: continue
                if c == in_str: in_str = None
            else:
                if c in '"' + "'" + '`': in_str = c
                elif c == '{':
                    if depth == 0: start = i
                    depth += 1
                elif c == '}':
                    depth -= 1
                    if depth == 0:
                        choice_str = choices_block[start:i+1]
                        ck = re.search(r'key:\s*[\'"]([A-Za-z0-9_]+)[\'"]', choice_str)
                        cn = re.search(r'next:\s*"([A-Z_0-9]+)"', choice_str)
                        cf = re.search(r'flag:\s*"([a-z_0-9]+)"', choice_str)
                        ci = re.search(r'item:\s*"([a-z_0-9]+)"', choice_str)
                        cc = re.search(r'condition:\s*s\s*=>\s*(.+?)(?=\s*\}\s*$)', choice_str, re.DOTALL)
                        choices.append({
                            'key': ck.group(1) if ck else None,
                            'next': cn.group(1) if cn else None,
                            'flag': cf.group(1) if cf else None,
                            'item': ci.group(1) if ci else None,
                            'condition': cc.group(1).strip() if cc else None,
                        })

    prep = re.search(r'preludes:\s*\{(.*?)\n      \}', body, re.DOTALL)
    pkeys = re.findall(r'\n        ([A-Za-z_][A-Za-z0-9_]*):\s*[`"]', prep.group(1)) if prep else []

    pbf = re.search(r'preludesByFlag:\s*\{(.*?)\n      \}', body, re.DOTALL)
    pbfkeys = re.findall(r'\n        ([a-z_][a-z_0-9]*):\s*[`"]', pbf.group(1)) if pbf else []

    nodes[nid] = {
        'choices': choices,
        'prelude_keys': pkeys,
        'preludeByFlag_keys': pbfkeys,
    }

am = re.search(r'const AWARENESS_MARKS = \[(.*?)\];', html, re.DOTALL).group(1)
AWARENESS = re.findall(r'"([a-z_]+)"', am)
wm = re.search(r'const WEAPONS_MARKS = \[(.*?)\];', html, re.DOTALL).group(1)
WEAPONS = re.findall(r'"([a-z_]+)"', wm)
il = re.search(r'const ITEM_LABELS = \{(.*?)\n\};', html, re.DOTALL).group(1)
ITEMS = re.findall(r'\n  ([a-z_][a-z_0-9]*):\s*\{', il)

print("=" * 70)
print("【节点清单 · {} 节点】".format(len(nodes)))
for nid in nodes:
    pr = len(nodes[nid]['prelude_keys'])
    pf = len(nodes[nid]['preludeByFlag_keys'])
    cn = len(nodes[nid]['choices'])
    cks = ','.join(c['key'] or '?' for c in nodes[nid]['choices'])
    print(f"  {nid:18s}: {cn} 选项 [{cks}] · prelude {pr} · byFlag {pf}")

print()
print("=" * 70)
print(f"【AWARENESS_MARKS · {len(AWARENESS)}】", AWARENESS)
print(f"【WEAPONS_MARKS · {len(WEAPONS)}】", WEAPONS)
print(f"【ITEM_LABELS · {len(ITEMS)}】", ITEMS)
print()
print("=" * 70)
print("【一致性检查】")
print()

# 检查 1: AWARENESS 和 WEAPONS 都应该在 ITEM_LABELS
miss = (set(AWARENESS) | set(WEAPONS)) - set(ITEMS)
print("[1] AWARENESS+WEAPONS 都在 ITEM_LABELS:", "OK" if not miss else f"FAIL 缺 {miss}")

# 检查 2: prelude key 一致性 - 上游 choice 的 flag/item 都要在下游 preludeByFlag 或 prelude key 出现?
# 不一定 — preludeByFlag 是可选的(玩家选了某 flag 但下个节点没专属 prelude 也 OK)
# 但 prelude (NT3_A 这种) 必须 match 上游 next + choice key

print()
print("[2] preludes key 与上游 next+choice 匹配:")
issues_2 = []
# 反向索引:谁 next 到我?
incoming = {}  # target_nid -> list of (src_nid, choice_key)
for nid, n in nodes.items():
    for ch in n['choices']:
        if ch['next']:
            incoming.setdefault(ch['next'], []).append((nid, ch['key']))

for nid, n in nodes.items():
    if not n['prelude_keys']:
        continue
    expected_keys = set(f"{src}_{ck}" for src, ck in incoming.get(nid, []))
    actual_keys = set(n['prelude_keys'])
    missing = expected_keys - actual_keys  # 上游有路径但没 prelude
    extra = actual_keys - expected_keys    # prelude 有但没上游路径
    if extra:
        issues_2.append(f"  {nid}: prelude 有但无上游路径 → {extra}")
    # missing 不算 issue(prelude 是可选的)

if issues_2:
    for line in issues_2:
        print(line)
else:
    print("  OK 所有 prelude key 都能匹配到上游 next+choice")

# 检查 3: preludeByFlag key 是否能被某条路径触发
print()
print("[3] preludeByFlag key 至少能被一条路径触发:")
issues_3 = []
all_settable = set()
for nid, n in nodes.items():
    for ch in n['choices']:
        if ch['flag']: all_settable.add(ch['flag'])
        if ch['item']: all_settable.add(ch['item'])
# hr_email_screenshot 在 N01 D 设置 - 已包含
# hot-trigger 三参数语法 {{flag|text|gate}} - flag 通过点击设置
hot_triggers_3arg = re.findall(r'\{\{([a-z_0-9]+)\|', html)
all_settable |= set(hot_triggers_3arg)
# 也可能有 data-unlock 的旧版
hot_triggers_old = re.findall(r'data-unlock="([a-z_0-9]+)"', html)
all_settable |= set(hot_triggers_old)
# 还有 setFlag 之类
for m in re.finditer(r'setFlag\("([a-z_0-9]+)"\)', html):
    all_settable.add(m.group(1))

for nid, n in nodes.items():
    for k in n['preludeByFlag_keys']:
        if k not in all_settable:
            issues_3.append(f"  {nid}: byFlag '{k}' 没有任何 choice/hot-trigger 设置它 — dead code")

if issues_3:
    for line in issues_3:
        print(line)
else:
    print("  OK 所有 preludeByFlag key 至少有一条路径可触发")

# 检查 4: condition 引用的 flag/item 是否都能被设置
print()
print("[4] choice condition 引用的 flag/item:")
issues_4 = []
for nid, n in nodes.items():
    for ch in n['choices']:
        if ch['condition']:
            for m in re.findall(r'flags\.has\("([a-z_0-9]+)"\)', ch['condition']):
                if m not in all_settable:
                    issues_4.append(f"  {nid}.{ch['key']}: condition 引用 flag '{m}' 但无人设置")
            for m in re.findall(r'items\.has\("([a-z_0-9]+)"\)', ch['condition']):
                if m not in all_settable:
                    issues_4.append(f"  {nid}.{ch['key']}: condition 引用 item '{m}' 但无人设置")
            for m in re.findall(r'choices\.([A-Z0-9_]+)', ch['condition']):
                if m not in nodes:
                    issues_4.append(f"  {nid}.{ch['key']}: condition 引用 choices.{m} 但节点不存在")

if issues_4:
    for line in issues_4:
        print(line)
else:
    print("  OK 所有 condition 引用都能设置")

# 检查 5: next 引用都存在
print()
print("[5] next 引用目标都存在:")
issues_5 = []
endings_section = re.search(r'endings:\s*\{(.*?)\n  \}\s*\};', html, re.DOTALL).group(1)
endings = set(re.findall(r'^    (E_[A-Z0-9_]+):\s*\{', endings_section, re.MULTILINE))

for nid, n in nodes.items():
    for ch in n['choices']:
        if ch['next'] and ch['next'] not in nodes and ch['next'] not in endings:
            issues_5.append(f"  {nid}.{ch['key']}: next='{ch['next']}' 不存在")

if issues_5:
    for line in issues_5:
        print(line)
else:
    print("  OK 全部 next 目标存在")

# 检查 6: 反制武器 / awareness item 的 effects 维度合理
print()
print("[6] item 设置点检查(awareness vs weapon vs key):")
for nid, n in nodes.items():
    for ch in n['choices']:
        if ch['item']:
            cat = []
            if ch['item'] in AWARENESS: cat.append("觉察")
            if ch['item'] in WEAPONS: cat.append("反制")
            if ch['item'] == 'hr_email_screenshot': cat.append("钥匙")
            if ch['item'] == 'v2_screenshot': cat.append("早期觉察")
            if not cat: cat = ["孤儿!"]
            print(f"  {nid}.{ch['key']:2s} item={ch['item']:30s} → {'/'.join(cat)}")

print()
print("=" * 70)
print("【路径采样模拟 · 4 条关键路径】")

# 模拟函数
def simulate(start, picks, pre_flags=None):
    state_flags = set(pre_flags or [])
    state_items = set()
    state_choices = {}
    state_visited = []
    cur = start
    log = []
    if state_flags:
        log.append(f"[预设 hot-trigger flags: {sorted(state_flags)}]")

    for step_num in range(50):
        if cur in endings:
            log.append(f"→ 结局 {cur}")
            break
        if cur == 'ENDING_GATE':
            # ENDING_GATE 用 next: function · 静态分析无法跑 · 这里给出维度判定
            stats_decisive = 0  # 简化:从 effects 静态累加比较复杂 · 这里只显示 awareness
            aw = len([x for x in (state_items | state_flags) if x in AWARENESS])
            if aw >= 4:
                log.append("→ ENDING_GATE → E_PM14 (awareness >= 4)")
                cur = 'E_PM14'
            else:
                log.append(f"→ ENDING_GATE → 需要维度判定(awareness={aw}/10)")
                cur = 'E_NORMAL'  # placeholder
            continue
        if cur not in nodes:
            log.append(f"FAIL 卡死:节点 {cur} 不存在")
            break

        node = nodes[cur]

        # 触发 prelude
        if state_visited:
            last = state_visited[-1]
            last_choice = state_choices.get(last)
            key = f"{last}_{last_choice}" if last_choice else None
            if key in node['prelude_keys']:
                log.append(f"  prelude · {key}")

        for k in node['preludeByFlag_keys']:
            if k in state_flags or k in state_items:
                log.append(f"  byFlag · {k}")

        # 找选项
        pick = picks.get(cur, 'A')  # 默认 A
        # 过滤可见选项(condition 满足)
        visible = []
        for ch in node['choices']:
            if ch['condition']:
                # 简化判断:能不能触发
                cond = ch['condition']
                ok = True
                for m in re.findall(r'flags\.has\("([a-z_0-9]+)"\)', cond):
                    if m not in state_flags: ok = False; break
                if ok:
                    for m in re.findall(r'items\.has\("([a-z_0-9]+)"\)', cond):
                        if m not in state_items: ok = False; break
                if ok:
                    for m in re.findall(r'choices\.([A-Z0-9_]+)\s*===\s*"([A-Za-z0-9]+)"', cond):
                        if state_choices.get(m[0]) != m[1]: ok = False; break
                    for m in re.findall(r'choices\.([A-Z0-9_]+)\s*!==\s*"([A-Za-z0-9]+)"', cond):
                        if state_choices.get(m[0]) == m[1]: ok = False; break
                if not ok:
                    continue
            visible.append(ch)

        chosen = None
        for ch in visible:
            if ch['key'] == pick:
                chosen = ch
                break
        if not chosen and visible:
            chosen = visible[0]
        if not chosen:
            log.append(f"FAIL 卡死:{cur} 无可选项(picks 给的 {pick} 也没条件)")
            break

        log.append(f"{cur} {chosen['key']} → {chosen['next']}" +
                   (f" [+flag {chosen['flag']}]" if chosen['flag'] else "") +
                   (f" [+item {chosen['item']}]" if chosen['item'] else ""))

        if chosen['flag']: state_flags.add(chosen['flag'])
        if chosen['item']: state_items.add(chosen['item'])
        state_choices[cur] = chosen['key']
        state_visited.append(cur)
        cur = chosen['next']

    aw_count = len([x for x in (state_items | state_flags) if x in AWARENESS])
    wp_count = len([x for x in (state_items | state_flags) if x in WEAPONS])
    return log, aw_count, wp_count, state_flags, state_items

# hot-trigger flag set:全开 = 模拟"点过所有 ^_^ / PM-14 / 老板黑话 / Gordon 等暗线钩子的玩家"
HOT_ALL = {'unlock_n01', 'unlock_n03', 'unlock_nt3', 'unlock_nw2'}

paths = [
    ("全 A 盲玩家(无 hot-trigger)", {}, set()),
    ("全 D awareness 玩家(点过所有 ^_^)", {nid: 'D' for nid in nodes}, HOT_ALL),
    ("反制路径 NT3E + N06CE(无 hot-trigger 也能反制)", {'NT3': 'E', 'N06C': 'E'}, set()),
    ("反制 + awareness 混合(高决断 + 高觉察 · N01 必选 D 拿钥匙)", {'N01': 'D', 'N02A': 'D', 'NT2': 'D', 'NT3': 'E', 'N06C': 'E', 'NW1': 'D', 'NW2': 'D', 'N04': 'D', 'N07': 'D', 'N08': 'C'}, HOT_ALL),
    ("B 计划玩家(共高决中)", {'N01': 'B', 'N02A': 'A', 'N03': 'C', 'NT1A': 'B', 'NT1B': 'B', 'NW1': 'C', 'NW2': 'B', 'N04': 'C', 'N06C': 'D', 'N07': 'C', 'N08': 'A'}, set()),
    ("Pro 路径(N01 C 解锁 NT1B D)", {'N01': 'C', 'N02A': 'A', 'N03': 'A', 'NT1A': 'A', 'NT1B': 'D', 'NW1': 'A', 'NW2': 'C', 'N04': 'C', 'N06C': 'D', 'N07': 'A', 'N08': 'A'}, set()),
    ("过头硬扛(N03 B + N04B B2 触发反噬)", {'N03': 'B', 'N04B': 'B2'}, set()),
]

for name, picks, pre in paths:
    print()
    print(f"--- {name} ---")
    log, aw, wp, flags, items = simulate('N01', picks, pre)
    for line in log:
        print(line)
    print(f"最终: awareness {aw}/10 · weapons {wp}/1 · flags {len(flags)} · items {len(items)}")
