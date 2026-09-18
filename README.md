# memory-curation

Agent skill：按 **user / project / session** 三层整理记忆文件。

- 默认隔离、按需检索、命中且相关才注入
- 跨项目比较用于**归类**（最多对照 2–3 个项目的规则/索引），不是为了注入内容
- 判断树：进度→session；仓库事实→project；协作偏好且多项目重复→user **候选**
- user 层写入必须用户确认；比较 ≠ 晋升

## 触发说法

- 整理记忆 / 清一下记忆 / 归类记忆 / 整理记忆文件
- 项目怎么比较 / 怎么分类 / 怎么判断
- memory curation / clean up memory

普通写代码、只查询历史笔记时**不要**使用本 skill。

## 安装

复制到宿主 agent 的全局 skills 目录：

```text
<agent-global-skills>/memory-curation/
├── SKILL.md
├── references/
│   ├── classification.md
│   └── report-template.md
├── scripts/
│   └── inventory.py
└── locales/
    ├── zh-CN.json
    └── en-US.json
```

安装后**新开会话**才会加载。

## 判断树（摘要）

```text
任务进度/草稿 → session
含路径/接口/版本，或仅单仓库成立 → project
关于用户希望 agent 如何协作？
  否 → project 或不入库
  是 → ≥2 个无关项目有相近表述？
         否 → project
         是 → 仅通用技术惯例？
                是 → project（不算 user）
                否 → user 候选（须确认 + 白名单）
```

## 安全约束

1. 比较 ≠ 晋升；project → user 须用户明确确认  
2. 默认只读 user + 当前项目 + 当前 session  
3. 最多对照 2–3 个其他项目的规则/索引级摘要  
4. 禁止把其他项目记忆注入普通任务  
5. 未绑定项目时不把事实写入伪造的 global project  
6. 默认先 dry-run 报告，确认后再改盘  

## 相关文件

- `SKILL.md` — 可执行流程  
- `references/classification.md` — 信号与硬规则  
- `references/report-template.md` — dry-run 报告模板  
- `scripts/inventory.py` — 可选盘点脚本（只读）  
