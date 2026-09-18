---
name: memory-curation
description: Curate agent memory under user/project/session scopes - inventory, reclassify via cross-project comparison, propose user-layer promotions, never auto-promote. Use when the user says "整理记忆", "清一下记忆", "归类记忆", "整理记忆文件", "帮我归类记忆", "memory curation", "clean up memory", or asks to organize MEMORY.md / memory scopes. Do NOT use for ordinary coding tasks, one-off memory search, or merely reading past notes without organizing them.
---

# Memory Curation

Organize memory files under three scopes (user / project / session). Cross-project comparison runs **here**, not during ordinary project work.

## Important

- **比较 ≠ 晋升**: multi-project similarity is evidence for a proposal only. Never write user-layer memory without explicit user confirmation.
- **Default read boundary**: only user memory + current project + current session notes. Expand to other projects only when classifying suspicious/candidate entries.
- **Never** inject curation findings into unrelated task contexts; do not dump other projects' session/code into this conversation.
- **unbound session**: do not invent a project; do not write project-scoped memory under a fake/global project id.
- Registered project paths come from the host project registry only; never guess paths.

## Instructions

### Step 0: Determine binding and scope set

1. Resolve `project_id`:
   - User named a project → use its registered absolute path
   - Runtime already bound a project → use it
   - `cwd` under a registered project → use it
   - Else → `unbound`
2. Note current `session_id` if available (for session notes).
3. Resolve memory locations (adapt to this agent's layout; do not hardcode another product's branding):

   | Scope | Typical location |
   |---|---|
   | user | `<memory-root>/global/MEMORY.md` |
   | project | `<project_id>/AGENTS.md` and/or `<memory-root>/projects/<project-slug>/` |
   | session | `<memory-root>/sessions/<session_id>/notes.md` |

If the user only wants one scope curated, honor that; otherwise default to user + bound project + current session.

### Step 1: Inventory (盘点)

Read the in-scope memory files. Produce an internal table of entries:

| id/line | text (short) | current scope | status | issues |
|---|---|---|---|---|

Flag:

- duplicates / near-duplicates
- expired or task-progress entries living in project/user
- missing or wrong `scope`
- project facts sitting in user layer
- user-candidate material sitting only in one project
- empty shells / placeholder lines

Do not rewrite files yet.

### Step 2: Comparative classification (only for flagged items)

For each **scope-suspicious** or **user-candidate** entry only:

1. Read **index/rule-level** content from at most **2–3** other registered projects:
   - `<other_project>/AGENTS.md` rules sections
   - MEMORY index/title-level bullets if present
2. Classify with these signals (see also `references/classification.md`):

| Signal | Scope |
|---|---|
| Paths, module names, APIs, versions | project |
| Only in one project; no similar rule elsewhere | project |
| User preference repeated in ≥2 unrelated projects | **user candidate** (confirm first) |
| Generic tech practice (Git, Python, lint) | stays project / not user |
| In-progress task notes | session |

3. Record `evidence: single-project | multi-project-hint` on candidates.
4. Do **not** paste other projects' memory text into task answers beyond the curation report.

### Step 3: Draft actions

Prepare a plan **before** editing disk:

| Finding | Action |
|---|---|
| Clearly project-local fact | keep/write project AGENTS.md or project memory |
| Clearly user whitelist preference, user already said "all projects" | write user MEMORY |
| multi-project-hint preference | **proposal only** → wait for user |
| expired session draft | archive/delete; do not promote |
| wrong-scope project fact in user layer | propose move to project (or delete if unbound) |
| duplicate | merge; keep the tighter wording |

User-layer whitelist only:

- reply language / communication style
- collaboration rules the user stated as global
- explicit global bans / workflow preferences
- explicitly remembered identity/role

### Step 4: Present proposal and wait

Report to the user in the conversation language (Chinese by default unless they asked otherwise):

1. Inventory summary (counts + major issues)
2. Proposed disk edits (file → change), including confirmed-safe project/user merges
3. **User-candidate promotion list** (max a few): quote + which projects suggested it + suggested user-layer wording
4. Ask for confirmation on promotions and any destructive deletes

Use the interactive question UI when presenting yes/no promotion choices if multiple candidates exist.

**Do not write user-layer promotions or delete entries until the user confirms** (non-destructive project-local merges the user already approved in the same request may proceed; when unsure, wait).

### Step 5: Apply confirmed changes

1. Edit files with precise paths only.
2. User memory file structure: keep `## Rules` / `## Architecture decisions` / `## Discovered durable knowledge`; short bullets; no project detail.
3. Project memory: `status: stable` for kept conclusions; `promoted_from` when elevating. Prefer project `AGENTS.md` for durable project rules.
4. Session notes: record curation outcome briefly; archive dead drafts.
5. Optional frontmatter:

```yaml
scope: user | project | session
project_id: <abs path>
status: draft | stable
source: user-explicit | derived | tool
evidence: single-project | multi-project-hint
promoted_from: null | <path or id>
```

### Step 6: Closing checklist

- [ ] No project facts written to global/user memory
- [ ] No auto-promotion to user without confirmation
- [ ] No other-project content injected as task knowledge
- [ ] No fake global project used as a dump for unbound facts
- [ ] Indexes updated; empty shells removed
- [ ] User told what changed and what stayed untouched

## Examples

**User**: 整理记忆  
**Action**: inventory user+bound project+session → flag issues → compare only suspicious items → propose list → wait → apply confirmed edits.

**User**: 把这条升到全局记忆：以后回复都用中文  
**Action**: whitelist hit + explicit → write user MEMORY.md; skip multi-project scan unless cleaning more items in the same request.

**User**: 帮我看下 <some-repo> 的代码  
**Action**: Do **not** load this skill. Ordinary project work; no curation sweep.

## Troubleshooting

| Problem | Fix |
|---|---|
| No other projects have AGENTS/MEMORY | Treat evidence as `single-project`; still propose only when whitelist + user language support it |
| User says "都写进去" without listing items | Apply only confirmed proposals; do not mass-promote all project notes |
| Unbound + project-looking entries | Leave in session or ask which project they belong to; never shove into global |
| Skill does not trigger | Ensure the host loads global skills; a new conversation may be required after install |

## Related

- Scope convention: the host's global agent instructions (e.g. `AGENTS.md` in the agent config root), if present
- Classification signals: `references/classification.md` (same folder)
