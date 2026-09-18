# Classification Signals (Memory Curation)

Use only during memory curation (or minimal write-time disambiguation). Not for ordinary task retrieval.

## Scope decision table

| Signal | Scope | Notes |
|---|---|---|
| Concrete path, module, API, dependency version | project | Bound to a repo |
| Appears in one project only; no similar rule in 2–3 others | project | Single-project fact |
| User collaboration preference with similar wording in ≥2 unrelated projects | user candidate | Confirm before write |
| Shared stack mistaken for "universal" (Python, Git, uv) | project | Tech default ≠ user memory |
| Task progress, TODO, throwaway decision | session | Do not promote |
| Explicit "以后都这样 / 所有项目都适用" | user | Still must pass whitelist |

## Whitelist for user layer

Allowed:

- Response language / tone preferences
- Collaboration rules stated as global
- Explicit global bans / workflow preferences
- Explicitly remembered identity/role

Denied:

- Repo architecture, paths, interfaces
- Task progress
- Single-project lessons

## Read budget during classification

- Max 2–3 other projects
- Only AGENTS rules sections and MEMORY index/title bullets
- Never other projects' session transcripts or source code
- Classification answers one question: "project or user?" — content is not task knowledge

## Hard rules

1. Comparison does not equal promotion.
2. Multi-project hint → propose to user → write only after confirm.
3. Unbound sessions never write `memory/projects/global/`.
4. Generic industry practice is not user memory.
