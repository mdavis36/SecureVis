# SecureVis
A smart computer vision driven security system.

# Hardware, Software and System Requirements 

Hardware Requirements

    R-Pi - Edge Device

      CPU : ARM Cortex-A53 1.4GHz

      RAM : 1GB SRAM

      Wifi / Ethernet

    Master System

      CPU : Intel i7-7700k 4.7 GHz

      RAM : 32GB

      GPU : GTX 1080Ti

    Network 

      Protocol: TCP/IP

    Cameras

      Logitech C270 - 720p @ 30fps

      uvcvideo LKM compatible  

  Software Requirements

    OpenCV : v3.3.0

    Yolo : v1-3	

    UVCVideo : Ensure LKM is loaded “# modprobe uvcvideo”

    JDK 8 for Java Application

    Java Swing for UI
    
    Python 3

  Operating System Requirements

    Edge Device

      Raspbian

    Master System

      Linux (e.g. Ubuntu / Arch)


# How to Run SecureVis

Before running any scripts, for the server.py and client.py scripts change the HOST value found on top of both scripts
to your IP address. 

Edge Device
    Run the client.py script in a python3 environment in the following way:
    
    client.py [ROOM_NAME] 1153
    
    Where [ROOM_NAME] can be replaced with the name of the room you'd like to setup, and 1153 is the port SecureVis uses.
    
Master System

    How to run the server module:
       
       Run the server.py script in a python3 environment in the following way:
       
        server.py 1153
        
        Where 1153 is the port we're listening on. 
        
    How to run the GUI:
    
        Using the HTTP link from GitHub, import the project into the eclipse ide (make sure you have the latest version of eclipse with with git extension), and under src/application run Main.java as a java application.
        
    

