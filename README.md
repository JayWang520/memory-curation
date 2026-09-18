# memory-curation

Agent skill：按 **user / project / session** 三层整理记忆文件。

- 默认隔离、按需检索、命中且相关才注入
- 跨项目比较用于**归类**，不用于自动晋升
- user 层写入必须用户确认

## 触发说法

- 整理记忆
- 清一下记忆
- 归类记忆 / 整理记忆文件
- memory curation / clean up memory

普通写代码、只查询历史笔记时**不要**使用本 skill。

## 安装

将本仓库中的 skill 内容复制到宿主 agent 的**全局 skills 目录**下的 `memory-curation/`（不要只复制 README）：

```text
<agent-global-skills>/memory-curation/
├── SKILL.md
├── references/classification.md
└── locales/
    ├── zh-CN.json
    └── en-US.json
```

安装后**新开会话**才会加载。

## 权威规则

- 仓库内 `SKILL.md`：可执行操作手册  
- `references/classification.md`：分类信号表  
- 宿主若有全局 `AGENTS.md` / 协作约定，以该约定中的记忆作用域章节为准  

## 安全约束（摘要）

1. 比较 ≠ 晋升；project → user 须用户明确确认  
2. 整理时默认只读 user + 当前项目 + 当前 session  
3. 最多对照 2–3 个其他项目的规则/索引级摘要  
4. 禁止把其他项目记忆注入普通任务上下文  
5. 未绑定项目时不把事实写入伪造的 global project
