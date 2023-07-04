This is a Flask application to calculate the cooking times for a joint of beef.
Timings are based on those provided by Delia Smith.

Application is to be run as a systemd service on rasppi4, tcp port 8081.

Needs Flask to be installed.
Needs the .service file to be copied (sudo cp) as /etc/systemd/system/beefcalc.service
    (Look in the .service file for commands to enable, start, stop check logs etc.)
Expects ~/.cfg/mail/cfg to provide the mail server, mail user and mail user password.
