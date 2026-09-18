# Curation Dry-Run Report Template

> Fill during Steps 1–4. Do not edit memory files until the user confirms gated actions.

## 1. Binding

| Field | Value |
|---|---|
| Mode | full / partial / explain |
| project_id | `<abs path>` or `unbound` |
| session_id | `<id>` or n/a |
| Files scanned | list paths |

## 2. Inventory summary

| Scope | Entries | Flagged |
|---|---:|---:|
| user | | |
| project | | |
| session | | |

Top issues (bullet list).

## 3. Per-entry decisions

| id | file:line | core claim | current | judged | evidence | action | confirm |
|---|---|---|---|---|---|---|---|
| U-01 | | | user | | | keep/move/merge/propose_user/drop | y/n |
| P-01 | | | project | | | | |
| S-01 | | | session | | | | |

### Judgment notes (only for flagged)

- **U-01**: why this scope — which signal; which projects were compared (rules/index only).

## 4. User-candidate proposals (gated)

For each candidate:

```text
Quote: "..."
Evidence: seen in <ProjectA rules> + <ProjectB index> (titles only)
Judged: user candidate
Suggested wording (user layer): "..."
Why whitelist: language / collaboration / ban / role
```

Ask: confirm write to user memory? (yes / no / edit wording)

## 5. Planned disk edits (after confirmation)

| File | Change |
|---|---|
| `<user MEMORY>` | |
| `<project AGENTS.md>` | |
| `<session notes>` | |

## 6. User confirmations

| Item | Decision |
|---|---|
| Promote U-01? | pending/yes/no |
| Delete/archive S-01? | pending/yes/no |

## 7. Post-apply checklist

- [ ] No project facts in user memory
- [ ] No unconfirmed user writes
- [ ] No cross-project content injected into other tasks
- [ ] evidence fields filled
- [ ] User received change summary
