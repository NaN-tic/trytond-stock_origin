# This file is part stock_origin module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import Pool
from . import shipment


def register():
    Pool.register(
        shipment.Move,
        shipment.ShipmentOut,
        shipment.ShipmentOutReturn,
        module='stock_origin', type_='model')
