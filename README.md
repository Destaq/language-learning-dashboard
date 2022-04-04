# language-learning-dashboard

A web dashboard you can use to track your time spent learning foreign languages with ease! Log your learning and visually see it mount up up over time!

Built specifically with the Chinese language in mind but applicable to other languages with minor or even no tweaking.

## Image Demonstration

![](/images/whole.png)

|             Light              |               Dark                |
| :----------------------------: | :-------------------------------: |
| ![](/images/light-whole-2.png) |    ![](/images/dark-whole.png)    |
|     ![](/images/goal.png)      |     ![](/images/dark-top.png)     |
|  ![](/images/light-track.png)  | ![](/images/dark-stats-lower.png) |

## Features:

- Detailed and customizable graphs of time spent learning
  - Supports weekly, monthly, and yearly intervals
  - Switch between two views of the graphs - one with learning types (reading, speaking, etc.) and one with specific methods (Anki, TV, Podcast, etc.)
  - See a breakdown with both a bar chart and a pie chart
- Set yourself learning goals
  - ... with deadlines, tracking, and more!
- Automate language logging with the 'Log Data from File' shortcut
  - Option to upload a `.csv` file with your language data instead of manual entry
  - A simple `.txt` file allows for stats updating
- Beautiful themes
  - Both dark mode and light mode are supported and can be toggled at will
- Detailed learning statistics
  - View total study time, vocab size, words read, a daily average, and more!

... and much more for you to discover!

## How to use

This dashboard is built with the following technologies: Python, Flask, Vue, Nuxt, TailwindCSS, and PostgreSQL. It's a bit of an unorthodox setup, so I'll try to explain it as best as I can. Here's how you can go about getting this running on your local machine.

1. Clone or download this repository
2. Ensure you have Python3 and [Node.js](https://nodejs.org/en/download/) installed,
3. Navigate to the `server` folder, which holds the Python code that allows the dashboard to run and store data. Install all requirements with the command `python3 -m pip install -r requirements.txt`.
4. Backend done! Let's make sure that we have a database running. Install Postgres (best done through the [Postgres App](https://postgresapp.com/)) and run the following command in your terminal: `createdb language-learning-dashboard`. If the command does not work, you may have to configure PostgreSQL command line tools, a very simple process described [on the Postgres App page](https://postgresapp.com/documentation/cli-tools.html).
5. We need to link the Python code to the database using Flask-Migrate. Create a file called `.env` in the `server` folder and populate it with the following values:

   ```
   export APP_SETTINGS="config.DevelopmentConfig"
   export DATABASE_URL="postgresql:///language-learning-dashboard"
   export FLASK_APP=app
   ```

   You should also consider putting in the config secret key in the `.env` file and reading from there rather than having it be hardcoded in the code.

   Then, we need to run the `flask db upgrade` command in the `server` folder to link the database to the Python migrations and code.

6. Almost done, let's just create some initial database values. In the `server` folder, run the following command: `python3 scripts/json_postgres_loader.py` (this sets up the chengyu database).
7. Moving onto the frontend: navigate to the `client` folder and run the following command in your terminal: `npm install`. We now have all our dependencies installed. Take care with messing with the `package.json` package versions, there are some dependency clashes with later versions that can't be really resolved.
8. Let's run our frontend and backend! In two terminal windows, run the following commands from the root server:
   ```
   cd client
   npm run dev
   ```
   and
   ```
   cd server
   python3 main.py
   ```

You should now be able to access and use the dashboard at http://localhost:3000. If you'd like to make specific changes to the dashboard, such as Quick Actions, Ability Breakdown, etc. you can just modify the source code, and it will be updated automatically.

Note that on Windows or perhaps Mac, this might still not be enough to get the app running. Try also create a new localStorage key-value pair for localhost:3000 with the following key: `theme` and value: `garden`. Also on Windows you need to set up `DATABASE_URL` in `.env` in the format `postgresql://user:password@localhost:5432/language-learning-dashboard` instead.

As for specifically using the dashboard: most everything is intuitive, though there is one shortcut to point out - the `Log Data from File` shortcut. This button allows you to automate the logging of your language data in three ways.

### Uploading a `.csv` file with your language data.

You can also use the `Log Data from File` shortcut to save yourself from manually inputting logs.

Example file (note dates have to be at the top in the format DD/MM/YY) and file has to be named `track - track.csv` (modify source code to change).

```
,03/28/22,03/29/22,03/30/22,03/31/22
TV,51,70,68,0
Class,65,0,60,0
Pleco,42,35,37,40
Webnovel,76,75,81,112
Audiobook,28,39,67,42
Chat,10,8,7,2
```

Finally, note that you may have to refresh for changes to take effect.

![](images/track-sheets.png)

A simple Google Sheets or Excel spreadsheet does the trick quite neatly. The numbers represent minutes spent on activity per day.

_Note that if you want to add custom activities, you have to define what catgory they belong to in the `server/blueprints/log.py` file._

### Uploading your flashcard files

You can upload a `.txt` file to track the number of unique words/characters you have learned, easily modifiable for other languages. The algorithm works by counting the total number of unique lines in the file (which is what Pleco exports by default for those of you planning on using this to learn Chinese).

Example file (note _must_ be named `pleco.txt`):

```
爱	ai4
八	ba1
爸爸	ba4ba5
杯子	bei1zi5
北京	Bei3jing1
本	ben3
不	bu4
不客气	bu4//ke4qi4
菜	cai4
...
```

### Uploading manual statistics data

Currently four types of manual statistics are supported, as you can see in the statistics in the main image for this repository. You can see what they are in the file below. Filename should be `stats.txt`.

```
# episodes_watched, chapters_read, characters_read, books_read
characters_read	1518000
chapters_read	30
episodes_watched	4
```

For each manual item, type the name on one line, and then press tab, and then type in the value you want to upload. Not all of these are required, but you can't upload a value for an item that doesn't exist. Note that the first time you import this data, it will show up twice - simply refresh the page.

---

Best of luck on your language learning journey! I hope this tool will be of use to you while you're on it.
