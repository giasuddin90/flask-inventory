from datetime import date, timedelta

from sqlalchemy import (
    Column,
    Integer,
    Text,
    String,
    DateTime,
    Date,
    ForeignKey,
    desc,
    Boolean,
    or_
)
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
DBSession = db.session

"""
important link
https://piotr.banaszkiewicz.org/blog/2012/06/29/flask-sqlalchemy-init_app/
"""


class Product(db.Model):
    """
   Table use for storing product and product detail in this table
    """
    __tablename__ = "product"

    id = Column(Integer, primary_key=True)
    name = Column(String())
    description = Column(Text())
    purchase_price = Column(Integer)
    sales_price = Column(Integer)
    total_unit = Column(Integer, default=0)
    product_code = Column(String())
    created_on = Column(DateTime)
    updated_on = Column(DateTime)
    is_published = Column(Boolean, default=True)
    purchase = db.relationship("Purchase", cascade="all, delete-orphan")
    sales = db.relationship("Sales", cascade="all, delete-orphan")
    damage = db.relationship("Damage", cascade="all, delete-orphan")

    # get all with descending order and limit from a table
    @classmethod
    def by_all(cls):
        """ Provide all product list with custom field"""
        # query = DBSession.query(Product).filter(Product.is_published == True)
        query = DBSession.query(Product)
        return query

    @classmethod
    def by_all_id(cls):
        """ Provide all publish product"""
        product_list = [('', 'Select Product')]
        query = DBSession.query(Product).filter(Product.is_published == True).all()
        for item in query:
            data = (item.id, item.name)
            product_list.append(data)

        return product_list

    @classmethod
    def by_search_filter(cls, searchtext):
        """ Provide search result based on base text and category field"""
        queryset = DBSession.query(Product).filter(or_(Product.base_text.ilike("%" + searchtext + "%"),
                                                       Product.category.ilike("%" + searchtext + "%"))).all()

        return queryset

    @classmethod
    def by_all_filter(cls, category):
        """ Data filter based in category"""
        query = DBSession.query(Product).filter(Product.category == category).all()
        return query

    @classmethod
    def by_id(cls, product_id):
        """Get product bases on product id"""
        query = DBSession.query(Product).filter_by(id=product_id).first()
        return query

    @classmethod
    def update_data(cls, data_id, **kwargs):
        """ Using for updating single product"""
        DBSession.query(Product).filter_by(id=data_id).update(kwargs)
        DBSession.commit()
        return 'keyword updated'

    # delete single topic by id
    @classmethod
    def delete_data(cls, data_id):
        """ Delete product based on id"""
        product = DBSession.query(Product).filter_by(id=data_id).first()
        DBSession.delete(product)
        DBSession.commit()
        return 'keyword deteted'

    @classmethod
    def create_data(cls, **kwargs):
        """Using for inserting product"""
        api = Product(**kwargs)
        DBSession.add(api)
        DBSession.commit()
        return 'topic created'

    @classmethod
    def increase_inventory(cls, data_id, amount):
        detail_data = DBSession.query(Product).filter_by(id=data_id).first()
        increment = detail_data.total_unit + amount
        final_data = {"total_unit": increment}
        DBSession.query(Product).filter_by(id=data_id).update(final_data)
        DBSession.commit()
        return detail_data

    @classmethod
    def decrease_inventory(cls, data_id, amount):
        detail_data = DBSession.query(Product).filter_by(id=data_id).first()
        available_unit = detail_data.total_unit - amount
        final_data = {"total_unit": available_unit}
        DBSession.query(Product).filter_by(id=data_id).update(final_data)
        DBSession.commit()
        return detail_data


class Sales(db.Model):
    """
    Table used for storing sales transaction
    """
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True)
    buyer_name = Column(String())
    buyer_address = Column(Text())
    seller_phone = Column(String())
    buyer_phone = Column(String())
    total_unit = Column(Integer, default=0)
    sales_price = Column(Integer)
    sales_commission = Column(Integer)
    sales_date = Column(Date)
    sales_week = Column(Integer)
    sales_month = Column(Integer)
    sales_year = Column(Integer)
    created_on = Column(DateTime)
    updated_on = Column(DateTime)
    product_id = Column(Integer, ForeignKey('product.id'))
    _name = db.relationship('Product')

    @property
    def name(self):
        return self._name.name

    @property
    def month_name(self):
        month_dict = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June',
                      7: 'July', 8: 'Augst', 9: 'September', 10: 'October', 11: 'November', 12: 'December'}
        m_name = month_dict[self.sales_month]
        return m_name + '-' + str(self.sales_year)


    @classmethod
    def by_all(cls):
        """ Provide all stored keyword with custom field"""
        query = DBSession.query(Sales)
        return query

    @classmethod
    def by_id(cls, data_id):
        """Get Keword bases on keyword id"""
        query = DBSession.query(Sales).filter_by(id=data_id).first()
        return query

    @classmethod
    def delete_data(cls, data_id):
        """ Using for deleting single keyword """
        DBSession.query(Sales).filter_by(id=data_id).delete()
        DBSession.commit()
        return 'purchase deleted'

    @classmethod
    def create_data(cls, **kwargs):
        """Using for inserting keyword"""
        api = Sales(**kwargs)
        DBSession.add(api)
        DBSession.commit()
        return 'purchase created'

    @classmethod
    def by_weekly_sales(cls):
        """ Provide all stored keyword with custom field"""
        today = date.today()
        last_week = today - timedelta(15)
        query = DBSession.query(Sales.sales_date.label("sales_date"),
                                db.func.sum(Sales.sales_commission).label("sales_profit"),
                                db.func.sum(Sales.total_unit).label("total_order"),
                                db.func.sum(Sales.sales_price).label("total_sales")).filter(
            Sales.sales_date >= last_week).group_by(Sales.sales_date).all()
        return query

    @classmethod
    def by_monthly_sales(cls):
        """ Provide all stored keyword with custom field"""
        today = date.today()
        last_six_month = today - timedelta(180)
        query = DBSession.query(Sales, Sales.sales_month.label("sales_month"),
                                db.func.sum(Sales.sales_commission).label("sales_profit"),
                                db.func.sum(Sales.total_unit).label("total_order"),
                                db.func.sum(Sales.sales_price).label("total_sales")).filter(
            Sales.sales_date >= last_six_month).group_by(Sales.sales_month).all()
        return query

    @classmethod
    def by_date_top_product(cls, date_param):
        """Provide total property count based on date"""
        query = DBSession.query(Sales, Sales.product_id.label("product_id"),
                                db.func.sum(Sales.sales_commission).label("total_sales_commission"),
                                db.func.sum(Sales.total_unit).label("total_order"),
                                db.func.sum(Sales.sales_price).label("total_sales")).filter(
            Sales.sales_date == date_param).group_by(Sales.product_id).order_by(
            desc(db.func.sum(Sales.total_unit))).all()
        return query


class Purchase(db.Model):
    """
     Table used for storing purchase transaction
    """
    __tablename__ = "purchase"

    id = Column(Integer, primary_key=True)
    seller_name = Column(String())
    seller_address = Column(Text())
    seller_phone = Column(String())
    total_unit = Column(Integer, default=0)
    purchase_price = Column(Integer)
    purchase_date = Column(Date)
    purchase_week = Column(Integer)
    purchase_month = Column(Integer)
    purchase_year = Column(Integer)
    created_on = Column(DateTime)
    updated_on = Column(DateTime)
    product_id = Column(Integer, ForeignKey('product.id'))

    _name = db.relationship('Product')

    @property
    def name(self):
        return self._name.name

    @classmethod
    def by_all(cls):
        """ Provide all stored keyword with custom field"""
        query = DBSession.query(Purchase)
        return query

    @classmethod
    def by_id(cls, data_id):
        """Get Keword bases on keyword id"""
        query = DBSession.query(Purchase).filter_by(id=data_id).first()
        return query

    @classmethod
    def delete_data(cls, data_id):
        """ Using for delating singel keyword """
        DBSession.query(Purchase).filter_by(id=data_id).delete()
        DBSession.commit()
        return 'purchase deleted'

    @classmethod
    def create_data(cls, **kwargs):
        """Using for inserting keyword"""
        api = Purchase(**kwargs)
        DBSession.add(api)
        DBSession.commit()
        return 'purchase created'


class Damage(db.Model):
    """
     Table used for storing damage product.
    """
    __tablename__ = "damage"

    id = Column(Integer, primary_key=True)
    damage_reason = Column(String())
    total_unit = Column(Integer)
    damage_amount = Column(Integer)
    damage_date = Column(Date)
    damage_week = Column(Integer)
    damage_month = Column(Integer)
    damage_year = Column(Integer)
    created_on = Column(DateTime)
    updated_on = Column(DateTime)
    product_id = Column(Integer, ForeignKey('product.id'))

    _name = db.relationship('Product')

    @property
    def name(self):
        return self._name.name

    @property
    def purchase_price(self):
        return self._name.purchase_price

    @property
    def month_name(self):
        month_dict = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June',
                      7: 'July', 8: 'Augst', 9: 'September', 10: 'October', 11: 'November', 12: 'December'}
        m_name = month_dict[self.damage_month]
        return m_name + '-' + str(self.damage_year)

    @classmethod
    def by_monthly_damage(cls):
        """ Provide all stored keyword with custom field"""
        today = date.today()
        last_six_month = today - timedelta(180)
        query = DBSession.query(Damage, Damage.damage_month.label("damage_month"),
                                db.func.sum(Damage.damage_amount).label("damage_amount"),
                                db.func.sum(Damage.total_unit).label("total_damage")).filter(
            Damage.damage_date >= last_six_month).group_by(Damage.damage_month).all()
        return query

    @classmethod
    def by_all(cls):
        """ Provide all stored keyword with custom field"""
        query = DBSession.query(Damage)
        return query

    @classmethod
    def by_id(cls, data_id):
        """Get Damage by id"""
        query = DBSession.query(Damage).filter_by(id=data_id).first()
        return query

    @classmethod
    def delete_data(cls, data_id):
        """ Using for delating singel keyword """
        DBSession.query(Damage).filter_by(id=data_id).delete()
        DBSession.commit()
        return 'purchase deleted'

    @classmethod
    def create_data(cls, **kwargs):
        """Using for inserting keyword"""
        api = Damage(**kwargs)
        DBSession.add(api)
        DBSession.commit()
        return 'purchase created'


