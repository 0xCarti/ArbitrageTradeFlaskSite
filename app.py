from flask import Flask, render_template, request
from datetime import datetime
import sqlite3

app = Flask(__name__)
list_num_trades = ['5', '10', '25', '50', '100']


@app.route('/')
def home():
    trades_amount = request.args.get('num_trades')
    price_thresh = request.args.get('price_thresh')

    if trades_amount is None:
        trades_amount = 25
    else:
        list_num_trades.remove(trades_amount)
        list_num_trades.insert(0, trades_amount)
        trades_amount = int(trades_amount)

    if price_thresh is None:
        price_thresh = 100.0
    else:
        price_thresh = int(price_thresh)

    # Connect to the database
    conn = sqlite3.connect('watcher/database.db')
    c = conn.cursor()

    # Query the database for the 5 most recent entries in the Trade table
    c.execute(f"SELECT * FROM sqltrade "
              f"WHERE profit >= {price_thresh} "
              f"ORDER BY id DESC "
              f"LIMIT {trades_amount}")
    trades = c.fetchall()

    # Close the connection to the database
    conn.close()
    # Get current date and time
    now = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    # Render the template with the trades data
    return render_template('desktop.html', trades=trades, now=now, list_num_trades=list_num_trades)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug='true')
