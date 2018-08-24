# This file is part stock_origin module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.model import fields
from trytond.pool import Pool, PoolMeta

__all__ = ['Move', 'ShipmentOut', 'ShipmentOutReturn']


class StockOriginMixin(object):
    "Mixin Stock Origin"
    origin = fields.Function(fields.Reference(
            'Origin', selection='get_origin'),
        'get_origin_value')
    origin_cache = fields.Reference('Origin Cache', selection='get_origin')
    origin_info = fields.Function(fields.Char('Origin Info'),
        'on_change_with_origin_info')
    origin_number = fields.Function(fields.Char('Origin Number'),
        'get_origin_number', searcher='search_origin_number_field')
    origin_reference = fields.Function(fields.Char('Origin Reference'),
        'get_origin_reference', searcher='search_origin_reference_field')

    @classmethod
    def _get_origin(cls):
        'Model names that use in reference type field'
        return []

    @classmethod
    def _get_searcher_number(cls):
        'Model names that use to search with reference field'
        return []

    @classmethod
    def _get_searcher_reference(cls):
        'Model names that use to search with reference field'
        return []

    @classmethod
    def get_origin(cls):
        Model = Pool().get('ir.model')
        models = cls._get_origin()
        models = Model.search([
                ('model', 'in', models),
                ])
        return [('', '')] + [(m.model, m.name) for m in models]

    @staticmethod
    def get_origin_name(origin, cache=None):
        Model = Pool().get('ir.model')

        if not origin:
            return

        model, = Model.search([('model', '=', origin.__name__)], limit=1)

        if cache:
            return '%s,%s' % (origin.__name__, origin.id)

        if hasattr(origin, 'code'):
            return '%s,%s' % (model.name, origin.code)
        if hasattr(origin, 'number'):
            return '%s,%s' % (model.name, origin.number)
        if hasattr(origin, 'reference'):
            return '%s,%s' % (model.name, origin.reference)
        else:
            return '%s,%s' % (model.name, origin.id)

    @fields.depends('origin')
    def on_change_with_origin_info(self, name=None):
        if self.origin:
            origin = self.origin_cache if self.origin_cache else self.origin
            return self.get_origin_name(origin)

    def get_origin_number(self, name):
        origin = self.origin_cache if self.origin_cache else self.origin
        if hasattr(origin, 'number'):
            return origin.number

    @classmethod
    def search_origin_number_field(cls, name, clause):
        domain = []
        for model in cls._get_searcher_number():
            domain.append(
                ('origin_cache.number',) + tuple(clause[1:]) + (model,)
            )
        if len(domain) > 1:
            domain.insert(0, 'OR')
        return domain

    def get_origin_reference(self, name):
        origin = self.origin_cache if self.origin_cache else self.origin
        if hasattr(origin, 'reference'):
            return origin.reference

    @classmethod
    def search_origin_reference_field(cls, name, clause):
        domain = []
        for model in cls._get_searcher_reference():
            domain.append(
                ('origin_cache.reference',) + tuple(clause[1:]) + (model,)
            )
        if len(domain) > 1:
            domain.insert(0, 'OR')
        return domain

    @classmethod
    def store_origin_cache(cls, shipments):
        to_write = []
        for shipment in shipments:
            if shipment.origin_cache:
                continue
            to_write.extend(([shipment], {
                'origin_cache': cls.get_origin_name(
                            shipment.origin, cache=True),
                }))
        if to_write:
            cls.write(*to_write)


class Move(metaclass=PoolMeta):
    __name__ = 'stock.move'

    @classmethod
    def _get_origin(cls):
        models = super(Move, cls)._get_origin()
        if 'stock.shipment.out' not in models:
            models.append('stock.shipment.out')
        return models


class ShipmentOut(StockOriginMixin, metaclass=PoolMeta):
    __name__ = 'stock.shipment.out'

    @classmethod
    def get_origin_value(cls, shipments, name):
        origin = {}
        for shipment in shipments:
            origin[shipment.id] = None
        return origin

    @classmethod
    def cancel(cls, shipments):
        super(ShipmentOut, cls).cancel(shipments)
        cls.store_origin_cache(shipments)

    @classmethod
    def wait(cls, shipments):
        super(ShipmentOut, cls).wait(shipments)
        cls.store_origin_cache(shipments)


class ShipmentOutReturn(StockOriginMixin, metaclass=PoolMeta):
    __name__ = 'stock.shipment.out.return'
    origin_shipment = fields.Many2One('stock.shipment.out', 'Origin Shipment')

    @classmethod
    def _get_origin(cls):
        'Model names that use in reference type field'
        return ['stock.shipment.out']

    @classmethod
    def get_origin_value(cls, shipments, name):
        origin = {}
        for shipment in shipments:
            origin[shipment.id] = (
                'stock.shipment.out,%s' % (shipment.origin_shipment.id)
                if shipment.origin_shipment else None)
        return origin

    @classmethod
    def create(cls, vlist):
        shipments = super(ShipmentOutReturn, cls).create(vlist)
        cls.store_origin_cache(shipments)
        return shipments

    @classmethod
    def cancel(cls, shipments):
        super(ShipmentOutReturn, cls).cancel(shipments)
        cls.store_origin_cache(shipments)

    @classmethod
    def receive(cls, shipments):
        super(ShipmentOutReturn, cls).receive(shipments)
        cls.store_origin_cache(shipments)
