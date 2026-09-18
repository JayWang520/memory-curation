# Classification Signals (Memory Curation)

Use during curation (or minimal write-time disambiguation). Not for ordinary task retrieval.

## Compare set

| Object | Read | Skip |
|---|---|---|
| Candidate | Core claim in one sentence | Full task narrative |
| Other projects | AGENTS rules; MEMORY title/index bullets | Code, session transcripts |
| Budget | Max 2–3 other projects | Bulk dump |

## Judgment tree

```text
task progress / throwaway draft -> session
project identifiers or single-repo truth -> project
collaboration preference?
  no -> project or do not store
  yes -> similar in >=2 unrelated projects?
           no -> project
           yes -> generic tech practice only?
                    yes -> project (not user)
                    no  -> user CANDIDATE (confirm + whitelist)
```

## Signal table

| Signal | Scope | Notes |
|---|---|---|
| Path, module, API, dependency version | project | Repo-bound |
| Only one project; no similar rule in 2–3 others | project | Single-project fact |
| Collaboration preference with similar wording in ≥2 unrelated projects | user candidate | Confirm before write |
| Shared stack mistaken for universal (Python/Git/uv) | project | Tech default ≠ user memory |
| Task progress, TODO, temporary choice | session | Do not promote |
| Explicit "以后都这样 / 所有项目都适用" | user | Still must pass whitelist |

## What is NOT cross-project evidence

- Same language/package manager/tooling defaults
- Host agent built-in behavior the user never stated as a preference
- Similar folder names by coincidence
- Generic industry practice unless the user claimed it as a personal global rule

## Whitelist for user layer

Allowed:

- Response language / tone
- Collaboration rules stated as global
- Explicit global bans / workflow preferences
- Explicitly remembered identity/role

Denied:

- Repo architecture, paths, interfaces
- Task progress
- Single-project lessons

## Read budget

- Max 2–3 other projects
- Rules/index only
- Never other projects' session transcripts or source code
- Classification answers "project or user?" — not "what should we build?"

## Hard rules

1. Comparison ≠ promotion.
2. Multi-project hint → propose → write only after user confirm.
3. Unbound sessions never write project memory under a fake global id.
4. Generic industry practice is not user memory.
5. Prefer dry-run report before any write.
