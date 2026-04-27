# 《运营修罗场》· 项目状态文档 v2.1

> **最后更新**:2026-04-24(晚)
> **唯一真理源**:`index.html`(1600+ 行单文件,所有 CSS/JS/剧情内嵌)
> **本文作用**:让新来的 AI / 人类 10 分钟读完接手

---

## 0.5 会话时间线

### 2026-04-25 · v2.2 重构启动(A2'+B1+C1)

用户反馈 v2.1 的 Mirror 暗线占比过重、暴露过早,游戏情感跑偏成"科幻谍战",需回归"运营 vs AM vs 客户 vs 达人"的职场修罗场本色。

**三大结构决策(用户批准)**:
- **A2'** · Mirror 大幅降权 · 删开屏标语、删 NT1 OA 句;保留 N01 HR 邮件 + ^_^ 加 hot-trigger;N02A 问卷合并 brief 附件推送
- **B1** · 痛点#4 合同扯皮合并进 NW3 · Emma 第 3 封跳出 "usage rights 6 个月,要加 30%" · 情绪定位:**被达人消耗到麻木**
- **C1** · 痛点#8 客户砍单新增 N06C · 周四 17:15 客户砍 KaptainK → 17:38 KaptainK 自己发了(双重灾难)

**全局机制升级 · 每选项独特后果 + 前置选择感知**:B/C 不再 `__M2__` 占位,M1 就走通带不同 flag · prelude 回响 + 选项可见性驱动因果链 · 感知跨度 2-3 节点

**⚠ 重要 domain 纠偏**(详见 pivot-11):运营提议 AM 拉客户会是**专业动作**,不是激进越界。C 选项维度加成从"决+险"改为"决+规+共"。

**人格光谱固定(N01)**:A 妥协型 `compliant_a` · B 反骨型 `ghosted_bryson` · C 专业型 `pro_alignment` · D 察觉型 hot-trigger item `hr_email_screenshot`

**口吻硬标准**(见 memory `feedback_tone.md`):选项 = 内心 OS 前置 + 动作 · 打工人自嗨梗撑反骨选项 · 微信黏糊语气词(哎/嘛/好滴 · 错别字保留)· Bryson 平级同事语气,把客户推前面 + 软垫子

**工具名修正**:`Modash` → `ezzzyKOL`

**节点总数**:原 17 → **18**(新增 N06C)

**已定稿节点**:
- ✅ N01 · 又一个周一 · 09:59(四选项矩阵 + 完整 body 文案)
- ✅ N02A · 入职心理评估 Part 3/3 · 10:05(四选项矩阵 + 画像 flag + 过渡段 4 路径 + 时间跳跃 + pro_alignment payoff 修正)
- ✅ N03 · Aurora 15 人名单 · 14:00
  - prelude 按 N01 flag 分 3 版 + D 叠加
  - 筛选漏斗 2,847 → 12 · 扣客户钦点 + 竞品 `海胆 Copilot` · **缺 6 人**
  - A 主动说服型(筛 5 人附理由打包推销 · meta 吐槽"成长还是堕落")
  - B 硬扛自嘲型(5 工具标签页 + 保洁阿姨 9 点 · 新梗"就当健身")
  - C 战略延后型(带 pro_alignment 自动追加"昨天会上客户也说不急了")
  - D hot-trigger(PM-14 水印截屏)
  - 后续影响预留表:A→NT1/NT3 放宽换条件 · B→N04B 展开深夜挖掘 · C→NT1 前贾斯珀问 · D→N08 相册 prelude
  - 海鲜 AI motif 确立为 running gag(帝王蟹 → 大闸蟹 → 海胆)
- ✅ N04B · 5 点半的办公室 · 时间因路径而异(四路径整合 · 标题 vs 时间错位黑色幽默)
  - 路径 A/C · 17:42 过渡(薇薇安/贾斯珀差异化)
  - 路径 D 叠加 · 相册三张照片
  - **路径 B · 22:47 深夜挖掘**(@MaybeNotJesse 菜市场虾视频 · 保洁阿姨 · 加班超时 push)
  - **B-1 / B-2 2 选 1**:B-1 适可而止 buff,**B-2 过头反噬 = 咖啡洒键盘 K 键失灵 · 贯穿周二 NT1/NT2/NT3**
  - 设计原则:内耗型反噬 >> 外部反噬(memory `feedback_ops_domain.md` 已补注)

**下一个待写**:NT1 · Aurora 项目站会 · 周二 09:30(承担 N01 / N03 / N04B 的 flag 兑现 · B-2 咖啡 K 键反噬首次登场)

---

### 2026-04-24 晚 · v2.1 口吻 demo(部分条款已被 v2.2 覆盖)

#### ✅ 已完成

- **Batch 0**:全局 `飞书 → 微信`(所有对话工具切换)
- **Batch 1**:flag / prelude / preludesByFlag 三件套框架落地
  - `renderNode` 前置取 `state.visitedNodes` 末节点 + `state.choices[lastNodeId]` 拼 key,命中 `node.preludes[key]` 注入斜体回响
  - `preludesByFlag` 叠加(多 flag 叠多段)
  - shadow choices:`condition: s => s.flags.has("xxx")` 控制选项可见
- **Batch 2 · body 大改**(共 19+ 处):
  - `NPC_KOL_RE` 扩 `Julia|Emma` 短名,13+ 处漏 wrap 修复
  - **NT1 全重写**:从"部门全员例会 + CPM 问责"→ `Aurora 项目站会`,4 人平级开会,Bryson 是同事口吻
  - NT2 / NT3 / N05 / N07.5 / N08 加 preludes 回响
  - N08 戈登空间悖论修复("只剩你 / 戈登人不在 / 从会议室出来")
  - "五彩斑斓地朴素" → `"要高级感,但别看起来贵"`(用户决定替换)
  - NW3 米拉邮件 `^_^` 解释为"系统自动加的"
  - E_NORMAL 结局尾加"凌晨 2:14 对话框敲三个字又删"
  - E_REBEL 输入法 `^_^` 自动联想
  - N11 开场加 People Ops / Influencer Ops 同词双义洞察
- **AM 人设修复**:Bryson 全局从"lead 命令"→ "平级同事,自己也被挤压"
- **本轮最新两处**(窗口最后改动):
  - N04B · **"Project Mirror 小石子"段删除**(旁白嚼暗线,用户 flag 太明显)→ 改为含糊的"*水印那行字早没了,你一度怀疑是不是熬夜眼花*"
  - NT1 · **`namelist → kollist`**(2 处,客户原话,行业术语更对)

### ⏸ 待用户批准(切窗口时停在这)

- **口吻大改 · 无厘头黑色幽默 demo**
  - 用户反馈:"现在文字叙事化 + 翻译腔 + 缺黑色幽默"
  - 病根定位:句子偏长 / 抽象比喻("小石子掉进脑子底层")/ 叙述者直接告诉情绪,而非场景演出
  - 口吻坐标:《大多数》打工人旁白 + Disco Elysium 简中内心吐槽 + 脉脉/小红书"乙方文学"
  - 改写三原则:(1) 具象名词替代抽象情绪 (2) 突兀吐槽打断叙事 (3) 甲方黑话 × 打工人反应的阶级摩擦
  - **已交付** N01 开场的原版 vs 改写版并排 demo(在对话里,未落盘 index.html)
  - 改写版关键改动:长句压成 punchline · 加"七点半响了你按掉 / 八点响了你又按掉 / 现在 09:59 进电梯" · 加吐槽旁白"*谢谢贾斯珀,第一波 judge,准时到账*" · 加 kicker"*仅需 2 分钟。你做这行三年,还没遇过一个是真的*"
  - **下一步**:等用户回来说对味 / 不对味,决定是否按此标准重写第一/二/三章

### 📋 Todo 状态(v2.1)

- [x] Batch 0 全局飞书→微信
- [x] Batch 1 flag/prelude 框架
- [x] Batch 2 body 文案 19+ 改动
- [x] Batch 3 playtest 多路径验证(eval 跑过,OK)
- [ ] **口吻 demo 批准** ← 用户回来第一件事
- [ ] 若批准,按新 tone 重写第一章 / 第二章 / 第三章
- [ ] 16 型人格表补 9 型
- [ ] N01 B/C 的 `__M2__` 占位扩成真节点(M2)

---

---

## 0. TL;DR

一个**文字 AVG 单机游戏**,主题是 **KOL 营销 agency 的运营岗日常**。双击即玩的单文件 HTML,目标是朋友圈传播 —— 传播钩子是**结局页的 16 型人格卡**(类似 MBTI)。

- **时长**:25 分钟单次
- **节点数**:17(本 demo) · 原设计 30+(后续 M2 扩展)
- **结局数**:4(一周目:E_NORMAL / E_GOOD / E_REBEL · 隐藏:E_TRUE_HERO)
- **复玩机制**:Mirror 暗线 + 隐藏结局 + M3 阶段再做 Bryson/老板视角二三周目
- **玩家视角**:运营,入职 3 个月

---

## 1. 核心定位(用户 2026-04-24 定案)

玩家通关后应该带走 3 件事:

| 情感/功能 | 承载元素 |
|---|---|
| **"这就是我的工作"的共鸣** | 运营视角 · 6 痛点 · 口语化对话 · 真实邮件抽样 |
| **好笑/可截图的分享** | 16 型人格卡(MBTI 式命名 + 扎心评语) |
| **复玩动力** | Mirror 暗线 · 隐藏结局 · 二周目换视角(M3) |
| **换位思考升华** | M3 解锁 Bryson / 老板视角,同一周看三遍 |

**Mirror 定性(重要)**:**明面是"员工决策画像/换位思考工具",暗里是"筛选员工"**。两种解读都有证据,玩家自己判断。这是成熟反乌托邦写法,比纯科幻监控高级。

**写作 tone 原则**:
- 夸张 ≠ 时间压缩,而是**把日常矛盾提炼成漫画级金句**(如"五彩斑斓地朴素")
- 运营视角**不直接接触客户**,客户只通过 Bryson(AM)的飞书转达出现
- Bryson 是**平级同事**(lead 但不是上司),不能用命令语气
- 运营和 AM 之间是"我被夹在客户和达人中间" vs "我被夹在老板和运营中间"的对等疲惫

---

## 2. 技术栈 & 文件清单

### 根目录(活跃文件)

| 文件 | 作用 | 状态 |
|---|---|---|
| `index.html` | 1600+ 行单文件 · 所有代码和剧情 | **唯一产物** |
| `PROJECT_STATE.md` | **本文** | 最新 · 先读这个 |
| `Growmax 运营执行SOP V20251125.docx` | SOP 术语参考 · 行业黑话来源 | 参考 |
| `.claude/launch.json` | 本地静态服务器(python 8000 / npx serve 8001) | 就绪 |

### `useless/`(冷宫 · 不要读)

已于 2026-04-24 晚挪入的过时文档,代码早就甩开它们 3 周,读了反而被误导:

- `HANDOFF.md`(v1 handoff,早期草稿,PROJECT_STATE.md 全面替代)
- `游戏设计文档_v0.3.md`(2400 行 v0.3 设计稿,Mirror 暗线部分尤其和当前偏离)
- `分支图与选项清单_v0.3.md`(节点地图 v0.3,现以 index.html 为准)
- `运营修罗场_PRD_v0.2.docx`(最早 PRD)
- `剧情节点表_v0.2.xlsx`(最早节点表)

**原则**:任何事实冲突一律以 `index.html` + `PROJECT_STATE.md` 为准。

**技术栈**:
- 容器:单文件 HTML,CSS/JS/剧情 JSON 全内嵌
- 字体:Google Fonts(Noto Serif SC + JetBrains Mono)
- 存储:暂未启用 localStorage(M3 二周目需要)
- 图:暂未接 canvas 雷达图(M3)
- 截图分享:暂未接 html2canvas(M3)
- 无任何框架,原生 DOM + innerHTML

---

## 3. 剧情骨架(17 节点地图)

```
周一 09:59  N01 · 又一个周一              [暗线 · HR 邮件闪现]
周一 10:05  N02A · 评估问卷              [暗线预热]
周一 14:00  N03 · Aurora 15 人名单       [痛点#1 找不到达人 · Mirror 水印]
周一 17:42  N04B · 5 点半的办公室        [过渡]

周二 09:30  NT1 · 周二早会               [情感线 · Bryson 异常 · CPM 话题]
周二 12:40  NT2 · 楼下全家 · Konstantin  [痛点#2 报价虚高傲慢]
周二 16:04  NT3 · 第三次改 Brief         [痛点#3 Brief 反复改 · 核心戏]

周三 09:15  NW1 · Vivian 的八卦         [情感线 · "巨婴"金句]
周三 14:20  NW2 · OA 套娃 + Gordon       [过渡 · gordon_hint]
周三 17:52  NW3 · Mila + Emma 拖稿       [痛点#5 拖稿循环 + 情感线]

周四 10:45  N05 · Julia "Not my audience"[痛点#6 KOL 顶回]
周四 14:30  N06B · 16 条反馈             [痛点#7 视频反复改]
周四 17:38  N07.5 · KaptainK 自己发了    [高潮事件]
周四 22:47  N08 · 没关灯的会议室         [Mirror 暗线高光]
周四 23:30  N09B · 回工位                [过渡 · 草稿箱 17 封]

周五 08:52  N10C · 通勤 + HR 约谈预告    [过渡]
周五 10:00  N11 · Seraphine 的办公室    [4 选项 → 4 结局]
                     │
                     ├── A "接受升职"      → E_NORMAL
                     ├── B "想一下"        → E_GOOD
                     ├── C "这合法吗?"   → E_REBEL
                     └── D(条件) "Mila 为什么走?" → E_TRUE_HERO
```

**6 痛点分布**:
- #1 找不到达人(N03)
- #2 报价虚高 + 傲慢(NT2 · Konstantin)
- #3 Brief 反复改(NT3 · "五彩斑斓地朴素")
- #5 拖稿 ghost 循环(NW3 · Emma 4 封催稿递进)
- #6 客户要求生硬 KOL 顶回(N05 · Julia)
- #7 视频反复修改(N06B · 16 条反馈)
- (#4 合同扯皮 · 被砍,和 #2 重合)
- (#8 客户倒闭战略取消 · 被砍,太极端)

**Mirror 暗线 3 处**(一周目):
- N01:HR 心理评估邮件(^_^ 瑜伽教练签名)
- N03:表格底部水印 `Internal Reference Only — Project Mirror`
- N08:深夜会议室 Ops Behavior Analysis 数据表 · 看到你自己 / Mila / Nolan 三人的画像

---

## 4. 项目与人物设定

**统一 campaign:Aurora AI · 产品首发 · Global · DDL 周五 EOD**(15 人达人)

### 固定 KOL 角色(3 + 1 背景)

| 角色 | 身份 | 出场节点 |
|---|---|---|
| **VelvetJulia** | 头部(3.2M) · Aurora 客户钦点之首 · "Email only. Do not chase." | N03(提名) · N05(顶 Brief) · N06B(rough cut 出 16 条反馈) |
| **KaptainK** | 中腰 · Aurora 客户钦点之二 · 经纪人 Konstantin 代理 | N03(提名) · NT2(Konstantin 抬价 $8,500) · NT3(Brief 反复改) · N07.5(**自己提前发了**) |
| **Emma Nguyen** | B+ · 主角自己从 Nox 挖的"12 人补人"之一 | N03(隐含) · NW3(拖稿 ghost 第 4 封) |
| MrTechLens | 第三个客户钦点 · 仅在 N03 出现姓名,不登场 | N03(提名) |

### 内部人物(v4 · 中文音译名)

| 人物 | 身份 | 功能 |
|---|---|---|
| 主角 `{playerName}` | 运营 · 入职 3 个月 | 玩家 |
| **布莱森**(原 Bryson) | AM · 平级 lead · 健身狂魔 · 对客户"全程陪同" | 客户压力传递者 · 语气平但让人不安 |
| **贾斯珀**(原 Jasper) | 实习生 · 上海小开(外滩三套房) · 体验生活 · 每天换不同高奢衬衫(Loro Piana / Brioni / Canali) | 喜剧背景音 · 对公司现象发问 |
| **薇薇安**(原 Vivian) | 老员工(7 年) · 八卦情报站 | 金句源("达人是巨婴,客户也是巨婴") |
| **米拉**(原 Mila) | HR 助理 · 本周离职 | 触发点:KPI 112% 但档级低于布莱森 97% |
| **戈登**(原 Gordon) | 挂名"顾问" · 四十出头 · 帽衫 · 黑色终端 | Mirror 系统的共同创造者(M2+揭露)· 本 demo 只有 `gordon_hint` flag |
| **瑟菲**(原 Seraphine) | HR 总监 · ^_^ 签名 · 瑜伽教练语调 | N11 终局对手 |

### 客户(不直接出现)

- **诺兰**(原 Nolan · Aurora CEO · 其实是老婆公司,他不知道)· 只通过布莱森飞书引用出现
- 客户的"五彩斑斓地朴素"病句风格都由布莱森转达

### 视觉人名体系(v4)

auto-wrap 机制:`renderMarkdownInline` 最后一步自动识别两类名字并上色,**无需手动 markdown 标记**。

| 类型 | 名字 | CSS class | 颜色 | 视觉 |
|---|---|---|---|---|
| 内部同事 | 布莱森 / 贾斯珀 / 薇薇安 / 米拉 / 戈登 / 瑟菲 / 诺兰 | `.npc-internal` | `#f5dfa5` 暖琥珀 | 加粗 + 轻底色 |
| KOL / 外部 | VelvetJulia / KaptainK / Emma Nguyen / Emma / MrTechLens / Konstantin | `.npc-kol` | `#8ed1c4` 青色 | 加粗 + 虚线下划 |

**嵌套 override**:`.hot-trigger` 内部的 `.npc-*` 继承外层暗米色/hover 紫,保证 trigger 视觉暗示不被盖住(关键 case:NW2 的`{{unlock_nw2|戈登}}`)。

---

## 5. 评分系统

### 4 维度

| 维度 | 正向字母 | 负向字母 | 含义 |
|---|---|---|---|
| 决 (决断) | D | H | 主动出击 vs 等指示 |
| 共 (共情) | E | C | 对他人处境敏感 vs 只看事务 |
| 规 (合规) | R | B | 按流程 vs 叛逆 |
| 险 (冒险) | V | S | 跨越合规红线 vs 保守 |

### 加权算法

```
实际入账值 = 选项基础数值 × 节点权重
```

节点权重(`weight`)分布:
- ×4:N11(道德锚点)
- ×3:N01、N05、N08(定调/转折)
- ×2:N03、NT2、NT3、N06B、N07.5、N09B(关键分支)
- ×1:NT1、NW1、NW2、NW3(性格积累)
- ×0.5:N02A、N04B、N10C(过渡)

### 字母分档(§5.3 v2 · 拉长三档)

实测一周目容易破 ±40,原 ±8 单一 `!` 档导致区分度丢失。v2 加入 `!!` 档:

| 累计值 | 标识 | 示例 |
|---|---|---|
| ≥ +25 | 大写 + !! | `D!!` |
| +10 ~ +24 | 大写 + ! | `D!` |
| +3 ~ +9 | 大写 | `D` |
| -2 ~ +2 | 中性 `·` | `·` |
| -9 ~ -3 | 小写 | `h` |
| -24 ~ -10 | 小写 + ! | `h!` |
| ≤ -25 | 小写 + !! | `h!!` |

`lettersToKey()` 去掉所有 `!+`(regex `/!+/g`)再 uppercase,映射到 16 型人格表。

### C 档冷血路径可达(v2 调整)

原问题:NT1/NW1 等节点的微温选项(共+1)导致玩家几乎必走 E 档位,C 档 7 人格不可达。

v2 修法:8 个选项的共情惩罚加深:
- NT1-A:+0 → **-2**(举手问 CPM · 无视 Bryson 面子)
- NT2-B:-1 → **-2**
- NT2-C:-1 → **-3**
- NW1-A:+1 → **-2**(否定同事八卦 = 冷)
- NW3-C:-2 → **-3**
- N06B-A:-2 → **-3**
- N07_5-C:-2 → **-3**
- N08-B:+1 → **-2**(走开装没看见 = 对同事冷漠)

验证:纯冷血路径 共 = -37 → `C!!` 档 · 触达 DCRV = ROI 型 · 冷面计算器 ✓

---

## 6. 道具 / flag / 隐藏结局机制

### 5 个"察觉类"道具/flag

| 标识 | 来源节点 | 选项 | 获取文案 |
|---|---|---|---|
| `v2_screenshot` (item) | N03 | C | 截屏筛选漏斗 + Mirror 水印 |
| `brief_nonsense` (item) | NT3 | D | "五彩斑斓地朴素"存进「证据」相册 |
| `vivian_quote` (flag) | NW1 | B 或 C | 听进去 Vivian 的"巨婴"金句 |
| `gordon_hint` (flag) | NW2 | B | Slack Gordon 追问 OA 系统 |
| `mirror_screenshot` (item) | N08 | A | 深夜拍下 Mirror 数据表 |

### E_TRUE_HERO 解锁条件

```js
condition: s => awarenessCount() >= 3 && s.stats.险 >= 10
```

**5 选 3 + 险 ≥ 10**。需要玩家有意识地选"察觉路线"且至少 50% 时间选险选项。
一周目保守玩家几乎触发不了,二周目有意识刷可触发。

### 隐藏选项机制(v3 · ARG 双层触发)

之前问题:5 个察觉道具/flag 都在"明面第 4 选项"里,玩家撞一撞就集齐,E_TRUE 太廉价。

v3 引入**双层门槛**:

**层 1 · 文本点击触发**(扩 markdown 加 `{{flag|text}}` 语法)
- 渲染:`<span class="hot-trigger" data-unlock="flag">text</span>`
- 触发前:视觉接近正文(#d8c89a + dotted underline)· 盲玩家不察觉
- hover:Mirror 紫 `#d8b8ff`
- 点击:`state.flags.add("unlock_xxx")` + 重渲当前节点 + 对应 choice 带 `.just-unlocked` 动画闪现
- 点击后:`.fired` 暗灰 · 已消化标记

**层 2 · 道具积累阈值**
- N08-A(拍照 → mirror_screenshot)condition: `awarenessCount() >= 2`
- 意思:前面 4 处(N03/NT3/NW1/NW2)已经至少有 2 个道具入手,才能看见 N08 拍照选项

**3 个文本触发点**(都使用 `{{flag|text}}` 语法):

| 节点 | trigger 词 | flag | 解锁 choice | 对应 item/flag |
|---|---|---|---|---|
| N03 | `Internal Reference Only — Project Mirror` | `unlock_n03` | C | `v2_screenshot` item |
| NT3 | `"五彩斑斓地朴素"` | `unlock_nt3` | D | `brief_nonsense` item |
| NW2 | `Gordon` | `unlock_nw2` | B | `gordon_hint` flag |

**N08-A 的条件门槛**:`condition: s => awarenessCount() >= 2`(不依赖点文本,依赖前面已收集 item/flag)

**NW1-B/C(`vivian_quote` flag)不加触发**:NW1 是 Vivian 主动过来"倾诉",玩家选择"信/不信"本来就是直接交互,不需要隐藏。

**技术实现要点**:
- `renderMarkdownInline` 新增 `{{flag|text}}` 解析,识别 `state.flags.has(flag)` 已触发态
- `renderNode(nodeId, { flashKey })` 支持可选 flashKey 参数,给新出现的 choice 加 `.just-unlocked` class
- 点击委托:`$game.querySelectorAll(".hot-trigger[data-unlock]")` 而非 inline onclick(CSP 友好 + 事件委托干净)
- `unlock_*` flag **不在** `AWARENESS_MARKS` 里,不算进 awarenessCount;**不在** `ITEM_LABELS` 里,公文包 / 结局线索卡不显示(它们只是"机制状态",不是"玩家收获")

### 双路径对照(v3 实测)

| 路径 | 线索 | 字母 | 人格 | 结局 |
|---|---|---|---|---|
| 盲玩家 · 不点 trigger | 0/5 | 浮动 | 视 stats 而定 | E_NORMAL / E_GOOD / E_REBEL |
| ARG 路径 · 点 3 trigger + 走险 | 5/5 | D!! E R V!! | MVP / DERV | E_TRUE_HERO |
| 冷血路径 · 不点 trigger + 全冷血 | 0/5 | D! C!! R!! V | ROI / DCRV | E_NORMAL |

---

## 7. 16 型人格表

**当前状态:只填了 7 型 + `_DEFAULT` 兜底**(其他型命中会 fall back)

已写:
- `DERS` · PPT 政治家
- `HERS` · 老好人之光
- `HCRS` · 优质 NPC
- `DCRS` · 工具人之神
- `HERV` · 善良的墙头草
- `DERV` · 修罗道行者
- `_DEFAULT` · 未定型新人

待补 9 型(建议等用户实际命中某型后针对性写):
DEBV / DEBS / DCRV / DCBV / DCBS / HEBV / HEBS / HCRV / HCBV / HCBS

每个人格结构:
```js
{
  title: "xxx",             // 名字
  mentalState: "...",       // 核心特质
  goodAt: "...",
  badAt: "...",
  bestPartner: "XXXX · xxx",
  nemesis: "YYYY · yyy",
  bossView: "老板眼中的你"
}
```

---

## 8. 视觉分层系统(已实装)

### 5 级 markdown 标记

| 类型 | 标记 | 渲染样式 |
|---|---|---|
| 旁白(默认) | 无标记 | #dcd6c8 衬线常规 |
| 对话(他人) | `"..."`(中文双引号) | #ffe8a8 暖白加粗 · **自动识别** |
| 内心 OS | `*...*` | #8a7f5f 斜体 |
| 常规强调 | `**...**` | #fff4dc 粗体亮白 |
| 剧情关键字 | `[[...]]` | #e8b87c 琥珀色 · 虚线下划 · 半透明底色 |
| 系统/代码 | `` `...` `` | #b0d8b5 等宽 · 暗底色块 |
| 引用/邮件块 | 整段 `> ...` | 左粗竖线 + 暗底 + 斜体 |

### 重要 bug 修复历史

**v1.0 bug**:`<br>` 被 markdown 转义为 `&lt;br&gt;`。
**v1.1 bug**:dialogue 正则吃了自己生成的 HTML 里的 `class="keyword"` 属性引号,导致 [[keyword]] 渲染崩坏。
**v1.2 修**:dialogue 正则改为只匹配中文引号 `\u201C / \u201D`,不吃 ASCII `"`。

当前渲染顺序(`renderMarkdownInline`):
```js
& → < → > 转义
→ [[...]] keyword
→ **...** strong
→ *...* em
→ `...` code
→ "..."(仅中文引号)dialogue
```

---

## 9. UI 功能

- **顶部时间线 HUD**:周一 › 周二 › 周三 › 周四 › 周五 · 当前日高亮 · Aurora briefing 副标题
- **开场 Briefing 卡**:Client / Campaign / Deliverable / DDL
- **手机适配**:≤640px · ≤380px 两档 media query
- **debug 接口**:
  ```js
  window.__state       // 看实时 stats/items/flags/choices
  window.skipTo("N08") // 跳任意节点
  window.jumpEnding("E_TRUE_HERO")
  ```

---

## 10. 已知问题 & TODO

### 🔴 结构性待办

- [ ] **16 型人格表只有 7 型** — 玩家命中未写型会看到 _DEFAULT 兜底,可接受但不理想
- [ ] **N01 的 B 和 C 选项仍指向 `__M2__` 占位** — 符合原 M1 demo 设计(只走路径①),但玩家会撞到"此路径 M2 开放"提示
- [ ] **E_GOOD / E_REBEL 虽然写了结局文案,但路径上不经过 E_TRUE_HERO 之外的任何"隐藏分叉"** — 其实三个浅结局都是线性的,只有 D 选项需要条件。对一周目够用

### 🟡 内容待调

- [ ] **NT1 早会(周二)**功能偏弱 · 目前只是情感线和 CPM 话题,和本周 Aurora 主线关联不强。建议加一句 Bryson 暗示 Aurora 客户"老板最近在看",和 N03/N04B 的"老板盯着"呼应
- [ ] **NW1 Vivian 金句 flag 只在 B/C 触发** · A 选项"不可能吧"的玩家拿不到 vivian_quote,公平度可议
- [ ] **N02A 评估问卷** · 目前只有一个选项 next,形同过渡。M2 可以让 20 题每道都影响性格维度
- [ ] **主角没有"升职对价"的直接感知** · N11 提到升职但从没铺垫主角的薪资/title 现状。E_NORMAL 结局提 Senior title 稍显突兀

### 🟢 视觉/UX 小调

- [ ] 时间线 HUD 在长内容节点(如 N08)上 sticky 时可能遮挡标题 —— 目前没明显 bug,但值得关注
- [ ] Mobile 下 Brioni / Konstantin 这种长英文人名可能出现溢出 —— 暂无反馈
- [ ] 手机无 hover,现在 `.choice:hover` 只在桌面起效 —— 正常

### ⏸ 显式延后(M2/M3)

- [ ] 二周目 Bryson 视角(M3)
- [ ] 三周目老板/Seraphine 视角(M3)
- [ ] 雷达图结算(M3)
- [ ] html2canvas 电子工牌保存 + 朋友圈分享(M3)
- [ ] localStorage 二周目存档 · 解锁状态持久化(M3)
- [ ] N01 B/C 路径 + 其他节点的 __M2__ 分支扩展(M2)

---

## 11. 设计决策记录(关键 pivot)

### pivot-1 · Mirror 暗线降权(一周目)

**原设计**:Mirror 占 6 个节点(N01/N02/N03/N08/N10D/N11),是主要戏份。
**问题**:和运营日常痛点抢戏,玩家感觉"反乌托邦"压过"职场共鸣"。
**当前**:Mirror 降为 3 处闪现 + N11 终局揭晓。日常痛点占 80% 戏份。

### pivot-2 · Mirror 重定性

**原**:赛博朋克监控工具(《黑镜》味)。
**当前**:**明面换位思考工具 / 暗里筛选工具**(两读模糊)。
**理由**:纯监控情绪是愤怒 → 一次性。两读模糊能撑三周目升级(Bryson 看到的是 A,老板看到的是 B,终局 = 都是)。

### pivot-3 · 痛点取舍

**8 痛点 → 6 痛点**(2026-04-24):
- 砍掉 #4 合同扯皮(和 #2 重合)
- 砍掉 #8 客户倒闭(太极端,压制其他戏)

### pivot-4 · 项目统一

**原问题**(用户 2026-04-24 试玩反馈):Kling / Aurora 多个项目名称在不同节点出现,剧情割裂。
**当前**:所有事件都在 **Aurora AI 产品首发 campaign** 下。3 固定 KOL(Julia/KaptainK/Emma) + MrTechLens 背景。**Kling 全删**。

### pivot-5 · 夸张化方向

**原写法**:时间压缩、版本号堆叠。
**用户反馈**:这不叫夸张,叫堆细节。
**当前**:**抽象成漫画金句**("是不是觉得他是碧昂丝"、"no choice 用得很顺"、"要高级感但别看起来贵")。
**2026-04-24 修订**:原标志性梗"五彩斑斓地朴素"被用户要求替换为"要高级感但别看起来贵",理由是前者过于一眼假,后者更贴近真实甲方原话。

### pivot-6 · Bryson 角色

**原**:组长式命令语气("别绕过我"、"AM 来 handle")。
**当前**:**平级同事 · 偶尔犯懒**。既传达客户压力也流露自己也被客户挤压的疲惫。

### pivot-7 · 运营视角收窄

**原**:运营和客户直接打交道。
**当前**:**运营不直接接触客户**,客户通过 Bryson 微信转达出现。主角视野 = 其他运营 + KOL + AM(Bryson)。

### pivot-8 · 沟通工具统一(2026-04-24)

全局 `飞书 → 微信`。理由:国内 agency 和客户对接实操上用微信更多,飞书反而显假。

### pivot-9 · AM 角色降级为平级(2026-04-24)

**原**:Bryson 是"lead",可以"问责"运营,开会代表客户施压。
**当前**:Bryson 是**完全平级的同事**,只反馈项目进度 / 达人名单缺口,不问责 CPM 等运营 KPI。NT1 因此从"部门例会"重写为"Aurora 项目站会"(4 人小桌)。

### pivot-10 · 口吻转向无厘头黑色幽默(2026-04-24 晚 · 进行中)

**原写法**:叙事化 + 翻译腔(长句 + 抽象比喻 + 叙述者告诉情绪)。
**目标**:具象名词 + 突兀吐槽 + 甲方黑话 × 打工人反应的阶级摩擦。
**参考坐标**:《大多数》打工人旁白 + Disco Elysium 简中内心吐槽 + 脉脉/小红书"乙方文学"。
**状态**:N01 开场的改写 demo 已交付用户,等切回窗口批准。**更新 2026-04-25**:用户默认按新口吻推进 v2.2,pivot-10 进入"执行中"。

### pivot-11 · C 选项从"激进越界"纠正为"专业对齐"(2026-04-25)

**原**:我(AI)把 N01 的 C 选项"让布莱森拉会对齐 brief"标为"激进越界"人格,维度加成 决+险。
**当前**:运营提议 AM 拉客户会、运营旁听/发言是 **pivot-7 的合规实现**,不是破坏。这是运营能做的**最专业**响应。
**维度修正**:从 决+险 改为 决+2 规+2 共+1 险0。
**真正的"险"**:跳过 AM 直接加客户微信 / 绕过 AM 发邮件——才算破坏 pivot-7。
**人格光谱修正**:N01 三选项 = 妥协型(A) / 反骨型(B) / **专业型**(C,不是激进型)+ 察觉型(D,隐藏第四维度)。

### pivot-14 · 修罗场 = 无厘头黑色喜剧,不是职场纪录片(2026-04-25 · 深化 pivot-10)

**原**:我在 N02A / N03 的背景设定里写"客户产品上线新功能要加进 brief"(真实系)。
**问题**:用户反馈"太真实了,没人喜欢玩的"。纯写实 = 丧,玩家没玩下去的欲望。
**当前**:所有**客户需求 / brief 改版 / 产品动态 / 业务触发 / 竞品名字 / 达人翻脸理由**都要**抽象化 + 夸张化**到漫画级别。保持真实职场结构(AM 转达 / 微信群 / 达人扯皮)的 **frame**,但把 **content** 推到无厘头。
**无厘头公式**:AI 行业黑话 × 民间俗物 × 商业升级叙事 = 笑点
**已实装样例**:客户连夜上"大闸蟹 Agent"分公母版本("公蟹主攻生产力 · 母蟹主攻情感陪伴 · 比帝王蟹 Agent 厉害多了")
**边界**:荒诞的是**甲方诉求**,不是**打工人反应**。Bryson 依然"哎...嘛",运营内心 OS 依然血压飙升("第三版了"、"下周是不是该石斑鱼了")。**打工人面对荒诞依然真实 = 笑点所在**。
**后续适用**:所有节点的客户动态 / brief 背景 / 达人话术按此处理。详见 memory `feedback_tone.md` 第 7 条。

### pivot-13 · 沟通渠道与 brief 归属纠偏(2026-04-25)

**原**:N02A 过渡段写"[新邮件] 布莱森 · 转发:Aurora_Brief_v3.pdf"。
**问题**:
1. Brief 是**客户**写的,布莱森不拥有,不能"转发"
2. Brief 修改沟通走**微信项目群**,不走邮件
3. Brief 改版要有**具体业务触发原因**,不能"客户改了"一笔带过
**当前**:场景改为"Aurora 项目群 · 布莱森 @ 你",触发原因"客户产品上线新功能要加进来"。
**How to apply**:详见 memory `feedback_ops_communication.md`。

### pivot-12 · 全局机制升级 · 每选项独特后果 + 前置选择感知(2026-04-25)

**原**:B/C 选项多通 `__M2__` 占位,感知机制(preludes / hot-trigger)只在少数节点。
**当前**:
- **B/C 选项 M1 就走通**,但带**不同 flag** 影响后续剧情
- flag 驱动后续节点的 **prelude 斜体回响** 和 **选项可见性**
- 玩家要能**感知到**"上次选了 X,这次多/少一个选项"——不是闷声修改
- **感知点跨度**:一般 2-3 节点后(太近太刻意,太远太淡)
- **提示频率**:3 次里提示 1 次,不能每次都旁白解说,否则变教学模式
**代价**:M1 总体文案量 × 1.3~1.5(每节点要写 2-3 个小变体)
**首次实战**:N02A 的 D 选项需要 N01 选过 D(hr_email_screenshot item)才出现——玩家能亲眼看到机制生效。

---

## 12. 素材来源(邮件语料)

主角 Mark@grow-max.com 的真实邮件已被挖掘,存在用户 `~/Downloads/`:
- `Cleaned_Emails_Full.csv` (5.3 MB · 全量)
- `Merged_Cleaned_Emails_01.txt` ~ `_48.txt`(每份 ~310 KB)

**典型金句提取**(来自邮件):
- 催稿递进:`just follow up` → `client is urging` → `we will have no choice but to cancel`
- Brief 改版:`Apology for the multiple emails, kindly check this one :)`
- 经纪人冷淡:`Unfortunately this rate is too low for [Name] as he has a lot of collaborations to prioritize`
- 达人拒接:`At the moment, all our collaboration slots are fully booked`

---

## 13. 下一步建议

按优先级:

1. **用户实机试玩** 全部 4 条路径 + 反馈 · **当前任务**
2. 根据命中型补 16 型人格表的具体评语
3. 考虑 NT1 加一句 Aurora 相关话(让 NT1 和主线 Aurora 有绑定)
4. M2 启动:N01-B/C 分支 + 其他 __M2__ 指向的节点扩充
5. M3 启动:二周目 Bryson 视角 · localStorage · 雷达图 · 截图分享

---

## 14. 给下一个 AI / 人类协作者

**读这些必读(按序)**:
1. 本文 §0.5(本次会话改动 + 待批准事项)
2. 本文其余部分
3. `index.html`(最少读:`const STORY` 节点数据段 + 引擎函数 `applyChoice` `computeLetters` `renderMarkdownInline` `bodyToHtml` `renderTimeline` + `renderNode` 里的 preludes 注入逻辑)

**不要读**:
- `useless/` 整个文件夹 —— 过时设计稿,全部已被 index.html 替代
- (如果为了补 §5 评分算法或 §4 16 型人格表的历史上下文可破例翻 `useless/游戏设计文档_v0.3.md`,但须知它是历史化石)

**用户偏好**:
- 中文沟通,必须
- 第一性原理,不盲目假设
- 复杂任务先出方案等批准
- **不要加注释**除非逻辑极不明显
- **不要自动 commit 或 push**
- 输出简洁,砍掉不改变决策的信息

**用户风格**:
- 真实从业者(KOL 营销 agency 运营岗)
- 写作品味高,对 tone 敏感
- 会试玩并提出具体反馈
- 喜欢"我想一下"的 pivot 时刻 · 不要急着推进

**已确立的禁区**:
- Mirror 不能纯监控(必须两读)
- Bryson 不能命令语气(必须平级)
- 客户不能直接出镜(必须 Bryson 转达)
- 夸张不是时间压缩(是漫画化金句)
- 暗线 ≠ 占大量戏份(暗线是调味剂)

---

**END**
