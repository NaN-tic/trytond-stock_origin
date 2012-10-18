#This file is part stock_origin module for Tryton.
#The COPYRIGHT file at the top level of this repository contains 
#the full copyright notices and license terms.

from trytond.model import fields
from trytond.pool import Pool, PoolMeta

__all__ = ['ShipmentOut']
__metaclass__ = PoolMeta

class ShipmentOut:
    "Customer Shipment"
    __name__ = 'stock.shipment.out'

    origin = fields.Reference('Origin', selection='get_origin')

    @classmethod
    def _get_origin(cls):
        'Return list of Model names for origin Reference'
        return []

    @classmethod
    def get_origin(cls):
        Model = Pool().get('ir.model')
        models = cls._get_origin()
        models = Model.search([
                ('model', 'in', models),
                ])
        return [('', '')] + [(m.model, m.name) for m in models]
