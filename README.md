isn-geiger-client
=================

>>ISN Geiger client receiving analogic-to-numeric data written in Python

<h4>Structure :</h4>
- backend: services writing/sending data
- frontend: services reading/receiving data
- serializable: objects that can be received or sent by communication services
- lib: classes used to create an application structure

<h4>Main.py is the main class, launching this app :</h4>
`````python
global Application

def main():
    services = []
    global Application
    Application = App(AppHandlerImpl(), services)
    Application.start()
    pass

if __name__ == '__main__':
    main()
`````

<h4>Python execution :</h4>
`````shell
##default configFilePath = config.cfg
python Main.py [configFilePath]
`````
