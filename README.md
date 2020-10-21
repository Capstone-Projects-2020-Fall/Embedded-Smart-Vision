# Module Template
For making new modules, please make a seperate branch off of this branch. The code gives the general structure of a module and will allow
for easier integration with other modules. Development should take place entirelty in the ExampleModule directory (which should be renamed 
to whatever your module is called), and the following three methods need to be implemented in the driver script:
1. __proc_message__ : This is in charge of processing any messages received from other modules. If you plan on using data from other modules, 
this is an especially important method to implement. If your module does not use anything from other modules, this can be ignored.
2. __operation__ : This is where your module performs whatever task it is designed to fulfill and is where you would send messages to other modules.\n
3. __load__ : This is the first method that is called in your module. Here you should handle all initialization of objects/data, which should
be passed to operation when called.

Minfo must also be updated for your module, as the Module name needs to be changed to whatever your module is called and the message code
needs to be changed to allow other modules to communicate with your module. Version should be changed upon stable releases of your module.

Any additional scripts you wish to use when implementing your module MUST be contained in your Module directory
