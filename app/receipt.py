from flask import Blueprint, url_for, redirect, render_template, flash, request, session
from app.models import Receipt
from app.models import Item
from flask_login import login_required
from app import db
from datetime import datetime

receipts = Blueprint('receipts', __name__)


@receipts.route("/receipt", methods=["GET", "POST"])
@login_required
def receipt():
    if request.method == "POST":
        # receipt = request.form
        receiptdate = request.form.get("receiptdate")
        receiptdate = datetime.strptime(receiptdate, "%Y-%m-%d")
        receiptshop = request.form.get("receiptshop")
        receiptloc = request.form.get("receiptloc")
        payer = request.form.get("receiptpayer")
        totprice = request.form.get("totprice")
        receiptadd = Receipt(date=receiptdate, shop=receiptshop, cost=totprice,
                             payer=payer, location=receiptloc)
        db.session.add(receiptadd)
        db.session.commit()

        itemname_list = request.form.getlist("itemname")
        itemprice_list = request.form.getlist("price")
        itemquantity_list = request.form.getlist("quantity")
        itemcategory_list = request.form.getlist("category")

        for itemname, itemprice, itemquantity, itemcategory in zip(itemname_list, itemprice_list, itemquantity_list, itemcategory_list):
            itemadd = Item(name=itemname, price=itemprice, quantity=itemquantity,
                           category=itemcategory, receipt_id=receiptadd.id)
            db.session.add(itemadd)

        db.session.commit()
        flash("The new receipt was added successfully! 🙂", category="info")
        return redirect(url_for("receipts.receipt"))
    else:
        return render_template("receipt.html")
