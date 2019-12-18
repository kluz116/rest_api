from app import app
from flask_mysqldb import MySQL


mysql = MySQL()
 
# MySQL configurations
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Python@2019'
app.config['MYSQL_DB'] = 'bunnystudio'
app.config['MYSQL_HOST'] = 'localhost'
mysql.init_app(app)