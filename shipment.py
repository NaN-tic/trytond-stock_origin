#This file is part stock_origin module for Tryton.
#The COPYRIGHT file at the top level of this repository contains 
#the full copyright notices and license terms.

from trytond.model import ModelView, ModelSQL, fields
from trytond.transaction import Transaction
from trytond.pool import Pool


class ShipmentOut(ModelSQL, ModelView):
    _name = 'stock.shipment.out'

    origin = fields.Reference('Origin', selection='origin_get')

    def origin_get(self):
        '''Origin get. Rewrite this method to add new origins'''
        res = []
        return res

ShipmentOut()
