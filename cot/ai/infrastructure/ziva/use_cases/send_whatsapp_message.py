
class SendWhatsAppMessageUseCase:
    def __init__(self, to_number, message):
        self.message = message
        self.to_number = to_number
    

    def execute(to_number, message):
        from twilio.rest import Client
        account_sid = "your_account_sid"
        auth_token = "your_auth_token"
        client = Client(account_sid, auth_token)

        message = client.messages.create(
            body=message,
            from_="whatsapp:+14155238886",  # Twilio's WhatsApp sandbox number
            to=f"whatsapp:{to_number}"
        )
        print(f"WhatsApp message sent: {message.sid}")