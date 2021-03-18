from bson import ObjectId
from flask import *
import random
from flask_pymongo import PyMongo
app = Flask("OneStopShop")
app.config["MONGO_URI"]="mongodb+srv://Ribhav:Ribhav@cluster0.7p7dv.mongodb.net/one-stop-shop-db?retryWrites=true&w=majority"
mongo = PyMongo(app)
app.config['SECRET_KEY'] = 'sOmE_rAnDom_woRd'
mongo.db.cart.drop()


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    elif request.method == "POST":
        u = {}
        for item in request.form:
            u[item] = request.form[item]
        print(u)
        mongo.db.users.insert_one(u)
        flash("Account Created Successfully", "green")
        return redirect("/login")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    elif request.method == "POST":
        u = {'Email': request.form['Email'], 'Password': request.form['Password']}
        found = mongo.db.users.find_one(u)
        if found == None:
            print(u)
            flash("The email or password you entered was incorrect.", "warning")
            return redirect('/login')
        else:
            print("found", found)
            session['user_info'] = {list(found.keys())[x]: list(found.values())[x] for x in range(1, 6)}
            flash('Successful login', "green")
            return redirect('/')

@app.route("/logout", methods=["GET", "POST"])
def logout():
    if request.method == "GET":
        session.pop("user_info")
        return redirect("/login")

@app.route('/index4', methods=['GET','POST'])
def index4():
    if request.method == "GET":
        if 'user_info' in session:
            found_products = mongo.db.products.find()
            fp = list(found_products)
            x=[]
            for f in fp:
                if fp.index(f) < 11:
                    x.append(f)
            print(x)
            return render_template("index4.html", featured = x, products = fp)
        else:
            flash("You must login first", "warning")
            return redirect('/login')
    elif request.method == "POST":
        doc={}
        for item in request.form:
            if int(request.form[item]) != 0:

                doc[item] = request.form[item]
        for docu in doc:
            x=doc.get(docu)
            y = {}
            y[docu] = x
            print(y)
            mongo.db.cart.insert_one(y)


        return redirect('/index4')
@app.route('/', methods=['GET','POST'])
def index():
    if request.method == "GET":
        if 'user_info' in session:
            found_products = mongo.db.products.find()
            fp = list(found_products)
            x = []
            for f in fp:
                if fp.index(f) < 11:
                    x.append(f)
            print(x)
            total = 0
            items = []
            stored_info = list(mongo.db.cart.find())
            for thing in stored_info:
                found_item = mongo.db.products.find_one({'Title': list(thing.keys())[1]})
                items.append(found_item)
            return render_template("index.html", featured=x, p=items, products=fp)
        else:
            flash("You must login first", "warning")
            return redirect('/login')
    elif request.method == "POST":
        print("it works")
        doc={}
        h = ['submit']
        found_products = mongo.db.products.find()
        fp = list(found_products)
        titles = []
        tre = []
        ht = []
        print("request.form")
        print(list(request.form))
        if list(request.form) == h:
            toggle = 1
            items = []
            stored_info = list(mongo.db.cart.find())
            for thing in stored_info:
                print("THING", thing)
                found = mongo.db.products.find_one({"Title" : list(thing.values())[1]})
                print("Thing that not working", found)
                found["Bought"] = list(thing.values())[2]
                found["item-total"] = int(found["Bought"]) * int(found["Price"])
                items.append(found)
            t = dict(request.form)
            print("search results:")
            print(t)
            for item in fp:
                print("item")
                for value in list(t.values()):
                    for values in value:
                        print(item['Title'])
                        if str(values).upper() in str(item['Title']).upper():
                            print("values")
                            print(values)
                            print(item["Title"])
                            tre.append(list(mongo.db.products.find({"Title": item["Title"]})))
            if len(tre) == 0:
                tre = list(found_products)
            print(tre)
            ht = []
            for thing in tre:
                for thi in thing:
                    ht.append(thi)


        else:
            toggle = 0
            print("add to cart")
            for item in request.form:


                if int(request.form[item]) != 0:

                    doc[item] = request.form[item]
            for docu in doc:
                x=doc.get(docu)
                y = {}
                y[docu] = x
                print('y', y)
                items = mongo.db.products.find({"Title" : list(y.keys())[0]})
                print("cart", items)
                items = list(items)
                mongo.db.cart.insert_one({"Title" : list(y.keys())[0], "Bought" : list(y.values())[0] })
                found_products = mongo.db.products.find()
                ht = list(found_products)
        print("ht", ht)
        iteems = []
        stored_cart = mongo.db.cart.find()
        print(stored_cart)
        for thing in list(stored_cart):
            print(thing)
            print(list(thing.values())[1])
            found_item = mongo.db.products.find_one({'Title': list(thing.values())[1]})
            print("found_item")
            print(found_item)
            found_item["Bought"] = list(thing.values())[2]
            found_item['item-total'] = int(found_item['Price']) * int(found_item['Bought'])
            iteems.append(found_item)
        print("Cart Problem", iteems)



        return render_template("index.html", products = ht, p = iteems, toggle = toggle)

@app.route('/buy', methods=['GET','POST'])
def buy():

    if request.method == "GET":
        found_products= mongo.db.products.find()
        fp = list(found_products)
        return render_template("buy.html", products = fp)

    elif request.method == "POST":
        doc={}
        utgru=34
        for item in request.form:
            if int(request.form[item]) != 0:

                doc[item] = request.form[item]
        ##{'Chair': 3}
        ##{'phone': 2}
        for docu in doc:
            x=doc.get(docu)
            y = {}
            y[docu] = x
            print(y)
            mongo.db.cart.insert_one(y)


        return redirect('/buy')

@app.route('/sell', methods=['GET','POST'])
def sell():

    if request.method == "GET":
        if 'user_info' in session:
            return render_template("sell.html")
        else:
            flash("You must login first", "warning")
            return redirect('/login')
    if request.method == "POST":
        info = {}
        for item in request.form:
            info[item] = request.form[item]
        mongo.db.products.insert_one(info)

    return redirect('/sell')
@app.route('/checkout', methods = ['GET', 'POST'])
def checkout():
    if request.method == "GET":

        total = 0
        items = []
        stored_info = mongo.db.cart.find()
        print(stored_info)
        for thing in list(stored_info):
            print(thing)
            print(list(thing.values())[1])
            found_item = mongo.db.products.find_one({'Title': list(thing.values())[1]})
            print("found_item")
            print(found_item)
            found_item["Bought"] = list(thing.values())[2]
            found_item['item-total'] = int(found_item['Price']) * int(found_item['Bought'])
            items.append(found_item)
            total = total + found_item['item-total']
        mongo.db.cart.drop()
        return render_template("checkout.html", products = items, total = total)
    if request.method == "POST":
        return redirect('/')
@app.route('/results')
def results():
    return render_template("results.html")

if __name__ == '__main__':
    app.run(debug=True)