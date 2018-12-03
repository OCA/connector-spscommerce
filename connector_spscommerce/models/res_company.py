# Copyright (c) Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    header_string = fields.Char('Company Header String')
    trading_partner_id = fields.Many2many(
        'edi.config',
        string='EDI Trading Partner',
        ondelete='cascade'
    )
