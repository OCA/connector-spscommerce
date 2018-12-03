# Copyright (c) Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import fields, models


class ProcurementRule(models.Model):
    _inherit = 'procurement.rule'

    po_number = fields.Char('Line Item PO Number from Converted 856')
    edi_line_num = fields.Integer('EDI PO Line #')
    asn_shipment = fields.Char('ASN Shipment Number')
    ship_to_code = fields.Char(
        'Ship To Warehouse',
        help="Trading Partner Ship to location code."
    )
    sale_line_id = fields.Many2one(
        'sale.order.line',
        'Sale Order Line',
        help='Sale Order Line from whence this Stock Move Was created'
    )
    so_id = fields.Many2one(
        'sale.order',
        'Sale Order',
        help='Sale Order from Whence this Invoice was created'
    )
    edi_yes = fields.Boolean(
        'From an EDI PO?',
        readonly=True,
        help="Is this order from an EDI purchase order, 850 EDI doc."
    )
    est_del_date = fields.Date(
        'Estimated Delivery Date',
        help="Calculated based on shipping method."
    )
    trading_partner_id = fields.Many2one(
        'edi.config',
        'Trading Partner',
        help='EDI Configuration  information for partner'
    )
    ship_not_before_date = fields.Date(
        'Do Not Ship Before This Date',
        help="Do Not Ship Before This Date."
    )
    cancel_after_date = fields.Date(
        'Cancel if Shipped After This Date',
        help="Cancel if Shipped After This Date."
    )

    def _get_stock_move_values(self, product_id, product_qty, product_uom,
                               location_id, name, origin, values, group_id):
        res = super(ProcurementRule, self).\
            _get_stock_move_values(product_id, product_qty, product_uom,
                                   location_id, name, origin, values, group_id)
        res['po_number'] = self.po_number or ''
        res['ship_to_code'] = self.ship_to_code or ''
        res['asn_shipment'] = self.asn_shipment or ''
        res['sale_line_id'] = self.sale_line_id.id or False
        res['edi_line_num'] = self.edi_line_num or 0
        res['so_id'] = self.so_id.id or False
        res['trading_partner_id'] = self.trading_partner_id and\
            self.trading_partner_id.id or False
        res['edi_yes'] = self.trading_partner_id and self.edi_yes or False
        res['ship_not_before_date'] = self.trading_partner_id and\
            self.ship_not_before_date or False
        res['cancel_after_date'] = self.trading_partner_id and\
            self.cancel_after_date or False
        return res
