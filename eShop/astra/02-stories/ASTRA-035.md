# ASTRA-035: Rehearse a backward-compatible schema addition

[Story index](README.md) · [Progress](../PROGRESS.md)

**Stage:** 6 — Persistence and domain rules  
**Type:** Migration practice · **Estimate:** 3-6 hours  
**Prerequisites:** [ASTRA-034](ASTRA-034.md)  
**Read first:** [Stage lesson](../01-lessons/06-data-and-domain.md)

## User story

As a catalog maintainer, I want an optional merchandising note stored safely so that existing products remain valid during a schema change.

## Starting point and scope

Practice field: nullable MerchandisingNote with a documented length limit. Treat this as a local course feature; the capstone does not depend on the field.

- [CatalogItem.cs](../../src/Catalog.API/Model/CatalogItem.cs)
- [CatalogItemEntityTypeConfiguration.cs](../../src/Catalog.API/Infrastructure/EntityConfigurations/CatalogItemEntityTypeConfiguration.cs)
- [Migrations](../../src/Catalog.API/Infrastructure/Migrations)
- [CatalogApi.cs](../../src/Catalog.API/Apis/CatalogApi.cs)

## Acceptance criteria

- [ ] Existing rows remain readable with a null note after migration.
- [ ] A valid note round-trips through the intended write/read path.
- [ ] Length and null behavior are explicit and enforced at the selected boundaries.
- [ ] The migration, snapshot, and local rollback consequences are reviewed.

## Suggested approach

1. Inspect EF package versions and design-time context creation before choosing tool commands.
2. Update mapping and intended API assignments as well as the model.
3. Generate and apply a migration to a disposable local database, preserving before/after evidence.

## Verification and evidence

Record exact EF tool/project/startup arguments, migration diff, existing-row check, and round-trip functional test. Explain that dropping the new column would lose newly stored notes.

## Hints, in order

1. An API update method can manually copy fields and therefore ignore a new property.
2. Do not assume a migration tool is already installed because EF runtime packages exist.

## Review conversation

How would mixed old and new application versions handle this field? Record the result using the [evidence template](../04-templates/story-evidence.md) and the [definition of done](../00-onboarding/04-first-contribution.md).
