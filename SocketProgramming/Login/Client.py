from socket import *
serverAddress = '127.0.0.1' # 서버 주소, 루프백 사용
serverPort = 9999 # 서버 포트 번호
clientSocket = socket(AF_INET, SOCK_STREAM) # 클라이언트 소켓 생성, IPv4 사용, TCP 사용
clientSocket.connect((serverAddress, serverPort)) # 서버 연결 시도
loginMsg = '' # 로그인 관련 메시지

# ID와 PW를 입력 후 서버에 전송
def Login(clientSocket):
    id = input("\nID : ")
    pw = input("PW : ")
    clientSocket.send(id.encode())
    clientSocket.send(pw.encode())
    loginMsg = clientSocket.recv(1024).decode() # Login 결과에 대한 메시지 수신
    return loginMsg

# ID와 PW 등록
def Register(clientSocket):
    id = input("\nNew ID : ")
    pw = input("New PW : ")
    clientSocket.send(id.encode())
    clientSocket.send(pw.encode())
    loginMsg = clientSocket.recv(1024).decode() # Register 결과에 대한 메시지 수신
    return loginMsg

# PW 변경
def ChangePw(clientSocket):
    firstPw = input("\nNew PW : ")
    secondPw = input("Reinput PW : ")
    clientSocket.send(firstPw.encode())
    clientSocket.send(secondPw.encode())
    loginMsg = clientSocket.recv(1024).decode() # ChangePw 결과에 대한 메시지 수신
    return loginMsg    

# 로그인과 등록 중 하나 선택
print("\n1. Login\n2. Register")
num = input("Input number : ")

if num == '1' : # 로그인을 선택한 경우
    loginMsg = 'Login'
    clientSocket.send(loginMsg.encode())
elif num == '2' : # 등록을 선택한 경우
    loginMsg = 'Register'
    clientSocket.send(loginMsg.encode())

while True:
    if loginMsg == 'Success': # 로그인 성공
        print("\nLogin success!")
        clientSocket.close()
        break
    elif loginMsg == 'Login': # 로그인 시도
        loginMsg = Login(clientSocket)
    elif loginMsg == 'Register': # 등록
        loginMsg = Register(clientSocket)

        if loginMsg == 'Register':
            print("\nDuplicate ID.. Reinput different ID")
        elif loginMsg == 'Login':
            print("\nID is registered successfully! Input ID and PW for login")
    elif loginMsg == 'ChangePw': # 비밀번호 변경
        loginMsg = ChangePw(clientSocket)

        if loginMsg == 'ChangePw':
            print("\nNew PW and reinputed PW are different.. Reinput PW")
        elif loginMsg == 'Login':
            print("\nPW is changed successfully! Input ID and PW for login")
    elif loginMsg == 'WrongId' : # 입력한 id가 데이터에 없을 때
        print("\nWrong ID..")
        
        # 재입력과 등록 중 선택
        print("\n1. Reinput\n2. Register")
        num = input("Input num : ")

        if (num == '1'): # 로그인을 선택한 경우
            loginMsg = 'Login'
            clientSocket.send(loginMsg.encode())
        elif (num == '2'): # 등록을 선택한 경우
            loginMsg = 'Register'
            clientSocket.send(loginMsg.encode())
    elif loginMsg == 'WrongPw' : # 입력한 pw가 데이터에 없을 때
        print("\nWrong PW..")

        # 재입력과 비밀번호 변경 중 선택
        print("\n1. Reinput\n2. Change PW")
        num = input("Input num : ")

        if num == '1': # 로그인을 선택한 경우
            loginMsg = 'Login'
            clientSocket.send(loginMsg.encode())
        elif num == '2': # 비밀번호 변경을 선택한 경우
            loginMsg = 'ChangePw'
            clientSocket.send(loginMsg.encode())