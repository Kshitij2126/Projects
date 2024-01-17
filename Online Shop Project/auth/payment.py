# Creating a User Payment Information Tab for the Shop Website - Kshitij Aji, ka598, Dec 15 2022

from flask import Flask, Blueprint, render_template, flash, redirect, url_for, current_app, session
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from sql.db import DB

# Adding Blueprint for payment -  Kshitij Aji, ka598, Dec 15 2022
payment = Blueprint('payment', __name__, url_prefix='/',
                    template_folder='templates')


# Creating a new Form Class for Payment Details -  Kshitij Aji, ka598, Dec 15 2022
class PaymentForm(FlaskForm):
    customer_name = StringField("Customer Name", validators=[DataRequired()])
    shipping_address = StringField(
        "Shipping Address", validators=[DataRequired()])
    credit_card_number = StringField(
        "Credit Card Number", validators=[DataRequired()])
    card_balance = StringField("Card Balance", validators=[DataRequired()])
    submit = SubmitField("Submit Payment Details")


# created new function for adding payment information -  Kshitij Aji, ka598, Dec 15 2022
@payment.route("/payment", methods=["GET", "POST"])
def payment():
    customer_name = None
    shipping_address = None
    credit_card_number = None
    card_balance = None
    form = PaymentForm()

    # Form Validation -  Kshitij Aji, ka598, Dec 16 2022
    if form.validate_on_submit():
        customer_name = form.customer_name.data
        form.customer_name.data = ""
        shipping_address = form.shipping_address.data
        form.shipping_address.data = ""
        credit_card_number = form.credit_card_number.data
        form.credit_card_number = ""
        card_balance = form.card_balance.data
        form.card_balance = ""

    return render_template("payment.html", customer_name=customer_name,
                           shipping_address=shipping_address, credit_card_number=credit_card_number,
                           card_balance=card_balance, form=form)
