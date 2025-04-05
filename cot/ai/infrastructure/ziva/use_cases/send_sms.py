
class SendSMSUseCase:
    def __init__(self,to_number, message) -> None:
        self.account_id = to_number
        self.message = message

    def execute(self):
        from twilio.rest import Client
        account_sid = "your_account_sid"
        auth_token = "your_auth_token"
        client = Client(self.account_sid, auth_token)

        message = client.messages.create(
            body=message,
            from_="+1234567890",  # Your Twilio phone number
            to=self.to_number
        )
        print(f"SMS sent: {message.sid}")
