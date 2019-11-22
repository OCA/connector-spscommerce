# Copyright (c) Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    trading_partner_res = fields.One2many(
        'edi.config',
        'trading_partner_id',
        required=False,
        ondelete='cascade',
    )
    edi_ids = fields.One2many(
        'edi.config',
        'edi_company_id',
        'EDI Company ID'
    )
    ship_to_code = fields.Char('Ship to Code')
    sender_id = fields.Char('EDI Sender Code')
