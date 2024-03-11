from flask import Flask
from predictor1 import *
from predictor5 import *
from predictor10 import *

import time
import atexit

from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)

scheduler = BackgroundScheduler()
todayCoins_1 = []
todayCoins_5 = []
todayCoins_10 = []

ai_1 = AI_1()
ai_5 = AI_5()
ai_10 = AI_10()

@app.route('/')
def hello_world():
    buttons_html = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Dashboard</title>
        <style>
            body, html {
                height: 100%;
                margin: 0;
                font-family: Arial, sans-serif;
            }
            .bg {
                /* The image used */
                background-image: url("/static/images/crypto.jpg");

                /* Full height */
                height: 100%;

                /* Center and scale the image nicely */
                background-position: center;
                background-repeat: no-repeat;
                background-size: cover;
            }
            .button-list {
                display: flex;
                flex-direction: row;
                align-items: center;
                justify-content: center;
                margin-top: 20px;
            }
            .button-list form {
                margin: 0 10px;
            }
            button {
                padding: 10px 20px;
                cursor: pointer;
                font-size: 16px;
                background-color: rgba(255,255,255,0.5);
                border: 2px solid black; /* Added black border */
                border-radius: 5px;
            }
            .info-box {
                background-color: rgba(0,0,0,0.6); /* Semi-transparent black background */
                color: white; /* White text color */
                margin: 20px auto; /* Centering the box */
                padding: 20px;
                width: 80%; /* Adjust the width as needed */
                border-radius: 10px; /* Rounded corners */
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.5); /* Shadow for depth */
                text-align: center; /* Center the text */
            }
        </style>
    </head>
    <body class="bg">
    <center>
        <h1>Growth Finder Application </h1>
        <h2>Welcome Trader! Please Select one of the Growth Rates below:</h2>
    </center>
        <div class="button-list">
            <form action="/show_coins_1" method="get"><button type="submit"><b>GR: 1%</b></button></form>
            <form action="/show_coins_5" method="get"><button type="submit"><b>GR: 5%</b></button></form>
            <form action="/show_coins_10" method="get"><button type="submit"><b>GR: 10%</b></button></form>
        </div>
        <div class="info-box">
            Important Reminders: Please check our website at 00:00 (UTC) for the latest predictions. Our forecasts are based on data collected five minutes before each trading candle closes. For best results, consider making trades at exactly 00:00 UTC. If you check later, make sure the cryptocurrency hasn't already hit the predicted growth rate to avoid trading at the wrong time. Remember to set a stop-loss and stick to it. It's also wise to have a clear trading plan, aiming to take profit at the same level as the predicted growth rate from the opening price.
        </div>
    </body>
    </html>
    '''
    return buttons_html




@app.route('/update_coins')
def updateCoins():
    print("coins updated")
    result_1 = ai_1.predict_today(5)
    result_5 = ai_5.predict_today(5)
    result_10 = ai_10.predict_today(5)
    todayCoins_1.clear()
    todayCoins_5.clear()
    todayCoins_10.clear()
    for value1,value5,value10 in zip(result_1, result_5, result_10):
        todayCoins_1.append(value1)
        todayCoins_5.append(value5)
        todayCoins_10.append(value10)
    return f'Updated today_Coins1: {todayCoins_1}, today_Coins5: {todayCoins_5}, today_Coins10: {todayCoins_10}'


@app.route('/show_coins_1')
def showCoins_1():
    result = ""
    # Wrap each value in a <div> that will inherently start on a new line
    for value in todayCoins_1:
        result += f"<div class='coin-value'>{value}</div>"

    # The CSS styles applied to .coin-value ensure each value is displayed in a separate box
    # The updated HTML and CSS to enhance clarity and ensure vertical alignment
    return f'''
<!DOCTYPE html>
<html>
<head>
    <title>Show Coins 1</title>
    <style>
        body, html {{
            height: 100%;
            margin: 0;
            padding: 0;
            font-family: Arial, sans-serif;
            background-image: url("/static/images/crypto.jpg");
            background-position: center;
            background-repeat: no-repeat;
            background-size: cover;
            text-align: center; /* Center the content */
        }}
        .coin-value {{
            margin: 10px auto;
            padding: 20px;
            background-color: rgba(255, 255, 255, 0.8); /* Semi-transparent white background */
            width: 10%; /* Adjust width as needed */
            border: 2px solid #000; /* Black border */
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* Subtle shadow for depth */
            border-radius: 10px; /* Rounded corners */
            display: block; /* Ensure each .coin-value is a block-level element, starting on a new line */
            max-width: 20%; /* Maximum width, adjust as needed */
            box-sizing: border-box; /* Include padding and border in the element's total width and height */
        }}
        h1 {{
            color: black;
            text-shadow: 2px 2px 4px #000; /* Shadow for better readability */
            margin-top: 20px; /* Space from the top */
        }}
    </style>
</head>
<body>
    <h1>Coins with High Probability of Experiencing 1% Growth Today:</h1>
    {result}
</body>
</html>
    '''


@app.route('/show_coins_5')
def showCoins_5():
    result = ""
    # Wrap each value in a <div> that will inherently start on a new line
    for value in todayCoins_5:
        result += f"<div class='coin-value'>{value}</div>"

    return f'''
<!DOCTYPE html>
<html>
<head>
    <title>Show Coins 1</title>
    <style>
        body, html {{
            height: 100%;
            margin: 0;
            padding: 0;
            font-family: Arial, sans-serif;
            background-image: url("/static/images/crypto.jpg");
            background-position: center;
            background-repeat: no-repeat;
            background-size: cover;
            text-align: center; /* Center the content */
        }}
        .coin-value {{
            margin: 10px auto;
            padding: 20px;
            background-color: rgba(255, 255, 255, 0.8); /* Semi-transparent white background */
            width: 10%; /* Adjust width as needed */
            border: 2px solid #000; /* Black border */
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* Subtle shadow for depth */
            border-radius: 10px; /* Rounded corners */
            display: block; /* Ensure each .coin-value is a block-level element, starting on a new line */
            max-width: 20%; /* Maximum width, adjust as needed */
            box-sizing: border-box; /* Include padding and border in the element's total width and height */
        }}
        h1 {{
            color: black;
            text-shadow: 2px 2px 4px #000; /* Shadow for better readability */
            margin-top: 20px; /* Space from the top */
        }}
    </style>
</head>
<body>
    <h1>Coins with High Probability of Experiencing 5% Growth Today:</h1>
    {result}
</body>
</html>
    '''



@app.route('/show_coins_10')
def showCoins_10():
    result = ""
    # Wrap each value in a <div> that will inherently start on a new line
    for value in todayCoins_10:
        result += f"<div class='coin-value'>{value}</div>"

    # The CSS styles applied to .coin-value ensure each value is displayed in a separate box
    # The updated HTML and CSS to enhance clarity and ensure vertical alignment
    return f'''
<!DOCTYPE html>
<html>
<head>
    <title>Show Coins 1</title>
    <style>
        body, html {{
            height: 100%;
            margin: 0;
            padding: 0;
            font-family: Arial, sans-serif;
            background-image: url("/static/images/crypto.jpg");
            background-position: center;
            background-repeat: no-repeat;
            background-size: cover;
            text-align: center; /* Center the content */
        }}
        .coin-value {{
            margin: 10px auto;
            padding: 20px;
            background-color: rgba(255, 255, 255, 0.8); /* Semi-transparent white background */
            width: 10%; /* Adjust width as needed */
            border: 2px solid #000; /* Black border */
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* Subtle shadow for depth */
            border-radius: 10px; /* Rounded corners */
            display: block; /* Ensure each .coin-value is a block-level element, starting on a new line */
            max-width: 20%; /* Maximum width, adjust as needed */
            box-sizing: border-box; /* Include padding and border in the element's total width and height */
        }}
        h1 {{
            color: black;
            text-shadow: 2px 2px 4px #000; /* Shadow for better readability */
            margin-top: 20px; /* Space from the top */
        }}
    </style>
</head>
<body>
    <h1>Coins with High Probability of Experiencing 10% Growth Today:</h1>
    {result}
</body>
</html>
    '''



@app.route('/start_schedule')
def startSchedule():
    updateCoins()
    print("scheduler called")
    scheduler.add_job(func=updateCoins, trigger="interval", seconds=86400)
    scheduler.start()

    # Shut down the scheduler when exiting the app
    atexit.register(lambda: scheduler.shutdown())
    return 'schedule started'


@app.route('/stop_schedule')
def stopSchedule():
    scheduler.shutdown()
    return 'schedule stopped'

startSchedule()
if __name__ == '__main__':
    app.run()