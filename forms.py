__author__ = 'giasuddin'
from wtforms import Form, ValidationError, BooleanField, validators, StringField, DateField, IntegerField

'''
Important link for date picker
https://gist.github.com/doobeh/3e685ef25fac7d03ded7
'''


def field_length_check(form, field):
    if field.data is None:
        raise ValidationError('Null field is not accepted')


class SalesDateSearchForm(Form):
    """
    This form is used for searching by date
    """
    sales_date = DateField(u'বিক্রির তারিখ', format="%m/%d/%Y", validators=[validators.optional()])


class ProductForm(Form):
    """This form used for inserting several type of product"""
    name = StringField(u'পণ্যের নাম', validators=[validators.data_required(), field_length_check])
    description = StringField(u'পণ্যের বিবরণ', validators=[validators.optional()])
    purchase_price = IntegerField(u'ক্রয় মূল্য ', validators=[validators.data_required(), field_length_check])
    sales_price = IntegerField(u'বিক্রয় মূল্য', validators=[validators.data_required(), field_length_check])
    product_code = StringField(u'পণ্যের কোড ', validators=[validators.data_required(), field_length_check])
    is_published = BooleanField(u'প্রকাশিত', validators=[validators.data_required(), field_length_check], default=True)


class SalesForm(Form):
    """This form store all sales transaction"""
    sales_date = DateField(u'বিক্রির তারিখ', format="%m/%d/%Y", validators=[validators.data_required()])
    total_unit = IntegerField(u'মোট ইউনিট', validators=[validators.data_required(), field_length_check])
    sales_price = IntegerField(u'বিক্রয় মূল্য', validators=[validators.data_required()])
    buyer_name = StringField(u'ক্রেতার নাম ', validators=[validators.data_required(), field_length_check])
    buyer_address = StringField(u'ক্রেতার ঠিকানা', validators=[validators.optional()])
    seller_phone = StringField(u'বিক্রাতার ফোন নম্বর ', validators=[validators.optional()])


class PurchaseForm(Form):
    """"This form store all purchase transaction"""
    purchase_date = DateField(u'ক্রয়ের তারিখ ', format="%m/%d/%Y", validators=[validators.data_required()])
    purchase_price = IntegerField(u'ক্রয় মূল্য', validators=[validators.data_required(), field_length_check])
    total_unit = IntegerField(u'মোট ইউনিট', validators=[validators.data_required(), field_length_check])
    seller_name = StringField(u'বিক্রাতার নাম ', validators=[validators.data_required(), field_length_check])
    seller_address = StringField(u'বিক্রাতার ঠিকানা', validators=[validators.optional()])
    seller_phone = StringField(u'বিক্রাতার ফোন', validators=[validators.optional()])


class DamageForm(Form):
    """This form store all damage product"""
    damage_date = DateField(u'নষ্টের  তারিখ', format="%m/%d/%Y", validators=[validators.optional()])
    total_unit = IntegerField(u'মোট ইউনিট', validators=[validators.data_required(), field_length_check])
    damage_reason = StringField(u'নষ্টের কারণ ', validators=[validators.data_required(), field_length_check])


