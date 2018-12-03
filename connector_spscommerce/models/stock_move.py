# Copyright (c) Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import api, fields, models


class StockMove(models.Model):
    _inherit = "stock.move"

    asn_shipment = fields.Char('ASN Shipment Number from 856')
    po_number = fields.Char('Line Item PO Number from 856')
    edi_line_num = fields.Integer('EDI PO line number')
    so_id = fields.Many2one(
        'sale.order',
        'Sale Order',
        help='Sale Order from when this Invoice was created'
    )
    edi_yes = fields.Boolean(
        'From an EDI PO?',
        help="Is this order from an EDI purchase order, 850 EDI doc."
    )
    ship_not_before_date = fields.Date(
        'Do Not Ship Before This Date',
        help="Do Not Ship Before This Date."
    )
    cancel_after_date = fields.Date(
        'Cancel if Shipped After This Date',
        help="Cancel if Shipped After This Date."
    )
    trading_partner_id = fields.Many2one(
        'edi.config',
        'Trading Partner',
        help='EDI Configuration information for partner'
    )
    package_code = fields.Selection(
        [('PLT71', 'PLT71'),
         ('CTN25', 'CTN25')],
        'Package Code',
        help="Pkg Code Qualifier.",
        default="PLT71"
    )
    product_material_description = fields.Char(
        'Product Material Description',
        help="ProductMaterialDescription"
    )
    consumer_package_code = fields.Char(
        'Consumer Package Code',
        help="ConsumerPackageCode"
    )
    gtin = fields.Char(
        'GTIN',
        help="GTIN"
    )
    upc_case_code = fields.Char(
        'UPC Case Code',
        help="UPCCaseCode"
    )
    natl_drug_code = fields.Char(
        'Natl Drug Code',
        help="NatlDrugCode"
    )
    international_standard_book_number = fields.Char(
        'International Standard Book Number',
        help="InternationalStandardBookNumber"
    )
    product_size_description = fields.Char(
        'Product Size Description',
        help="ProductSizeDescription"
    )
    product_color_description = fields.Char(
        'Product Color Description',
        help="ProductColorDescription"
    )

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
    po_number = fields.Char(
        'PO Number from EDI 850',
        help="PO Number from EDI 850."
    )
    edi_line_num = fields.Char(
        'Line Number from EDI 850',
        help="Line Number from EDI 850."
    )
    reference_qual = fields.Char(
        'Reference Qual',
        help="Code specifying the type of data in the"
        "ReferenceID/ReferenceDescription."
    )
    reference_id = fields.Char(
        'Reference ID',
        help="Code specifying the type of data in the"
        "ReferenceID/ReferenceDescription."
    )
    ref_description = fields.Char(
        'Description',
        help="Free-form textual description to clarify the"
        "related data elements and their content."
    )
    note_code = fields.Char(
        'Note Code',
        help="Code specifying the type of note."
    )
    note_information_field = fields.Char(
        'Note Information Field',
        help="Free-form textual description of the note."
    )
    pack_qualifier = fields.Char('Pack Qualifier')
    pack_value = fields.Char('Pack Value')
    pack_size = fields.Char('Pack Size')
    pack_uom = fields.Char('Pack UOM')
    packing_medium = fields.Char('Packing Medium')
    packing_material = fields.Char('Packing Material')

    @api.multi
    def _assign_picking(self):
        result = super(StockMove, self)._assign_picking()
        pick_ids = {}

        for move in self:
            picking = move.picking_id
            if not picking or pick_ids.get(picking.id, False):
                continue
            pick_ids[picking.id] = move.id
            edi_yes = move.procurement_id.edi_yes
            if edi_yes:
                res = {}
                res['trading_partner_id'] = \
                    move.procurement_id.trading_partner_id and\
                    move.procurement_id.trading_partner_id.id or False
                res['edi_yes'] = move.procurement_id.trading_partner_id\
                    and edi_yes or False
                res['ship_not_before_date'] = \
                    move.procurement_id.trading_partner_id and\
                    move.procurement_id.ship_not_before_date or False
                res['cancel_after_date'] = \
                    move.procurement_id.trading_partner_id and\
                    move.procurement_id.cancel_after_date or False
                picking.write(res)
        return result
