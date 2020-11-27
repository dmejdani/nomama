from flask import Blueprint, url_for, redirect, render_template, flash, request, session
from app.models import Receipt, Item
from flask_login import login_required
from app import db
from datetime import datetime
import traceback

receipts = Blueprint('receipts', __name__)


def is_new_receipt(date, cost):
    result = Receipt.query.filter_by(date=date).filter_by(cost=cost).first()
    return result == None


@receipts.route("/receipt", methods=["GET", "POST"])
@login_required
def receipt():
    if request.method == "POST":
        try:
            # receipt = request.form
            receiptdate = request.form.get("receiptdate")
            receiptdate = datetime.strptime(receiptdate, "%Y-%m-%d")
            receiptshop = request.form.get("receiptshop")
            receiptloc = request.form.get("receiptloc")
            payer = request.form.get("receiptpayer")

            itemname_list = request.form.getlist("itemname")
            itemprice_list = request.form.getlist("price")
            itemquantity_list = request.form.getlist("quantity")
            itemcategory_list = request.form.getlist("category")

            totprice = 0
            for i in range(len(itemprice_list)):
                totprice += float(itemprice_list[i])*int(itemquantity_list[i])
            print(totprice)

            receiptadd = Receipt(date=receiptdate, shop=receiptshop, cost=totprice,
                                 payer=payer, location=receiptloc)

            db.session.add(receiptadd)
            db.session.flush()

            for itemname, itemprice, itemquantity, itemcategory in zip(itemname_list, itemprice_list, itemquantity_list, itemcategory_list):
                itemadd = Item(name=itemname, price=itemprice, quantity=itemquantity,
                               category=itemcategory, receipt_id=receiptadd.id)
                db.session.add(itemadd)

            if not is_new_receipt(receiptdate, totprice):
                flash(
                    f"There is already a receipt with date: {receiptdate}  and total price: {totprice}!", category="warning")
                return redirect(url_for("receipts.receipt"))

        # go here if something goes wrong in the try block
        except:
            traceback.print_exc()
            db.session.rollback()
            flash(
                "Something went wrong! 😟 Database session rolled back successfully!", category="danger")
            return redirect(url_for("receipts.receipt"))
        # commit changes if nothing went wrong in the try block
        else:
            db.session.commit()
            flash("The new receipt was added successfully! 🙂", category="info")
            return redirect(url_for("receipts.receipt"))

    else:
        return render_template("receipt.html")
