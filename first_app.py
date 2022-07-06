from flask import Flask, render_template,request,url_for,redirect
import datetime
from flask_mysqldb import MySQL,MySQLdb
import logging

app=Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'esg_db'

mysql = MySQL(app)


#app = Flask(__name__)


@app.route('/')
def hello():
    return render_template('index.html',utc_dt=datetime.datetime.utcnow())

@app.route('/form')
def form():
    return render_template('form.html')

@app.route('/login', methods = ['POST', 'GET'])

def login():
    if request.method == 'GET':
        return "Login via the login Form"
     
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        cursor = mysql.connection.cursor()
        cursor.execute(''' INSERT INTO artists(NAME,TRACK) VALUES(%s,%s)''',(name,age))
        mysql.connection.commit()
        cursor.close()
        return f"Done!!"

@app.route('/select', methods = ['POST', 'GET'])
def select():
    if request.method == 'GET':
        return "Login via the login Form"
     
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        cursor = mysql.connection.cursor()
        cursor.execute(''' INSERT INTO artists(NAME,TRACK) VALUES(%s,%s)''',(name,age))
        mysql.connection.commit()
        cursor.close()
        return f"Done!!"
@app.route("/ii", methods = ["POST", "GET"])
def ii():
    if request.method == "GET":
        return render_template("ii.html", fsizevalue = "hiii")
@app.route("/db", methods = ["POST", "GET"])
def db():
    if request.method == "GET":
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT distinct size_type  FROM  esg_db.etf_table where size_type in('small','medium','large') ")
        output = cur.fetchall()
        #outt=str(output)
        cur.close
        return render_template("db.html", data = output)
        
    elif  request.method == "POST":
        selectt = request.form.get('fsizedropdown')
        if request.form['click_but'] == 'Filter By Size':
            logging.basicConfig(filename='user_log.log', level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

            cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cur.execute("SELECT distinct size_type  FROM  esg_db.etf_table where size_type in('small','medium','large')")
            output = cur.fetchall()
            outt=str(output)
            cur.close
            

            app.logger.info('you have selected filter size'+selectt)
            cur1 = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            print("SELECT fund_short_name, currency, fund_family  FROM  esg_db.etf_table where size_type="+outt)
            cur1.execute("SELECT fund_short_name, currency, fund_family  FROM  esg_db.etf_table where size_type='"+selectt+"'")
            output1 = cur1.fetchall()
            cur1.close
            cur3=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cur3.execute("INSERT into esg_db.user_log (user_name,activity_performed) values('Hardik','Hardik has seleced'%s)",[selectt])
            mysql.connection.commit()
            cur3.close
            return render_template("db.html", fsizevalue = output1,data=output)
        elif request.form['click_but'] == 'Filter By Allocation':
            filterbyalloc = request.form.get('ffundallocation')
            if filterbyalloc=="fund_sector_basic_materials":
                logging.basicConfig(filename='user_log.log', level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
                cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cur.execute("SELECT distinct size_type  FROM  esg_db.etf_table where size_type in('small','medium','large')")
                output = cur.fetchall()
                outt=str(output)
                cur.close
                app.logger.info('filtering by fundallocation on {0}'.format(filterbyalloc))
                cur1 = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                print("SELECT fund_short_name, currency, fund_family  FROM  esg_db.etf_table where size_type='"+filterbyalloc+"'")
                cur1.execute("SELECT t1.fund_short_name,currency,fund_family FROM etf_table t1 where (t1.fund_sector_basic_materials=t1.fund_sector_basic_materials and t1.fund_sector_basic_materials > ISNULL(NULLIF(fund_sector_communication_services,0)) and t1.fund_sector_basic_materials> ISNULL(NULLIF(fund_sector_consumer_cyclical,0)) and t1.fund_sector_basic_materials > ISNULL(NULLIF(fund_sector_consumer_defensive,0)) and t1.fund_sector_basic_materials > ISNULL(NULLIF(fund_sector_energy,0)) and t1.fund_sector_basic_materials > ISNULL(NULLIF(fund_sector_communication_services,0)) and t1.fund_sector_basic_materials > ISNULL(NULLIF(fund_sector_financial_services,0)) and t1.fund_sector_basic_materials > ISNULL(NULLIF(fund_sector_healthcare,0)) and t1.fund_sector_basic_materials > ISNULL(NULLIF(fund_sector_industrials,0)) and t1.fund_sector_basic_materials > ISNULL(NULLIF(fund_sector_real_estate,0)) and t1.fund_sector_basic_materials>ISNULL(NULLIF(fund_sector_technology,0)) and t1.fund_sector_basic_materials >ISNULL(NULLIF(fund_sector_utilities,0))) and t1.fund_sector_basic_materials is not null")
                basicmaterials = cur1.fetchall()
                cur1.close
                cur3=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cur3.execute("INSERT into esg_db.user_log (user_name,activity_performed) values('Hardik','Hardik has seleced filter'%s)",[filterbyalloc])
                mysql.connection.commit()
                cur3.close
                
                return render_template("db.html", fsizevalue = basicmaterials,data=output)
            elif filterbyalloc=="fund_sector_healthcare":

                cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cur.execute("SELECT distinct size_type  FROM  esg_db.etf_table where size_type in('small','medium','large')")
                output = cur.fetchall()
                outt=str(output)
                cur.close
                logging.basicConfig(filename='user_log.log', level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
                cur1 = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                print("SELECT fund_short_name, currency, fund_family  FROM  esg_db.etf_table where size_type='"+filterbyalloc+"'")
                cur1.execute("SELECT t1.fund_short_name,currency,fund_family FROM etf_table t1 where (t1.fund_sector_healthcare=t1.fund_sector_healthcare and t1.fund_sector_healthcare> ISNULL(NULLIF(fund_sector_basic_materials,0)) and t1.fund_sector_healthcare > ISNULL(NULLIF(fund_sector_communication_services,0)) and t1.fund_sector_healthcare> ISNULL(NULLIF(fund_sector_consumer_cyclical,0)) and t1.fund_sector_healthcare > ISNULL(NULLIF(fund_sector_consumer_defensive,0)) and t1.fund_sector_healthcare > ISNULL(NULLIF(fund_sector_energy,0)) and t1.fund_sector_healthcare > ISNULL(NULLIF(fund_sector_communication_services,0)) and t1.fund_sector_healthcare > ISNULL(NULLIF(fund_sector_financial_services,0)) and t1.fund_sector_healthcare > ISNULL(NULLIF(fund_sector_healthcare,0)) and t1.fund_sector_healthcare > ISNULL(NULLIF(fund_sector_industrials,0)) and t1.fund_sector_healthcare > ISNULL(NULLIF(fund_sector_real_estate,0)) and t1.fund_sector_healthcare>ISNULL(NULLIF(fund_sector_technology,0)) and t1.fund_sector_healthcare >ISNULL(NULLIF(fund_sector_utilities,0))) and t1.fund_sector_healthcare is not null")
                basicmaterials = cur1.fetchall()
                cur1.close
                app.logger.info('filtering by fundallocation on {0}'.format(filterbyalloc))

                cur3=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cur3.execute("INSERT into esg_db.user_log (user_name,activity_performed) values('Hardik','Hardik has seleced filter'%s)",[filterbyalloc])
                mysql.connection.commit()
                cur3.close
                return render_template("db.html", fsizevalue = basicmaterials,data=output)

            elif filterbyalloc=="fund_sector_energy":

                cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cur.execute("SELECT distinct size_type  FROM  esg_db.etf_table where size_type in('small','medium','large')")
                output = cur.fetchall()
                outt=str(output)
                cur.close
                logging.basicConfig(filename='user_log.log', level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
                cur1 = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                print("SELECT fund_short_name, currency, fund_family  FROM  esg_db.etf_table where size_type='"+filterbyalloc+"'")
                cur1.execute("SELECT t1.fund_short_name,currency,fund_family FROM etf_table t1 where (t1.fund_sector_energy>ISNULL(NULLIF(fund_sector_industrials,0)) and t1.fund_sector_energy=t1.fund_sector_energy and t1.fund_sector_energy> ISNULL(NULLIF(fund_sector_healthcare,0)) and t1.fund_sector_energy> ISNULL(NULLIF(fund_sector_basic_materials,0)) and t1.fund_sector_energy > ISNULL(NULLIF(fund_sector_communication_services,0)) and t1.fund_sector_energy> ISNULL(NULLIF(fund_sector_consumer_cyclical,0)) and t1.fund_sector_energy > ISNULL(NULLIF(fund_sector_consumer_defensive,0)) and t1.fund_sector_energy > ISNULL(NULLIF(fund_sector_utilities,0)) and t1.fund_sector_energy > ISNULL(NULLIF(fund_sector_communication_services,0)) and t1.fund_sector_energy > ISNULL(NULLIF(fund_sector_financial_services,0)) and t1.fund_sector_energy > ISNULL(NULLIF(fund_sector_healthcare,0))  and t1.fund_sector_energy > ISNULL(NULLIF(fund_sector_real_estate,0)) and t1.fund_sector_energy>ISNULL(NULLIF(fund_sector_technology,0)) and t1.fund_sector_energy >ISNULL(NULLIF(fund_sector_utilities,0))) and t1.fund_sector_energy is not null")
                basicmaterials = cur1.fetchall()
                cur1.close
                app.logger.info('filtering by fundallocation on {0}'.format(filterbyalloc))

                cur3=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cur3.execute("INSERT into esg_db.user_log (user_name,activity_performed) values('Hardik','Hardik has seleced filter'%s)",[filterbyalloc])
                mysql.connection.commit()
                cur3.close
                return render_template("db.html", fsizevalue = basicmaterials,data=output)
    

            elif filterbyalloc=="fund_sector_communication_services":

                cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cur.execute("SELECT distinct size_type  FROM  esg_db.etf_table where size_type in('small','medium','large')")
                output = cur.fetchall()
                outt=str(output)
                cur.close
                logging.basicConfig(filename='user_log.log', level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
                cur1 = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                print("SELECT fund_short_name, currency, fund_family  FROM  esg_db.etf_table where size_type='"+filterbyalloc+"'")
                countofrecords=cur1.execute("SELECT t1.fund_short_name FROM etf_table t1 where (t1.fund_sector_basic_materials< ISNULL(NULLIF(fund_sector_communication_services,0)) and t1.fund_sector_communication_services=t1.fund_sector_communication_services and t1.fund_sector_communication_services> ISNULL(NULLIF(fund_sector_consumer_cyclical,0)) and t1.fund_sector_communication_services > ISNULL(NULLIF(fund_sector_consumer_defensive,0)) and t1.fund_sector_communication_services > ISNULL(NULLIF(fund_sector_energy,0))  and t1.fund_sector_communication_services > ISNULL(NULLIF(fund_sector_financial_services,0)) and t1.fund_sector_communication_services > ISNULL(NULLIF(fund_sector_healthcare,0)) and t1.fund_sector_communication_services > ISNULL(NULLIF(fund_sector_industrials,0)) and t1.fund_sector_communication_services > ISNULL(NULLIF(fund_sector_real_estate,0)) and t1.fund_sector_communication_services>ISNULL(NULLIF(fund_sector_technology,0)) and t1.fund_sector_communication_services >ISNULL(NULLIF(fund_sector_utilities,0))) and t1.fund_sector_communication_services is not null")
                
                print(countofrecords)
                
                commservice = cur1.fetchall()
                cur1.close
                app.logger.info('filtering by fundallocation on {0}'.format(filterbyalloc))
                cur3=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cur3.execute("INSERT into esg_db.user_log (user_name,activity_performed) values('Hardik','Hardik has seleced filter'%s)",[filterbyalloc])
                mysql.connection.commit()
                cur3.close
                return render_template("db.html", fsizevalue = commservice,data=output)    

            elif filterbyalloc=="fund_sector_consumer_cyclical":

                cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cur.execute("SELECT distinct size_type  FROM  esg_db.etf_table where size_type in('small','medium','large')")
                output = cur.fetchall()
                outt=str(output)
                logging.basicConfig(filename='user_log.log', level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
                cur.close
                cur1 = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                print("SELECT fund_short_name, currency, fund_family  FROM  esg_db.etf_table where size_type='"+filterbyalloc+"'")
                cur1.execute("SELECT t1.fund_short_name,currency,fund_family FROM etf_table t1 where (t1.fund_sector_consumer_cyclical> ISNULL(NULLIF(fund_sector_basic_materials,0)) and  t1.fund_sector_consumer_cyclical=t1.fund_sector_consumer_cyclical and t1.fund_sector_consumer_cyclical > ISNULL(NULLIF(fund_sector_communication_services,0)) and t1.fund_sector_communication_services > ISNULL(NULLIF(fund_sector_consumer_defensive,0)) and t1.fund_sector_communication_services > ISNULL(NULLIF(fund_sector_energy,0)) and t1.fund_sector_communication_services > ISNULL(NULLIF(fund_sector_communication_services,0)) and t1.fund_sector_communication_services > ISNULL(NULLIF(fund_sector_financial_services,0)) and t1.fund_sector_communication_services > ISNULL(NULLIF(fund_sector_healthcare,0)) and t1.fund_sector_communication_services > ISNULL(NULLIF(fund_sector_industrials,0)) and t1.fund_sector_communication_services > ISNULL(NULLIF(fund_sector_real_estate,0)) and t1.fund_sector_communication_services>ISNULL(NULLIF(fund_sector_technology,0)) and t1.fund_sector_communication_services >ISNULL(NULLIF(fund_sector_utilities,0))) and t1.fund_sector_communication_services is not null")
                commservice = cur1.fetchall()
                cur1.close
                app.logger.info('filtering by fundallocation on {0}'.format(filterbyalloc))
                cur3=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cur3.execute("INSERT into esg_db.user_log (user_name,activity_performed) values('Hardik','Hardik has seleced filter'%s)",[filterbyalloc])
                mysql.connection.commit()
                cur3.close
                return render_template("db.html", fsizevalue = commservice,data=output)        
            elif filterbyalloc=="fund_sector_consumer_defensive":

                cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cur.execute("SELECT distinct size_type  FROM  esg_db.etf_table where size_type in('small','medium','large')")
                output = cur.fetchall()
                outt=str(output)
                logging.basicConfig(filename='user_log.log', level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
                cur.close
                cur1 = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                print("SELECT fund_short_name, currency, fund_family  FROM  esg_db.etf_table where size_type='"+filterbyalloc+"'")
                cur1.execute("SELECT t1.fund_short_name,currency,fund_family FROM etf_table t1 where (fund_sector_consumer_defensive>ISNULL(NULLIF(t1.fund_sector_consumer_cyclical,0)) and t1.fund_sector_consumer_defensive> ISNULL(NULLIF(fund_sector_basic_materials,0)) and  t1.fund_sector_consumer_defensive=t1.fund_sector_consumer_defensive and t1.fund_sector_consumer_defensive > ISNULL(NULLIF(fund_sector_communication_services,0)) and  t1.fund_sector_consumer_defensive > ISNULL(NULLIF(fund_sector_energy,0)) and t1.fund_sector_consumer_defensive > ISNULL(NULLIF(fund_sector_communication_services,0)) and t1.fund_sector_consumer_defensive > ISNULL(NULLIF(fund_sector_financial_services,0)) and t1.fund_sector_consumer_defensive > ISNULL(NULLIF(fund_sector_healthcare,0)) and t1.fund_sector_consumer_defensive > ISNULL(NULLIF(fund_sector_industrials,0)) and t1.fund_sector_consumer_defensive > ISNULL(NULLIF(fund_sector_real_estate,0)) and t1.fund_sector_consumer_defensive>ISNULL(NULLIF(fund_sector_technology,0)) and t1.fund_sector_consumer_defensive >ISNULL(NULLIF(fund_sector_utilities,0))) and t1.fund_sector_consumer_defensive is not null")
                commservice = cur1.fetchall()
                cur1.close
                app.logger.info('filtering by fundallocation on {0}'.format(filterbyalloc))
                cur3=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cur3.execute("INSERT into esg_db.user_log(user_name,activity_performed) values('Hardik','Hardik has seleced filter'%s)",[filterbyalloc])
                mysql.connection.commit()
                cur3.close
                return render_template("db.html", fsizevalue = commservice,data=output)
            elif filterbyalloc=="fund_sector_industrials":

                cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cur.execute("SELECT distinct size_type  FROM  esg_db.etf_table where size_type in('small','medium','large')")
                output = cur.fetchall()
                outt=str(output)
                logging.basicConfig(filename='user_log.log', level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
                cur.close
                cur1 = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                print("SELECT fund_short_name, currency, fund_family  FROM  esg_db.etf_table where size_type='"+filterbyalloc+"'")
                cur1.execute("SELECT t1.fund_short_name,currency,fund_family FROM etf_table t1 where (t1.fund_sector_industrials=t1.fund_sector_industrials and t1.fund_sector_industrials> ISNULL(NULLIF(fund_sector_healthcare,0)) and t1.fund_sector_industrials> ISNULL(NULLIF(fund_sector_basic_materials,0)) and t1.fund_sector_industrials > ISNULL(NULLIF(fund_sector_communication_services,0)) and t1.fund_sector_industrials> ISNULL(NULLIF(fund_sector_consumer_cyclical,0)) and t1.fund_sector_industrials > ISNULL(NULLIF(fund_sector_consumer_defensive,0)) and t1.fund_sector_industrials > ISNULL(NULLIF(fund_sector_energy,0)) and t1.fund_sector_industrials > ISNULL(NULLIF(fund_sector_communication_services,0)) and t1.fund_sector_industrials > ISNULL(NULLIF(fund_sector_financial_services,0)) and t1.fund_sector_industrials > ISNULL(NULLIF(fund_sector_healthcare,0)) and t1.fund_sector_industrials > ISNULL(NULLIF(fund_sector_industrials,0)) and t1.fund_sector_industrials > ISNULL(NULLIF(fund_sector_real_estate,0)) and t1.fund_sector_industrials>ISNULL(NULLIF(fund_sector_technology,0)) and t1.fund_sector_healthcare >ISNULL(NULLIF(fund_sector_utilities,0))) and t1.fund_sector_healthcare is not null")
                commservice = cur1.fetchall()
                cur1.close
                app.logger.info('filtering by fundallocation on {0}'.format(filterbyalloc))
                cur3=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cur3.execute("INSERT into esg_db.user_log(user_name,activity_performed) values('Hardik','Hardik has seleced filter'%s)",[filterbyalloc])
                mysql.connection.commit()
                cur3.close
                return render_template("db.html", fsizevalue = commservice,data=output)    

            elif filterbyalloc=="fund_sector_real_estate":

                cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cur.execute("SELECT distinct size_type  FROM  esg_db.etf_table where size_type in('small','medium','large')")
                output = cur.fetchall()
                outt=str(output)
                logging.basicConfig(filename='user_log.log', level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
                cur.close
                cur1 = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                print("SELECT fund_short_name, currency, fund_family  FROM  esg_db.etf_table where size_type='"+filterbyalloc+"'")
                cur1.execute("SELECT t1.fund_short_name,currency,fund_family FROM etf_table t1 where (t1.fund_sector_industrials=t1.fund_sector_industrials and t1.fund_sector_industrials> ISNULL(NULLIF(fund_sector_healthcare,0)) and t1.fund_sector_industrials> ISNULL(NULLIF(fund_sector_basic_materials,0)) and t1.fund_sector_industrials > ISNULL(NULLIF(fund_sector_communication_services,0)) and t1.fund_sector_industrials> ISNULL(NULLIF(fund_sector_consumer_cyclical,0)) and t1.fund_sector_industrials > ISNULL(NULLIF(fund_sector_consumer_defensive,0)) and t1.fund_sector_industrials > ISNULL(NULLIF(fund_sector_energy,0)) and t1.fund_sector_industrials > ISNULL(NULLIF(fund_sector_communication_services,0)) and t1.fund_sector_industrials > ISNULL(NULLIF(fund_sector_financial_services,0)) and t1.fund_sector_industrials > ISNULL(NULLIF(fund_sector_healthcare,0)) and t1.fund_sector_industrials > ISNULL(NULLIF(fund_sector_industrials,0)) and t1.fund_sector_industrials > ISNULL(NULLIF(fund_sector_real_estate,0)) and t1.fund_sector_industrials>ISNULL(NULLIF(fund_sector_technology,0)) and t1.fund_sector_industrials >ISNULL(NULLIF(fund_sector_utilities,0))) and t1.fund_sector_industrials is not null")
                commservice = cur1.fetchall()
                cur1.close
                app.logger.info('filtering by fundallocation on {0}'.format(filterbyalloc))
                cur3=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cur3.execute("INSERT into esg_db.user_log (user_name,activity_performed) values('Hardik','Hardik has seleced filter'%s)",[filterbyalloc])
                mysql.connection.commit()
                cur3.close
                return render_template("db.html", fsizevalue = commservice,data=output)        

            elif filterbyalloc=="fund_sector_technology":

                cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cur.execute("SELECT distinct size_type  FROM  esg_db.etf_table where size_type in('small','medium','large')")
                output = cur.fetchall()
                outt=str(output)
                logging.basicConfig(filename='user_log.log', level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
                cur.close
                cur1 = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                print("SELECT fund_short_name, currency, fund_family  FROM  esg_db.etf_table where size_type='"+filterbyalloc+"'")
                cur1.execute("SELECT t1.fund_short_name,currency,fund_family FROM etf_table t1 where (t1.fund_sector_technology>fund_sector_industrials and t1.fund_sector_technology=t1.fund_sector_technology and t1.fund_sector_technology> ISNULL(NULLIF(fund_sector_healthcare,0)) and t1.fund_sector_technology> ISNULL(NULLIF(fund_sector_basic_materials,0)) and t1.fund_sector_technology > ISNULL(NULLIF(fund_sector_communication_services,0)) and t1.fund_sector_technology> ISNULL(NULLIF(fund_sector_consumer_cyclical,0)) and t1.fund_sector_technology > ISNULL(NULLIF(fund_sector_consumer_defensive,0)) and t1.fund_sector_technology > ISNULL(NULLIF(fund_sector_energy,0)) and t1.fund_sector_technology > ISNULL(NULLIF(fund_sector_communication_services,0)) and t1.fund_sector_technology > ISNULL(NULLIF(fund_sector_financial_services,0)) and t1.fund_sector_technology > ISNULL(NULLIF(fund_sector_healthcare,0)) and t1.fund_sector_technology > ISNULL(NULLIF(fund_sector_industrials,0)) and t1.fund_sector_technology > ISNULL(NULLIF(fund_sector_real_estate,0)) and t1.fund_sector_technology>ISNULL(NULLIF(fund_sector_technology,0)) and t1.fund_sector_technology >ISNULL(NULLIF(fund_sector_utilities,0))) and t1.fund_sector_technology is not null")
                commservice = cur1.fetchall()
                cur1.close
                app.logger.info('filtering by fundallocation on {0}'.format(filterbyalloc))
                cur3=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cur3.execute("INSERT into esg_db.user_log(user_name,activity_performed) values('Hardik','Hardik has seleced filter'%s)",[filterbyalloc])
                mysql.connection.commit()
                cur3.close
                return render_template("db.html", fsizevalue = commservice,data=output)            
            elif filterbyalloc=="fund_sector_utilities":

                cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cur.execute("SELECT distinct size_type  FROM  esg_db.etf_table where size_type in('small','medium','large')")
                output = cur.fetchall()
                outt=str(output)
                logging.basicConfig(filename='user_log.log', level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
                cur.close
                cur1 = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                print("SELECT fund_short_name, currency, fund_family  FROM  esg_db.etf_table where size_type='"+filterbyalloc+"'")
                cur1.execute("SELECT t1.fund_short_name,currency,fund_family FROM etf_table t1 where (t1.fund_sector_utilities>ISNULL(NULLIF(fund_sector_industrials,0)) and t1.fund_sector_utilities=t1.fund_sector_utilities and t1.fund_sector_utilities> ISNULL(NULLIF(fund_sector_healthcare,0)) and t1.fund_sector_utilities> ISNULL(NULLIF(fund_sector_basic_materials,0)) and t1.fund_sector_utilities > ISNULL(NULLIF(fund_sector_communication_services,0)) and t1.fund_sector_utilities> ISNULL(NULLIF(fund_sector_consumer_cyclical,0)) and t1.fund_sector_utilities > ISNULL(NULLIF(fund_sector_consumer_defensive,0)) and t1.fund_sector_utilities > ISNULL(NULLIF(fund_sector_energy,0)) and t1.fund_sector_utilities > ISNULL(NULLIF(fund_sector_communication_services,0)) and t1.fund_sector_technology > ISNULL(NULLIF(fund_sector_financial_services,0)) and t1.fund_sector_technology > ISNULL(NULLIF(fund_sector_healthcare,0))  and t1.fund_sector_technology > ISNULL(NULLIF(fund_sector_real_estate,0)) and t1.fund_sector_technology>ISNULL(NULLIF(fund_sector_technology,0))) and t1.fund_sector_utilities is not null")
                commservice = cur1.fetchall()
                cur1.close
                app.logger.info('filtering by fundallocation on {0}'.format(filterbyalloc))
                cur3=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cur3.execute("INSERT into esg_db.user_log (user_name,activity_performed) values('Hardik','Hardik has seleced filter'%s)",[filterbyalloc])
                mysql.connection.commit()
                cur3.close
                return render_template("db.html", fsizevalue = commservice,data=output)                
if __name__ == "__main__":
    app.run()