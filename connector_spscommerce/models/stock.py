# Copyright (c) Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import fields, models


class ProductPricelist(models.Model):
    _inherit = 'product.pricelist'

    def price_get_wrapper(self, prod_id, qty, partner=None):
        return self.price_rule_get(prod_id, qty, partner=partner)


class StockQuant(models.Model):
    _inherit = "stock.quant"

    tracking_number = fields.Char(
        'Tracking Number',
        help="Tracking Number"
    )
    bol = fields.Char(
        'Bill of Lading Number',
        help="Bill of Lading Number"
    )
    package_code = fields.Selection(
        [('PLT71', 'PLT71'), ('CTN25', 'CTN25')],
        'Package Code',
        help="Pkg Code Qualifier.",
        default="PLT71"
    )


class StockQuantPackage(models.Model):
    _inherit = "stock.quant.package"

    tracking_number = fields.Char(
        'Tracking Number',
        help="Tracking Number"
    )
    bol = fields.Char(
        'Bill of Lading Number',
        help="Bill of Lading Number"
    )
    package_code = fields.Selection(
        [('PLT71', 'PLT71'), ('CTN25', 'CTN25')],
        'Package Code',
        help="Pkg Code Qualifier.",
        default="PLT71"
    )


class DeliveryCarrier(models.Model):
    _inherit = "delivery.carrier"

    scac_code = fields.Char(
        'SCAC Ship Method Code',
        help="Shipping carrier code."
    )
