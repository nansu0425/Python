from multiprocessing.dummy import connection
from socket import *
serverAddress = '127.0.0.1' # 서버 주소, 루프백 사용
serverPort = 9999 # 서버 포트 번호
serverSocket = socket(AF_INET, SOCK_STREAM) # 클라이언트 소켓 생성, IPv4 사용, TCP 사용
serverSocket.bind((serverAddress, serverPort)) # 포트를 서버 소켓에 바인딩
serverSocket.listen(1) # 클라이언트 요청 대기, 최대 연결 가능 수 = 1
print("Server is ready to receive")

code = 0
loginData = {} # id와 pw 정보 데이터
loginCode = {1:'Success', 2:'WrongId', 3:'WrongPw', 4:'Login', 5:'Register', 6:'ChangePw'} # login과 관련된 메시지에 매핑된 코드

def CheckLoginData(connectionSocket, inputId, inputPw): # id와 pw 확인
    try:
        if inputPw == loginData[inputId]: # 입력한 id가 데이터에 존재하고 pw가 일치하는 경우
            connectionSocket.send(loginCode[1].encode())
            return 1
        else: # 입력한 id가 데이터에 존재하지만 pw가 일치하지 않는 경우
            connectionSocket.send(loginCode[3].encode())
            return 3
    except KeyError as e: # 입력한 id가 데이터에 존재하지 않는 경우
        connectionSocket.send(loginCode[2].encode())
        return 2

def Register(connectionSocket, inputId, inputPw): # id와 pw 등록
    if inputId in loginData: # 입력한 id가 있는 id인 경우
        connectionSocket.send(loginCode[5].encode())
        return 5
    
    # 입력한 id가 새로운 id인 경우
    loginData[inputId] = inputPw 
    connectionSocket.send(loginCode[4].encode())
    return 4

def ChangePw(connectionSocket, inputId, inputFirstPw, inputSecondPw): # pw 변경
    if inputFirstPw != inputSecondPw: # 처음 입력한 pw와 확인 pw가 다른 경우
        connectionSocket.send(loginCode[6].encode())
        return 6

    # 처음 입력한 pw와 확인 pw가 같은 경우
    loginData[inputId] = inputFirstPw
    connectionSocket.send(loginCode[4].encode())
    return 4

while True:
    connectionSocket, address = serverSocket.accept() # 연결 요청이 들어오면 연결 소켓을 생성하고 주소를 리턴

    # 로그인과 등록 중 선택
    loginMsg = connectionSocket.recv(1024).decode()
    if loginMsg == 'Login': # 로그인인 경우
        code = 4
    elif loginMsg == 'Register': # 등록인 경우
        code = 5

    while True:
        if loginCode[code] == 'Success': # 로그인 성공한 경우
            connectionSocket.close()
            break
        elif loginCode[code] == 'Login': # 로그인 시도
            inputId = connectionSocket.recv(1024).decode() # 입력한 id 수신
            inputPw = connectionSocket.recv(1024).decode() # 입력한 pw 수신
            code = CheckLoginData(connectionSocket, inputId, inputPw) # id와 pw 확인
        elif loginCode[code] == 'Register': # 등록하는 경우
            inputId = connectionSocket.recv(1024).decode() # 입력한 id 수신
            inputPw = connectionSocket.recv(1024).decode() # 입력한 pw 수신
            code = Register(connectionSocket, inputId, inputPw)
        elif loginCode[code] == 'ChangePw': # 비밀번호를 변경하는 경우
            inputFirstPw = connectionSocket.recv(1024).decode() # 입력한 새로운 pw 수신
            inputSecondPw = connectionSocket.recv(1024).decode() # 입력한 확인 pw 수신
            code = ChangePw(connectionSocket, inputId, inputFirstPw, inputSecondPw)
        elif loginCode[code] == 'WrongId': # id가 잘못된 경우
            loginMsg = connectionSocket.recv(1024).decode()

            if loginMsg == 'Login': # 로그인인 경우
                code = 4
            elif loginMsg == 'Register': # 등록인 경우
                code = 5
        elif loginCode[code] == 'WrongPw' : # PW가 잘못된 경우
            loginMsg = connectionSocket.recv(1024).decode()            
            
            if loginMsg == 'Login': # 로그인인 경우
                code = 4
            elif loginMsg == 'ChangePw': # 비밀번호 변경인 경우
                code = 6