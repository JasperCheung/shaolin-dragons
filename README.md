![4 GIFS 1 WORD](static/img/banner.png)
# Shaolin Dragons Present: **4 GIFS 1 WORD**
Join the hype and play 4 GIFS 1 WORD, the ultimate puzzle game of the 21st century. Choose a category, marvel at four related GIFs, and spell out the word that connects them all together. Each word guessed correctly wins you a whopping 100 points—the more you get, the higher you climb on the rankings. Challenge yourself and your friends to see who can get to the top.

## Features
* Variety of word categories
* Automatic gameplay with both mouse-click and keyboard input
* Gif and word flagging option
* Realtime app statistics
* Saved scores and rankings for authenticated users

## How It Works

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
For your [Giphy](https://developers.giphy.com) API key:
1. Click *Create an App*.
2. Enter account credentials.
3. Enter app name and description (4 GIFS 1 WORD, word puzzle game with gifs.)
4. Your key will appear on your dashboard.

### Start playing
1. Clone the repo by running:
```
$ git clone git@github.com:slau8/shaolin-dragons.git
```
2. With your virtual environment activated, run these commands:
```
$ cd shaolin-dragons
```
3. Add your API key in its appropriate location in ``` .secrets.txt ```. For example:
```
{
  "giphy" : "this_is_my_api_key"
}
```
4. Run the following:
```
$ python app.py
```
You can then view the webpage by opening the URL `localhost:5000` in a web browser.

## Contributors
Jasper Cheung, Shannon Lau, Carol Pan, Helen Ye
