# Diagnostics Description Field

## Goal

Add an optional `description` field to the backend diagnostics model so the API can store and return free-form text attached to a diagnostic record.

## Scope

- Add nullable `description` column to `diagnostics` table.
- Expose `description` in diagnostics pydantic contracts for create, update, and read flows.
- Add a dedicated Alembic migration for the schema change.

## Design

- Storage: use a nullable text field on the SQLAlchemy `Diagnostics` model.
- API contract: `description` is optional and defaults to `None`.
- Migration: add `description` on upgrade and drop it on downgrade.

## Risks

- Existing clients may ignore the new field, which is acceptable because it is optional.
- No data backfill is required because the column is nullable.
