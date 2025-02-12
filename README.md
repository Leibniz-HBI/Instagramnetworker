# IgNet - Instagram Networker

The Instagram Networker is a python based scraper for revealing a network structure between users on Instagram. The app has the aim to start with one initial user that you can choose from, scrape a chosen amount of followings/followers and extract their user data. This program is only for public accounts and will recognize private accounts and skip these! 

### Status of the Program:

At the moment you can chose from an initial user account to start and also you can manage the amount of followers/followings to look at. It will save a json file with the initial users data (username, Name, User ID, Number of Followers/Followings) and the links to the the followers and followings. After this step it will visit the the numbers of followings/followers in that list and create the same  json for them. This is a basic loop that is created and can gather massive amounts of information in a short period of time.


### Upcoming Features:

* the aim to add a live plot showing different statistics that can be viewed interactively <br>
* Adding a comment + reply scraper <br>
* Adding hashtag/word analysis possibilities <br>
* Search for a hashtag and scrape the users using it <br>

### How to Use:

_If your are an experienced Python user and you know what to do with the Pipfile, than you may probably want to skip the first 3 steps!_

**1.** This Program requires Python 3. If you haven’t installed Python already, please make sure to visit [the official Python downloads](https://www.python.org/downloads/) and download the package made for your Operating System. 

**2.** After installing Python 3 you will need to install pipenv, which will allow you to install all needed libraries seamlessly. 

Open your Command Line and enter 

`pip install pipenv`

**3.** After installing pipenv you will have to navigate to the Instagram Networkers folder within your command line window. 
After this, enter this following line:

`pipenv install` 

It will automatically take all the information within the delivered pipfile and install these credentials within your personal environment. 

**4.** Download the needed geckodriver for your operating system,  from the geckodriver folder wihtin this repo. Make sure to save the file in the same folder as the main.py file. 

**5.** After installing your environment, you can open the static_data_file.py with a text editor of your choice. In this file you will need to provide your login credentials and essentially: the initial user account to start with and the amount of followers/followings you want to look at.
Taken together these 5 lines need your attention:

	scraperStartProfileUrl = 'https://www.instagram.com/INITIALSERACCOUNT'
	loginUser = YOURUSERNAME
	loginPassword = YOURSUPERSECUREPASSWORD
	followersAmount = 0
	followingsAmount = 5

If you want to only look at the followers or the followings you can go ahead and leave the one you don’t want at 0. Whenever you have you file ready, make sure to save it. 

**6.** Switch back to you command line and and enter

`pipenv run python main.py`

It should now open a firefox window starting the login and scrape process like a human being would do it. If you don’t want to see this window, you can simply go into the main.py file and edit line 26 ‘options.headless = False’ to ’options.headless = True’. It will do the process in the background. 

**7.** Whenever done with the process, the application will create a folder called ‚Outputs’ and save all the .json files within this folder. 

### Workarounds at Timeouts:

Since this application is not an official API wrapper, but a simulator, it is not directly approved by Instagram. Therefore you could have problems with timeouts, if you send to many requests at once. At the moment the bot is automated in the best way for the momentarily designed Instagram Site. This could change, and you could get timeouts or delays.

The way to solve this by going again to the static_data_file and change **„secondsToWait“** to a higher number. We have set it to 8seconds, which gave us no errors at a handful of tests and a 24h run on a AWS server. 

### Questions or Problems?
If any issues should occur, or you have a problem getting the application to run, please open an [issue](https://github.com/Leibniz-HBI/Instagramnetworker/issues). 


Enjoy
