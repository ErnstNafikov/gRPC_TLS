import threading
import grpc
protos, services = grpc.protos_and_services("chat.proto")
from grpc._channel import _Rendezvous

# Задайте адрес и порт сервера gRPC
SERVER_ADDRESS = 'grpc-ernst.ddns.net'
SERVER_PORT = 443

# Путь к вашему сертификату сервера (PEM формат)

def run():
    # Загрузка сертификата сервера
    with open('certificate.pem', 'rb') as f:
        trusted_certs = f.read()
    credentials = grpc.ssl_channel_credentials(root_certificates=trusted_certs)
    # Установка соединения с сервером gRPC
    channel = grpc.secure_channel(f"{SERVER_ADDRESS}:{SERVER_PORT}", credentials,  (('grpc.ssl_target_name_override', 'grpc-ernst.ddns.net',),))
    #channel = grpc.insecure_channel(f"{SERVER_ADDRESS}:{SERVER_PORT}")
    stub = services.ChattingStub(channel)
    #threading.Thread(target=_listen_for_messages(stub), daemon=True).start()
    # Цикл будет обрабатывать все пришедшие
    messages = stub.MessageStream(protos.Empty())
    print("Response received:",messages.next().text)
    print("Response received:",messages.next().text)
    channel.close()
        
    
def _listen_for_messages(stub):
    # Цикл будет ждать, пока придут сообщения, обрабатывать все пришедшие и ждать дальше
    try:
        # Вызов метода вашего gRPC сервиса
        response = stub.MessageStream(protos.Empty())
        for message in response:
            print("Response received:",message.author)
    except _Rendezvous as e:
        print("Error:", e.details())
    
if __name__ == '__main__':
    run()