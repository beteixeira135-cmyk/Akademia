---
name: akademia-tcc
description: Use for every substantive task in the Akademia repository, especially TCC II, 3-PG, scientific writing, experiments, calibration, data, figures, audits, and deliverable generation. Start from the current project memory and verify claims against source files.
---

# Akademia TCC workflow

Use this skill for work in this repository. It provides the detailed procedure behind the persistent project rules in `CLAUDE.md` and `AGENTS.md`. The project-level command is `/akademia-tcc`.

## Where this skill applies

This is a Claude Code project skill, shared through the repository at `.claude/skills/akademia-tcc/SKILL.md`. Claude Code can invoke it automatically from its description or directly as `/akademia-tcc`; `CLAUDE.md` also tells Claude Code to read it for every substantive repository task. Claude.ai web, Desktop, or Projects do not automatically load this repository file; those surfaces require a separately enabled account skill or project instructions.

## 1. Establish current state before acting

1. Read `AGENTS.md`, `memoria/contexto_ativo.md`, and `memoria/progresso.md`. Read `PASSAGEM_DE_BASTAO.md` if present.
2. For TCC finalization or a handoff task, read the relevant current files in `handoff_claude/`, `entregavel_final/`, and `auditoria_final/`. Treat handoffs as leads, not proof; check the current branch, files, and outputs.
3. Record the current branch, `HEAD`, working-tree status, and the task's allowed files. Preserve pre-existing changes and do not edit `main`. Create or use a task branch according to the user's and repository's workflow; do not switch branches without authorization.
4. Confirm each claimed input/output exists before relying on it. Use the repository's exact paths and inspect history when provenance matters. Never infer that a file exists because a handoff says it does.

## 2. Protect the repository and data

- Use only secondary data. Never invent or silently estimate a measurement, parameter, result, citation, or DOI. If the source is missing, state that it is missing.
- Do not reconstruct a missing CSV from a summary, figure, screenshot, or reported totals. If a required source is absent, block only conclusions and artifacts that depend on it; continue independent work.
- Keep simulated results distinct from field observations. A comparison with literature is not automatically validation.
- Do not change 3-PG equations, parameters, or the scientific engine unless the user explicitly requests that scope. Preserve the original behavior: `compensation=None` must remain reproducible and its tests must keep passing.
- Do not overwrite or revert user changes. Make surgical changes only within the requested and authorized scope.
- Do not claim a Google Drive upload or Diary entry unless it was actually completed and verified. When required access is unavailable, record it as pending.

## 3. Handle scientific evidence correctly

- **Verification** checks that code implements the intended equations or agrees with a reference implementation.
- **Calibration** estimates parameters from observations used for fitting.
- **Validation** compares predictions with independent observations. Cross-validation within the calibration experiment is not independent validation; label it accurately.
- For each numerical claim, identify its generating file/script, filters, denominator, units, and rounding. Prefer regenerable outputs and `auditoria_final/auditar_numeros.py`; do not type new values from memory.
- Before using a scenario matrix, inspect the exact CSV and its provenance. Confirm row counts, eligibility flags, versions, groups, and the calculation behind each reported percentage. Do not substitute an older matrix with a similar name.
- Treat negative paired loss as a simulated outcome under the stated formula, not as evidence of a real physiological benefit. Check signs, denominators, and paired controls before interpreting it.
- Confirm references from source material available in the repository or a verifiable primary source. Mark unresolved citations or empirical claims as pending instead of filling gaps.

## 4. Run checks without hidden Git side effects

Before any pipeline command, inspect `ferramentas/pipeline.py`. In the current implementation, every successful stage except `passagem`, including `verificar`, calls `gerar_passagem.py`, stages all files with `git add -A`, commits, and pushes `HEAD:main`. A failed stage also edits memory and regenerates the handoff.

Therefore:

- Never run `python3 ferramentas/pipeline.py ...` as a routine preflight or validation. It can publish changes to `main`.
- Prefer the relevant underlying checks directly, after confirming their commands and required inputs. If a needed check is unavailable, report the exact missing tool/input and continue only with independent checks.
- Do not push or publish unless the user explicitly requests it. Follow the active repository instructions for commits, but verify the branch and staged file list before committing.
- Do not install tools, download datasets, or alter ignored local data without checking the task scope and obtaining user approval when the action is consequential.

## 5. Edit and validate the TCC

- Write in Brazilian Portuguese, following the project's ABNT conventions, clear active phrasing, and the style of TCC I.
- Keep objectives, methods, results, discussion, conclusions, tables, figure captions, and abstracts consistent. Check units, ages, scenario filters, sample sizes, denominators, uncertainty intervals, and cross-references.
- Do not call a result a validation if independence from calibration is unconfirmed. Describe adapted benchmarks and their transfer limitations explicitly.
- Run the smallest relevant tests and the numeric audit when their dependencies and source data are available. For document generation, use the current repository generator and verify all referenced figures resolve; generate PDF only when a PDF renderer is available.
- A failed or unavailable check is not a pass. Report it with the command, exit result, and blocker.

## 6. Close out each task

1. Recheck `git status`, branch, and diff; confirm only intended files changed.
2. Update the relevant files in `memoria/` and `handoff_claude/` when project state or decisions changed. Regenerate `PASSAGEM_DE_BASTAO.md` and `CONTEXTO_EMPACOTADO.md` only when the generator is available and safe to run.
3. Report the branch and commit, changed files, commands and concrete results, generated artifacts, and unresolved blockers. Do not call the TCC final or audited unless the required evidence and checks passed.
