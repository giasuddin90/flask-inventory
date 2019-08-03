import datetime
import os

from flask import (
    redirect, render_template, request, url_for
)

from models import Product, Purchase, Sales, Damage
from helper import pager, profit_calculate, database_backup_func, check_mac_security
from forms import ProductForm, SalesForm, PurchaseForm, DamageForm, SalesDateSearchForm
from app import app
from app import SQLITE_PATH


@app.route('/')
def home():
    """ view showing index page and all keyword list """
    item_per_page = 50
    query = Product.by_all()
    queryset = Product.by_all().limit(item_per_page)
    pagination_item = pager(query.count(), item_per_page)
    if request.args.get('next_page', ''):
        next = request.args['next_page']
        queryset = queryset.offset(pagination_item[int(next)])
    return render_template('product_list.html', queryset=queryset, pagination_item=pagination_item)


@app.route('/software/sicurity')
def security_page():
    return render_template('software_licence.html')


@app.route('/product/top-sell')
def top_selling_product():
    data_param = "2018-10-27"
    form = SalesDateSearchForm(request.form)
    queryset = Sales.by_date_top_product(data_param)
    if request.args.get('sales_date', ''):
        any_sales_date = request.args['sales_date']
        format_str = '%m/%d/%Y'
        datetime_obj = datetime.datetime.strptime(any_sales_date, format_str)
        data_param = str(datetime_obj.date())
        queryset = Sales.by_date_top_product(data_param)
    return render_template('top_selling_product_list.html', form=form, queryset=queryset, sales_date_param=data_param)


@app.route('/product/sales-report')
def sales_report():
    queryset = Sales.by_weekly_sales()
    queryset_month = Sales.by_monthly_sales()
    query_damage = Damage.by_monthly_damage()

    return render_template('sales_report.html', queryset=queryset, queryset_month=queryset_month,
                           query_damage=query_damage)


@app.route('/product/create', methods=('GET', 'POST'))
def product_create():
    """ View using for inserting keyword"""

    if check_mac_security():
        pass
    else:
        return redirect(url_for('security_page'))

    entry = Product()
    form = ProductForm(request.form)
    if request.method == 'POST' and form.validate():
        form.populate_obj(entry)
        entry.created_on = datetime.datetime.now()

        data_keyword = entry.__dict__
        data_keyword.pop("_sa_instance_state")
        Product.create_data(**data_keyword)
        return redirect(url_for('home'))
    return render_template('product_create.html', form=form, operation="create")


@app.route('/product/update/<int:product_id>', methods=('GET', 'POST'))
def product_update(product_id):
    """Update existing keyword"""
    if check_mac_security():
        pass
    else:
        return redirect(url_for('security_page'))

    entry = Product.by_id(product_id)
    form = ProductForm(request.form, entry)
    if request.method == 'POST' and form.validate():
        form_data = form.data
        Product.update_data(product_id, **form_data)
        return redirect(url_for('home'))
    return render_template('product_create.html', form=form, data_id=product_id, operation="update")


@app.route('/product/delete/<int:product_id>', methods=('POST', 'GET'))
def product_delete(product_id):
    """Delete existing keyword """
    if check_mac_security():
        pass
    else:
        return redirect(url_for('security_page'))

    entry = Product.delete_data(product_id)
    return redirect(url_for('home'))


"""
starting purchase area
"""


@app.route('/product/purchase/<int:product_id>', methods=('GET', 'POST'))
def purchase_create(product_id):
    """ View using for inserting keyword"""
    entry = Purchase()
    form = PurchaseForm(request.form)
    if request.method == 'POST' and form.validate():
        form.populate_obj(entry)
        entry.created_on = datetime.datetime.now()
        entry.product_id = product_id

        data_keyword = entry.__dict__
        data_keyword.pop("_sa_instance_state")
        user_date = data_keyword['purchase_date']

        data_keyword["purchase_month"] = user_date.month
        data_keyword["purchase_week"] = user_date.isocalendar()[1]
        data_keyword["purchase_year"] = user_date.year

        """
        Data insert for purchase
        """
        Purchase.create_data(**data_keyword)
        data = Product.increase_inventory(entry.product_id, entry.total_unit)
        return redirect(url_for('product_purchase_list'))
    return render_template('purchase_create.html', form=form, data_id=product_id)


@app.route('/product/all-purchase')
def product_purchase_list():
    """ view showing index page and all keyword list """
    item_per_page = 50
    query = Purchase.by_all()
    queryset = Purchase.by_all().limit(item_per_page)
    pagination_item = pager(query.count(), item_per_page)
    if request.args.get('next_page', ''):
        next = request.args['next_page']
        queryset = queryset.offset(pagination_item[int(next)])
    return render_template('purchase_list.html', queryset=queryset, pagination_item=pagination_item)


@app.route('/product/purchase/delete/<int:purchase_id>', methods=('POST', 'GET'))
def purchase_delete(purchase_id):
    """Delete existing keyword """
    purchase_data = Purchase.by_id(purchase_id)
    Product.decrease_inventory(purchase_data.product_id, purchase_data.total_unit)
    Purchase.delete_data(purchase_id)
    return redirect(url_for('product_purchase_list'))


'''
Starting sales area
'''


@app.route('/product/stock-out')
def stock_out():
    return render_template('stock_out.html')


@app.route('/product/sales/<int:product_id>', methods=('GET', 'POST'))
def sales_create(product_id):
    """ View using for inserting keyword"""
    product_data = Product.by_id(product_id)
    entry = Sales()
    form = SalesForm(request.form)
    if request.method == 'POST' and form.validate():
        form.populate_obj(entry)
        entry.created_on = datetime.datetime.now()
        entry.product_id = product_id
        entry.sales_commission = profit_calculate(product_data.purchase_price, entry.sales_price, entry.total_unit)
        data_keyword = entry.__dict__
        data_keyword.pop("_sa_instance_state")
        user_date = data_keyword['sales_date']

        data_keyword["sales_month"] = user_date.month
        data_keyword["sales_week"] = user_date.isocalendar()[1]
        data_keyword["sales_year"] = user_date.year

        """
        Data insert for purchase
        """
        if entry.total_unit <= product_data.total_unit:
            Sales.create_data(**data_keyword)
            data = Product.decrease_inventory(entry.product_id, entry.total_unit)
            return redirect(url_for('product_sales_list'))
        else:
            return redirect(url_for('stock_out'))

    return render_template('sales_create.html', form=form, data_id=product_id)


@app.route('/product/all-sales')
def product_sales_list():
    """ view showing index page and all keyword list """
    item_per_page = 50
    query = Sales.by_all()
    queryset = Sales.by_all().limit(item_per_page)
    pagination_item = pager(query.count(), item_per_page)
    if request.args.get('next_page', ''):
        next = request.args['next_page']
        queryset = queryset.offset(pagination_item[int(next)])
    return render_template('sales_list.html', queryset=queryset, pagination_item=pagination_item)


@app.route('/product/sales/delete/<int:sales_id>', methods=('POST', 'GET'))
def sales_delete(sales_id):
    """Delete existing keyword """
    sales_data = Sales.by_id(sales_id)
    Product.increase_inventory(sales_data.product_id, sales_data.total_unit)
    Sales.delete_data(sales_id)
    return redirect(url_for('product_sales_list'))


'''
Staring damage area
'''


@app.route('/product/damage/<int:product_id>', methods=('GET', 'POST'))
def damage_create(product_id):
    """ View using for inserting keyword"""
    product_data = Product.by_id(product_id)

    entry = Damage()
    form = DamageForm(request.form)
    if request.method == 'POST' and form.validate():
        form.populate_obj(entry)
        entry.created_on = datetime.datetime.now()
        entry.product_id = product_id

        data_keyword = entry.__dict__
        data_keyword.pop("_sa_instance_state")
        user_date = data_keyword['damage_date']

        data_keyword["damage_month"] = user_date.month
        data_keyword["damage_week"] = user_date.isocalendar()[1]
        data_keyword["damage_year"] = user_date.year
        data_keyword["damage_amount"] = product_data.purchase_price * entry.total_unit

        """
        Data insert for Damage
        """
        if entry.total_unit <= product_data.total_unit:
            Damage.create_data(**data_keyword)
            data = Product.decrease_inventory(entry.product_id, entry.total_unit)
            return redirect(url_for('product_damage_list'))
        else:
            return redirect(url_for('stock_out'))

    return render_template('damage_create.html', form=form, data_id=product_id)


@app.route('/product/all-damages')
def product_damage_list():
    """ view showing index page and all keyword list """
    item_per_page = 50
    query = Damage.by_all()
    queryset = Damage.by_all().limit(item_per_page)
    pagination_item = pager(query.count(), item_per_page)
    if request.args.get('next_page', ''):
        next = request.args['next_page']
        queryset = queryset.offset(pagination_item[int(next)])
    return render_template('damage_list.html', queryset=queryset, pagination_item=pagination_item)


@app.route('/product/damage/delete/<int:damage_id>', methods=('POST', 'GET'))
def damage_delete(damage_id):
    """Delete existing keyword """
    dmage_data = Damage.by_id(damage_id)
    Product.increase_inventory(dmage_data.product_id, dmage_data.total_unit)
    Damage.delete_data(damage_id)
    return redirect(url_for('product_damage_list'))


'''
Staring database backup area
'''


@app.route('/backup-data')
def database_backup():
    """Uploading backup file"""
    back_up = database_backup_func()
    return render_template('backup_message.html')


@app.route('/backup/file-upload', methods=('POST', 'GET'))
def upload():
    """Uploading backup file"""
    file_extensions = [".db"]
    upload_error = None

    if request.method == 'POST':
        db_file = request.files['file']
        filename = db_file.filename
        split_file = os.path.splitext(filename)
        upload_file_ext = split_file[1]

        if upload_file_ext in file_extensions:
            # new_filename = "inventory.db"
            db_file.save(SQLITE_PATH)
            return redirect(url_for('home'))

        else:
            upload_error = "ভুল ব্যাকআপ ফাইল আপলোড করেছেন।  "

    return render_template('backup_upload.html', error_message=upload_error)






