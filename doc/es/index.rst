==============================
Stock. Procedencia del albarán
==============================

Añade la procedencia del albarán de salida para relacionar con: venta...

Este módulo sólo añade el campo que relaciona un albarán con su origen.

Para que en el momento de generar el albarán se rellene automáticamente su
origen, instale los módulos correspondientes a su origen, por ejemplo:

* Albarán desde pedido de venta

En los listados de albaranes de cliente y albaranes de devolución se muestra
solamente los origenes en cache (no calculado) para ahorar tiempo de espera.

Para los albaranes de cliente se realiza la cache en el momento de "en espera".
Para los albaranes de devolución se realiza la cache en el momento de "recebido".
