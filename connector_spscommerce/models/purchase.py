# -*- coding: utf-8 -*-
# Copyright (c) Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from openerp import fields, models


class purchase_order_line(models.Model):
    _inherit = "purchase.order.line"

    asn_shipment = fields.Char('ASN Shipment Number from Converted 856')
    po_number = fields.Char('Line Item PO Number from Converted 856')
