from flask import Flask, render_template, request
from datetime import datetime, timedelta
import smtplib, os
from configparser import ConfigParser
from email.message import EmailMessage

app = Flask(__name__)

def calctimings(vars):
# Calculator for timings for cooking a beef joint
# based on Delia Smith

   weight = float(vars['weight'])
   warmup = timedelta(minutes=int(vars['warmup']))
   standing = timedelta(minutes=int(vars['standing']))
   serve = datetime.strptime(vars['serve'], '%H:%M')

   maincook = timedelta(minutes=int((weight*15*2.2)+15))
   onhigh = timedelta(minutes=20)

   timings = {}
   timings['weight'] = weight
   timings['warmup'] = int(vars['warmup'])
   timings['standing'] = int(vars['standing'])
   timings['maincook'] = int((weight*15*2.2)+15)
   timings['carve'] = serve.strftime('%H:%M')
   timings['outofoven'] = (serve - standing).strftime('%H:%M')
   timings['tempdown'] = (serve - standing - maincook).strftime('%H:%M')
   timings['intooven'] = (serve - standing - maincook - onhigh).strftime('%H:%M')
   timings['ovenon'] = (serve - standing - maincook - onhigh - warmup).strftime('%H:%M')

   return timings

def sendtimings(vars):
   emailconfig = ConfigParser()
   emailconfigfile = os.path.expanduser('~/') + '.cfg/mail.cfg'
   emailconfig.read(emailconfigfile)
   mailserver = emailconfig.get('btmail', 'mailserver')
   mailuser = emailconfig.get('btmail', 'mailuser')
   mailpwd = emailconfig.get('btmail', 'mailpwd')

   msg = EmailMessage()
   msg['Subject'] = 'Beef cooking timings'
   msg['From'] = f"Beef Cooking Calculator <{mailuser}>"
   msg['To'] = 'marek.wolski+cookingbeef@gmail.com,'
   # msg['To'] = 'marek.wolski+cookingbeef@gmail.com,marek.wolski@live.com'

   msgtext = (
      f'<!DOCTYPE html>'
      f'<html>'
      f'<body>'
      f'<h1>Hello! Here are your beef cooking timings:</h1>'
      f'<p>These are based on a joint weight of {vars["weight"]}kg and a desired serving time of {vars["carve"]}.<br>'
      f'It includes {vars["warmup"]} minutes to allow the oven to get to temperature (200\N{DEGREE SIGN}C) '
      f'and {vars["standing"]} minutes resting time before carving.</p>'
      f'<p><b style="font-size: larger;">{vars["ovenon"]}</b> Take the joint out of the fridge. Switch oven on to heat to 200\N{DEGREE SIGN}C.</p>'
      f'<p><b style="font-size: larger;">{vars["intooven"]}</b> Put the beef into the oven, cooking at 200\N{DEGREE SIGN}C for 20 minutes.</p>'
      f'<p><b style="font-size: larger;">{vars["tempdown"]}</b> Turn the oven down to 160\N{DEGREE SIGN}C and cook for a further {vars["maincook"]} minutes.</p>'
      f'<p><b style="font-size: larger;">{vars["outofoven"]}</b> Take the beef out of the oven to rest.</p>'
      f'<p><b style="font-size: larger;">{vars["carve"]}</b> Carve, serve and enjoy!</p>'
      f'<br><hr>'
      f'Beef cooking times requested at {vars["time"]}<br>'
      f'Beef cooking calculator on {os.uname()[1]} (http://192.168.1.44:8081/)'
      f'</body>'
      f'</html>'
   )

   msg.set_content(msgtext, subtype='html')

   with smtplib.SMTP_SSL(mailserver, 465) as server:
      server.login(mailuser, mailpwd)
      server.set_debuglevel(0)
      server.send_message(msg)


@app.route("/ping")
def ping():
   return "Ping! (" + datetime.now().strftime("%Y-%m-%d %H:%M") + ")"


@app.route('/')
def beefcalculator():
    t = {
       'title': 'Beef Cooking: Timing Calculator',
       'time': datetime.now().strftime("%Y-%m-%d %H:%M"),
       'host': os.uname()[1]
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
   t = calctimings(tvalues)
   t['time'] = datetime.now().strftime("%Y-%m-%d %H:%M")
   t['host'] = os.uname()[1]
   t['email1'] = request.args.get('email1') # returns 'None' if not checked
   t['email2'] = request.args.get('email2') # returns 'None' if not checked
   t['email3'] = request.args.get('email3') # returns 'None' if not checked
   sendtimings(t)
   return render_template('beef-times.html', **t)

if __name__ == "__main__":
   app.run(host='0.0.0.0', port=8081, debug=True)
