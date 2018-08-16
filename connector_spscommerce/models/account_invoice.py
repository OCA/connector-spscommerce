# -*- coding: utf-8 -*-
# Copyright (c) Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from datetime import datetime
import re
import dicttoxml
from openerp.osv import fields, osv
import openerp.addons.decimal_precision as dp


class account_invoice_line(osv.osv):
    _inherit = "account.invoice.line"

    _columns = {
        'asn_shipment': fields.char('ASN Shipment Number from Converted 856'),
        'po_number': fields.char('Line Item PO Number from Converted 856'),
        'buyer_part_number': fields.char(string='Buyer Part Number'),
        'edi_line_qty': fields.float('Original EDI Quantity', digits_compute=dp.get_precision('Product Unit of Measure')),
        'vendor_part_number': fields.char('VendorPartNumber'),
        'consumer_package_code': fields.char('ConsumerPackageCode'),
        'gtin': fields.char('GTIN'),
        'upc_case_code': fields.char('UPCCaseCode'),
        'purchase_price_basis': fields.char('PurchasePriceBasis'),
        'product_size_code': fields.char('ProductSizeCode'),
        'product_size_description': fields.char('ProductSizeDescription'),
        'product_color_code': fields.char('ProductColorCode'),
        'product_color_description': fields.char('ProductColorDescription'),
        'product_material_code': fields.char('ProductMaterialCode'),
        'product_material_description': fields.char('ProductMaterialDescription'),
        'department': fields.char('Department'),
        'classs': fields.char('Class'),
        'price_type_id_code': fields.char('PriceTypeIDCode'),
        'edi_line_num': fields.integer('EDI PO line number'),
        'multiple_price_quantity': fields.float('MultiplePriceQuantity'),
        'class_of_trade_code': fields.char('ClassOfTradeCode'),
        'item_description_type': fields.char('ItemDescriptionType'),
        'product_characteristic_code': fields.char('ProductCharacteristicCode'),
        'agency_qualifier_code': fields.char('AgencyQualifierCode'),
        'product_description_code': fields.char('ProductDescriptionCode'),
        'pack_qualifier': fields.char('PackQualifier'),
        'pack_value': fields.integer('PackValue'),
        'pack_size': fields.char('PackSize'),
        'pack_uom': fields.char('PackUOM'),
        'packing_medium': fields.char('PackingMedium'),
        'packing_material': fields.char('PackingMaterial'),
        'pack_weight': fields.float('PackWeight'),
        'pack_weight_uom': fields.char('PackWeightUOM'),
        'location_code_qualifier':fields.char('LocationCodeQualifier', help="Code identifying the structure or format of the related location number(s)."),
        'location':fields.char('Location', help="For CrossDock, it's the marked for location. For MultiStore[could also be DC] ship-to location."),
        'allow_chrg_indicator':fields.char('AllowChrgIndicator', help="Code which indicates an allowance or charge for the service specified."),
        'allow_chrg_code':fields.char('AllowChrgCode', help="Code describing the type of allowance or charge for the service specified."),
        'allow_chrg_agency_code':fields.char('AllowChrgAgencyCode', help="Code identifying the agency assigning the code values."),
        'allow_chrg_agency':fields.char('AllowChrgAgency', help="Agency maintained code identifying the service, promotion, allowance, or charge."),
        'allow_chrg_amt':fields.float('AllowChrgAmt', help="Amount of the allowance or charge."),
        'allow_chrg_percent':fields.float('AllowChrgPercent', help="Percentage of allowance or charge. Percentages should be represented as real numbers[0% through 100% should be normalized to 0.0 through 100.00].."),
        'percent_dollar_basis':fields.float('PercentDollarBasis', help="."),
        'allow_chrg_rate':fields.float('AllowChrgRate', help="Amount of the allowance or charge."),
        'allow_chrg_handling_code':fields.char('AllowChrgHandlingCode', help="Code indicating method of handling for an allowance or charge.."),
        'allow_chrg_qty_uom':fields.char('AllowChrgQtyUOM', help=""),
        'allow_chrg_handling_description':fields.char('AllowChrgHandlingDescription', help="Free-form textual description of the note."),
    }


class account_invoice(osv.osv):
    _inherit = "account.invoice"

    _columns = {
        'asn_shipment': fields.char('ASN Shipment Number from Converted 856'),
        'client_order_ref': fields.text('Customer PO #', help="Customer PO #"),
        'ship_to_code': fields.char('Ship To Warehouse', help="Trading Partner Ship to location code."),
        'supplier_code': fields.char('Supplier Code', help="This is the date from the 856."),
        'edi_yes': fields.boolean('From an EDI PO?', readonly=True, help="Is this order from an EDI purchase order, 850 EDI doc."),
        '810_sent_timestamp': fields.datetime('810 Sent Date', help="The timestamp for when the 856 was sent."),
        'trading_partner_id': fields.many2one('edi.config', 'Trading Partner', help='EDI Configuration information for partner'),
        'invoice_check': fields.boolean('810 EDI Invoice Sent?', readonly=True, help="Is checked if EDI 810 invoice is sent."),
        'ship_not_before_date': fields.date('Estimated Shipping Date', help="This is the date from the 856."),
        'cancel_after_date': fields.date('Cancel if Shipped After This Date', help="Cancel if Shipped After This Date."),
        'sale_id': fields.many2one('sale.order', 'Sale Order', help='Sale Order from Whence this Invoice Was created'),
        'picking_id': fields.many2one('stock.picking','Picking ID', help='Stock Picking ID whence this invoice was created'),
        'scac_code': fields.char('SCAC Code', help="This is the shipping alpha code from your carrier."),
        'bol_num': fields.char('BoL Number', help="This is bill of lading number from your carrier/shipper."),
        'tracking_num': fields.char('Supplier Code', help="This is the tracking number from your carrier."),
        'sender_id':fields.char(string='EDI Sender Code',),
        'tset_purpose_code':fields.char('TsetPurposeCode', help="Code identifying purpose of the document.."),
        'purchase_order_type_code':fields.char('PurchaseOrderTypeCode', help="Code specifying the type of purchase order."),
        'po_type_description':fields.char('POTypeDescription', help="Free form text to describe the type of order."),
        'ship_complete_code':fields.char('ShipCompleteCode', help="Code to identify a specific requirement or agreement of sale. Should only be used to indicate if an item can be placed on backorder."),
        'department':fields.char('Department', help="Name or number identifying an area wherein merchandise is categorized within a store."),
        'division':fields.char('Division', help="Different entities belonging to the same parent company."),
        'promotion_deal_number':fields.char('PromotionDealNumber', help="Number uniquely identifying an agreement for a special offer or price."),
        'carrier_pro_number':fields.char('CarrierProNumber', help=""),
        'bill_of_lading_number':fields.char('BillOfLadingNumber', help=""),
        'terms_type':fields.char('TermsType', help="Code identifying type of payment terms."),
        'terms_basis_date_code':fields.char('TermsBasisDateCode', help="Code identifying the beginning of the terms period."),
        'terms_discount_percentage':fields.char('TermsDiscountPercentage', help="Terms discount percentage available to the purchaser"),
        'terms_discount_due_days':fields.char('TermsDiscountDueDays', help="Number of days by which payment or invoice must be received in order to receive the discount noted."),
        'terms_net_due_days':fields.char('TermsNetDueDays', help="Number of days until total invoice amount is due[discount not applicable."),
        'payment_method_code':fields.char('PaymentMethodCode', help="Indication of the instrument of payment."),
        'fob_pay_code':fields.char('FOBPayCode', help="Code identifying payment terms for transportation charges."),
        'fob_location_qualifier':fields.char('FOBLocationQualifier', help="Code identifying type of location at which ownership of goods is transferred."),
        'fob_location_description':fields.char('FOBLocationDescription', help="Free-form textual description of the location at which ownership of goods is transferred."),
        'fob_title_passage_code':fields.char('FOBTitlePassageCode', help="Code describing the location of ownership of the goods."),
        'fob_title_passage_location':fields.char('FOBTitlePassageLocation', help="Location of ownership of the goods."),
        'carrier_trans_method_code':fields.char('CarrierTransMethodCode', help="Code specifying the method or type of transportation for the shipment."),
        'carrier_alpha_code':fields.char('CarrierAlphaCode', help="Standard Carrier Alpha Code[SCAC] - "),
        'carrier_routing':fields.char('CarrierRouting', help="Free-form description of the routing/requested routing for shipment or the originating carrier's identity."),
        'routing_sequence_code':fields.char('RoutingSequenceCode', help=""),
        'service_level_code':fields.char('ServiceLevelCode', help="Code indicating the level of transportation service or the billing service offered by the transportation carrier."),
        'reference_qual':fields.char('ReferenceQual', help="Code specifying the type of data in the ReferenceID/ReferenceDescription."),
        'reference_id':fields.char('ReferenceID', help="Code specifying the type of data in the ReferenceID/ReferenceDescription."),
        'ref_description':fields.char('Description', help="Free-form textual description to clarify the related data elements and their content."),
        'note_code':fields.char('NoteCode', help="Code specifying the type of note."),
        'note_information_field':fields.char('NoteInformationField', help="Free-form textual description of the note."),
        'allow_chrg_indicator':fields.char('AllowChrgIndicator', help="Code which indicates an allowance or charge for the service specified."),
        'allow_chrg_code':fields.char('AllowChrgCode', help="Code describing the type of allowance or charge for the service specified."),
        'allow_chrg_agency_code':fields.char('AllowChrgAgencyCode', help="Code identifying the agency assigning the code values."),
        'allow_chrg_agency':fields.char('AllowChrgAgency', help="Agency maintained code identifying the service, promotion, allowance, or charge."),
        'allow_chrg_amt':fields.float('AllowChrgAmt', help="Amount of the allowance or charge."),
        'allow_chrg_percent_qual':fields.char('AllowChrgPercentQual', help="Code indicating on what basis an allowance or charge percent is calculated.."),
        'allow_chrg_percent':fields.float('AllowChrgPercent', help="Percentage of allowance or charge. Percentages should be represented as real numbers[0% through 100% should be normalized to 0.0 through 100.00].."),
        'allow_chrg_handling_code':fields.char('AllowChrgHandlingCode', help="Code indicating method of handling for an allowance or charge.."),
        'reference_identification':fields.char('ReferenceIdentification', help=""),
        'allow_chrg_handling_description':fields.char('AllowChrgHandlingDescription', help="Free-form textual description of the note."),
    }
    
    def create_text_810(self, cr, uid, invoice_ids, context=None):
        
        today = str(datetime.now().strftime('%Y%m%d')) or ''
        processed = 0
        num = ''
        # for each invoice
        invoices_list = {'Invoices':[]}
        for invoice in self.browse(cr, uid, invoice_ids, context=context):
            num += invoice.number
            #skip non customer invoice records
            if invoice.type not in ('out_invoice') or invoice.state in ('draft','cancel','paid'):
                continue
            
            #Grab the vendor_id and trading_partner_id for EDI in the edi_config.
            trading_partner_code = invoice.trading_partner_id.partner_header_string
            vendor_code = invoice.trading_partner_id.vendor_header_string
            
            date_format = "%Y-%m-%d"
            #invoice date
            inv_date = invoice.date_invoice
            dateinv_object = datetime.strptime(inv_date, date_format)
            inv_date = dateinv_object.date()
            inv_date = str(inv_date)
            
            #purchase date
            po_date = invoice.purchase_id and invoice.purchase_id.date_order or ''
            if po_date:
                datepo_object = datetime.strptime(po_date, date_format)
                po_date = datepo_object.date()
                po_date = str(po_date)
            
            #ship date
            ship_date = invoice.picking_id and invoice.picking_id.date_done or ''
            if ship_date:
                ship_object = datetime.strptime(ship_date, date_format)
                ship_date = ship_object.date()
                ship_date = str(ship_date)
                
            # initialize
            invoice_dict = {'Invoice':{}}
            # 1. Header Line - one line for the order
            meta_dict = {'Meta': {'Version': '1.0'}}
            header_dict = {'Header': {'InvoiceHeader': {
                'TradingPartnerId': trading_partner_code,
                'InvoiceNumber': str(invoice.number),
                'InvoiceDate':inv_date,
                'PurchaseOrderDate':po_date,
                'PurchaseOrderNumber':invoice.purchase_id and invoice.purchase_id.number or '',
                'ReleaseNumber':str(invoice.number),
                'InvoiceTypeCode':'U5',
                'BuyersCurrency':invoice.currency_id and invoice.currency_id.name or '',
                'Department':invoice.department or '',
                'Vendor':vendor_code,
                'PromotionDealNumber':invoice.promotion_deal_number or '',
                'CarrierProNumber':invoice.carrier_pro_number or '',
                'BillOfLadingNumber':invoice.bill_of_lading_number,
                'ShipDate':ship_date,
                'CustomerOrderNumber':invoice.sale_id and invoice.sale_id.name or '',
            },
                'PaymentTerms': {
                    'TermsType':invoice.terms_type or '',
                    'TermsBasisDateCode':invoice.terms_basis_date_code or '',
                    'TermsDiscountPercentage':invoice.terms_discount_percentage or '',
                    'TermsDiscountDate':inv_date,
                    'TermsDiscountDueDays':invoice.terms_discount_due_days or '',
                    'TermsNetDueDate':inv_date,
                    'TermsNetDueDays':invoice.terms_net_due_days or '',
                    'TermsDiscountAmount':0,
                    'TermsDescription':invoice.payment_term_id.note or '',
                },
                'Date': {                                                    
                    'DateTimeQualifier1':'196',
                    'Date1':inv_date,
                    'Time1':'',
                },
                'Contact':{
                    'ContactTypeCode':'BD',
                    'ContactName':invoice.picking_id and invoice.picking_id.partner_id and invoice.picking_id.partner_id.name or '',
                    'PrimaryPhone':invoice.picking_id and invoice.picking_id.partner_id and invoice.picking_id.partner_id.phone or '',
                    'PrimaryFax':invoice.picking_id and invoice.picking_id.partner_id and invoice.picking_id.partner_id.fax or '',
                    'PrimaryEmail':invoice.picking_id and invoice.picking_id.partner_id and invoice.picking_id.partner_id.email or '',
                },
                'Address':{
                    'AddressTypeCode':'Z7',
                    'LocationCodeQualifier':'92',
                    'AddressLocationNumber':'11111',
                    'AddressName':invoice.partner_id.name,
                    'Address1':invoice.partner_id.street,
                    'Address2':invoice.partner_id.street2,
                    'City':invoice.partner_id.city,
                    'State':invoice.partner_id.state_id.name,
                    'PostalCode':invoice.partner_id.zip,
                    'Country':invoice.partner_id.country_id.name,
                    'Contact':{
                        'ContactTypeCode':'BD',
                        'ContactName':invoice.picking_id and invoice.picking_id.partner_id and invoice.partner_id.name or '',
                        'PrimaryPhone':invoice.picking_id and invoice.picking_id.partner_id and invoice.partner_id.phone or '',
                        'PrimaryFax':invoice.picking_id and invoice.picking_id.partner_id and invoice.partner_id.fax or '',
                        'PrimaryEmail':invoice.picking_id and invoice.picking_id.partner_id and invoice.email or '',
                    },
                },
                'Reference':{
                    'ReferenceQual':invoice.reference_qual or '',
                    'ReferenceID':invoice.reference_id or '',
                    'Description':invoice.ref_description or '',
                },
                'Notes':{
                    'NoteCode':invoice.note_code or '',
                    'NoteInformationField':invoice.note_information_field or '',
                },
                'Tax':{
                    'TaxTypeCode':'S',
                    'TaxAmount':'1845.08',
                    'TaxPercent':'8.50',
                    'JurisdictionQual':'CC',
                    'JurisdictionCode':'07034',
                    'TaxExemptCode':'2',
                    'TaxID':'99990000',
                },
                'ChargesAllowances':{
                    'AllowChrgIndicator':invoice.allow_chrg_indicator or '',
                    'AllowChrgCode':invoice.allow_chrg_code or '',
                    'AllowChrgAmt':invoice.allow_chrg_amt or 0,
                    'AllowChrgPercentQual':invoice.allow_chrg_percent_qual or '',
                    'AllowChrgPercent':invoice.allow_chrg_percent or 0,
                    'AllowChrgHandlingCode':invoice.allow_chrg_handling_code or '',
                    'AllowChrgHandlingDescription':invoice.allow_chrg_handling_description or '',
                },
                'FOBRelatedInstruction':{
                    'FOBPayCode':invoice.fob_pay_code or '',
                    'FOBLocationQualifier': invoice.fob_location_qualifier or '',
                    'FOBLocationDescription':invoice.fob_location_description or '',
                    'FOBTitlePassageCode': invoice.fob_title_passage_code or '',
                    'FOBTitlePassageLocation':invoice.fob_title_passage_location or '',
                },
                'CarrierInformation':{
                    'CarrierTransMethodCode':invoice.carrier_trans_method_code or '',
                    'CarrierAlphaCode':invoice.carrier_alpha_code or '',
                    'CarrierRouting':invoice.carrier_routing or '',
                    'CarrierEquipmentNumber':invoice.routing_sequence_code or '',
                },
                'ServiceLevelCodes':{
                    'ServiceLevelCode':invoice.service_level_code or '',
                },
            }
            }
            invoice_dict.get('Invoice').update(meta_dict)
            invoice_dict.get('Invoice').update(header_dict)
            #LineItems
            lineitems_list = {'LineItems': []}
            total_lines = 0
            total_qty = 0
            total_weight = 0
            #for each item line
            for line in invoice.invoice_line_ids:
                total_lines += 1
                total_qty += line.quantity
                total_weight += (line.product_id.weight * line.quantity)        
                lineitem_dict = {'LineItem':{}}
                invoiceline_dict = {'InvoiceLine': {
                    'LineSequenceNumber':int(line.id),
                    'BuyerPartNumber':line.buyer_part_number or '',
                    'VendorPartNumber':line.product_id.default_code or '',
                    'ConsumerPackageCode':'093597609541',
                    'EAN':line.product_id.barcode,
                    'GTIN':line.gtin or '',
                    'UPCCaseCode':line.upc_case_code or '',
                    'NatlDrugCode':'51456-299',
                    'InternationalStandardBookNumber':'999-0-555-22222-0',
                    'ProductID':{
                        'PartNumberQual':'IS',
                        'PartNumber':line.product_id.default_code,
                    },
                    'PurchasePrice':line.price_unit,
                    'ShipQty':line.quantity,
                    'ShipQtyUOM':'P4',
                    'ProductSizeCode':line.product_size_code or '',
                    'ProductSizeDescription':line.product_size_description or '',
                    'ProductColorCode':line.product_color_code or '',
                    'ProductColorDescription':line.product_color_description or '',
                    'ProductMaterialDescription':line.product_material_description or '',
                    'NRFStandardColorAndSize':{
                        'NRFColorCode':'600',
                        'NRFSizeCode':'42-10651',                    
                    }
                },
                    'ProductOrItemDescription':{
                        'ItemDescriptionType':line.item_description_type or '',
                        'AgencyQualifierCode':line.agency_qualifier_code or '',
                        'ProductDescriptionCode':line.product_id.default_code,
                        'ProductDescription':line.name,
                    },
                    'PhysicalDetails':{
                        'PackQualifier': line.pack_qualifier or '',
                        'PackValue':line.pack_value or 0,
                        'PackSize':line.pack_size or '',
                        'PackUOM':line.pack_uom or '',
                    },
                    'Tax':{
                        'TaxTypeCode':'S',
                        'TaxAmount':'1845.08',
                        'TaxPercent':'8.50',
                        'JurisdictionQual':'CC',
                        'JurisdictionCode':'07034',
                        'TaxExemptCode':'2',
                        'TaxID':'99990000',
                    },
                    'ChargesAllowances':{
                        'AllowChrgIndicator':line.allow_chrg_indicator or '',
                        'AllowChrgCode':line.allow_chrg_code or '',
                        'AllowChrgAmt':line.allow_chrg_amt or 0,
                        'AllowChrgPercentQual':'',
                        'AllowChrgPercent':line.allow_chrg_percent or 0,
                        'AllowChrgHandlingCode':line.allow_chrg_handling_code or '',
                        'AllowChrgHandlingDescription':line.allow_chrg_handling_description or '',
                    },
                }
                lineitem_dict.get('LineItem').update(invoiceline_dict)
                lineitems_list.get('LineItems').append(lineitem_dict)
            
            invoice_dict.get('Invoice').update(lineitems_list)
            
            # Summary
            summary_dict = {'Summary': {
                'TotalAmount':invoice.amount_total or '',
                'TotalNetSalesAmount':invoice.amount_untaxed,
                'TotalTermsDiscountAmount':0,
                'TotalQtyInvoiced':total_qty,
                'TotalWeight':total_weight,
                'TotalLineItemNumber':total_lines,
                'InvoiceAmtDueByTermsDate':0,
                'TotalQtyInvoicedUOM':'P3',
                'TotalWeightUOM':'HD',
            }
            }
            invoice_dict.get('Invoice').update(summary_dict)
            # update invoice
            today = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  
            invoice.write({'810_sent_timestamp':today})
            invoices_list.get('Invoices').append(invoice_dict)
            processed += 1
        # Convert dictionary to xml
        xml = dicttoxml.dicttoxml(invoices_list, attr_type=False, root=False)
        xml = xml.replace('<item>','').replace('</item>','')
        xml = xml.replace('<item>','').replace('<Invoices>','<?xml version="1.0" encoding="utf-8"?><Invoices xmlns="http://www.spscommerce.com/RSX">')
        # Write ASN doc to text file
        num = re.findall('\d+', num)[0]
        filename = '810_' + today + '%s.xml' % num
        filename.replace('/', '_')
        fd = open(invoice.trading_partner_id.out_path + filename, 'w')
        fd.write(xml)
        fd.close()
        return processed
    
    def _create_810_wrapper(self, cr, uid, context=None):
        #search for invoices that are edi_yes = True and 810_sent_timestamp = False.
        eligible_invoices = self.search(cr, uid, [('edi_yes','=',True),('810_sent_timestamp','=',False)], context=context)       
        return eligible_invoices and self.create_text_810(cr, uid, eligible_invoices, context=context) or False

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
