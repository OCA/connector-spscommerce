# Copyright (c) Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import api, fields, models


class EdiConfig(models.Model):
    _name = "edi.config"
    _description = "EDI Configuration Systems"

    edi_company_id = fields.Many2one(
        'res.company',
        string='EDI Company',
        help="The Main EDI Company.",
        ondelete='cascade'
    )
    route_id = fields.Many2one(
        'stock.location.route',
        string='Stock Transfer Route',
        help="""Select Dropshipping if applicable or another route. This will
        be the route used in sale order lines."""
    )
    vendor_header_string = fields.Char('EDI Vendor ID')
    partner_header_string = fields.Char('Partner Header ID')
    billto_header_string = fields.Char('Bill to Header ID')
    salesperson = fields.Many2one(
        'res.partner',
        string='Sales Person',
        help="The Salesperson for EDI Trading Partner.",
        ondelete='cascade'
    )
    in_path = fields.Char('EDI In Path')
    out_path = fields.Char('EDI Out Path')
    log_path = fields.Char('EDI Logs Path')
    archive_path = fields.Char('EDI Archive Path')
    trading_partner_id = fields.Many2one(
        'res.partner',
        string='Trading Partner',
        help="The trading partner for EDI.",
        ondelete='cascade'
    )
    is_thirdparty = fields.Boolean('Ship Directly to Customer')
    is_sku = fields.Boolean('Use SKU instead of UPC')
    auto_workflow = fields.Many2one(
        'sale.workflow.process',
        string='Automatic Workflow',
        ondelete='restrict'
    )
    ack_855 = fields.Boolean('EDI 855 Ack')
    ack_997 = fields.Boolean('EDI 997 Ack')

    @api.multi
    def name_get(self):
        res = []
        for record in self:
            res.append((record['id'], record.trading_partner_id.name))
        return res
