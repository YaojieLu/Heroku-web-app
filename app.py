import requests
from flask import Flask, render_template, request, redirect
from alpha_vantage.timeseries import TimeSeries
import pandas as pd
from bokeh.plotting import figure
from bokeh.embed import components

def getPlot(plottype, ticker):
    ts = TimeSeries('F22C7VNXIPTIWNIF', output_format='pandas')
    df, _ = ts.get_daily(symbol=ticker)
    df = df.rename(columns={'1. open': 'open', '2. high': 'high',\
                            '3. low': 'low', '4. close': 'close',\
                            '5. volume':'volume'})
    TOOLS = 'pan,wheel_zoom,box_zoom,reset,save'
    if plottype == 'Price':
        inc = df['close'] > df['open']
        dec = df['open'] > df['close']
        w = 12*60*60*1000
        title = ticker + ' candlestick'
        p = figure(x_axis_type='datetime', tools=TOOLS, plot_width=1000,\
                   title=title)
        p.xaxis.major_label_orientation = 3.1415926/4
        p.grid.grid_line_alpha=0.3
        p.segment(df.index, df.high, df.index, df.low, color='black')
        p.vbar(df.index[inc], w, df['open'][inc], df['close'][inc],\
               fill_color='#D5E1DD', line_color='black')
        p.vbar(df.index[dec], w, df['open'][dec], df['close'][dec],\
               fill_color='#F2583E', line_color='black')
    else:
        title = ticker + ' volume'
        p = figure(x_axis_type='datetime', tools=TOOLS, plot_width=1000,\
                   title=title)
        p.xaxis.major_label_orientation = 3.1415926/4
        p.grid.grid_line_alpha=0.3
        p.line(df.index, df.volume, color='black')
    return p

app = Flask(__name__)

@app.route('/')
def main():
    return redirect('/index')

@app.route('/index', methods=['GET','POST'])
def index():
	return render_template('index.html')

@app.route('/graph', methods=['GET','POST'])
def graph():
    ticker=request.form['ticker']
    ticker=ticker.upper()
    plottype = request.form['plottype']

    plot=getPlot(plottype, ticker)

    script, div= components(plot)
    return render_template('graph.html', script=script, div=div)

if __name__ == '__main__':
  app.run(port=33507)