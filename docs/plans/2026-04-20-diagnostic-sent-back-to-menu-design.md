## Goal

After a user sends a diagnostic file successfully, show a single reply keyboard button: `Назад в меню`.

## Scope

- Update the confirmation screen shown after `DiagnosticsAPI().create_diagnostic(...)`.
- Do not change the confirmation text or the flow before the file is sent.

## Chosen Approach

- Add a dedicated reply keyboard with one button: `Назад в меню`.
- Use that keyboard on the success message instead of removing the keyboard entirely.

## Why This Approach

- Matches the requested behavior exactly.
- Keeps the post-submit screen focused on one next action.
- Avoids changing other diagnostic keyboards that are used earlier in the flow.

## Risks

- Minimal. The only behavior change is the presence of one reply button on the final confirmation message.

## Verification

- Send a diagnostic file through the existing flow.
- Confirm the success message still appears.
- Confirm the user sees only the `Назад в меню` button after submission.
