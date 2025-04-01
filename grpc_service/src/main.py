import grpc
from concurrent import futures
from service.posts_service import PostService
import posts_service_pb2_grpc as pb2_grpc


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb2_grpc.add_PostServiceServicer_to_server(PostService(), server)
    server.add_insecure_port('[::]:50051')
    print("gRPC server started on port 50051")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
