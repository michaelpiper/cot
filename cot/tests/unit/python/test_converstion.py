import unittest

from ....ai.domain.models.chat import Chat, UserChat

from ....ai.domain.models.conversation import Conversation


class TestConversation(unittest.TestCase):
    def setUp(self):
        self.conversation = Conversation(
            id="1"
        )

    def test_empty_history(self):
        # Test when history is empty
        result = self.conversation.get_chats_for_prompt()
        self.assertEqual(result, [])

    def test_single_user_message(self):
        # Test with a single user message
        self.conversation.add_chat("user", "text", "Hello")
        result = self.conversation.get_chats_for_prompt()
        expected = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Hello"}
                ]
            }
        ]
        self.assertEqual(result, expected)

    def test_single_assistant_message(self):
        # Test with a single assistant message (should be skipped)
        self.conversation.add_chat("assistant", "text", "Hi there")
        result = self.conversation.get_chats_for_prompt()
        self.assertEqual(result, [])

    def test_mixed_messages(self):
        # Test with mixed user and assistant messages
        self.conversation.add_chat(Chat("Hi there").setType("text").setRole("assistant"))  # Should be skipped
        self.conversation.add_chat("user", "text", "Hello")
        self.conversation.add_chat("assistant", "text", "How can I help you?")
        self.conversation.add_chat("user", "text", "Tell me a joke")
        self.conversation.add_chat("assistant", "text", "Why did the chicken cross the road?")
        result = self.conversation.get_chats_for_prompt()
        expected = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Hello"}
                ]
            },
            {
                "role": "assistant",
                "content": [
                    {"type": "text", "text": "How can I help you?"}
                ]
            },
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Tell me a joke"}
                ]
            },
            {
                "role": "assistant",
                "content": [
                    {"type": "text", "text": "Why did the chicken cross the road?"}
                ]
            }
        ]
        self.assertEqual(result, expected)

    def test_last_parameter(self):
        # Test the `last` parameter to limit the number of chats
        self.conversation.add_chat("user", "text", "Message 1")
        self.conversation.add_chat("assistant", "text", "Reply 1")
        self.conversation.add_chat("user", "text", "Message 2")
        self.conversation.add_chat("assistant", "text", "Reply 2")
        self.conversation.add_chat("user", "text", "Message 3")
        self.conversation.add_chat("assistant", "text", "Reply 3")
        result = self.conversation.get_chats_for_prompt(last=3)
        expected = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Message 3"}
                ]
            },
            {
                "role": "assistant",
                "content": [
                    {"type": "text", "text": "Reply 3"}
                ]
            }
        ]
        self.assertEqual(result, expected)

    def test_skip_non_user_at_start(self):
        self.conversation.add_chat("assistant", "How can I help you?")
        self.conversation.add_chat("user", "What's my balance?")
        self.conversation.add_chat("assistant", "Let me check that for you.")

        # Get the last user message
        last_user_message = self.conversation.get_last_user_message()
        self.assertEqual(last_user_message, "What's my balance?")
        
    def test_skip_non_user_at_start(self):
        # Test skipping non-user messages at the start
        self.conversation.add_chat("assistant", "text", "Hi there")  # Should be skipped
        self.conversation.add_chat("assistant", "text", "How are you?")  # Should be skipped
        self.conversation.add_chat("user", "text", "Hello")
        self.conversation.add_chat("assistant", "text", "How can I help you?")
        result = self.conversation.get_chats_for_prompt()
        expected = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Hello"}
                ]
            },
            {
                "role": "assistant",
                "content": [
                    {"type": "text", "text": "How can I help you?"}
                ]
            }
        ]
        self.assertEqual(result, expected)
    def test_one_user_at_start(self):
        # Test skipping non-user messages at the start
        self.conversation.add_chat(UserChat("Hello").asText())
        result = self.conversation.get_chats_for_prompt(last=10)
        expected = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Hello"}
                ]
            }
        ]
        self.assertEqual(result, expected)

    def test_multiple_messages_same_role(self):
        # Test multiple messages from the same role
        self.conversation.add_chat("user", "text", "Message 1")
        self.conversation.add_chat("user", "text", "Message 2")
        self.conversation.add_chat("assistant", "text", "Reply 1")
        self.conversation.add_chat("assistant", "text", "Reply 2")
        result = self.conversation.get_chats_for_prompt()
        expected = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Message 1"},
                    {"type": "text", "text": "Message 2"}
                ]
            },
            {
                "role": "assistant",
                "content": [
                    {"type": "text", "text": "Reply 1"},
                    {"type": "text", "text": "Reply 2"}
                ]
            }
        ]
        self.assertEqual(result, expected)

if __name__ == "__main__":
    unittest.main()