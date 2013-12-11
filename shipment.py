#This file is part stock_origin module for Tryton.
#The COPYRIGHT file at the top level of this repository contains 
#the full copyright notices and license terms.

from trytond.model import fields
from trytond.pool import Pool, PoolMeta
from trytond.transaction import Transaction
from trytond.rpc import RPC

__all__ = ['ShipmentOut', 'ShipmentOutReturn', 'CreateShipmentOutReturn']
__metaclass__ = PoolMeta


class ShipmentOut:
    __name__ = 'stock.shipment.out'
    origin = fields.Function(fields.Reference('Origin', selection='get_origin'),
        'get_origin_value')

    @classmethod
    def __setup__(cls):
        super(ShipmentOut, cls).__setup__()
        cls.__rpc__.update({
                'get_origin': RPC(),
                })

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

    @classmethod
    def get_origin_value(cls, shipments, name):
        origin = {}
        for shipment in shipments:
            origin[shipment.id] = None
        return origin


class ShipmentOutReturn:
    __name__ = 'stock.shipment.out.return'
    origin = fields.Function(fields.Reference('Origin', selection='get_origin'),
        'get_origin_value')
    origin_shipment = fields.Many2One('stock.shipment.out', 'Origin Shipment')

    @classmethod
    def __setup__(cls):
        super(ShipmentOutReturn, cls).__setup__()
        cls.__rpc__.update({
                'get_origin': RPC(),
                })

    @classmethod
    def _get_origin(cls):
        'Return list of Model names for origin Reference'
        return ['stock.shipment.out']

    @classmethod
    def get_origin(cls):
        Model = Pool().get('ir.model')
        models = cls._get_origin()
        models = Model.search([
                ('model', 'in', models),
                ])
        return [('', '')] + [(m.model, m.name) for m in models]

    @classmethod
    def get_origin_value(cls, shipments, name):
        origin = {}
        for shipment in shipments:
            origin[shipment.id] = (
                'stock.shipment.out,%s' % (shipment.origin_shipment.id)
                if shipment.origin_shipment else None)
        return origin


class CreateShipmentOutReturn:
    __name__ = 'stock.shipment.out.return.create'

    def do_start(self, action):
        pool = Pool()
        ShipmentOut = pool.get('stock.shipment.out')
        ShipmentOutReturn = pool.get('stock.shipment.out.return')

        action, data = super(CreateShipmentOutReturn, self).do_start(action)
        shipment_ids = Transaction().context['active_ids']
        shipment_outs = ShipmentOut.browse(shipment_ids)
        shipment_out_returns = ShipmentOutReturn.browse(data['res_id'])

        for shipment_out, shipment_out_return in \
                zip(shipment_outs, shipment_out_returns):
            shipment_out_return.origin_shipment = shipment_out
            shipment_out_return.save()
        return action, data
