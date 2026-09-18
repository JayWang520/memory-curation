# memory-curation

MiMo Desktop / MiMoCode 全局 skill：按 **user / project / session** 三层整理记忆文件。

- 默认隔离、按需检索、命中且相关才注入
- 跨项目比较用于**归类**，不用于自动晋升
- user 层写入必须用户确认

## 触发说法

- 整理记忆
- 清一下记忆
- 归类记忆 / 整理记忆文件
- memory curation / clean up memory

普通写代码、只查询历史笔记时**不要**使用本 skill。

## 安装（MiMo Desktop）

将本仓库中的 skill 内容复制到全局 skills 目录（不要只复制 README）：

```text
~/.config/mimocode/skills/memory-curation/
├── SKILL.md
├── references/classification.md
└── locales/
    ├── zh-CN.json
    └── en-US.json
```

Windows 示例路径：

```text
C:\Users\<你>\.config\mimocode\skills\memory-curation\
```

安装后**新开对话**才会加载。

## 权威规则

完整约定见本机（或你自己的）全局指令：

`~/.config/mimocode/AGENTS.md`

仓库内 `SKILL.md` 是可执行操作手册；`references/classification.md` 是分类信号表。

## 安全约束（摘要）

1. 比较 ≠ 晋升；project → user 须用户明确确认  
2. 整理时默认只读 user + 当前项目 + 当前 session  
3. 最多对照 2–3 个其他项目的规则/索引级摘要  
4. 禁止把其他项目记忆注入普通任务上下文  
5. 未绑定项目时不写 `memory/projects/global/`
