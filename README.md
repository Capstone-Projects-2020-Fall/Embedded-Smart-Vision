# Embedded-Smart-Vision
### Hardware Requirements
Raspberry pi
USB video camera or raspberry pi camera module
LED light and circuit (must be connected to GPIO pin 18 of the raspberry pi) or whatever hardware you need to complete your specified action.

### Building and Running
Before anything, make sure your raspberry pi is fully updated and that python3.7 or later is installed. To do this, use the following commands:

    sudo apt-get update
    sudo apt-get upgrade
    sudo apt-get install python3.7

Pip is also necessary for this software. Follow this guide to set up or upgrade pip https://pip.pypa.io/en/latest/installing/ (Important: pip3 is required, as older versions will not be able to install all necessary dependencies). Once pip and python are installed and up to date, navigate to the software’s base directory wherever it was installed. Using pip, you will install all required dependencies using the provided requirements.txt file. This can be done as follows:

    pip3 install -r requirements.txt

If you plan on using the provided action module or an action that requires the use of GPIO pins, you must do the above step with root permissions (since utilizing GPIO pins requires running scripts with root permissions). To do this, simply add the “sudo” keyword before the command:

    sudo pip3 install -r requirements.txt

If you run into any errors installing the dependencies (notably opencv), you may need to install some linux libraries that the dependencies require in order to function. Once all dependencies are installed you can start the node with the following command:

    python3 main.py

Again, if you are utilizing GPIO pins you will need to run with root permissions and must use the “sudo” keyword.

### Changing Faces
It is likely that you want to change which people the software tries to find in the frame of the camera. To do this, you will want to find the "Faces" directory in the classification module. In this directory, you will find multiple subdirectories, each of which correspond to one person, and a file named "embeddings". Delete any subdirectories of people you don't wish to attempt to classify anymore and add subdirectories for each person you wish to attempt to classify from now on. In the subdirectories, add as many pictures as you would like of the person. Then, from the Classification_Module directory, run the following command:
    
    python3 Create_embeddings.py
    
This will recreate the embeddings and store them in the "embeddings" file mentioned previously. If the software cannot locate the face in a provided picture, it will alert you and delete the picture. Once embeddings are created, run the software as before and your new embeddings will be used instead.

### Connecting to Central Server
This software can run independently and gather data, but there is also the option to connect it (along with other raspberry pi’s) to a central server that gives access to the data from all raspberry pi’s in one location. See https://github.com/Capstone-Projects-2020-Fall/Embedded-Smart-Vision-Server for building the server. Once the server is built and running, you will need to alter the config.json file in the base directory for this application. In this file you must specify the IP address of the central server you wish to connect to. You may also change the node name in order to uniquely identify different nodes. The port should not be altered unless you changed the port in the source code of the Socket Server on the central server. Once the config.json file has been updated, simply running the module with the same command as before will connect it to the central server.

### Monitoring the Application
This application comes with a local web portal that allows you to monitor the data from it. Using it, you can view the live video feed from the node as well as any recorded videos with their accompanying tags. It can be accessed on the raspberry pi itself at the loopback address or on any computer on the same network at the raspberry pi’s internal IP address (use ifconfig to determine the IP address of the raspberry pi). For either address it will accept connections on port 5000. If you are connected to a central server, you can use the central server’s web application to monitor the raspberry pi. It is nearly identical to the local web portal, but is public facing and can only be accessed by using the server’s IP address. Like the web portal, connections will only be accepted on port 5000.
