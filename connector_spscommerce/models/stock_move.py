# -*- coding: utf-8 -*-
# Copyright (c) Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from openerp import api, fields, models


class StockMove(models.Model):
    _inherit = "stock.move"
    
    asn_shipment = fields.Char('ASN Shipment Number from 856')
    po_number = fields.Char('Line Item PO Number from 856')
    edi_line_num = fields.Integer('EDI PO line number')
    sale_line_id = fields.Many2one('sale.order.line', 'Sale Order Line',
                                   help='Sale Order Line from Whence this'
                                        ' Stock Move Was created')
    so_id = fields.Many2one('sale.order', 'Sale Order',
                            help='Sale Order from when this Invoice was'
                                 ' created')
    edi_yes = fields.Boolean('From an EDI PO?',
                             help="Is this order from an EDI purchase order,"
                                  " 850 EDI doc.")
    ship_not_before_date = fields.Date('Do Not Ship Before This Date',
                                       help="Do Not Ship Before This Date.")
    cancel_after_date = fields.Date('Cancel if Shipped After This Date',
                                    help="Cancel if Shipped After This Date.")
    trading_partner_id = fields.Many2one('edi.config', 'Trading Partner',
                                         help='EDI Configuration information'
                                              ' for partner')
    package_code = fields.Selection((('PLT71', 'PLT71'),
                                     ('CTN25', 'CTN25')),
                                    'Package Code',
                                    help="Pkg Code Qualifier.",
                                    default="PLT71")
    
    @api.cr_uid_ids_context
    def _picking_assign(self, cr, uid, move_ids, context=None): 
        result = super(StockMove, self).\
            _picking_assign(cr, uid, move_ids, context=context)
        pick_ids = {}
        
        for move in self.browse(cr, uid, move_ids, context=context):
            picking = move.picking_id
            if not picking or pick_ids.get(picking.id, False):
                continue
            pick_ids[picking.id] = move.id
            edi_yes = move.procurement_id.edi_yes
            if edi_yes:
                res = {}
                res['trading_partner_id'] =\
                    move.procurement_id.trading_partner_id and\
                    move.procurement_id.trading_partner_id.id or False
                res['edi_yes'] = move.procurement_id.trading_partner_id\
                                 and edi_yes or False
                res['ship_not_before_date'] =\
                    move.procurement_id.trading_partner_id and\
                    move.procurement_id.ship_not_before_date or False
                res['cancel_after_date'] =\
                    move.procurement_id.trading_partner_id and\
                    move.procurement_id.cancel_after_date or False
                picking.write(res)
        return result
