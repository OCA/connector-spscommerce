# -*- coding: utf-8 -*-
# Copyright (c) Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from openerp.osv import fields, osv

class purchase_order_line(osv.osv):
    _inherit = "purchase.order.line"
    
    _columns = {
        'asn_shipment': fields.char('ASN Shipment Number from Converted 856'),
        'po_number': fields.char('Line Item PO Number from Converted 856'),
    }
