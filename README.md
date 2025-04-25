# Karaoke Web Based
## A fully functional karaoke project written in python(fastapi).

This project is a web based karaoke system with scoring and difficulty settings.

The list below is the functions of the project

Core functions

* song player with audio similarity function

Other functions

* song queue for managing song queues to be played
* song library used to manage songs updating deleting song list
* settings for managing karaoke player configuration
## Prerequisites
* vscode must be installed
* python must already been installed make sure the env variables are added


## Run Locally

Clone the project

```bash
  git clone https://github.com/artjayjay/karaoke_webbased
```

Go to the project directory when opened in vscode

```bash
  cd fastapi_server
```

Install dependencies

```bash
  pip install -r requirements.txt
```

requirements.txt information below

package1==2.0.1  
package2>=2.26.0  
package3  
package4~=1.3.0  
package5<4.0.0

...

just install all package that was missing when running the app

Start the server

```bash
  python app.py
```
## How to use
* put localhost:8000 to browser url
* localhost:8000 <== this is a main server
* localhost:8000/karaokeplayer <== this is a karaokeplayer to another tab
server1 <= use to input main server and server2 for karaokeplayer server



to run use vscode and make sure the python is already installed to the machine or docker
then cd to the fastapiserver directory then run "python app.py"  
this is the dashboard of the app below
![dashboard1](https://github.com/user-attachments/assets/b102cf43-c583-4724-8d15-793195442570)
When clicking search on dashboard this will pop up below
![dashboard2](https://github.com/user-attachments/assets/e8b2a309-1583-4e97-a783-a3328ddfbbc5)
To add song queue just click edit button on table to select the song then click add to queue button  
Just click save to save the changes
![dashboard3](https://github.com/user-attachments/assets/ed562414-fa02-4f29-bd88-304172228429)
![dashboard4](https://github.com/user-attachments/assets/64d71e0d-babb-4e72-a821-927bffe11fb5)
This is the song library tab below
![songlibrary1](https://github.com/user-attachments/assets/9fab59da-c9d3-49a5-b0ea-7e99012016cb)
To add new song input all details on song data form below
![songlibrary1](https://github.com/user-attachments/assets/d8c29d2d-496c-46a3-883d-09b37806585c)
Then click add new button to save to the server the song details  
To update or delete just use update button and delete button
![songlibrary2](https://github.com/user-attachments/assets/1c429385-bf29-4082-ba2d-2f923e798fa4)
To select genre just click dropdown shown below
![songlibrary3](https://github.com/user-attachments/assets/488eb0e3-c802-42fe-b792-91948d0ab797)
This is the settings below to edit if you can enable disable option to show karaoke score
and singers name  
There is as also an option to update score background either using video or picture itself
and also applause sound  
2 servers name can be change one is for main server which is the main karaoke app and second is karaoke player  
to save the changes just click save settings button
![settings1](https://github.com/user-attachments/assets/e7e4501b-a941-4b91-a791-c9895f7498f3)
![settings2](https://github.com/user-attachments/assets/e6006b0c-b17a-4d65-a7b9-de00579ab6d5)
