![4 GIFS 1 WORD](static/img/banner.png)
# Shaolin Dragons Present: **4 GIFS 1 WORD**
Join the hype and play 4 GIFS 1 WORD, the ultimate puzzle game of the 21st century. Choose a category, marvel at four related gifs, and spell out the word that connects them all together. Each word guessed correctly wins you a whopping 100 points—the more you get, the higher you climb on the rankings. Challenge yourself and your friends to see who can get to the top.

**Watch our demo [here](https://youtu.be/aSXudnaZqlw)!**

## Features
* Variety of word categories
* Automatic gameplay with both mouse-click and keyboard input
* Gif zoom popups
* Gif and word flagging option
* Realtime app statistics
* Saved scores and rankings for authenticated users

## How It Works
4 GIFS 1 WORD uses the [Datamuse API](https://www.datamuse.com/api/) to find hyponyms (words of more specific meaning than a general term) of specific hand-picked categories. From a set of hyponyms, a selected keyword is generated, along with four corresponding gifs from the [Giphy API](https://developers.giphy.com).

When a user plays the game, their score and history are saved in database tables so that each round produces fresh, tasteful gifs. Users can additionally flag inaccurate or inappropriate words and gifs.

### Dependencies
* Python 2.7
* Flask
* Requests
* SQLite3
* HTML/CSS

## Getting Started
### Virtual Environment, Flask, and Requests
Flask needs to be installed in order to run this program. It is ideally stored in a virtual environment (venv).

To install a venv called <name>, run these commands in your terminal:
```
$ pip install virtualenv
$ virtualenv <name>
```
On Mac/Linux, start up your venv with:
```
$ . <name>/bin/activate
```
On Windows:
```
$ . <name>/Script/activate
```
In your activated venv, run the following:
```
$ pip install flask
$ pip install requests
```

### SQLite3
Download SQLite3 [here](https://www.sqlite.org/download.html).

### API Configuration
The Giphy API provides a collection of gifs based a query string. 4 GIFS 1 WORD uses this API to retrieve gifs corresponding to a given word.

For your [Giphy](https://developers.giphy.com) API key:
1. Click *Create an App*.
2. Enter account credentials.
3. Enter app name and description (4 GIFS 1 WORD, word puzzle game with gifs).
4. Your key will appear on your dashboard.

Clone the repo and move into it:
```
$ git clone git@github.com:slau8/shaolin-dragons.git
$ cd shaolin-dragons
```
Open ``` .secrets.txt ``` and add your API key in its appropriate location. For example:
```
{
  "giphy" : "this_is_my_api_key"
}
```

#### Troubleshooting
After you run the app, you may receive an error due to one of these issues:
1. Incorrect .secrets.txt format
2. Incorrect API key
3. Exhausted API key

These issues can be fixed by executing the API configuration instructions again. (An exhausted API key may require retrieving a new key).

### Launching the App
With your virtual environment activated, run:
```
$ python app.py
```
You can now view the webpage by opening the URL `localhost:5000` in a web browser.

## Contributors
Jasper Cheung, Shannon Lau, Carol Pan, Helen Ye

| Name        | Role                         |
| ------------|------------------------------|
| Jasper (PM) | Category and word selection  |
| Shannon     | Front-end, game animations   |
| Carol       | Databases, word flagging     |
| Helen       | API processing, gif flagging |
