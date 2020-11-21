from flask import Blueprint, url_for, redirect, render_template, flash, request, session
from app.models import Receipt
from app.models import Item
from flask_login import login_required
from app import db

receipts = Blueprint('receipts', __name__)


@receipts.route("/receipt", methods=["GET", "POST"])
@login_required
def receipt():
    if request.method == "POST":
        session.perment = True
        # receipt = request.form
        receiptdate = request.form["receiptdate"]
        receiptshop = request.form["receiptshop"]
        receiptloc = request.form["receiptloc"]
        payer = request.form["receiptpayer"]
        totprice = request.form["totprice"]

        receiptadd = Receipt(date=receiptdate, shop=receiptshop, cost=totprice,
                             payer=payer, location=receiptloc)

        db.session.add(receiptadd)
        db.session.commit()

        # print(receipt)
        return redirect(url_for("receipts.receipt"))
    else:
        return render_template("receipt.html")
