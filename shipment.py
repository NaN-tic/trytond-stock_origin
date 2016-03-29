#This file is part stock_origin module for Tryton.
#The COPYRIGHT file at the top level of this repository contains 
#the full copyright notices and license terms.

from trytond.model import fields
from trytond.pool import Pool, PoolMeta
from trytond.rpc import RPC

__all__ = ['Move', 'ShipmentOut', 'ShipmentOutReturn']


class Move:
    __metaclass__ = PoolMeta
    __name__ = 'stock.move'

    @classmethod
    def _get_origin(cls):
        models = super(Move, cls)._get_origin()
        if not 'stock.shipment.out' in models:
            models.append('stock.shipment.out')
        return models


class ShipmentOut:
    __metaclass__ = PoolMeta
    __name__ = 'stock.shipment.out'
    origin = fields.Function(fields.Reference('Origin', selection='get_origin'),
        'get_origin_value')
    origin_cache = fields.Reference('Origin Cache', selection='get_origin')
    origin_info = fields.Function(fields.Char('Origin Info'),
        'on_change_with_origin_info')

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

    @staticmethod
    def get_origin_name(origin, cache=None):
        pool = Pool()

        if not origin:
            return None

        model_origin = '%s' % origin.__name__
        id_origin = origin.id

        model, = pool.get('ir.model').search([('model', '=', model_origin)], limit=1)
        origin, = pool.get(model_origin).browse([id_origin])

        if cache:
            return '%s,%s' % (origin.__name__, id_origin)

        if hasattr(origin, 'code'):
            return '%s,%s' % (model.name, origin.code)
        if hasattr(origin, 'reference'):
            return '%s,%s' % (model.name, origin.reference)
        else:
            return '%s,%s' % (model.name, id_origin)

    @fields.depends('origin')
    def on_change_with_origin_info(self, name=None):
        if self.origin:
            return self.get_origin_name(self.origin)
        return None

    @classmethod
    def store_origin_cache(cls, shipments):
        for shipment in shipments:
            cls.write([shipment], {
                    'origin_cache': cls.get_origin_name(shipment.origin, cache=True),
                    })

    @classmethod
    def cancel(cls, shipments):
        super(ShipmentOut, cls).cancel(shipments)
        cls.store_origin_cache(shipments)

    @classmethod
    def wait(cls, shipments):
        super(ShipmentOut, cls).wait(shipments)
        cls.store_origin_cache(shipments)


class ShipmentOutReturn:
    __metaclass__ = PoolMeta
    __name__ = 'stock.shipment.out.return'
    origin = fields.Function(fields.Reference('Origin', selection='get_origin'),
        'get_origin_value')
    origin_cache = fields.Reference('Origin Cache', selection='get_origin')
    origin_info = fields.Function(fields.Char('Origin Info'),
        'on_change_with_origin_info')
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

    @staticmethod
    def get_origin_name(origin, cache=None):
        pool = Pool()

        if not origin:
            return None

        model_origin = '%s' % origin.__name__
        id_origin = origin.id

        model, = pool.get('ir.model').search([('model', '=', model_origin)], limit=1)
        origin, = pool.get(model_origin).browse([id_origin])

        if cache:
            return '%s,%s' % (origin.__name__, id_origin)

        if hasattr(origin, 'code'):
            return '%s,%s' % (model.name, origin.code)
        if hasattr(origin, 'reference'):
            return '%s,%s' % (model.name, origin.reference)
        else:
            return '%s,%s' % (model.name, id_origin)

    @fields.depends('origin')
    def on_change_with_origin_info(self, name=None):
        if self.origin:
            return self.get_origin_name(self.origin)
        return None

    @classmethod
    def store_origin_cache(cls, shipments):
        for shipment in shipments:
            cls.write([shipment], {
                    'origin_cache': cls.get_origin_name(shipment.origin, cache=True),
                    })

    @classmethod
    def cancel(cls, shipments):
        super(ShipmentOutReturn, cls).cancel(shipments)
        cls.store_origin_cache(shipments)

    @classmethod
    def receive(cls, shipments):
        super(ShipmentOutReturn, cls).receive(shipments)
        cls.store_origin_cache(shipments)
