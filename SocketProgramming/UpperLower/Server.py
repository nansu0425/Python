from socket import *
serverName = '127.0.0.1' # 서버 ip 주소, 루프백 사용
serverPort = 12000 # 서버 포트 번호
serverSocket = socket(AF_INET, SOCK_STREAM) # serverSocket이라고 하는 서버의 소켓 생성, AF_INET -> IPv4사용, SOCK_STREAM -> TCP 소켓
serverSocket.bind((serverName, serverPort)) # 소켓을 포트에 맵핑
serverSocket.listen(1) # 서버가 클라이언트로부터의 TCP 연결 요청을 듣도록 한다, 파라미터는 연결의 최대 수
print("The server is ready to receive")

while True:
    connectionSocket, addr = serverSocket.accept() # 클라이언트의 연결 요청이 들어오면 accept를 호출해서 클라이언트와 연결된 소켓을 생성하고 주소 정보를 리턴
    # 문장과 modeNum 수신
    sentence = connectionSocket.recv(1024).decode()
    modeNum = connectionSocket.recv(1024).decode()

    # modeNum에 따라 문장의 대소문자 변경
    if modeNum == '1':
        modifiedSentence = sentence.upper()
    elif modeNum == '2':
        modifiedSentence = sentence.lower()
    else:
        modifiedSentence = "Error"

    connectionSocket.send(modifiedSentence.encode()) # 클라이언트와 연결된 소켓을 통해 TCP 연결로 보낸다
    connectionSocket.close() # 클라이언트 연결 소켓을 닫는다