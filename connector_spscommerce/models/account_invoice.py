# Copyright (c) Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import re
import dicttoxml
from odoo import api, fields, models
from datetime import datetime
from odoo.addons import decimal_precision as dp
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DS
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DSD
from odoo.exceptions import UserError


class AccountInvoiceLine(models.Model):
    _inherit = "account.invoice.line"

    asn_shipment = fields.Char('ASN Shipment Number from Converted 856')
    po_number = fields.Char('Line Item PO Number from Converted 856')
    buyer_part_number = fields.Char('Buyer Part Number')
    edi_line_qty = fields.Float(
        'Original EDI Quantity',
        digits=dp.get_precision('Product Unit of Measure')
    )
    vendor_part_number = fields.Char('Vendor Part Number')
    consumer_package_code = fields.Char('Consumer Package Code')
    gtin = fields.Char('GTIN')
    upc_case_code = fields.Char('UPC Case Code')
    purchase_price_basis = fields.Char('Purchase PriceBasis')
    product_size_code = fields.Char('Product Size Code')
    product_size_description = fields.Char('Product Size Description')
    product_color_code = fields.Char('Product Color Code')
    product_color_description = fields.Char('Product Color Description')
    product_material_code = fields.Char('Product Material Code')
    product_material_description = fields.Char('Product Material Description')
    department = fields.Char('Department')
    classs = fields.Char('Class')
    price_type_id_code = fields.Char('PriceType ID Code')
    edi_line_num = fields.Integer('EDI PO line number')
    multiple_price_quantity = fields.Float('Multiple PriceQuantity')
    class_of_trade_code = fields.Char('Class Of Trade Code')
    item_description_type = fields.Char('Item Description Type')
    product_characteristic_code = fields.Char('Product Characteristic Code')
    agency_qualifier_code = fields.Char('Agency Qualifier Code')
    product_description_code = fields.Char('Product Description Code')
    pack_qualifier = fields.Char('Pack Qualifier')
    pack_value = fields.Integer('Pack Value')
    pack_size = fields.Char('Pack Size')
    pack_uom = fields.Char('Pack UOM')
    packing_medium = fields.Char('Packing Medium')
    packing_material = fields.Char('Packing Material')
    pack_weight = fields.Float('Pack Weight')
    pack_weight_uom = fields.Char('Pack Weight UOM')
    location_code_qualifier = fields.Char(
        'Location Code Qualifier',
        help="Code identifying the structure or format of the related"
        "location number(s)."
    )
    location = fields.Char(
        'Location',
        help="For CrossDock, it's the marked for location. For MultiStore"
        "[could also be DC] ship-to location."
    )
    allow_chrg_indicator = fields.Char(
        'Allow Chrg Indicator',
        help="Code which indicates an allowance or charge for the"
        "service specified."
    )
    allow_chrg_code = fields.Char(
        'Allow Chrg Code',
        help="Code describing the type of allowance or charge for the"
        "service specified."
    )
    allow_chrg_agency_code = fields.Char(
        'Allow Chrg Agency Code',
        help="Code identifying the agency assigning the code values."
    )
    allow_chrg_agency = fields.Char(
        'Allow Chrg Agency',
        help="Agency maintained code identifying the service, promotion,"
        "allowance, or charge."
    )
    allow_chrg_amt = fields.Float(
        'Allow Chrg Amt',
        help="Amount of the allowance or charge."
    )
    allow_chrg_percent = fields.Float(
        'Allow Chrg Percent',
        help='''Percentage of allowance or charge. Percentages should be
        represented as real numbers[0% through 100% should be normalized to
        0.0 through 100.00]..'''
    )
    percent_dollar_basis = fields.Float(
        'Percent Dollar Basis',
    )
    allow_chrg_rate = fields.Float(
        'Allow Chrg Rate',
        help="Amount of the allowance or charge."
    )
    allow_chrg_handling_code = fields.Char(
        'Allow Chrg Handling Code',
        help="Code indicating method of handling for an allowance or charge.."
    )
    allow_chrg_qty_uom = fields.Char('Allow Chrg Qty UOM')
    allow_chrg_handling_description = fields.Char(
        'Allow Chrg Handling Description',
        help="Free-form textual description of the note."
    )


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    asn_shipment = fields.Char('ASN Shipment Number from Converted 856')
    client_order_ref = fields.Text(
        'Customer PO #',
        help="Customer PO #"
    )
    ship_to_code = fields.Char(
        'Ship To Warehouse',
        help="Trading Partner Ship to location code."
    )
    supplier_code = fields.Char(
        'Supplier Code',
        help="This is the date from the 856."
    )
    edi_yes = fields.Boolean(
        'From an EDI PO?',
        # readonly=True,
        help="Is this order from an EDI purchase order, 850 EDI doc."
    )
    sent_timestamp = fields.Datetime(
        '810 Sent Date',
        help="The timestamp for when the 856 was sent."
    )
    trading_partner_id = fields.Many2one(
        'edi.config',
        'Trading Partner',
        help='EDI Configuration information for partner'
    )
    invoice_check = fields.Boolean(
        '810 EDI Invoice Sent?',
        readonly=True,
        help="Is checked if EDI 810 invoice is sent."
    )
    ship_not_before_date = fields.Date(
        'Estimated Shipping Date',
        help="This is the date from the 856."
    )
    cancel_after_date = fields.Date(
        'Cancel if Shipped After This Date',
        help="Cancel if Shipped After This Date."
    )
    sale_id = fields.Many2one(
        'sale.order',
        'Sale Order',
        help='Sale Order from Whence this Invoice Was created'
    )
    picking_id = fields.Many2one(
        'stock.picking',
        'Picking ID',
        help='Stock Picking ID whence this invoice was created'
    )
    scac_code = fields.Char(
        'SCAC Code',
        help="This is the shipping alpha code from your carrier."
    )
    bol_num = fields.Char(
        'BoL Number',
        help="This is bill of lading number from your carrier/shipper."
    )
    tracking_num = fields.Char(
        'Supplier Code',
        help="This is the tracking number from your carrier."
    )
    sender_id = fields.Char('EDI Sender Code')
    tset_purpose_code = fields.Char(
        'TsetPurposeCode',
        help="Code identifying purpose of the document.."
    )
    purchase_order_type_code = fields.Char(
        'Purchase Order Type Code',
        help="Code specifying the type of purchase order."
    )
    po_type_description = fields.Char(
        'PO Type Description',
        help="Free form text to describe the type of order."
    )
    ship_complete_code = fields.Char(
        'Ship Complete Code',
        help='''Code to identify a specific requirement or agreement of sale.
        Should only be used to indicate if an item can be
        placed on backorder.'''
    )
    department = fields.Char(
        'Department',
        help="Name or number identifying an area wherein merchandise is"
        "categorized within a store."
    )
    division = fields.Char(
        'Division',
        help="Different entities belonging to the same parent company."
    )
    promotion_deal_number = fields.Char(
        'Promotion Deal Number',
        help="Number uniquely identifying an agreement for a"
        "special offer or price."
    )
    carrier_pro_number = fields.Char('Carrier Pro Number')
    bill_of_lading_number = fields.Char('Bill Of Lading Number')
    terms_type = fields.Char(
        'Terms Type',
        help="Code identifying type of payment terms."
    )
    terms_basis_date_code = fields.Char(
        'Terms Basis Date Code',
        help="Code identifying the beginning of the terms period."
    )
    terms_discount_percentage = fields.Char(
        'Terms Discount Percentage',
        help="Terms discount percentage available to the purchaser"
    )
    terms_discount_due_days = fields.Char(
        'Terms Discount Due Days',
        help="Number of days by which payment or invoice must be received in"
        "order to receive the discount noted."
    )
    terms_net_due_days = fields.Char(
        'Terms Net Due Days',
        help="Number of days until total invoice amount is due[discount"
        "not applicable."
    )
    payment_method_code = fields.Char(
        'Payment Method Code',
        help="Indication of the instrument of payment."
    )
    fob_pay_code = fields.Char(
        'FOB Pay Code',
        help="Code identifying payment terms for transportation Charges."
    )
    fob_location_qualifier = fields.Char(
        'FOB Location Qualifier',
        help="Code identifying type of location at which ownership of"
        "goods is transferred."
    )
    fob_location_description = fields.Char(
        'FOB Location Description',
        help="Free-form textual description of the location at which"
        "ownership of goods is transferred."
    )
    fob_title_passage_code = fields.Char(
        'FOB Title Passage Code',
        help="Code describing the location of ownership of the goods."
    )
    fob_title_passage_location = fields.Char(
        'FOB Title Passage Location',
        help="Location of ownership of the goods."
    )
    carrier_trans_method_code = fields.Char(
        'Carrier Trans Method Code',
        help="Code specifying the method or type of transportation"
        "for the shipment."
    )
    carrier_alpha_code = fields.Char(
        'CarrierAlphaCode',
        help="Standard Carrier Alpha Code[SCAC] - "
    )
    carrier_routing = fields.Char(
        'CarrierRouting',
        help="Free-form description of the routing/requested routing for"
        "shipment or the originating carrier's identity."
    )
    routing_sequence_code = fields.Char('Routing Sequence Code')
    service_level_code = fields.Char(
        'Service Level Code',
        help="Code indicating the level of transportation service or the"
        "billing service offered by the transportation carrier."
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
        help="Free-form textual description to clarify the related data"
        "elements and their content."
    )
    note_code = fields.Char(
        'NoteCode',
        help="Code specifying the type of note."
    )
    note_information_field = fields.Char(
        'Note Information Field',
        help="Free-form textual description of the note."
    )
    allow_chrg_indicator = fields.Char(
        'Allow Chrg Indicator',
        help="Code which indicates an allowance or Charge for the"
        "service specified."
    )
    allow_chrg_code = fields.Char(
        'Allow Chrg Code',
        help="Code describing the type of allowance or Charge for"
        "the service specified."
    )
    allow_chrg_agency_code = fields.Char(
        'Allow Chrg Agency Code',
        help="Code identifying the agency assigning the code values."
    )
    allow_chrg_agency = fields.Char(
        'Allow Chrg Agency',
        help="Agency maintained code identifying the service, promotion,"
        "allowance, or charge."
    )
    allow_chrg_amt = fields.Float(
        'Allow Chrg Amt',
        help="Amount of the allowance or Charge."
    )
    allow_chrg_percent_qual = fields.Char(
        'Allow Chrg Percent Qual',
        help="Code indicating on what basis an allowance or charge"
        "percent is calculated.."
    )
    allow_chrg_percent = fields.Float(
        'Allow Chrg Percent',
        help='''Percentage of allowance or charge. Percentages should be
        represented as real numbers[0% through 100% should be
        normalized to 0.0 through 100.00]..'''
    )
    allow_chrg_handling_code = fields.Char(
        'Allow Chrg Handling Code',
        help="Code indicating method of handling for an allowance or charge.."
    )
    reference_identification = fields.Char('Reference Identification')
    allow_chrg_handling_description = fields.Char(
        'Allow Chrg Handling Description',
        help="Free-form textual description of the note."
    )

    @api.multi
    def create_text_810(self):

        today = str(datetime.now().strftime('%Y%m%d')) or ''
        processed = 0
        num = ''

        # for each invoice
        invoices_list = {'Invoices': []}
        for invoice in self:
            num += invoice.number or '1'

            # skip non customer invoice records
#                if invoice.type not in ('out_invoice'
#                        ) or invoice.state in ('draft', 'cancel', 'paid'):
#                    continue

            # Grab the vendor_id and trading_partner_id for EDI
            # in the edi_config.
            trading_partner_code = \
                invoice.trading_partner_id.partner_header_string or 'Test'
            vendor_code =\
                invoice.trading_partner_id.vendor_header_string or 'Test'

            # date_format = "%Y-%m-%d"
            # invoice date
            inv_date = invoice.date_invoice
            dateinv_object = datetime.strptime(inv_date, DS)
            inv_date = dateinv_object.date()
            inv_date = str(inv_date)

            # purchase date
            po_date = \
                invoice.purchase_id and invoice.purchase_id.date_order or ''
            if po_date:
                datepo_object = datetime.strptime(po_date, DS)
                po_date = datepo_object.date()
                po_date = str(po_date)

            # ship date
            ship_date = \
                invoice.picking_id and invoice.picking_id.date_done or ''
            if ship_date:
                ship_object = datetime.strptime(ship_date, DS)
                ship_date = ship_object.date()
                ship_date = str(ship_date)

            # initialize
            invoice_dict = {'Invoice': {}}
            # 1. Header Line - one line for the order
            meta_dict = {'Meta': {'Version': '1.0'}}
            header_dict = {'Header': {'InvoiceHeader': {
                'TradingPartnerId': trading_partner_code,
                'InvoiceNumber': str(invoice.number),
                'InvoiceDate': inv_date,
                'PurchaseOrderDate': po_date,
                'PurchaseOrderNumber':
                invoice.purchase_id and invoice.purchase_id.number or '',
                'ReleaseNumber': str(invoice.number),
                'InvoiceTypeCode': 'U5',
                'BuyersCurrency':
                invoice.currency_id and invoice.currency_id.name or '',
                'Department': invoice.department or '',
                'Vendor': vendor_code,
                'PromotionDealNumber': invoice.promotion_deal_number or '',
                'CarrierProNumber': invoice.carrier_pro_number or '',
                'BillOfLadingNumber': invoice.bill_of_lading_number,
                'ShipDate': ship_date,
                'CustomerOrderNumber':
                invoice.sale_id and invoice.sale_id.name or '',
            },
                'PaymentTerms': {
                    'TermsType': invoice.terms_type or '',
                    'TermsBasisDateCode': invoice.terms_basis_date_code or '',
                    'TermsDiscountPercentage':
                    invoice.terms_discount_percentage or '',
                    'TermsDiscountDate': inv_date,
                    'TermsDiscountDueDays':
                    invoice.terms_discount_due_days or '',
                    'TermsNetDueDate': inv_date,
                    'TermsNetDueDays': invoice.terms_net_due_days or '',
                    'TermsDiscountAmount': 0,
                    'TermsDescription': invoice.payment_term_id.note or '',
                },
                'Date': {
                    'DateTimeQualifier1': '196',
                    'Date1': inv_date,
                    'Time1': '',
                },
                'Contact': {
                    'ContactTypeCode': 'BD',
                    'ContactName':
                    invoice.picking_id and invoice.picking_id.partner_id and
                    invoice.picking_id.partner_id.name or '',
                    'PrimaryPhone':
                    invoice.picking_id and invoice.picking_id.partner_id and
                    invoice.picking_id.partner_id.phone or '',
                    'PrimaryFax':
                    invoice.picking_id and invoice.picking_id.partner_id and
                    invoice.picking_id.partner_id.fax or '',
                    'PrimaryEmail':
                    invoice.picking_id and invoice.picking_id.partner_id and
                    invoice.picking_id.partner_id.email or '',
                },
                'Address': {
                    'AddressTypeCode': 'Z7',
                    'LocationCodeQualifier': '92',
                    'AddressLocationNumber': '11111',
                    'AddressName': invoice.partner_id.name,
                    'Address1': invoice.partner_id.street,
                    'Address2': invoice.partner_id.street2,
                    'City': invoice.partner_id.city,
                    'State': invoice.partner_id.state_id.name,
                    'PostalCode': invoice.partner_id.zip,
                    'Country': invoice.partner_id.country_id.name,
                    'Contact': {
                        'ContactTypeCode': 'BD',
                        'ContactName': invoice.picking_id and
                        invoice.picking_id.partner_id and
                        invoice.partner_id.name or '',
                        'PrimaryPhone': invoice.picking_id and
                        invoice.picking_id.partner_id and
                        invoice.partner_id.phone or '',
                        'PrimaryFax': invoice.picking_id and
                        invoice.picking_id.partner_id and
                        invoice.partner_id.fax or '',
                        'PrimaryEmail': invoice.picking_id and
                        invoice.picking_id.partner_id and invoice.email or '',
                    },
                },
                'Reference': {
                    'ReferenceQual': invoice.reference_qual or '',
                    'ReferenceID': invoice.reference_id or '',
                    'Description': invoice.ref_description or '',
                },
                'Notes': {
                    'NoteCode': invoice.note_code or '',
                    'NoteInformationField':
                    invoice.note_information_field or '',
                },
                'Tax': {
                    'TaxTypeCode': 'S',
                    'TaxAmount': '1845.08',
                    'TaxPercent': '8.50',
                    'JurisdictionQual': 'CC',
                    'JurisdictionCode': '07034',
                    'TaxExemptCode': '2',
                    'TaxID': '99990000',
                },
                'ChargesAllowances': {
                    'AllowChrgIndicator': invoice.allow_chrg_indicator or '',
                    'AllowChrgCode': invoice.allow_chrg_code or '',
                    'AllowChrgAmt': invoice.allow_chrg_amt or 0,
                    'AllowChrgPercentQual':
                    invoice.allow_chrg_percent_qual or '',
                    'AllowChrgPercent': invoice.allow_chrg_percent or 0,
                    'AllowChrgHandlingCode':
                    invoice.allow_chrg_handling_code or '',
                    'AllowChrgHandlingDescription':
                    invoice.allow_chrg_handling_description or '',
                },
                'FOBRelatedInstruction': {
                    'FOBPayCode': invoice.fob_pay_code or '',
                    'FOBLocationQualifier':
                    invoice.fob_location_qualifier or '',
                    'FOBLocationDescription':
                    invoice.fob_location_description or '',
                    'FOBTitlePassageCode':
                    invoice.fob_title_passage_code or '',
                    'FOBTitlePassageLocation':
                    invoice.fob_title_passage_location or '',
                },
                'CarrierInformation': {
                    'CarrierTransMethodCode':
                    invoice.carrier_trans_method_code or '',
                    'CarrierAlphaCode': invoice.carrier_alpha_code or '',
                    'CarrierRouting': invoice.carrier_routing or '',
                    'CarrierEquipmentNumber':
                    invoice.routing_sequence_code or '',
                },
                'ServiceLevelCodes': {
                    'ServiceLevelCode': invoice.service_level_code or '',
                },
            }
            }
            invoice_dict.get('Invoice').update(meta_dict)
            invoice_dict.get('Invoice').update(header_dict)
            # LineItems
            lineitems_list = {'LineItems': []}
            total_lines = 0
            total_qty = 0
            total_weight = 0
            # for each item line
            for line in invoice.invoice_line_ids:
                total_lines += 1
                total_qty += line.quantity
                total_weight += (line.product_id.weight * line.quantity)
                lineitem_dict = {'LineItem': {}}
                invoiceline_dict = {'InvoiceLine': {
                    'LineSequenceNumber': int(line.id),
                    'BuyerPartNumber': line.buyer_part_number or '',
                    'VendorPartNumber': line.product_id.default_code or '',
                    'ConsumerPackageCode': '093597609541',
                    'EAN': line.product_id.barcode,
                    'GTIN': line.gtin or '',
                    'UPCCaseCode': line.upc_case_code or '',
                    'NatlDrugCode': '51456-299',
                    'InternationalStandardBookNumber': '999-0-555-22222-0',
                    'ProductID': {
                        'PartNumberQual': 'IS',
                        'PartNumber': line.product_id.default_code,
                    },
                    'PurchasePrice': line.price_unit,
                    'ShipQty': line.quantity,
                    'ShipQtyUOM': 'P4',
                    'ProductSizeCode': line.product_size_code or '',
                    'ProductSizeDescription':
                    line.product_size_description or '',
                    'ProductColorCode': line.product_color_code or '',
                    'ProductColorDescription':
                    line.product_color_description or '',
                    'ProductMaterialDescription':
                    line.product_material_description or '',
                    'NRFStandardColorAndSize': {
                        'NRFColorCode': '600',
                        'NRFSizeCode': '42-10651',
                    }
                },
                    'ProductOrItemDescription': {
                        'ItemDescriptionType':
                        line.item_description_type or '',
                        'AgencyQualifierCode':
                        line.agency_qualifier_code or '',
                        'ProductDescriptionCode':
                        line.product_id.default_code,
                        'ProductDescription': line.name,
                    },
                    'PhysicalDetails': {
                        'PackQualifier': line.pack_qualifier or '',
                        'PackValue': line.pack_value or 0,
                        'PackSize': line.pack_size or '',
                        'PackUOM': line.pack_uom or '',
                    },
                    'Tax': {
                        'TaxTypeCode': 'S',
                        'TaxAmount': '1845.08',
                        'TaxPercent': '8.50',
                        'JurisdictionQual': 'CC',
                        'JurisdictionCode': '07034',
                        'TaxExemptCode': '2',
                        'TaxID': '99990000',
                    },
                    'ChargesAllowances': {
                        'AllowChrgIndicator': line.allow_chrg_indicator or '',
                        'AllowChrgCode': line.allow_chrg_code or '',
                        'AllowChrgAmt': line.allow_chrg_amt or 0,
                        'AllowChrgPercentQual': '',
                        'AllowChrgPercent': line.allow_chrg_percent or 0,
                        'AllowChrgHandlingCode':
                        line.allow_chrg_handling_code or '',
                        'AllowChrgHandlingDescription':
                        line.allow_chrg_handling_description or '',
                    },
                }
                lineitem_dict.get('LineItem').update(invoiceline_dict)
                lineitems_list.get('LineItems').append(lineitem_dict)
            invoice_dict.get('Invoice').update(lineitems_list)

            # Summary
            summary_dict = {'Summary': {
                'TotalAmount': invoice.amount_total or '',
                'TotalNetSalesAmount': invoice.amount_untaxed,
                'TotalTermsDiscountAmount': 0,
                'TotalQtyInvoiced': total_qty,
                'TotalWeight': total_weight,
                'TotalLineItemNumber': total_lines,
                'InvoiceAmtDueByTermsDate': 0,
                'TotalQtyInvoicedUOM': 'P3',
                'TotalWeightUOM': 'HD',
            }
            }
            invoice_dict.get('Invoice').update(summary_dict)
            # update invoice
            today = datetime.now().strftime(DSD)
            invoice.write({'sent_timestamp': today})
            invoices_list.get('Invoices').append(invoice_dict)
            processed += 1

        # Convert dictionary to xml
        xml = dicttoxml.dicttoxml(invoices_list, attr_type=False, root=False)
        xml = xml.decode("utf-8")
        xml = xml.replace('<item>', '').replace('</item>', '')
        xml = xml.replace('<item>', '').\
            replace('<Invoices>',
                    '<?xml version="1.0" encoding="utf-8"?>' +
                    '<Invoices xmlns="http://www.spscommerce.com/RSX">')
        print("*****  SUCCESSFULLY STORED  *****")
        # Write ASN doc to text file
        num = re.findall('\d+', num)
        filename = '810_' + today + '%s.xml' % num
        filename.replace('/', '_')
        if not invoice.trading_partner_id.out_path:
            raise UserError('Add out path in Trading Partner')
        fd = open(invoice.trading_partner_id.out_path + filename, 'w')
        fd.write(xml)
        fd.close()
        return processed

    @api.model
    def _create_810_wrapper(self):
        # search for invoices that are edi_yes = True
        # and sent_timestamp = False.
        eligible_invoices = self.search([('edi_yes', '=', True),
                                         ('sent_timestamp', '=', False)])
        return eligible_invoices and\
            eligible_invoices.create_text_810() or False

    # done as a server action
    @api.multi
    def action_create_text_810(self):
        """ Creates a new 810 and puts it into the outbox
        """
        # number of orders to process
        toprocess = len(self.ids)
        # process orders to write 810
        processed = self.create_text_810()
        return (toprocess - processed)
