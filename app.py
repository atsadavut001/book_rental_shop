from os import error
from flask import Flask, flash, redirect, render_template, request, session, jsonify
from flask_session import Session
import sqlite3
from helpers import login_required
import json
import datetime

app = Flask(__name__)

app.secret_key = "sk_book_rental_shop"
app.config["SESSION_TYPE"] = "filesystem"
app.config["TEMPLATES_AUTO_RELOAD"] = True

@app.route("/")
def index_page():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()
    if request.method == "POST":
        if not request.form.get("username"):
            return render_template("login.html", error_massage = "not defined username")

        elif not request.form.get("password"):
            return render_template("login.html", error_massage = "not defined password")
        
        user_admin = []
        user_admin_num = 0
        with sqlite3.connect("book_rental_shop.db") as con:
            cur = con.cursor()
            data = cur.execute("SELECT * FROM users WHERE username = '" + request.form.get("username") + "' AND password = '" + request.form.get("password") + "' AND user_active = 'true'")
            for row in data:
                user_admin_num += 1
                user_admin.append(row)
            con.commit()

        if user_admin_num > 0:
            session["user_id"] = user_admin[0][0]
            session["username"] = user_admin[0][1]
            return redirect("/dashboard")
        else:
            return render_template("login.html", error_massage = "username not found")

    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

# -------------------------------- Dashboard --------------------------------
@app.route("/dashboard")
@login_required
def dashboard():
    rents = []
    with sqlite3.connect("book_rental_shop.db") as con:
        cur = con.cursor()
        data = cur.execute("SELECT rent.rt_id, members.mb_name, rent.rt_status, rent.rt_create_at FROM rent JOIN members on members.mb_id = rent.mb_id ORDER BY rent.rt_create_at DESC")
        for row in data:
            rents.append({
                "id":row[0],
                "member":row[1],
                "status":row[2],
                "date":row[3]
            })
        con.commit()
    return render_template("dashboard.html",rents = rents)

# -------------------------------- Members --------------------------------
@app.route("/member", methods=["GET", "POST"])
@login_required
def member():
    error_status = False
    error_massage = ''
    if request.method == "POST":
        
        if not request.form.get("code"):
            error_status = True
            error_massage = "Add Members not defined code"

        elif not request.form.get("name"):
            error_status = True
            error_massage = "Add Members not defined name"

        elif not request.form.get("credit"):
            error_status = True
            error_massage = "Add Members not defined credit"

        if not error_status:
            with sqlite3.connect("book_rental_shop.db") as con:
                cur = con.cursor()
                check_unique = 0
                for row in cur.execute("SELECT* FROM members WHERE mb_code = '" + request.form.get("code") + "' OR mb_name = '" + request.form.get("name") + "'"):
                    check_unique += 1
                
                if check_unique == 0:
                    data = cur.execute("INSERT INTO members (mb_code, mb_name, mb_credit) VALUES ('" + request.form.get("code") + "', '" + request.form.get("name") + "', '" + request.form.get("credit") + "')")
                else:
                    error_massage = "Add Members Unique"
                con.commit()

    members = []
    with sqlite3.connect("book_rental_shop.db") as con:
        cur = con.cursor()
        data = cur.execute("SELECT * FROM members ORDER BY mb_id DESC")
        for row in data:
            members.append({
                "id":row[0],
                "code":row[1],
                "name":row[2],
                "credit":row[3],
                "active":row[4]
            })
        con.commit()
    return render_template("member.html", members = members, error_massage = error_massage)

@app.route("/member/<int:mb_id>", methods=["GET", "POST"])
@login_required
def member_option(mb_id):
    if request.method == "POST" and request.args.get('credit'):
            with sqlite3.connect("book_rental_shop.db") as con:
               cur = con.cursor()
               data = cur.execute(f"SELECT mb_credit FROM members WHERE mb_code = '{mb_id}'")
               for row in cur.execute(f"SELECT mb_credit FROM members WHERE mb_code = '{mb_id}'"):
                   cur.execute(f"UPDATE members SET mb_credit = '{int(request.args.get('credit')) + int(row[0])}' WHERE mb_code = '{mb_id}'")
               con.commit() 

    elif request.method == "GET" and request.args.get('option') == 'D':
        with sqlite3.connect("book_rental_shop.db") as con:
           cur = con.cursor()
           cur.execute(f"DELETE FROM members WHERE mb_id = '{mb_id}'")
           con.commit()           

    return redirect("/member")

# -------------------------------- Books --------------------------------
@app.route("/books", methods=["GET", "POST"])
@login_required
def books():
    books = []
    error_status = False
    error_massage = ''

    if request.args.get('error_massage'):
        error_massage = request.args.get('error_massage')

    if request.method == "POST":
        
        if not request.form.get("add_name"):
            error_status = True
            error_massage = "Add Book not defined name"

        elif not request.form.get("add_price"):
            error_status = True
            error_massage = "Add Book not defined price"

        elif not request.form.get("add_num"):
            error_status = True
            error_massage = "Add Book not defined num"

        if not error_status:
            with sqlite3.connect("book_rental_shop.db") as con:
                cur = con.cursor()
                check_unique = 0
                for row in cur.execute("SELECT* FROM books WHERE bk_name = '" + request.form.get("add_name") + "'"):
                    check_unique += 1
                
                if check_unique == 0:
                    data = cur.execute("INSERT INTO books (bk_name, bk_price, bk_type, bk_num) VALUES ('" + request.form.get("add_name") + "', '" + request.form.get("add_price") + "', '" + request.form.get("add_type") + "', '" + request.form.get("add_num") + "')")
                else:
                    error_massage = "Add Book Unique"
                con.commit()

    with sqlite3.connect("book_rental_shop.db") as con:
        cur = con.cursor()
        data = cur.execute("SELECT * FROM books ORDER BY bk_id DESC")
        for row in data:
            books.append({
                "id":row[0],
                "name":row[1],
                "price":row[2],
                "type":row[3],
                "num":row[6],
                "active":row[4]
            })
        con.commit()
    return render_template("book.html", books = books, error_massage = error_massage)

@app.route("/books/<int:bk_id>", methods=["GET", "POST"])
@login_required
def books_option(bk_id):
    error_status = False
    error_massage = ''
    if request.method == "POST":
        if not request.form.get("edit_name"):
            error_status = True
            error_massage = "Edit Book not defined name"

        elif not request.form.get("edit_price"):
            error_status = True
            error_massage = "Edit Book not defined price"

        elif not request.form.get("edit_num"):
            error_status = True
            error_massage = "Edit Book not defined num"

        if not error_status:
            with sqlite3.connect("book_rental_shop.db") as con:
                cur = con.cursor()
                check_unique = 0
                for row in cur.execute(f"SELECT * FROM books WHERE bk_name = '{request.form.get('edit_name')}' AND bk_id != '{bk_id}'"):
                    check_unique += 1
                if check_unique == 0:
                    cur.execute(f"UPDATE books SET bk_name = '{request.form.get('edit_name')}', bk_price = '{request.form.get('edit_price')}', bk_type = '{request.form.get('edit_type')}', bk_num = '{request.form.get('edit_num')}' WHERE bk_id = '{bk_id}'")
                else:
                    error_massage = "Edit Book Unique name"
                con.commit() 

    elif request.method == "GET" and request.args.get('option') == 'D':
        with sqlite3.connect("book_rental_shop.db") as con:
           cur = con.cursor()
           print(bk_id)
           cur.execute(f"DELETE FROM books WHERE bk_id = '{bk_id}'")
           con.commit()           

    return redirect(f"/books?error_massage={error_massage}")

# -------------------------------- Rent --------------------------------
@app.route("/rent")
@login_required
def rent():
    rents = []
    with sqlite3.connect("book_rental_shop.db") as con:
        cur = con.cursor()
        data = cur.execute("SELECT rent.rt_id, members.mb_name, rent.rt_status, rent.rt_create_at FROM rent JOIN members on members.mb_id = rent.mb_id ORDER BY rent.rt_create_at DESC")
        for rent in data:
            rents.append({
                "id": rent[0],
                "member": rent[1],
                "status": rent[2],
                "date": rent[3],
                "books": ''
            })
        for index in range(len(rents)):
            items = cur.execute(f"SELECT books.bk_name FROM rent_item JOIN books on books.bk_id = rent_item.bk_id WHERE rent_item.rt_id = '{rents[index]['id']}'")
            books = ''
            for item in items:
                books += f'{item[0]},'
            
            rents[index]['books'] = str(json.dumps(books))

        con.commit()
    return render_template("rent.html",rents = rents)

@app.route("/newrent")
@login_required
def newrent():
    members = []
    books = []
    with sqlite3.connect("book_rental_shop.db") as con:
        cur = con.cursor()
        datab = cur.execute("SELECT * FROM books")
        for row in datab:
            books.append({
                "id":row[0],
                "name":row[1],
                "price":row[2],
                "type":row[3],
                "num":row[6],
                "active":row[4]
            })

        datam = cur.execute("SELECT * FROM members")
        for row in datam:
            members.append({
                "id":row[0],
                "code":row[1],
                "name":row[2],
                "credit":row[3],
                "active":row[4]
            })
        con.commit()

    return render_template("new-rent.html" ,members = members, books = books)

@app.route("/saverent", methods=["POST"])
@login_required
def saverent():
    body = json.loads(request.data)
    books = body['book']
    member = body['member']
    
    rent_price = 0
    for row in books:
        rent_price += int(row['price'])
    
    with sqlite3.connect("book_rental_shop.db") as con:
        cur = con.cursor()

        admin_id = str(session["user_id"])
        cur.execute(f"INSERT INTO rent (mb_id, rt_price, rt_create_at, rt_create_by) VALUES ('{member['id']}', '{rent_price}', '{datetime.datetime.now()}', '{admin_id}')")
        bdObjectRent = cur.execute(f"SELECT rt_id FROM rent WHERE mb_id = '{member['id']}' ORDER BY rt_create_at DESC LIMIT 1")
        for row in bdObjectRent:
            rent_id = row[0]
        for row in books:
            cur.execute(f"INSERT INTO rent_item (rt_id, bk_id) VALUES ('{int(rent_id)}', '{int(row['id'])}')")

        member_credit = 0
        bdObjectMember = cur.execute(f"SELECT mb_credit FROM members WHERE mb_id = '{member['id']}'")
        for row in bdObjectMember:
           member_credit = row[0]
        cur.execute(f"UPDATE members SET mb_credit = '{member_credit - rent_price}' WHERE mb_id = '{member['id']}'")
        
        con.commit()

    return redirect("/rent")

@app.route("/rentchangestatus/<int:rt_id>")
@login_required
def rentchangestatus(rt_id):
    with sqlite3.connect("book_rental_shop.db") as con:
        cur = con.cursor()
        admin_id = str(session["user_id"])
        cur.execute(f"UPDATE rent SET rt_status = 'returned', rt_create_at = '{datetime.datetime.now()}', rt_create_by = '{admin_id}' WHERE rt_id = '{rt_id}'")
    return redirect("/rent")