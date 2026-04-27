# 运营修罗场 · KOL Survivor

一个关于 **KOL 营销 agency 运营岗** 一周生存的单文件 HTML 文字 AVG。

> 客户在改 brief · 达人在催稿 · HR 在发问卷 · 你今天是周一 09:59。
> 周五 EOD 之前要把 15 个海外达人定下来。
> 路上你会撞见米拉抱箱走过 · 听见 Vivian 说 " 都是在哄婴儿 " · 错收一封不该看到的邮件。

---

## 怎么玩

直接打开 `index.html` 就行 —— 没有任何依赖,纯单文件浏览器游戏。

或者本地起 server:

```bash
python -m http.server 8765
# 然后浏览器打开 http://localhost:8765/index.html
```

输入名字 → 选 4 个维度 → 5 天工作日 → 5 种结局之一 + 16 型职场人格分析。

---

## 玩法机制

| 维度 | 含义 |
|---|---|
| **决** | 决断力 · 该硬的时候硬 |
| **共** | 共情力 · 该软的时候软 |
| **规** | 合规度 · 流程感 / 留痕能力 |
| **险** | 风险偏好 · 越界 / 截图 / 反制 |

5 个结局:
- **E_NORMAL** · 上岸者
- **E_BLADE** · 执剑人(高决断 · 主动 weaponize)
- **E_PLANB** · Plan B 在身(高共情 · 默默存证)
- **E_NUMB** · 装糊涂大师(回避所有 D 选项)
- **E_PM14** · 未命名(觉察 ≥ 4 项暗线触发 · 开放结局)

---

## 文件结构

```
smallgame/
├── index.html              # 游戏本体 · 单文件 HTML(CSS + JS + 剧情数据全内嵌)
├── PROJECT_STATE.md        # 开发笔记 · 设计决策 / 节点演进
├── _export_story.py        # 导出全剧情成 txt · 用于 review
├── _path_check.py          # 路径一致性检查 · 静态结构验证 + 路径模拟
├── _count_chars.py         # 节点字数统计
└── README.md
```

---

## 灵感

- 《大多数》打工人旁白
- Disco Elysium 简中内心 OS
- 脉脉 / 小红书 " 乙方文学 "
- 真实 KOL agency 运营日常

---

## License

MIT
