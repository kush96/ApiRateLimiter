import socket
from threading import Thread
from threading import Lock
import pickle
import copy
from rateLimObject import Bucket


def Main():
    # Define all
    global usrLog,lock,usr_lock,exit_lock,supUsr,defSetting
    # IP and Port of Server
    host = '127.0.0.1'
    port = 5555
    # Print on start
    print '*'*40
    print 'server started'
    print '*'*40
    # Lock is a mutex type lock variable
    lock = Lock()                          # Three locks
    usr_lock = Lock()                      # which we have used at various
    exit_lock = Lock()                     # locations within program
    # Initially , superuser not logged in
    # superuser is a special user which can change click limits for
    # normal users.
    supUsr = 0
    # Default settings for the 5 APIs
    defSetting = [
        Bucket(10, 60),  # clickLimit, refreshTime for API1
        Bucket(10, 60),  # clickLimit, refreshTime for API2
        Bucket(10, 60),  # clickLimit, refreshTime for API3
        Bucket(10, 60),  # clickLimit, refreshTime for API4
        Bucket(10, 60),  # clickLimit, refreshTime for API5
        0                # indicates if user logged in already(1 = logged in)
    ]
    # Make socket object for server
    s = socket.socket()
    # s.bind() binds IP and Port for Server
    s.bind((host, port))

    # Keep running this loop to accept connections from different clients
    while (True):
        # Server keeps listening for connections
        s.listen(5)
        # c = socket object for connecting client
        # addr = IP and PORT number of connecting client
        c, addr = s.accept()

        # For every client that connects, make a thread. This way, we can
        # connect multiple clients to the server at once. After making a
        # thread, Main() continues through it's loop looking for new
        # incoming connections .

        # Note : try...except block to catch exception when thread not formed.
        #        Usually thread formed without any hassle and except doesn't
        #        execute
        try:
            Thread(target=client_thread, args=(c, addr)).start()
        except:
            print(" Error in forming thread")


# Each thread formed runs this function
def client_thread(c, addr):
    global usrLog,lock,usr_lock,exit_lock,supUsr

    # If superuser logged in , wait till it logs out
    if supUsr == 1:
        c.send('superuser logged in , pls try again later')
    else:
        c.send('good to go')
    # Print IP + PORT of incoming connections
    print('Connection from: ' + str(addr))

    # Recieve userID from client
    user_ID = c.recv(1024).decode('utf-8')
    # If NULL break
    # Recieved data is NULL when client program shuts down
    if not user_ID:
        return
    # Print User Id
    print 'User ID = '+ str(user_ID) + ' connected!!'

    # If user_ID == superuser
    # run specific program for superuser
    if user_ID == 'superuser':
        # These two locks acquired so that no new user is accepted ,
        # also any user in the middle of using its application becomes
        # unresponsive till superuser logs out
        usr_lock.acquire()
        lock.acquire()
        # try finally block to release locks when superuser logs out
        try:
            # change supUsr = 1 to indicate superuser logged in
            supUsr = 1
            # send message to superuser
            c.send('*'*10 + "Welcome superuser" +'*'*10)

            # Run a loop excepting username that you wish to change rate limit
            # for
            while(True):
                # Recieve from client, the name of user
                name = c.recv(1024)
                if not name:
                    return
                # Check if name valid, if not ask user to enter name again
                while True:
                    if (str(name) in usrLog.keys()) :
                        c.send('valid name entered')
                        break
                    c.send('name does not exist, please enter valid name!!')
                    name = c.recv(1024)
                    if not name:
                        return
                # Recieve API Id for which you wish to change rate limit for
                api= c.recv(1024)
                if not api :
                    return
                # Except new click limit from superuser
                cLim = c.recv(1024)
                if not cLim:
                    return
                # Except new refresh limit from superuser
                rLim = c.recv(1024)
                if not rLim:
                    return
                # Change click limit of user + API combination
                usrLog[str(name)][int(api) - 1] = Bucket(int(cLim),int(rLim))
                # Send success message
                c.send('succesfully changed limit')
        finally:
            # Log out super user
            supUsr = 0
            # Release locks
            usr_lock.release()
            lock.release()
    else:
        # else statement executed when user != superuser

        # acquire lock
        # We used locks here to mantain synchronous use of usrLog. Using the
        # lock we can avoid multiple log ins by same user on different
        # systems
        usr_lock.acquire()
        # try finally again to release lock no matter what
        try:
            # Check for userID in dictionary (Hash map)
            # first 'if' condition executes when userID already exists,
            # and we wish to act on already existing username.
            # 'else' executes when userID doesn't exist. A new key is added
            # to usrLog, and a new defSeting object assigned to it

            # Executed when userID in usrLog keys
            if user_ID in usrLog.keys() :

                # Check if user already logged in
                if usrLog[str(user_ID)][-1] == 0:
                    c.send("Welcome "+ str(user_ID))
                    usrLog[str(user_ID)][-1] = 1
                else :
                    c.send('User already logged in!!!')

            # Executed when userID NOT in usrLog keys
            else:
                # Make a deep copy of defSetting (default settings).
                usrLog[str(user_ID)] = copy.deepcopy(defSetting)
                # Send welcome message to client
                c.send("Welcome "+ str(user_ID))
                # Log in user
                usrLog[str(user_ID)][-1] = 1
        finally:
            # Release locks
            usr_lock.release()


        while(True):
            # Recieve api_ID from client
            api_ID = c.recv(1024).decode('utf-8')
            # If NULL break
            if not api_ID:
                break

            # This locks prevents asynchronous behaviour also.
            # After recieving user_ID and api_ID, we can proceede to check
            # If rate limit for user + API combination is exceeded or not
            lock.acquire()
            try:
                # runs if user has NOT run out of click limits
                if usrLog[str(user_ID)][int(api_ID) - 1].reduce():
                    # Send number of clicks left and seconds to refresh time
                    # to client
                    c.send('clicks left : '+ str(usrLog[str(user_ID)][int(api_ID) - 1].get()[0])
                           + ' time remaining : ' + str(usrLog[str(user_ID)][int(api_ID) - 1].get()[1])
                           + ' seconds' )
                # runs if user has run out of click limits
                else :
                    c.send('limit exceeded!!!')
            finally:
                # release lock
                lock.release()

        # close client socket and log out user
        exit_lock.acquire()
        try:
            usrLog[user_ID][-1] = 0
            c.close()
        finally:
            exit_lock.release()



if __name__ == '__main__':
    try :
        try :
            with open('key_dictionary') as f :
                usrLog = pickle.load(f)
            print 'Number of previous records loaded = ' + str(len(usrLog))
        except :
            usrLog = {}  # Dictionary of users as keys
        Main()
    finally:
        with open('key_dictionary','w') as f:
            pickle.dump(usrLog, f)