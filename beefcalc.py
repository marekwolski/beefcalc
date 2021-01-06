from flask import Flask, render_template, request
from datetime import datetime, timedelta
app = Flask(__name__)

def beefcalc(vars):
# Calculator for timings for cooking a beef joint
# based on Delia Smith

   weight = float(vars['weight'])
   warmup = timedelta(minutes=int(vars['warmup']))
   standing = timedelta(minutes=int(vars['standing']))
   serve = datetime.strptime(vars['serve'], '%H:%M')

   maincook = timedelta(minutes=int((weight*15*2.2)+15))
   onhigh = timedelta(minutes=20)

   beeftimings = {}
   beeftimings['weight'] = weight
   beeftimings['warmup'] = int(vars['warmup'])
   beeftimings['maincook'] = int((weight*15*2.2)+15)
   beeftimings['carve'] = serve.strftime('%H:%M')
   beeftimings['outofoven'] = (serve - standing).strftime('%H:%M')
   beeftimings['tempdown'] = (serve - standing - maincook).strftime('%H:%M')
   beeftimings['intooven'] = (serve - standing - maincook - onhigh).strftime('%H:%M')
   beeftimings['ovenon'] = (serve - standing - maincook - onhigh - warmup).strftime('%H:%M')

   return beeftimings


@app.route("/ping")
def ping():
   return "Ping! (" + datetime.now().strftime("%Y-%m-%d %H:%M") + ")"


@app.route('/')
def beefcalculator():
    t = {
       'title': 'Beef Cooking: Timing Calculator',
       'time': datetime.now().strftime("%Y-%m-%d %H:%M")
    }
    return render_template('beefcalc.html', **t)

@app.route('/beeftimes')
def beeftimes():
   tvalues = {
        'weight': request.args.get('weight'),
        'warmup': request.args.get('warmup'),
        'standing': request.args.get('standing'),
        'serve': request.args.get('serve')
    }
   t = beefcalc(tvalues)
   t['title'] = 'Beef Cooking Timings'
   t['time'] = datetime.now().strftime("%Y-%m-%d %H:%M")
   return render_template('beef-times.html', **t)

if __name__ == "__main__":
   app.run(host='0.0.0.0', port=8081, debug=True)
