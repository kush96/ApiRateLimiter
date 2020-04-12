################           ###############
################           ###############
                              Kush Singh
API Rate Limiter            Lokesh Chhabra
                             Gangesh Dhar
################           ###############
################           ###############

A simple server based API rate limiting application using Python tested and working on Ubuntu 16.06.


*************
Prerequisites
*************
-> Active internet connection (for API requests) 
-> Also working on windows pc
-> Ubuntu 16.06
-> Python 2.7
-> Download and Install Pycharm 
-> Download following python libraries
   a. Pip (version 9.0.1)
   b. Requests (version 2.19.1)
   c. Pickleshare (version 0.7.5)

************
Installation
************

1. Download and install Jetbrains Pycharm lite.

2. In pycharm create new project (File -> make new project) and save it.

3. Download all the files included in the package and save it in this project folder.

4.  From (File- > settings) open (Project -> project interpreter) and ( click “+” button on the top right side) by which you can search and install Pip, Requests and Pickleshare libraries. 

5. After installing libraries come back to ( Project Interpreter and select Python 2.7 as your interpreter).

6. If ( Python 2.7 is not an option then first install python 2.7 in your system and repeat step 5 ) 

7. Further in step 5 click “+” button and set path for python 2.7 executable file which is in usr/bin/python2.7

8. After completing all the above steps restart pycharm.

9. Now open the working project folder, and follow steps to run given below.

********************
Files in the Project
********************

1. client.py
2. Server.py
3. rateLimObject.py
4. DummyAPI1.py
5. DummyAPI2.py
6. DummyAPI3.py
7. API4.py
8. API5.py

*********************
Steps to Run the Code
*********************

1. Open first terminal and type the command python Server.py ( this will run the server)

2. Open second terminal and type the command python client.py (this will run first client)

3. Fill the user_id for the client (which is unique for each client like its phone no)

4. Now it will ask you which API you would like to access( numbered 1 to 5 ).

5. Press any one to access the API or you can press ‘q’ to exit.

6. Every time you access an API it will show number of clicks left and time remaining(which is the refresh time)

7. If you want to change the refresh_time limit or the number of max_clicks type user_id as “superuser” and follow the steps.

8. After completion press n to terminate the process.

9. You can open multiple terminals to access multiple clients at the same time and access their clicks count left.

10. Added file storage system for further functionality to save the userLog data when the Server stops, so that is can be accessed again when the Server restarts.

11.  Interrupt the server using Ctrl C  and after restart, have a look at the size the dictionary.
