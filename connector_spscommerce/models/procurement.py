# -*- coding: utf-8 -*-
# Copyright (c) Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from openerp import fields, models


class procurement_order(models.Model):
    _inherit = 'procurement.order'

    po_number = fields.Char('Line Item PO Number from Converted 856')
    edi_line_num = fields.Integer('EDI PO Line #')
    asn_shipment = fields.Char('ASN Shipment Number')
    ship_to_code = fields.Char('Ship To Warehouse',
                               help="Trading Partner Ship to location"
                                    " code.")
    sale_line_id = fields.Many2one('sale.order.line', 'Sale Order Line',
                                   help='Sale Order Line from whence this'
                                        ' Stock Move Was created')
    so_id = fields.Many2one('sale.order', 'Sale Order',
                            help='Sale Order from Whence this Invoice was'
                                 ' created')
    edi_yes = fields.Boolean('From an EDI PO?', readonly=True,
                             help="Is this order from an EDI purchase"
                                  " order, 850 EDI doc.")
    est_del_date = fields.Date('Estimated Delivery Date',
                               help="Calculated based on shipping method.")
    trading_partner_id = fields.Many2one('edi.config', 'Trading Partner',
                                         help='EDI Configuration'
                                              ' information for partner')
    ship_not_before_date = fields.Date('Do Not Ship Before This Date',
                                       help="Do Not Ship Before This"
                                            " Date.")
    cancel_after_date = fields.Date('Cancel if Shipped After This Date',
                                    help="Cancel if Shipped After This"
                                         " Date.")

    def _run_move_create(self, cr, uid, procurement, context=None):
        res = super(procurement_order, self). \
            _run_move_create(cr, uid, procurement=procurement, context=context)
        res['po_number'] = procurement.po_number or ''
        res['ship_to_code'] = procurement.ship_to_code or ''
        res['asn_shipment'] = procurement.asn_shipment or ''
        res['sale_line_id'] = procurement.sale_line_id.id or False
        res['edi_line_num'] = procurement.edi_line_num or 0
        res['so_id'] = procurement.so_id.id or False
        res['trading_partner_id'] = procurement.trading_partner_id and \
                                    procurement.trading_partner_id.id or False
        res['edi_yes'] = procurement.trading_partner_id and \
                         procurement.edi_yes or False
        res['ship_not_before_date'] = procurement.trading_partner_id and \
                                      procurement.ship_not_before_date or False
        res['cancel_after_date'] = procurement.trading_partner_id and \
                                   procurement.cancel_after_date or False

        return res
