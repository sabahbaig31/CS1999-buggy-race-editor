from flask import Flask, render_template, request, jsonify
import sqlite3 as sql

# app - The flask application where all the magical things are configured.
app = Flask(__name__)

# Constants - Stuff that we need to know that won't ever change!
DATABASE_FILE = "database.db"
DEFAULT_BUGGY_ID = "1"
BUGGY_RACE_SERVER_URL = "http://rhul.buggyrace.net"

#------------------------------------------------------------
# the index page
#------------------------------------------------------------
@app.route('/')
def home():
    return render_template('index.html', server_url=BUGGY_RACE_SERVER_URL)

#------------------------------------------------------------
# creating a new buggy:
#  if it's a POST request process the submitted data
#  but if it's a GET request, just show the form
#------------------------------------------------------------
@app.route('/new', methods = ['POST', 'GET'])
def create_buggy():
    if request.method == 'GET':

        con = sql.connect(DATABASE_FILE)
        con.row_factory = sql.Row
        cur = con.cursor()
        cur.execute("SELECT * FROM buggies")
        record = cur.fetchone(); 

        return render_template("buggy-form.html", buggy = record)
    elif request.method == 'POST':
        msg=""
        qty_wheels = request.form['qty_wheels']
        flag_color = request.form['flag_color']
        flag_pattern = request.form['flag_pattern']
        flag_color_secondary = request.form['flag_color_secondary']
        power_type = request.form['power_type']
        power_units = request.form['power_units']
        aux_power_type = request.form['aux_power_type']
        aux_power_units = request.form['aux_power_units']
        hamster_booster = request.form['hamster_booster']
        tyres = request.form['tyres']
        qty_tyres = request.form['qty_tyres']
        armour = request.form['armour']
        attack = request.form['attack']
        qty_attacks = request.form['qty_attacks']
        fireproof = request.form['fireproof']
        insulated = request.form['insulated']
        antibiotic = request.form['antibiotic']
        banging = request.form['banging']
        algo = request.form['algo']

        total_cost = 0
        cost = ""
       
        if fireproof == 'true':
            total_cost += 70

        if insulated == 'true':
            total_cost += 100

        if antibiotic == 'true':
            total_cost += 90

        if banging == 'true':
            total_cost += 42

        if power_type == 'petrol':
            total_cost += (4*int(power_units))
        elif power_type == 'fusion':
            total_cost += (400*int(power_units))
        elif power_type == 'steam':
            total_cost += (3*int(power_units))
        elif power_type == 'bio':
            total_cost += (5*int(power_units))
        elif power_type == 'electric':
            total_cost += (20*int(power_units))
        elif power_type == 'rocket':
            total_cost += (16*int(power_units))
        elif power_type == 'hamster':
            total_cost += (3*int(power_units))
        elif power_type == 'thermo':
            total_cost += (300*int(power_units))
        elif power_type == 'solar':
            total_cost += (40*int(power_units))
        elif power_type == 'wind':
            total_cost += (20*int(power_units))

        if aux_power_type == 'petrol':
            total_cost += (4*int(power_units))
        elif aux_power_type == 'fusion':
            total_cost += (400*int(power_units))
        elif aux_power_type == 'steam':
            total_cost += (3*int(power_units))
        elif aux_power_type == 'bio':
            total_cost += (5*int(power_units))
        elif aux_power_type == 'electric':
            total_cost += (20*int(power_units))
        elif aux_power_type == 'rocket':
            total_cost += (16*int(power_units))
        elif aux_power_type == 'hamster':
            total_cost += (3*int(power_units))
        elif aux_power_type == 'thermo':
            total_cost += (300*int(power_units))
        elif aux_power_type == 'solar':
            total_cost += (40*int(power_units))
        elif aux_power_type == 'wind':
            total_cost += (20*int(power_units))

        if tyres == 'knobbly':
            total_cost += (15*int(qty_tyres))
        elif tyres == 'slick':
            total_cost += (10*int(qty_tyres))
        elif tyres == 'steelband':
            total_cost += (20*int(qty_tyres))
        elif tyres == 'reactive':
            total_cost += (40*int(qty_tyres))
        elif tyres == 'maglev':
            total_cost += (50*int(qty_tyres)) 

        if armour == 'none':
            total_cost += 0*(1+((int(qty_wheels)-4)/10))
        elif armour == 'wood':
            total_cost += 40*(1+((int(qty_wheels)-4)/10))
        elif armour == 'aluminium':
            total_cost += 200*(1+((int(qty_wheels)-4)/10))
        elif armour == 'thinsteel':
            total_cost += 100*(1+((int(qty_wheels)-4)/10))
        elif armour == 'thicksteel':
            total_cost += 200*(1+((int(qty_wheels)-4)/10))
        elif armour == 'titanium':
            total_cost += 290*(1+((int(qty_wheels)-4)/10))
            
        if attack == 'none':
            total_cost += (0*int(qty_attacks))
        elif attack == 'spike':
            total_cost += (5*int(qty_attacks))
        elif attack == 'flame':
            total_cost += (20*int(qty_attacks))
        elif attack == 'charge':
            total_cost += (28*int(qty_attacks))
        elif attack == 'biohazard':
            total_cost += (30*int(qty_attacks))

        cost = f"{total_cost}"
        
       
        try:
            with sql.connect(DATABASE_FILE) as con:
                cur = con.cursor()
                cur.execute(
                    """
                    UPDATE buggies set qty_wheels=?, flag_color=?, flag_pattern=?, flag_color_secondary=?,
                    power_type=?, power_units=?, aux_power_type=?, aux_power_units=?, hamster_booster=?,
                    tyres=?, qty_tyres=?, armour=?, attack=?, qty_attacks=?, fireproof=?, insulated=?,
                    antibiotic=?, banging=?, algo=?, total_cost=? WHERE id=?

                    """,

                    (qty_wheels, flag_color, flag_pattern, flag_color_secondary,
                    power_type, power_units, aux_power_type, aux_power_units, hamster_booster,
                    tyres, qty_tyres, armour, attack, qty_attacks, fireproof, insulated,
                    antibiotic, banging, algo, total_cost, DEFAULT_BUGGY_ID)
                )
                con.commit()
                msg = "Record successfully saved"
                #msg = f"flag_color={flag_color}"
        except:
            con.rollback()
            msg = "error in update operation"
        finally:

            con.close()
        return render_template("updated.html", msg = msg, cost = cost)

#------------------------------------------------------------
# a page for displaying the buggy
#------------------------------------------------------------
@app.route('/buggy')
def show_buggies():
    con = sql.connect(DATABASE_FILE)
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM buggies")
    record = cur.fetchone(); 

    return render_template("buggy.html", buggy = record)

#------------------------------------------------------------
# a placeholder page for editing the buggy: you'll need
# to change this when you tackle task 2-EDIT
#------------------------------------------------------------
@app.route('/edit')
def edit_buggy():
    return render_template("buggy-form.html")

#------------------------------------------------------------
# You probably don't need to edit this... unless you want to ;)
#
# get JSON from current record
#  This reads the buggy record from the database, turns it
#  into JSON format (excluding any empty values), and returns
#  it. There's no .html template here because it's *only* returning
#  the data, so in effect jsonify() is rendering the data.
#------------------------------------------------------------
@app.route('/json')
def summary():
    con = sql.connect(DATABASE_FILE)
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM buggies WHERE id=? LIMIT 1", (DEFAULT_BUGGY_ID))

    buggies = dict(zip([column[0] for column in cur.description], cur.fetchone())).items() 
    return jsonify({ key: val for key, val in buggies if (val != "" and val is not None) })

# You shouldn't need to add anything below this!
if __name__ == '__main__':
    app.run(debug = True, host="0.0.0.0")
