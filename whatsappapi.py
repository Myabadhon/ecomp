from twilio.rest import Client

sid = "AC2c1a77273403f41ede9e00a43bee36c7"
authToken = "5a53dc6fba3ddd9428ba3eafe9545a83"
client = Client(sid, authToken)

sender_number = "whatsapp:+14155238886"
receiver_number = "whatsapp:+8801953636469"
message = "Hello Mukti Apu, Thanks for the Center Fruit"
messages = client.messages.create(to=receiver_number, from_=sender_number, body=message)
