import greet_pb2_grpc
import greet_pb2
import time
import grpc

def get_client_stream_requests():
    while True:
        name = input("Please enter a name or nothing to stop chatting")
        if name == "":
            break

        hello_request = greet_pb2.HelloRequest(greeting="Hello there...", name=name)
        yield hello_request

def sayHello(stub):
    hello_request = greet_pb2.HelloRequest(greeting="Bonjour",
                                           name="Youtube")
    print(stub.SayHello(hello_request))

def parrotSaysHello(stub):
    hello_request = greet_pb2.HelloRequest(greeting="Bonjour",
                                           name="Youtube")
    hello_replies = stub.ParrotSayHello(hello_request);
    for reply in hello_replies:
        print(reply)

def clientSaysHello(stub):
    stream_request = get_client_stream_requests()
    response = stub.ChattyClientSaysHello(stream_request)
    print(response)

def interactiveHello(stub):
    client_message = get_client_stream_requests()
    server_stream_response = stub.InteractingHello(client_message)

    for response in server_stream_response:
        print(response)


def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = greet_pb2_grpc.GreeterStub(channel)
        print("1. SayHello - Unary")
        print("2. ParrotSayHello - Server Side Streaming")
        print("3. ChattyClientSaysHello - Client Side Streaming")
        print("4. InteractingHello - Both Streaming")

        rpc_call = input("Choose an option")

        if rpc_call == "1":
            sayHello(stub)

        elif rpc_call == "2":
            parrotSaysHello(stub)

        elif rpc_call == "3":
            clientSaysHello(stub)

        elif rpc_call == "4":
            interactiveHello(stub)




if __name__ == "__main__":
    run()

