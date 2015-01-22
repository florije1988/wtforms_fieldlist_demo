# -*- coding: utf-8 -*-
__author__ = 'florije'

from wtforms import Form, IntegerField, SelectField, TextField, FieldList, FormField
from wtforms import validators
from collections import namedtuple

OrderEntry = namedtuple('OrderEntry', ['quantity', 'producetype'])
Order = namedtuple('Order', ['name', 'order_entries'])


class OrderEntryForm(Form):
    quantity = IntegerField('Quantity',
                            [validators.Required(), validators.NumberRange(min=1)])
    # we will be dynamically adding choices
    producetype = SelectField('Produce',
                              [validators.Required()],
                              choices=[
                                  (1, 'carrots'),
                                  (2, 'turnips'),
                              ])


class OrderForm(Form):
    name = TextField('Crop', [validators.Length(min=3, max=60)])
    order_entries = FieldList(FormField(OrderEntryForm))

# Test Print of just the OrderEntryForm
o_form = OrderEntryForm()
print o_form.producetype()

# Create a test order
order_entry_1 = OrderEntry(4, 1)
order_entry_2 = OrderEntry(2, 2)

order = Order('My First Order', [order_entry_1, order_entry_2])

order_form = OrderForm(obj=order)
print order_form.validate()

print order_form.name
print order_form.order_entries