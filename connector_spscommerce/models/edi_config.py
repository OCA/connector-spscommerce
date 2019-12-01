# -*- coding: utf-8 -*-
# Copyright (c) Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from openerp import fields, models


class edi_config(models.Model):
    _name = "edi.config"
    _description = "EDI Configuration Systems"

    edi_company_id = fields.Many2one('res.company',
                                     string='EDI Company',
                                     help="The Main EDI Company.",
                                     required=False, ondelete='cascade')
    route_id = fields.Many2one('stock.location.route',
                               string='Stock Transfer Route',
                               help="""Select Dropshipping if applicable
                                 or another route. This will be the route
                                  used in sale order lines.""")
    vendor_header_string = fields.Char(string='EDI Vendor ID', )
    partner_header_string = fields.Char(string='Partner Header ID', )
    billto_header_string = fields.Char(string='Bill to Header ID', )
    salesperson = fields.Many2one('res.partner', string='Sales Person',
                                  help="The Salesperson for EDI Trading"
                                       " Partner.",
                                  required=False, ondelete='cascade')
    in_path = fields.Char(string='EDI In Path', )
    out_path = fields.Char(string='EDI Out Path', )
    log_path = fields.Char(string='EDI Logs Path', )
    archive_path = fields.Char(string='EDI Archive Path', )
    trading_partner_id = fields.Many2one('res.partner',
                                         string='Trading Partner',
                                         help="The trading partner for"
                                              " EDI.",
                                         required=False,
                                         ondelete='cascade')
    is_thirdparty = fields.Boolean('Ship Directly to Customer')
    is_sku = fields.Boolean('Use SKU instead of UPC')
    auto_workflow = fields.Many2one('sale.workflow.process',
                                    string='Automatic Workflow',
                                    ondelete='restrict')
    ack_855 = fields.Boolean('EDI 855 Ack')
    ack_997 = fields.Boolean('EDI 997 Ack')

    def name_get(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        res = []
        for record in self.browse(cr, uid, ids, context=context):
            res.append((record['id'], record.trading_partner_id.name))
        return res


class company_config(models.Model):
    _inherit = 'res.company'

    header_string = fields.Char(string='Company Header String', )
    trading_partner_id = fields.Many2many('edi.config',
                                          string='EDI Trading Partner',
                                          required=False,
                                          ondelete='cascade')


class res_partner(models.Model):
    _inherit = 'res.partner'

    trading_partner_res = fields.One2many('edi.config',
                                          'trading_partner_id',
                                          required=False,
                                          ondelete='cascade',
                                          help='')
    edi_ids = fields.One2many('edi.config', 'edi_company_id',
                              'EDI Company ID')
    ship_to_code = fields.Char(string='Ship to Code', )
    sender_id = fields.Char(string='EDI Sender Code', )
