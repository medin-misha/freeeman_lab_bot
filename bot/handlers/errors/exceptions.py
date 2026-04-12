from __future__ import annotations


class BotAppError(Exception):
    """Base exception for bot application errors."""


class UserFacingError(BotAppError):
    def __init__(
        self,
        message_key: str,
        fallback_text: str | None = None,
        *,
        detail: str | None = None,
    ) -> None:
        super().__init__(fallback_text or message_key)
        self.message_key = message_key
        self.fallback_text = fallback_text
        self.detail = detail

    def resolve_message(self, messages: dict[str, str]) -> str:
        return (
            messages.get(self.message_key)
            or self.fallback_text
            or messages.get("server_error")
            or "На стороне сервера произошла ошибка. Пожалуйста, обратитесь в поддержку."
        )


class FileTooLargeError(UserFacingError):
    def __init__(self, *, detail: str | None = None) -> None:
        super().__init__(
            message_key="file_too_large",
            fallback_text="Файл больше 1000 МБ. Сожми его или раздели и отправь снова.",
            detail=detail,
        )


class InvalidDiagnosticFileError(UserFacingError):
    def __init__(self, *, detail: str | None = None) -> None:
        super().__init__(
            message_key="invalid_diagnostic_file",
            fallback_text=(
                "Пришли один файл: голосовое, аудио или документ. "
                "Максимальный размер файла — 1000 МБ."
            ),
            detail=detail,
        )


class InvalidDiagnosticDescriptionError(UserFacingError):
    def __init__(self, *, detail: str | None = None) -> None:
        super().__init__(
            message_key="diagnostic_description_invalid",
            fallback_text="Пришли ответ одним текстовым сообщением.",
            detail=detail,
        )


class SupportRequiredError(BotAppError):
    def __init__(
        self,
        *,
        endpoint: str | None = None,
        status_code: int | None = None,
        detail: str | None = None,
    ) -> None:
        super().__init__(detail or "Support required")
        self.endpoint = endpoint
        self.status_code = status_code
        self.detail = detail
