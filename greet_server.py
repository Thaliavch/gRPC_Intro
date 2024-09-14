from concurrent import futures
import time
import grpc
import greet_pb2
import greet_pb2_grpc

class GreeterServicer(greet_pb2_grpc.GreeterServicer):
    def SayHello(self, request, context):
        print("Say Hello Request Made:")
        print(request)
        hello_reply = greet_pb2.HelloReply()
        hello_reply.message = f"{request.greeting} {request.name}"
        return hello_reply

    def ParrotSayHello(self, request, context):
        print("Parrot says hello request made")
        print(request)

        for i in range(3):
            parrot_say_hello_reply = greet_pb2.HelloReply()
            parrot_say_hello_reply.message = f"Parrot {request.name} replies that {request.greeting} for the {i} time"
            yield parrot_say_hello_reply
            time.sleep(3)


    def ChattyClientSaysHello(self, request_iterator, context):
        client_say_hello_reply = greet_pb2.DelayedReply()

        for request in request_iterator:
            print(request)
            client_say_hello_reply.request.append(request)

        client_say_hello_reply.message = f"This is the server response. You sent {len(client_say_hello_reply.request)} messages"
        return client_say_hello_reply


    def InteractingHello(self, request_iterator, context):
        for request in request_iterator:
            print("Message received")
            message_response = greet_pb2.HelloReply()
            message_response.message = f"Request Received from {request.name} and the message is {request.greeting}"
            yield message_response


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    greet_pb2_grpc.add_GreeterServicer_to_server(GreeterServicer(), server)
    server.add_insecure_port("localhost:50051")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()