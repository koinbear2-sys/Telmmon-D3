"""Convert natural-language requests into safe, structured commands.

The interpreter only describes work. It never launches applications, opens
tabs, sends messages, or performs any other side effect.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
import re
from typing import Mapping, Sequence


class CommandType(str, Enum):
    """Supported command categories."""

    OPEN_APPLICATION = "open_application"
    OPEN_APPLICATIONS = "open_applications"
    CREATE_BROWSER_TABS = "create_browser_tabs"
    DRAFT_EMAIL = "draft_email"
    SEND_EMAIL = "send_email"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class Command:
    """A command that a planner or executor can validate before running."""

    type: CommandType
    parameters: Mapping[str, object] = field(default_factory=dict)
    requires_confirmation: bool = False
    source_text: str = ""


class CommandInterpreter:
    """Interpret a small, predictable set of computer-use instructions.

    Matching is intentionally conservative. Requests that do not match a
    supported command are returned as ``UNKNOWN`` instead of being guessed.
    """

    _COUNT_WORDS = {
        "one": 1,
        "two": 2,
        "three": 3,
        "four": 4,
        "five": 5,
        "six": 6,
        "seven": 7,
        "eight": 8,
        "nine": 9,
        "ten": 10,
    }

    def interpret(self, text: str) -> Command:
        """Return a structured command for *text*.

        Empty or unsupported input is represented by ``CommandType.UNKNOWN``.
        """

        source_text = text.strip()
        if not source_text:
            return self._unknown(source_text)

        normalized = re.sub(r"\s+", " ", source_text).lower()

        if re.fullmatch(r"send(?: this)?(?: email| message)?", normalized):
            return Command(
                type=CommandType.SEND_EMAIL,
                requires_confirmation=True,
                source_text=source_text,
            )

        draft_match = re.fullmatch(r"draft an? email to (.+)", normalized)
        if draft_match:
            return Command(
                type=CommandType.DRAFT_EMAIL,
                parameters={"recipient": draft_match.group(1).strip()},
                source_text=source_text,
            )

        tabs_match = re.fullmatch(
            r"open (?:chrome|a browser) and create (\w+) tabs?", normalized
        )
        if tabs_match:
            count = self._parse_count(tabs_match.group(1))
            if count is not None:
                return Command(
                    type=CommandType.CREATE_BROWSER_TABS,
                    parameters={"browser": "chrome", "count": count},
                    source_text=source_text,
                )

        applications = self._parse_application_list(normalized)
        if applications:
            command_type = (
                CommandType.OPEN_APPLICATION
                if len(applications) == 1
                else CommandType.OPEN_APPLICATIONS
            )
            return Command(
                type=command_type,
                parameters={"applications": applications},
                source_text=source_text,
            )

        return self._unknown(source_text)

    def interpret_many(self, texts: Sequence[str]) -> tuple[Command, ...]:
        """Interpret several requests while preserving their input order."""

        return tuple(self.interpret(text) for text in texts)

    def _parse_application_list(self, text: str) -> tuple[str, ...]:
        if not text.startswith("open "):
            return ()

        requested = text[5:].strip()
        parts = re.split(r"\s+and\s+|\s*,\s*", requested)
        applications = tuple(part.strip() for part in parts if part.strip())
        if any("create" in application for application in applications):
            return ()
        return applications

    def _parse_count(self, value: str) -> int | None:
        if value.isdigit():
            count = int(value)
            return count if count > 0 else None
        return self._COUNT_WORDS.get(value)

    def _unknown(self, source_text: str) -> Command:
        return Command(type=CommandType.UNKNOWN, source_text=source_text)


def interpret(text: str) -> Command:
    """Convenience wrapper for callers that need one interpretation."""

    return CommandInterpreter().interpret(text)