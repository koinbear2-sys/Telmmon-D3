import unittest

from src.ai.interpreter import Command, CommandInterpreter, CommandType


class CommandInterpreterTests(unittest.TestCase):
    def setUp(self) -> None:
        self.interpreter = CommandInterpreter()

    def test_open_application(self) -> None:
        command = self.interpreter.interpret("Open Roblox")

        self.assertEqual(command, Command(
            type=CommandType.OPEN_APPLICATION,
            parameters={"applications": ("roblox",)},
            source_text="Open Roblox",
        ))

    def test_open_multiple_applications(self) -> None:
        command = self.interpreter.interpret("Open Discord and my development environment")

        self.assertEqual(command.type, CommandType.OPEN_APPLICATIONS)
        self.assertEqual(
            command.parameters["applications"],
            ("discord", "my development environment"),
        )

    def test_preserves_application_profile_requests(self) -> None:
        command = self.interpreter.interpret("Open my usual work applications")

        self.assertEqual(command.type, CommandType.OPEN_APPLICATION)
        self.assertEqual(
            command.parameters["applications"],
            ("my usual work applications",),
        )

    def test_create_browser_tabs_supports_word_counts(self) -> None:
        command = self.interpreter.interpret("Open Chrome and create three tabs")

        self.assertEqual(command.type, CommandType.CREATE_BROWSER_TABS)
        self.assertEqual(command.parameters, {"browser": "chrome", "count": 3})

    def test_send_email_requires_confirmation(self) -> None:
        command = self.interpreter.interpret("Send this email")

        self.assertEqual(command.type, CommandType.SEND_EMAIL)
        self.assertTrue(command.requires_confirmation)

    def test_unknown_requests_are_not_guessed(self) -> None:
        command = self.interpreter.interpret("Make everything better")

        self.assertEqual(command.type, CommandType.UNKNOWN)


if __name__ == "__main__":
    unittest.main()