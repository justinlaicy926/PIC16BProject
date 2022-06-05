---
layout: post
title: webapp development
---

# Web-development

In this project, we would develope a web page that allows users to submit and view messages. Here is the link to the github repo: https://github.com/edwardliu24/web_development

## App.py

First we need to create a py file called app. The file contains several helper functions.

### Preparation

First, we need to import all the modules we need.


```python
import re
from flask import Flask, g, render_template, request, redirect, url_for,abort
import io
import numpy as np
import sqlite3
```


```python
# Create web app, run with flask run
# (set "FLASK_ENV" variable to "development" first!!!)

app = Flask(__name__)
```

### Main page


```python
@app.route('/')

# after running
# $ export FLASK_ENV=development; flask run
# site will be available at 
# http://localhost:5000

def main():
    return render_template('main.html')
```

### Submit Page


```python
#submit page
@app.route('/submit/', methods=['POST', 'GET'])
def submit():
    if request.method == 'GET':
        return render_template('submit.html')
    else:
        try:
            # call the database function if successful submission
            insert_message(request)
            return render_template('submit.html', thanks=True)
        except:
            return render_template('submit.html', error=True)
```

### View Page


```python
@app.route('/view/', methods=['POST','GET'])
def view():
    if request.method == 'GET':
        return render_template('view.html')
    else:
        try:
            output = random_messages(request.form["number"])
            return render_template('view.html',output = output)
        except:
            return render_template('view.html', error = True)
```

### Helper function

Now we have all the pages would be shown on the website. We need to have some helper function to properly run the app.

The first function is to store the messages data. We would create a database using sqlite3.


```python
def get_message_db():
    try:
        return g.message_db
    except:
        g.message_db = sqlite3.connect("messages_db.sqlite")
        cmd = \
        '''
        CREATE TABLE IF NOT EXISTS `messages` (
            id  INTEGER  ,
            handle TEXT,
            message TEXT
        );
        '''
        cursor = g.message_db.cursor()
        cursor.execute(cmd)
        return g.message_db
```

The second function we need is to insert the messages into the data base.


```python
def insert_message(request):
    name = request.form["name"]
    message = request.form["message"]

    conn = get_message_db()
    cursor = conn.cursor()

    cmd1 = "SELECT COUNT(*) FROM message_table"
    cursor.execute(cmd1)
    id = cursor.fetchone()[0] + 1

    insert_cmd = \
    f'''
    INSERT INTO message_table 
    (id, handle, message)
    VALUES
    (?,?,?)
    '''
    data =(id. name, message)
    cursor.execute(insert_cmd,data)

    conn.commit()
    conn.close()
```

The third function is to present the stored messages and handle some edge cases.


```python
def random_messages(n):
    # refer to insert_messages and discussion view function 
    # HINT SQL command - ORDER BY RANDOM()
    conn = get_message_db()
    cursor = conn.cursor()

    length_cmd = "SELECT COUNT(*) FROM message_table"
    cursor.execute(length_cmd)
    num_len = cursor.fetchone()[0]

    output =""

    if (int(n)>num_len):
        output = ("Too many messages :(. This is the best we can do.")
        n = str(num_len)

    cmd = "SELECT * FROM message_table ORDER BY RANDOM() LIMIT" + n

    for row in cursor.execute(cmd): 
        output = output + row[2] + "<br>" + "- " + row[1] + "<br><br>"

    conn.close()

    return output
```

## Webpage Templates

There are four webpages of this app, which are "main","base","view" and "submit", and I would show the "submit" template.

There are first, a text box for submitting a message, second, a text box for submitting the name of the user, and third a “submit” button.
I will also put navigation links inside a base.html template, then have the submit.html template extend base.html.


![png]({{ site.baseurl }}/images/submit.png)

There is somthing wrong with the flask envirnoment on my computer, so I was not able to the style and present the screenshots. I would update all these after fixing the flask issue.
