# Copyright (c) Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import fields, models


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    asn_shipment = fields.Char('ASN Shipment Number from Converted 856')
    po_number = fields.Char('Line Item PO Number from Converted 856')
    edi_yes = fields.Boolean(
        'From an EDI PO?',
        help="Is this order from an EDI purchase order, 850 EDI doc."
    )
