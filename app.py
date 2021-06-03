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
        if not qty_wheels.isdigit():
            msg = f"Error: 'Number of wheels:{qty_wheels}' is not a number"
            return render_template("updated.html", msg = msg)

        flag_color = request.form['flag_color']
        if flag_color[0] != '#':
            msg = f"Error: 'Colour of flag:{flag_color}' is not a valid colour code"
            return render_template("updated.html", msg = msg)

        flag_pattern = request.form['flag_pattern']
        patterns = ['Plain', 'Vertical stripes', 'Horizontal stripes', 'Diagonal stripes', 'Checkered', 'Spots']
        if flag_pattern.isdigit():
            msg = f"Error: 'Pattern on flag:{flag_pattern}' is not a valid string"
            return render_template("updated.html", msg = msg)

        flag_color_secondary = request.form['flag_color_secondary']
        if flag_color_secondary[0] != '#':
            msg = f"Error: 'Colour of flag:{flag_color_secondary}' is not a valid colour code"
            return render_template("updated.html", msg = msg)

        power_type = request.form['power_type']
        if power_type.isdigit():
            msg = f"Error: 'Primary motive power:{power_type}' is not a valid string"
            return render_template("updated.html", msg = msg)

        power_units = request.form['power_units']
        if not power_units.isdigit():
            msg = f"Error: 'Primary motive power units:{power_units}' is not a number"
            return render_template("updated.html", msg = msg)

        aux_power_type = request.form['aux_power_type']
        if aux_power_type.isdigit():
            msg = f"Error: 'Auxiliary motive power:{aux_power_type}' is not a valid string"
            return render_template("updated.html", msg = msg)

        aux_power_units = request.form['aux_power_units']
        if not aux_power_units.isdigit():
            msg = f"Error: 'Auxiliary motive power units:{aux_power_units}' is not a number"
            return render_template("updated.html", msg = msg)

        hamster_booster = request.form['hamster_booster']
        if not hamster_booster.isdigit():
            msg = f"Error: 'Hamster booster:{hamster_booster}' is not a number"
            return render_template("updated.html", msg = msg)

        tyres = request.form['tyres']
        if tyres.isdigit():
            msg = f"Error: 'Type of tyres:{tyres}' is not a valid string"
            return render_template("updated.html", msg = msg)

        qty_tyres = request.form['qty_tyres']
        if not qty_tyres.isdigit():
            msg = f"Error: 'Number of tyres:{qty_tyres}' is not a number"
            return render_template("updated.html", msg = msg)

        armour = request.form['armour']
        if armour.isdigit():
            msg = f"Error: 'Armour:{armour}' is not a valid string"
            return render_template("updated.html", msg = msg)

        attack = request.form['attack']
        if attack.isdigit():
            msg = f"Error: 'Offensive capability:{attack}' is not a valid string"
            return render_template("updated.html", msg = msg)

        qty_attacks = request.form['qty_attacks']
        if not qty_attacks.isdigit():
            msg = f"Error: 'Number of attacks:{qty_attacks}' is not a number"
            return render_template("updated.html", msg = msg)

        fireproof = request.form['fireproof']
        bool_vals = ['true', 'false']
        if fireproof not in bool_vals:
            msg = f"Error: 'Fireproof?:{fireproof}' is not valid input"
            return render_template("updated.html", msg = msg)

        insulated = request.form['insulated']
        if insulated not in bool_vals:
            msg = f"Error: 'Insulated?:{insulated}' is not valid input"
            return render_template("updated.html", msg = msg)

        antibiotic = request.form['antibiotic']
        if antibiotic not in bool_vals:
            msg = f"Error: 'Antibiotic?:{antibiotic}' is not valid input"
            return render_template("updated.html", msg = msg)

        banging = request.form['banging']
        if banging not in bool_vals:
            msg = f"Error: 'Banging?:{banging}' is not valid input"
            return render_template("updated.html", msg = msg)

        algo = request.form['algo']
        if algo.isdigit():
            msg = f"Error: 'Race computer algorithm:{algo}' is not a valid string"
            return render_template("updated.html", msg = msg)

        if flag_color == flag_color_secondary:
            msg = "Error: The buggy you just created violates Flag design rule number 1. Please try again."
            return render_template("updated.html", msg = msg)

        if not int(qty_wheels) % 2 == 0:
            msg = "Error: The buggy you just created violates Wheels and tyres rule number 1. Please try again."
            return render_template("updated.html", msg = msg)

        if qty_tyres < qty_wheels:
            msg = "Error: The buggy you just created violates Wheels and tyres rule number 2. Please try again."
            return render_template("updated.html", msg = msg)

        non_cons_pow = ["fusion", "thermo", "solar", "wind"]

        if power_type in non_cons_pow and int(power_units) > 1:
            msg = "Error: The buggy you just created violates Power rule number 1. Please try again."
            

        elif aux_power_type in non_cons_pow and int(aux_power_units) > 1:
            msg = msg + "Error: The buggy you just created violates Backup power rule number 1. Please try again."
            return render_template("updated.html", msg = msg)

        if not power_type == "hamster" and int(hamster_booster) > 0:
            msg = "Error: The buggy you just created violates Hamster booster rule number 1. Please try again."
            return render_template("updated.html", msg = msg)

        if not aux_power_type == "hamster" and int(hamster_booster) > 0:
            msg = "Error: The buggy you just created violates Hamster booster rule number 1. Please try again."
            return render_template("updated.html", msg = msg)




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


@app.route('/rules')
def display_rules():
    return render_template("rules.html")

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
