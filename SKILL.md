---
name: memory-curation
description: Curate agent memory under user/project/session scopes - inventory entries, compare at most 2-3 other projects on rules/index only, classify with a fixed decision tree, propose user-layer promotions, never auto-promote. Use when the user says "整理记忆", "清一下记忆", "归类记忆", "整理记忆文件", "帮我归类记忆", "memory curation", "clean up memory", or asks how projects are compared / how memory is classified. Do NOT use for ordinary coding tasks, one-off memory search, or merely reading past notes without organizing them.
---

# Memory Curation

Organize memory into **user / project / session**. Cross-project comparison is a **classification step**, not a knowledge-injection step.

## Important

- **比较 ≠ 晋升**: multi-project similarity is only evidence for a *proposal*.
- **Default read boundary**: user memory + current project + current session notes.
- **Never** paste other projects' memory into ordinary task answers.
- **unbound**: do not invent a project; never dump facts under a fake/global project id.
- **Do not guess project paths**; use the host registry or user-provided absolute paths only.
- Prefer **dry-run** (Steps 0–4) before any disk write (Step 5).

## Modes

| User intent | Mode | What runs |
|---|---|---|
| 整理记忆 / 归类 / clean up | full | Steps 0–6 |
| 「怎么比较 / 怎么分类」 | explain + optional dry-run | Judgment section + report only |
| 「只整理 user 层」等 | partial | Honor the named scope only |
| 普通写代码 / 查一下笔记 | none | Do **not** load this skill |

## How projects are compared (方法)

### What is compared

| Object | Read | Do not read |
|---|---|---|
| Candidate entry | Core claim (one sentence) | Surrounding task chatter |
| Other projects | `AGENTS.md` rules sections; MEMORY **title/index** bullets | Source code, full session logs, deep path details |
| Budget | At most **2–3** other projects | Whole memory dump |

The comparison answers only: **"Which scope does this claim belong to?"**

### How to compare (procedure)

1. Rewrite the candidate as a **core claim** (what behavior/fact does it constrain?).
2. Mark signals: path/API/version? collaboration preference? task progress?
3. For each of 2–3 other projects, read rules/index only — is there a **similar claim type**?
4. Record `evidence: single-project | multi-project-hint`.
5. Decide via the judgment tree below.
6. Propose; do not write until confirmation rules allow it.

### Judgment tree (怎么判断)

```text
Is it task progress / throwaway draft?
  YES -> session

Does it contain project-specific identifiers
(path, module, API, version) OR clearly only true for one repo?
  YES -> project

Is it about HOW the user wants the agent to collaborate
(language, isolation, workflow bans, role)?
  NO  -> project (or do not store)
  YES -> Similar wording in >=2 unrelated projects?
           NO  -> project
           YES -> Is it only generic tech practice
                  (git/python/lint/tooling defaults)?
                    YES -> project (NOT user)
                    NO  -> user CANDIDATE
                           (whitelist + user confirm required)
```

### What does NOT count as cross-project evidence

- Same tech stack on both sides (both Python, both Git, both uv)
- Host/agent default behavior that is not a user preference
- Coincidental similar filenames or folder layout
- Industry standards (conventional commit style, semver) unless the user stated them as *personal global rules*

### Hard rules

1. Comparison does **not** equal promotion.
2. `user` candidate → propose → write **only after** explicit user confirmation.
3. Unbound sessions never write project memory under a fake global id.
4. Generic industry practice is not user memory.
5. Classification artifacts stay in the curation report; they are not task knowledge.

## User-layer whitelist

Allowed:

- Response language / tone
- Collaboration rules the user stated as global
- Explicit global bans / workflow preferences
- Explicitly remembered identity/role

Denied:

- Repo architecture, paths, interfaces, dependency conclusions
- Task progress
- Single-project lessons

## Instructions

### Step 0: Binding, mode, paths

1. Resolve `project_id` (first hit wins):
   - User named a registered project → absolute path
   - Runtime binding → use it
   - `cwd` under a registered project → use it
   - Else → `unbound`
2. Note `session_id` if available.
3. Resolve locations (host layout; keep product-agnostic wording):

   | Scope | Typical location |
   |---|---|
   | user | `<memory-root>/global/MEMORY.md` |
   | project | `<project_id>/AGENTS.md` and/or `<memory-root>/projects/<slug>/` |
   | session | `<memory-root>/sessions/<session_id>/notes.md` |

4. Choose mode (full / partial / explain).

Optional deterministic assist:

```bash
python scripts/inventory.py --user <user-memory-file> \
  --project-agents <project>/AGENTS.md \
  --session <session-notes-file>
```

If paths are missing, skip the script and inventory by reading files directly.

### Step 1: Inventory (盘点)

Build an entry table (do not edit disk yet):

| id | file:line | core claim (short) | current scope | status | issues |
|---|---|---|---|---|---|

Flag issues:

- duplicate / near-duplicate
- task progress living in project/user
- missing or wrong scope
- project facts sitting in user layer
- possible user-candidate (collaboration preference)
- empty shell / placeholder
- overly long entry that should be split

### Step 2: Comparative classification (flagged items only)

For each flagged entry, run **How projects are compared** + judgment tree.

Output per candidate:

```yaml
id: U-03
claim: "默认中文回复"
current: user
judged: user | project | session
evidence: multi-project-hint | single-project
seen_in: [projectA_rules, projectB_index]  # index/rule level only
action: keep | move | merge | propose_user | drop
needs_confirm: true|false
```

### Step 3: Draft actions

| Finding | Action | Confirm? |
|---|---|---|
| Clearly project-local | keep/write project AGENTS.md / project memory | no (if already correct) |
| Project fact in user layer | move to that project or drop if unbound | yes if destructive |
| Whitelist + user already said "all projects" | write user MEMORY | use that explicit statement |
| multi-project-hint collaboration pref | **propose_user** only | **yes, always** |
| Expired session draft | archive/drop | yes if delete |
| Duplicate | merge tighter wording | no for pure merge |

### Step 4: Dry-run report (default before writes)

Use `references/report-template.md`. Structure:

1. Binding + mode + files scanned
2. Inventory counts
3. Per-entry decisions (table)
4. **User-candidate proposals** (quote + projects + suggested wording)
5. Planned disk edits
6. Ask for confirmation on promotions/deletes

Use interactive question UI when multiple yes/no promotion choices exist.

**Gate:** no user-layer write and no destructive delete until user confirms.

### Step 5: Apply confirmed changes only

1. Edit exact paths only.
2. User file sections stay: `## Rules` / `## Architecture decisions` / `## Discovered durable knowledge`.
3. Project durable rules prefer `AGENTS.md`; mark `status: stable`; set `promoted_from` when elevating.
4. Session notes: record curation outcome; archive dead drafts.
5. Frontmatter (optional but recommended):

```yaml
scope: user | project | session
project_id: <abs path>
status: draft | stable
source: user-explicit | derived | tool
evidence: single-project | multi-project-hint
promoted_from: null | <path or id>
```

6. Re-run inventory script if available; confirm flagged issues are resolved or explicitly deferred.

### Step 6: Closing checklist

- [ ] No project facts written to user/global memory
- [ ] No auto-promotion to user without confirmation
- [ ] No other-project content injected as task knowledge
- [ ] No fake global project dump for unbound facts
- [ ] Judgments recorded with `evidence`
- [ ] Indexes updated; empty shells removed
- [ ] User told what changed and what stayed untouched

## Examples

**User**: 整理记忆  
**Action**: full dry-run → report → wait → apply confirmed edits.

**User**: 项目怎么比较怎么分类怎么判断？  
**Action**: explain the judgment tree; offer optional dry-run inventory. Do not mass-edit.

**User**: 把这条升到全局：以后回复都用中文  
**Action**: whitelist + explicit → write user MEMORY.md; no multi-project scan required unless also curating.

**User**: 看一下 `<repo>` 的代码  
**Action**: do not load this skill.

## Troubleshooting

| Problem | Fix |
|---|---|
| Other projects have no AGENTS/MEMORY | `evidence: single-project`; only propose user items when whitelist + explicit user language support it |
| User says "都写进去" without a list | Apply only listed/confirmed proposals; no mass-promotion |
| Unbound + project-looking entries | Leave in session or ask which project; never shove into global |
| Two projects share a tech default | Still project — not user |
| Skill not triggering | Host must load global skills; new conversation after install |
| Git push to the skill repo fails (443 timeout) | Update files via host API if available; content must stay brand-agnostic |

## Related files

- `references/classification.md` — signals, whitelist, hard rules
- `references/report-template.md` — dry-run report skeleton
- `scripts/inventory.py` — optional deterministic inventory helper
- Host global agent instructions (e.g. `AGENTS.md` memory-scope section), if present
