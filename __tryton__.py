#This file is part stock_origin module for Tryton.
#The COPYRIGHT file at the top level of this repository contains 
#the full copyright notices and license terms.
{
    'name': 'Stock Origin',
    'name_ca_ES': 'Origen estoc',
    'name_es_ES': 'Origen stock',
    'version': '2.4.0',
    'author': 'Zikzakmedia',
    'email': 'zikzak@zikzakmedia.com',
    'website': 'http://www.zikzakmedia.com/',
    'description': '''Add origin of shipment: sale, TPV...''',
    'description_ca_ES': '''Afegeix l'origen del albarà: venda, TPV...''',
    'description_es_ES': '''Añade el origen del albarán: venta, TPV...''',
    'depends': [
        'ir',
        'res',
        'stock',
    ],
    'xml': [
        'shipment.xml',
    ],
    'translation': [
        'locale/ca_ES.po',
        'locale/es_ES.po',
    ]
}
