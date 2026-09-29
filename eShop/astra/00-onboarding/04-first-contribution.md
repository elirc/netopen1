# Make your first contribution

A contribution is complete when a reviewer can understand its purpose, inspect the change, and reproduce the relevant checks. A large diff is not evidence of learning.

## Start with a bounded task

Choose ASTRA-005 for your first documentation change. Read the current text, reproduce the discrepancy, and propose an exact correction. For code stories, state the user-visible behavior first and list three acceptance cases before editing.

The repository's [contribution guide](../../CONTRIBUTING.md) accepts small fixes directly as PRs and asks for discussion on larger suggestions. Course assignments are practice proposals. You may complete them in a local branch or your fork without submitting each to the upstream project.

## Establish a safe branch

```powershell
git status --short
git branch --show-current
git remote -v
git switch -c astra/ASTRA-005-onboarding-note
```

Inspect the status before branching. A new branch does not isolate existing uncommitted files; they remain in the working tree. Do not overwrite them. If you need to change the same file, coordinate or use a clean checkout. Keep local workbooks separate from someone else's modifications.

For sequential stories, start the next branch from the reviewed previous result when there is a dependency. For independent exercises, branch from your chosen course baseline. Record that choice. A later story can require both an earlier skill and its actual code change.

## Work in small steps

1. Reproduce the current behavior and capture the command, input, or screenshot.
2. Read the nearest production code and existing test style.
3. Add a regression test when behavior changes warrant one. Verify it fails for the intended reason.
4. Make the smallest cohesive change.
5. Run the relevant checks and inspect the complete diff.

For a documentation correction, preview Markdown and verify its links and commands; do not create a code test to assert a sentence. For a domain rule, use an existing unit-test project. For binding, routing, or SQL behavior, use functional tests. The [test lesson](../01-lessons/07-testing-strategy.md) explains the boundary.

## Review exactly what will be committed

```powershell
git diff --check
git diff
git add -- astra/workbook/onboarding-note.md
git diff --cached
git status --short
git commit -m "docs: record reproducible eShop onboarding steps"
```

The staged path above is an example: replace it with the actual file you changed. Stage explicit files or use `git add -p`; do not stage unrelated work. A commit should tell one coherent story. Never commit dashboard login URLs, `.env`, test authentication state, or copied secrets.

## Prepare a reviewable PR

Use [the PR template](../04-templates/pull-request.md). Lead with the concrete problem and resulting behavior. Include scope, acceptance evidence, test commands and outcomes, and any known limitation.

Example:

> The onboarding note used the README's .NET 9 prerequisite, which conflicts with the SDK selected in this checkout. The updated note points new contributors to global.json and the web solution filter. Verified the source links and recorded the SDK and build outcomes.

Only say “verified” for checks you performed. “Not run: Docker unavailable” is useful evidence; “all good” is not.

To share, push your branch to a remote you control and open a draft PR, or give a mentor the local diff. Inspect the remote before pushing. This course does not assume your fork exists or that you have upstream write access.

## Respond to review

For each comment, identify the behavior or maintainability concern. Ask for an example if the requested outcome is unclear. Make a focused follow-up commit and reply with what changed and how it was checked. Explain tradeoffs when you disagree.

A mentor may ask you to remove extra abstraction, change a test input, or separate two concerns. That is part of the exercise. Do not rewrite shared branch history without coordinating. For a local bad edit, inspect a file's diff before restoring it; for an already shared commit, a targeted follow-up or revert preserves the history.

## Definition of done for this course

- The story's acceptance criteria have evidence.
- Changed behavior has suitable automated coverage, plus manual evidence where needed.
- Relevant checks have recorded outcomes; blockers are explicit.
- The diff contains no unrelated edits or generated credentials.
- You can explain the code, the test boundary, and one tradeoff.
- The reviewer or your structured self-review has accepted the result.

Use ASTRA-006 to rehearse the review cycle before moving into C# and test work.
