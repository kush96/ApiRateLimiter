import socket
from DummyAPI1 import dummyAPI1
from DummyAPI2 import dummyAPI2
from DummyAPI3 import dummyAPI3
from API4 import api4
from API5 import api5
# import all the API's that the client will use

def Main():
    # Address of Server to which client will connect
    host = '127.0.0.1'
    port = 5555

    # Server socket object to recieve and send api_IDs
    s = socket.socket()
    # Estabilishing connection to server
    s.connect((host, port))

    # recieve message indicating if superuser already logged in
    supUsr_message1 = s.recv(1024)
    if str(supUsr_message1) == 'superuser logged in , pls try again later' :
        print str(supUsr_message1)
        return

    # Ask for user ID
    userID = raw_input('Enter user ID : ')

    # Send user ID to Server
    s.send(userID)

    # If superuser requests log in
    if str(userID) == 'superuser':
        supUsr_message = s.recv(1024)
        print str(supUsr_message)

        while True:
            # Ask superuser if rate limits have to be changed
            inp = raw_input('Do you wish to change rate limit(y/n) : ')
            # If answer == 'n' exit
            if (inp == 'n'):
                break

            # If answer NOT == 'n'
            # Ask for credentials
            print('Enter credentials of user + api(ID) down below')

            # Enter name of user whose rate limit has to be changed
            name = raw_input('Enter name of user : ')
            # send name to server
            s.send(name)
            # get confirmation if name is right
            name_confirm = str(s.recv(1024))
            print name_confirm
            # This loop runs if name doesn't exist in hash map
            while name_confirm == 'name does not exist, please enter valid name!!':
                name = raw_input('Enter name of user : ')
                s.send(name)
                name_confirm = str(s.recv(1024))
                print name_confirm

            # Give api ID to server
            api = input('Enter api ID : ')
            # Check if valid api
            while (api not in [1, 2, 3, 4, 5]):
                print('Enter valid api!!')
                api = input('Enter api ID : ')
            s.send(str(api))

            # Self explanatory ...duh
            print 'Enter new values for user '

            # Ask for new click limit from user
            cLim = raw_input('Enter new click limit : ')
            # Send to server
            s.send(str(cLim))
            # Ask for new refresh time
            rLim = raw_input('Enter new refresh time : ')
            # Send to server
            s.send(str(rLim))

            # Wait for sucess message
            success_message = s.recv(1024)
            # Print success message
            print success_message

    else :
        # Recieve api_ID telling if input is acceptable
        recvd = s.recv(1024)
        # If user logged in then exit program
        print str(recvd)
        if str(recvd) == 'User already logged in!!!':
            return
        # Ask the user which api to use
        api_ID = raw_input('-> choose 1 API (1-5 or \'q\' to quit) ')
        # If api Id not 1-5 or 'q', run this loop
        while api_ID != 'q' and (int(api_ID) > 5 or int(api_ID) < 0):
            print('-> wrong number !!!!!')
            api_ID = raw_input('-> choose 1 API (1-5 or \'q\' to quit) ')

        # If api Id between 1-5 run below loop
        while api_ID != 'q':

            # Tell the server API_ID requested
            s.send(api_ID)

            # Confirmation message if user + api has not run out of click limit
            api_confirm_message = s.recv(1024)
            print('-> Received from server: ' + str(api_confirm_message))

            # If server allows user to use api
            if str(api_confirm_message)  != 'limit exceeded!!!':
                num = int(api_ID)
                if num == 1:
                    dummyAPI1()
                elif num == 2:
                    dummyAPI2()
                elif num == 3:
                    dummyAPI3()
                elif num == 4:
                    api4()
                elif num ==5:
                    api5()

            # Keep asking for API in loop or press q to quit
            api_ID = raw_input('-> choose 1 API (1-5 or \'q\' to quit) ')

            # If api_id is correct, run below code
            while api_ID != 'q' and (int(api_ID) > 5 or int(api_ID) < 0):
                print("-> wrong number !!!!!")
                api_ID = raw_input('-> choose 1 API (1-5 or \'q\' to quit) ')

    # Close server socket
    s.close()

# Runs only if run directly (not imported)
if __name__ == '__main__':
    Main()
