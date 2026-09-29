# ASTRA-065: Rehearse local release and rollback

[Story index](README.md) · [Progress](../PROGRESS.md)

**Stage:** 11 — Design and delivery  
**Type:** Delivery lab · **Estimate:** 4-8 hours  
**Prerequisites:** [ASTRA-064](ASTRA-064.md), [ASTRA-035](ASTRA-035.md)  
**Read first:** [Stage lesson](../01-lessons/11-design-and-delivery.md)

## User story

As the teammate trying a change, I want a repeatable local release procedure so that I can verify it and recover the previous behavior.

## Starting point and scope

Choose one completed course feature. Use a local practice checkout and test-owned data; cloud deployment is outside this course.

- [Program.cs](../../src/eShop.AppHost/Program.cs)
- [eShop.Web.slnf](../../eShop.Web.slnf)
- [Migrations](../../src/Catalog.API/Infrastructure/Migrations)

## Acceptance criteria

- [ ] The runbook includes prerequisite state, build, local startup, smoke checks, and shutdown.
- [ ] Any migration is identified with its data-preservation and rollback consequences.
- [ ] A return to the previous application version is rehearsed or its exact blocker documented.
- [ ] The runbook avoids deleting unrelated containers, volumes, or uncommitted work.

## Suggested approach

1. Write the procedure before executing it.
2. Use a disposable database if the selected feature changes schema.
3. Have a mentor or structured self-review follow the same steps.

## Verification and evidence

Submit before/after smoke outcomes and the local rollback evidence. Distinguish code rollback from reversing schema or data changes.

## Hints, in order

1. Reverting a commit does not undo data already written.
2. An additive nullable field may allow old code to run without dropping the column.

## Review conversation

Which rollback step has a different risk from simply rebuilding old code? Record the result using the [evidence template](../04-templates/story-evidence.md) and the [definition of done](../00-onboarding/04-first-contribution.md).
