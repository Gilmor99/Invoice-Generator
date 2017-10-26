"""
Invoice Genertaion Flask Application
"""

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.inspection import inspect
from database_setup import Base, Account, Invoice, InvoiceLine

app = Flask(__name__)
app.debug = True
app.secret_key = 'super_secret_key'


engine = create_engine('sqlite:///invoices.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()



@app.route('/')
@app.route('/accounts')
def showAccounts():
    """
        Show All Accounts Function
        Acts as the application Root
    """
    accounts = session.query(Account).all()
    return render_template('accounts.html', accounts=accounts)



@app.route('/accounts/JSON')
def showAccountsJSON():
    """ JSON API interface to query all accounts """
    accounts = session.query(Account).all()
    return jsonify(Account=[i.serialize for i in accounts])



@app.route('/accounts/new', methods=['GET', 'POST'])
def newAccount():
    """ Craete New Account Function """
    if request.method == 'POST':
        newAccount = Account(company=request.form['company'],
                address=request.form['address'],                              city=request.form['city'],
                state=request.form['state'],
                zipcode=request.form['zipcode'],
                tel=request.form['tel'],
                fax=request.form['fax']
                )
        session.add(newAccount)
        session.commit()
        flash("New account created!")
        return redirect(url_for('showAccounts'))
    else:
        return render_template('newaccount.html')


@app.route('/accounts/<int:account_id>/edit', methods=['GET', 'POST'])
def editAccount(account_id):
    """ Edit Account Function """
    editedAccount = session.query(Account).filter_by(id=account_id).one()
    if request.method == 'POST':
        if request.form['company']:
            editedAccount.company = request.form['company']
        if request.form['address']:
            editedAccount.address = request.form['address']
        if request.form['city']:
            editedAccount.city = request.form['city']
        if request.form['state']:
            editedAccount.state = request.form['state']
        if request.form['zipcode']:
            editedAccount.zipcode = request.form['zipcode']
        if request.form['tel']:
            editedAccount.tel = request.form['tel']
        if request.form['fax']:
            editedAccount.fax = request.form['fax']
        session.add(editedAccount)
        session.commit()
        flash("Account Successfuly Updated!")
        return redirect(url_for('showAccounts'))
    else:
        return render_template('editaccount.html', account=editedAccount)


@app.route('/accounts/<int:account_id>/delete', methods=['GET', 'POST'])
def deleteAccount(account_id):
    """" Delete Account Function"""
    deletedAccount = session.query(Account).filter_by(id=account_id).one()
    if request.method == 'POST':
        session.query(Account).filter_by(id=account_id).delete()
        session.query(Invoice).filter_by(account_id=account_id).delete()
        session.query(InvoiceLine).filter_by(account_id=account_id).delete()
        session.commit()
        flash("Account Successfuly Deleted!")
        return redirect(url_for('showAccounts'))
    else:
        return render_template('deleteaccount.html', account=deletedAccount)


@app.route('/accounts/<int:account_id>/')
@app.route('/accounts/<int:account_id>/invoice')
def accountInvoices(account_id):
    """ Show existing invoices per account"""
    account = session.query(Account).filter_by(id=account_id).one()
    invoices = session.query(Invoice).filter_by(account_id=account_id)
    return render_template('invoice.html', account=account, invoices=invoices)


@app.route('/accounts/<int:account_id>/invoice/JSON')
def accountInvoicesJSON(account_id):
    """ JSON API interface to query all invoices per account """
    account = session.query(Account).filter_by(id=account_id).one()
    invoices = session.query(Invoice).filter_by(
        account_id=account_id).all()
    return jsonify(Invoice=[i.serialize for i in invoices])


@app.route('/accounts/<int:account_id>/new', methods=['GET', 'POST'])
def newInvoice(account_id):
    """ Create New Invoice """
    account = session.query(Account).filter_by(id=account_id).one()
    if request.method == 'POST':
        newInvoice = Invoice(fromName=request.form['fromName'],
                    number=request.form['number'],
                    billTo=request.form['billTo'],
                    toAddress=request.form['toAddress'],
                    toCity=request.form['toCity'],
                    toState=request.form['toState'],
                    toZipcode=request.form['toZipcode'],
                    toTel=request.form['toTel'],
                    toFax=request.form['toFax'],
                    date=request.form['date'],
                    paymentTerms=request.form['paymentTerms'],
                    dueDate=request.form['dueDate'],
                    balanceDue=request.form['balanceDue'],
                    subTotal=request.form['subTotal'],
                    taxFlag=request.form['taxFlag'],
                    tax=request.form['tax'],
                    discountFlag=request.form['discountFlag'],
                    discount=request.form['discount'],
                    shipping=request.form['shipping'],
                    total=request.form['total'],
                    amountPaid=request.form['amountPaid'],
                    account_id=account.id)
        session.add(newInvoice)
        session.flush()
        descriptions = request.form.getlist('description')
        quantities = request.form.getlist('quantity')
        rates = request.form.getlist('rate')
        amounts = request.form.getlist('amount')
        for idx in range(0, len(descriptions)):
            newLineItem = InvoiceLine(description=descriptions[idx], quantity=quantities[idx], rate=rates[idx], amount=amounts[idx], invoice_id=newInvoice.id)
            session.add(newLineItem)
        session.commit()
        flash("New Invoice Created!")
        return redirect(url_for('accountInvoices', account_id=account.id))
    else:
        return render_template('newinvoice.html', account=account)


@app.route('/accounts/<int:account_id>/<int:invoice_id>/edit', methods=['GET', 'POST'])
def editInvoice(account_id, invoice_id):
    """ Edit existing Invoice function """
    account = session.query(Account).filter_by(id=account_id).one()
    editedInvoice = session.query(Invoice).filter_by(id=invoice_id).one()
    editedLineItems = session.query(InvoiceLine).filter_by(invoice_id=invoice_id)
    if request.method == 'POST':
        editedInvoice.number = request.form['number']
        editedInvoice.billTo = request.form['billTo']
        editedInvoice.toAddress = request.form['toAddress']
        editedInvoice.toCity = request.form['toCity']
        editedInvoice.toState = request.form['toState']
        editedInvoice.toZipcode = request.form['toZipcode']
        editedInvoice.toTel = request.form['toTel']
        editedInvoice.toFax = request.form['toFax']
        editedInvoice.fromName = request.form['fromName']
        editedInvoice.date = request.form['date']
        editedInvoice.paymentTerms = request.form['paymentTerms']
        editedInvoice.dueDate = request.form['dueDate']
        editedInvoice.balanceDue = request.form['balanceDue']
        editedInvoice.subTotal = request.form['subTotal']
        editedInvoice.taxFlag = request.form['taxFlag']
        editedInvoice.tax = request.form['tax']
        editedInvoice.discountFlag = request.form['discountFlag']
        editedInvoice.shipping = request.form['shipping']
        editedInvoice.discount = request.form['discount']
        editedInvoice.total = request.form['total']
        editedInvoice.amountPaid = request.form['amountPaid']
        session.add(editedInvoice)
        session.query(InvoiceLine).filter_by(invoice_id=invoice_id).delete()
        descriptions = request.form.getlist('description')
        quantities = request.form.getlist('quantity')
        rates = request.form.getlist('rate')
        amounts = request.form.getlist('amount')
        for idx in range(0, len(descriptions)):
            newLineItem = InvoiceLine(description=descriptions[idx], quantity=quantities[idx], rate=rates[idx], amount=amounts[idx], invoice_id=editedInvoice.id)
            session.add(newLineItem)
        session.commit()
        flash("Invoice Successfuly Edited")
        return redirect(url_for('accountInvoices', account_id=account.id))
    else:
        return render_template('editinvoice.html', invoice=editedInvoice, account=account, lineItems=editedLineItems)


#JSON API
@app.route('/accounts/<int:account_id>/<int:invoice_id>/JSON')
def invoiceJSON(account_id, invoice_id):
    """ JSON API interface to existing invoice """
    account = session.query(Account).filter_by(id=account_id).one()
    invoice = session.query(Invoice).filter_by(id=invoice_id).one()
    lineItems = session.query(InvoiceLine).filter_by(invoice_id=invoice_id)
    return jsonify(Invoice=[invoice.serialize], InvoiceLine=[i.serialize for i in lineItems])


@app.route('/accounts/<int:account_id>/<int:invoice_id>/delete', methods=['GET', 'POST'])
def deleteInvoice(account_id, invoice_id):
    """ Delete Invoice function """
    account = session.query(Account).filter_by(id=account_id).one()
    invoiceToDelete = session.query(Invoice).filter_by(id=invoice_id).one()
    deletedLineItems = session.query(InvoiceLine).filter_by(invoice_id=invoice_id)
    if request.method == 'POST':
        session.query(Invoice).filter_by(id=invoice_id).delete()
        session.query(InvoiceLine).filter_by(invoice_id=invoice_id).delete()
        session.commit()
        flash("Invoice Successfuly Deleted")
        return redirect(url_for('accountInvoices', account_id=account.id))
    else:
        return render_template('deleteinvoice.html', invoice=invoiceToDelete, account=account)


if __name__ == '__main__':
    """ Application is available of port 5000 """
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
