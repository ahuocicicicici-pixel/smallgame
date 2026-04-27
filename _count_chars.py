"""统计每节点 body 中文字数 · 找超过 300 字的"""
import re

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

nodes_section = re.search(r'nodes:\s*\{(.*?)\n  \},\s*endings:', text, re.DOTALL).group(1)
node_pat = re.compile(r'^    ([A-Z_0-9]+):\s*\{(.*?)(?=^    [A-Z_0-9]+:\s*\{)', re.MULTILINE | re.DOTALL)
sentinel = nodes_section + '\n    __SENTINEL__: {'

import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

print("节点 body 字数(中文字符)")
print("-" * 50)
total = 0
over_300 = 0
for m in node_pat.finditer(sentinel):
    nid = m.group(1)
    if nid == '__SENTINEL__':
        continue
    body = m.group(2)
    # body 字段 — 反引号或函数
    bm = re.search(r'body:\s*`(.*?)`,', body, re.DOTALL)
    if not bm:
        bm = re.search(r'body:\s*function.*?\{(.*?)\n      \},', body, re.DOTALL)
    if bm:
        bd = bm.group(1)
        chinese = sum(1 for c in bd if '一' <= c <= '鿿')
        flag = ' ▲超 300' if chinese > 300 else ''
        print(f'{nid:18s}: {chinese:4d} 字{flag}')
        total += 1
        if chinese > 300:
            over_300 += 1

print("-" * 50)
print(f"总节点 {total} · 超 300 字 {over_300} · 占比 {100*over_300/total:.0f}%")
