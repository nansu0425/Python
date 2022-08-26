from socket import *
serverName = '127.0.0.1' # 서버 ip 주소, 루프백 사용
serverPort = 12000 # 서버 포트 번호
clientSocket = socket(AF_INET, SOCK_STREAM) # clientSocket이라고 하는 클라이언트의 소켓 생성, AF_INET -> IPv4사용, SOCK_STREAM -> TCP 소켓
clientSocket.connect((serverName, serverPort)) # 클라이언트와 서버 간에 TCP 연결을 시도, 세 방향 핸드셰이크 수행
sentence = input("Input sentence : ") # 문장 입력

# modeNum의 1번은 대문자 변환, 2번은 소문자 변환
if sentence.isupper(): # 문장이 전부 대문자인 경우
    modeNum = '2'
elif sentence.islower(): # 문장이 전부 소문자인 경우
    modeNum = '1'
else: # 문장이 대소문자가 섞여있는 경우
    modeNum = input("1. To upper case\n2. To Lower case\nInput number : ") 

# 문장과 modeNum을 클라이언트 소켓을 통해 TCP 연결로 보낸다
clientSocket.send(sentence.encode())
clientSocket.send(modeNum.encode())
modifiedSentence = clientSocket.recv(1024) # 수정된 문자열을 서버로부터 수신하여 저장
print("Form Server :", modifiedSentence.decode()) # 수정된 문자열 출력
clientSocket.close() # 클라이언트 소켓을 닫는다