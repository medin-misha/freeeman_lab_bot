# Bot Diagnostic Description Input

## Goal

Before sending a diagnostic file to the backend, collect one free-form text message from the user and store it as diagnostic `description`.

## Scope

- Add a new FSM step in `bot` after file upload and before final confirmation.
- Prompt the user to send one text message containing `ФИО`, `Возраст`, `Город` and optional reflections.
- Pass the text through `DiagnosticsAPI.create_diagnostic(...)` into backend `description`.

## Design

- Flow: user opens diagnostics flow -> sends file -> bot requests one text message -> bot stores it in FSM -> bot asks for final confirmation -> on confirm sends file + description.
- Validation is minimal: accept any non-empty text as-is.
- Retry action resets the collected file and description, then returns the user to the file upload step.

## Risks

- Users may send an incomplete text, but this is accepted by design.
- Non-text content at the description step must be handled with a clear retry prompt.
