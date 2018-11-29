# -*- coding: utf-8 -*-
# Copyright (c) Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import re
from datetime import datetime

import dicttoxml
import openerp.addons.decimal_precision as dp
from openerp import api, fields, models


class account_invoice_line(models.Model):
    _inherit = "account.invoice.line"

    asn_shipment = fields.Char('ASN Shipment Number from Converted 856')
    po_number = fields.Char('Line Item PO Number from Converted 856')
    buyer_part_number = fields.Char(string='Buyer Part Number')
    edi_line_qty = fields.Float('Original EDI Quantity',
                                digits_compute=dp.get_precision(
                                    'Product Unit of Measure'))
    vendor_part_number = fields.Char('VendorPartNumber')
    consumer_package_code = fields.Char('ConsumerPackageCode')
    gtin = fields.Char('GTIN')
    upc_case_code = fields.Char('UPCCaseCode')
    purchase_price_basis = fields.Char('PurchasePriceBasis')
    product_size_code = fields.Char('ProductSizeCode')
    product_size_description = fields.Char('ProductSizeDescription')
    product_color_code = fields.Char('ProductColorCode')
    product_color_description = fields.Char('ProductColorDescription')
    product_material_code = fields.Char('ProductMaterialCode')
    product_material_description = fields.Char(
        'ProductMaterialDescription')
    department = fields.Char('Department')
    classs = fields.Char('Class')
    price_type_id_code = fields.Char('PriceTypeIDCode')
    edi_line_num = fields.Integer('EDI PO line number')
    multiple_price_quantity = fields.Float('MultiplePriceQuantity')
    class_of_trade_code = fields.Char('ClassOfTradeCode')
    item_description_type = fields.Char('ItemDescriptionType')
    product_Characteristic_code = fields.Char(
        'ProductCharacteristicCode')
    agency_qualifier_code = fields.Char('AgencyQualifierCode')
    product_description_code = fields.Char('ProductDescriptionCode')
    pack_qualifier = fields.Char('PackQualifier')
    pack_value = fields.Integer('PackValue')
    pack_size = fields.Char('PackSize')
    pack_uom = fields.Char('PackUOM')
    packing_medium = fields.Char('PackingMedium')
    packing_material = fields.Char('PackingMaterial')
    pack_weight = fields.Float('PackWeight')
    pack_weight_uom = fields.Char('PackWeightUOM')
    location_code_qualifier = fields.Char('LocationCodeQualifier',
                                          help="Code identifying the structure or format of the related location number(s).")
    location = fields.Char('Location',
                           help="For CrossDock, it's the marked for location. For MultiStore[could also be DC] ship-to location.")
    allow_chrg_indicator = fields.Char('AllowChrgIndicator',
                                       help="Code which indicates an allowance or Charge for the service specified.")
    allow_chrg_code = fields.Char('AllowChrgCode',
                                  help="Code describing the type of allowance or Charge for the service specified.")
    allow_chrg_agency_code = fields.Char('AllowChrgAgencyCode',
                                         help="Code identifying the agency assigning the code values.")
    allow_chrg_agency = fields.Char('AllowChrgAgency',
                                    help="Agency maintained code identifying the service, promotion, allowance, or Charge.")
    allow_chrg_amt = fields.Float('AllowChrgAmt',
                                  help="Amount of the allowance or Charge.")
    allow_chrg_percent = fields.Float('AllowChrgPercent',
                                      help="Percentage of allowance or Charge. Percentages should be represented as real numbers[0% through 100% should be normalized to 0.0 through 100.00]..")
    percent_dollar_basis = fields.Float('PercentDollarBasis', help=".")
    allow_chrg_rate = fields.Float('AllowChrgRate',
                                   help="Amount of the allowance or Charge.")
    allow_chrg_handling_code = fields.Char('AllowChrgHandlingCode',
                                           help="Code indicating method of handling for an allowance or Charge..")
    allow_chrg_qty_uom = fields.Char('AllowChrgQtyUOM', help="")
    allow_chrg_handling_description = fields.Char(
        'AllowChrgHandlingDescription',
        help="Free-form textual description of the note.")


class account_invoice(models.Model):
    _inherit = "account.invoice"

    asn_shipment = fields.Char('ASN Shipment Number from Converted 856')
    client_order_ref = fields.Text('Customer PO #', help="Customer PO #")
    ship_to_code = fields.Char('Ship To Warehouse',
                               help="Trading Partner Ship to location code.")
    supplier_code = fields.Char('Supplier Code',
                                help="This is the date from the 856.")
    edi_yes = fields.Boolean('From an EDI PO?', readonly=True,
                             help="Is this order from an EDI purchase order, 850 EDI doc.")
    sent_timestamp_810 = fields.Datetime('810 Sent Date',
                                      help="The timestamp for when the 856 was sent.")
    trading_partner_id = fields.Many2one('edi.config', 'Trading Partner',
                                         help='EDI Configuration information for partner')
    invoice_check = fields.Boolean('810 EDI Invoice Sent?', readonly=True,
                                   help="Is checked if EDI 810 invoice is sent.")
    ship_not_before_date = fields.Date('Estimated Shipping Date',
                                       help="This is the date from the 856.")
    cancel_after_date = fields.Date('Cancel if Shipped After This Date',
                                    help="Cancel if Shipped After This Date.")
    sale_id = fields.Many2one('sale.order', 'Sale Order',
                              help='Sale Order from Whence this Invoice Was created')
    picking_id = fields.Many2one('stock.picking', 'Picking ID',
                                 help='Stock Picking ID whence this invoice was created')
    scac_code = fields.Char('SCAC Code',
                            help="This is the shipping alpha code from your carrier.")
    bol_num = fields.Char('BoL Number',
                          help="This is bill of lading number from your carrier/shipper.")
    tracking_num = fields.Char('Supplier Code',
                               help="This is the tracking number from your carrier.")
    sender_id = fields.Char(string='EDI Sender Code', )
    tset_purpose_code = fields.Char('TsetPurposeCode',
                                    help="Code identifying purpose of the document..")
    purchase_order_type_code = fields.Char('PurchaseOrderTypeCode',
                                           help="Code specifying the type of purchase order.")
    po_type_description = fields.Char('POTypeDescription',
                                      help="Free form text to describe the type of order.")
    ship_complete_code = fields.Char('ShipCompleteCode',
                                     help="Code to identify a specific requirement or agreement of sale. Should only be used to indicate if an item can be placed on backorder.")
    department = fields.Char('Department',
                             help="Name or number identifying an area wherein merchandise is categorized within a store.")
    division = fields.Char('Division',
                           help="Different entities belonging to the same parent company.")
    promotion_deal_number = fields.Char('PromotionDealNumber',
                                        help="Number uniquely identifying an agreement for a special offer or price.")
    carrier_pro_number = fields.Char('CarrierProNumber', help="")
    bill_of_lading_number = fields.Char('BillOfLadingNumber', help="")
    terms_type = fields.Char('TermsType',
                             help="Code identifying type of payment terms.")
    terms_basis_date_code = fields.Char('TermsBasisDateCode',
                                        help="Code identifying the beginning of the terms period.")
    terms_discount_percentage = fields.Char('TermsDiscountPercentage',
                                            help="Terms discount percentage available to the purchaser")
    terms_discount_due_days = fields.Char('TermsDiscountDueDays',
                                          help="Number of days by which payment or invoice must be received in order to receive the discount noted.")
    terms_net_due_days = fields.Char('TermsNetDueDays',
                                     help="Number of days until total invoice amount is due[discount not applicable.")
    payment_method_code = fields.Char('PaymentMethodCode',
                                      help="Indication of the instrument of payment.")
    fob_pay_code = fields.Char('FOBPayCode',
                               help="Code identifying payment terms for transportation Charges.")
    fob_location_qualifier = fields.Char('FOBLocationQualifier',
                                         help="Code identifying type of location at which ownership of goods is transferred.")
    fob_location_description = fields.Char('FOBLocationDescription',
                                           help="Free-form textual description of the location at which ownership of goods is transferred.")
    fob_title_passage_code = fields.Char('FOBTitlePassageCode',
                                         help="Code describing the location of ownership of the goods.")
    fob_title_passage_location = fields.Char('FOBTitlePassageLocation',
                                             help="Location of ownership of the goods.")
    carrier_trans_method_code = fields.Char('CarrierTransMethodCode',
                                            help="Code specifying the method or type of transportation for the shipment.")
    carrier_alpha_code = fields.Char('CarrierAlphaCode',
                                     help="Standard Carrier Alpha Code[SCAC] - ")
    carrier_routing = fields.Char('CarrierRouting',
                                  help="Free-form description of the routing/requested routing for shipment or the originating carrier's identity.")
    routing_sequence_code = fields.Char('RoutingSequenceCode', help="")
    service_level_code = fields.Char('ServiceLevelCode',
                                     help="Code indicating the level of transportation service or the billing service offered by the transportation carrier.")
    reference_qual = fields.Char('ReferenceQual',
                                 help="Code specifying the type of data in the ReferenceID/ReferenceDescription.")
    reference_id = fields.Char('ReferenceID',
                               help="Code specifying the type of data in the ReferenceID/ReferenceDescription.")
    ref_description = fields.Char('Description',
                                  help="Free-form textual description to clarify the related data elements and their content.")
    note_code = fields.Char('NoteCode',
                            help="Code specifying the type of note.")
    note_information_field = fields.Char('NoteInformationField',
                                         help="Free-form textual description of the note.")
    allow_chrg_indicator = fields.Char('AllowChrgIndicator',
                                       help="Code which indicates an allowance or Charge for the service specified.")
    allow_chrg_code = fields.Char('AllowChrgCode',
                                  help="Code describing the type of allowance or Charge for the service specified.")
    allow_chrg_agency_code = fields.Char('AllowChrgAgencyCode',
                                         help="Code identifying the agency assigning the code values.")
    allow_chrg_agency = fields.Char('AllowChrgAgency',
                                    help="Agency maintained code identifying the service, promotion, allowance, or Charge.")
    allow_chrg_amt = fields.float('AllowChrgAmt',
                                  help="Amount of the allowance or Charge.")
    allow_chrg_percent_qual = fields.Char('AllowChrgPercentQual',
                                          help="Code indicating on what basis an allowance or Charge percent is calculated..")
    allow_chrg_percent = fields.float('AllowChrgPercent',
                                      help="Percentage of allowance or Charge. Percentages should be represented as real numbers[0% through 100% should be normalized to 0.0 through 100.00]..")
    allow_chrg_handling_code = fields.Char('AllowChrgHandlingCode',
                                           help="Code indicating method of handling for an allowance or Charge..")
    reference_identification = fields.Char('ReferenceIdentification',
                                           help="")
    allow_chrg_handling_description = fields.Char(
        'AllowChrgHandlingDescription',
        help="Free-form textual description of the note.")

    def create_text_810(self, cr, uid, invoice_ids, context=None):

        today = str(datetime.now().strftime('%Y%m%d')) or ''
        processed = 0
        num = ''
        # for each invoice
        invoices_list = {'Invoices': []}
        for invoice in self.browse(cr, uid, invoice_ids, context=context):
            num += invoice.number
            # skip non customer invoice records
            if invoice.type not in ('out_invoice') or invoice.state in (
                    'draft', 'cancel', 'paid'):
                continue

            # Grab the vendor_id and trading_partner_id for EDI in the edi_config.
            trading_partner_code = invoice.trading_partner_id.partner_header_string
            vendor_code = invoice.trading_partner_id.vendor_header_string

            date_format = "%Y-%m-%d"
            # invoice date
            inv_date = invoice.date_invoice
            dateinv_object = datetime.strptime(inv_date, date_format)
            inv_date = dateinv_object.date()
            inv_date = str(inv_date)

            # purchase date
            po_date = invoice.purchase_id and invoice.purchase_id.date_order or ''
            if po_date:
                datepo_object = datetime.strptime(po_date, date_format)
                po_date = datepo_object.date()
                po_date = str(po_date)

            # ship date
            ship_date = invoice.picking_id and invoice.picking_id.date_done or ''
            if ship_date:
                ship_object = datetime.strptime(ship_date, date_format)
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
                'PurchaseOrderNumber': invoice.purchase_id and invoice.purchase_id.number or '',
                'ReleaseNumber': str(invoice.number),
                'InvoiceTypeCode': 'U5',
                'BuyersCurrency': invoice.currency_id and invoice.currency_id.name or '',
                'Department': invoice.department or '',
                'Vendor': vendor_code,
                'PromotionDealNumber': invoice.promotion_deal_number or '',
                'CarrierProNumber': invoice.carrier_pro_number or '',
                'BillOfLadingNumber': invoice.bill_of_lading_number,
                'ShipDate': ship_date,
                'CustomerOrderNumber': invoice.sale_id and invoice.sale_id.name or '',
            },
                'PaymentTerms': {
                    'TermsType': invoice.terms_type or '',
                    'TermsBasisDateCode': invoice.terms_basis_date_code or '',
                    'TermsDiscountPercentage': invoice.terms_discount_percentage or '',
                    'TermsDiscountDate': inv_date,
                    'TermsDiscountDueDays': invoice.terms_discount_due_days or '',
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
                    'ContactName': invoice.picking_id and invoice.picking_id.partner_id and invoice.picking_id.partner_id.name or '',
                    'PrimaryPhone': invoice.picking_id and invoice.picking_id.partner_id and invoice.picking_id.partner_id.phone or '',
                    'PrimaryFax': invoice.picking_id and invoice.picking_id.partner_id and invoice.picking_id.partner_id.fax or '',
                    'PrimaryEmail': invoice.picking_id and invoice.picking_id.partner_id and invoice.picking_id.partner_id.email or '',
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
                        'ContactName': invoice.picking_id and invoice.picking_id.partner_id and invoice.partner_id.name or '',
                        'PrimaryPhone': invoice.picking_id and invoice.picking_id.partner_id and invoice.partner_id.phone or '',
                        'PrimaryFax': invoice.picking_id and invoice.picking_id.partner_id and invoice.partner_id.fax or '',
                        'PrimaryEmail': invoice.picking_id and invoice.picking_id.partner_id and invoice.email or '',
                    },
                },
                'Reference': {
                    'ReferenceQual': invoice.reference_qual or '',
                    'ReferenceID': invoice.reference_id or '',
                    'Description': invoice.ref_description or '',
                },
                'Notes': {
                    'NoteCode': invoice.note_code or '',
                    'NoteInformationField': invoice.note_information_field or '',
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
                    'AllowChrgPercentQual': invoice.allow_chrg_percent_qual or '',
                    'AllowChrgPercent': invoice.allow_chrg_percent or 0,
                    'AllowChrgHandlingCode': invoice.allow_chrg_handling_code or '',
                    'AllowChrgHandlingDescription': invoice.allow_chrg_handling_description or '',
                },
                'FOBRelatedInstruction': {
                    'FOBPayCode': invoice.fob_pay_code or '',
                    'FOBLocationQualifier': invoice.fob_location_qualifier or '',
                    'FOBLocationDescription': invoice.fob_location_description or '',
                    'FOBTitlePassageCode': invoice.fob_title_passage_code or '',
                    'FOBTitlePassageLocation': invoice.fob_title_passage_location or '',
                },
                'CarrierInformation': {
                    'CarrierTransMethodCode': invoice.carrier_trans_method_code or '',
                    'CarrierAlphaCode': invoice.carrier_alpha_code or '',
                    'CarrierRouting': invoice.carrier_routing or '',
                    'CarrierEquipmentNumber': invoice.routing_sequence_code or '',
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
                    'ProductSizeDescription': line.product_size_description or '',
                    'ProductColorCode': line.product_color_code or '',
                    'ProductColorDescription': line.product_color_description or '',
                    'ProductMaterialDescription': line.product_material_description or '',
                    'NRFStandardColorAndSize': {
                        'NRFColorCode': '600',
                        'NRFSizeCode': '42-10651',
                    }
                },
                    'ProductOrItemDescription': {
                        'ItemDescriptionType': line.item_description_type or '',
                        'AgencyQualifierCode': line.agency_qualifier_code or '',
                        'ProductDescriptionCode': line.product_id.default_code,
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
                        'AllowChrgHandlingCode': line.allow_chrg_handling_code or '',
                        'AllowChrgHandlingDescription': line.allow_chrg_handling_description or '',
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
            today = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            invoice.write({'sent_timestamp_810': today})
            invoices_list.get('Invoices').append(invoice_dict)
            processed += 1
        # Convert dictionary to xml
        xml = dicttoxml.dicttoxml(invoices_list, attr_type=False, root=False)
        xml = xml.replace('<item>', '').replace('</item>', '')
        xml = xml.replace('<item>', '').replace('<Invoices>',
                                                '<?xml version="1.0" encoding="utf-8"?><Invoices xmlns="http://www.spscommerce.com/RSX">')
        # Write ASN doc to text file
        num = re.findall('\d+', num)[0]
        filename = '810_' + today + '%s.xml' % num
        filename.replace('/', '_')
        fd = open(invoice.trading_partner_id.out_path + filename, 'w')
        fd.write(xml)
        fd.close()
        return processed

    def _create_810_wrapper(self, cr, uid, context=None):
        # search for invoices that are edi_yes = True and sent_timestamp_810 = False.
        eligible_invoices = self.search(cr, uid, [('edi_yes', '=', True), (
            'sent_timestamp_810', '=', False)], context=context)
        return eligible_invoices and self.create_text_810(cr, uid,
                                                          eligible_invoices,
                                                          context=context) or False

    # done as a server action        
    def action_create_text_810(self, cr, uid, ids, context=None):
        """ Creates a new 810 and puts it into the outbox
        """
        if context is None:
            context = {}
        # number of orders to process
        toprocess = len(ids)
        # process orders to write 810
        processed = self.create_text_810(cr, uid, ids, context=context)
        return (toprocess - processed)
