# -*- coding: utf-8 -*-
# Copyright (c) Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from openerp.osv import fields, orm, osv


class edi_config(osv.osv):
    _name = "edi.config"
    _description = "EDI Configuration Systems"

    _columns = {
        'edi_company_id': fields.many2one('res.company',
                                          string ='EDI Company',
                                          help="The Main EDI Company.",
                                          required=False, ondelete='cascade'),
        'route_id': fields.many2one('stock.location.route',
                                    string ='Stock Transfer Route',
                                    help="""Select Dropshipping if applicable
                                     or another route. This will be the route
                                      used in sale order lines."""),
        'vendor_header_string': fields.char(string='EDI Vendor ID',),
        'partner_header_string': fields.char(string='Partner Header ID',),
        'billto_header_string': fields.char(string='Bill to Header ID',),
        'salesperson': fields.many2one('res.partner', string='Sales Person',
                                      help="The Salesperson for EDI Trading"
                                           " Partner.",
                                      required=False, ondelete='cascade'),
        'in_path': fields.char(string='EDI In Path',),
        'out_path': fields.char(string='EDI Out Path',),
        'log_path': fields.char(string='EDI Logs Path',),
        'archive_path': fields.char(string='EDI Archive Path',),
        'trading_partner_id': fields.many2one('res.partner',
                                              string='Trading Partner',
                                              help="The trading partner for"
                                                   " EDI.",
                                              required=False,
                                              ondelete='cascade'),
        'is_thirdparty': fields.boolean('Ship Directly to Customer'),
        'is_sku': fields.boolean('Use SKU instead of UPC'),
        'auto_workflow': fields.many2one('sale.workflow.process',
                                         string='Automatic Workflow',
                                         ondelete='restrict'),
        'ack_855': fields.boolean('EDI 855 Ack'),
        'ack_997': fields.boolean('EDI 997 Ack'),
    }

    def name_get(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        res = []
        for record in self.browse(cr, uid, ids, context=context):
            res.append((record['id'], record.trading_partner_id.name))			
        return res


class company_config(orm.Model):
    _inherit = 'res.company'
    
    _columns = {
        'header_string': fields.char(string='Company Header String',),
        'trading_partner_id': fields.many2many('edi.config',
                                               string='EDI Trading Partner',
                                               required=False,
                                               ondelete='cascade'),
    }


class res_partner(orm.Model):
    _inherit = 'res.partner'
    
    _columns = {
        'trading_partner_res': fields.one2many('edi.config',
                                               'trading_partner_id',
                                               required=False,
                                               ondelete='cascade',
                                               help=''),
        'edi_ids': fields.one2many('edi.config', 'edi_company_id',
                                   'EDI Company ID'),
        'ship_to_code': fields.char(string='Ship to Code',),
        'sender_id': fields.char(string='EDI Sender Code',),
    }