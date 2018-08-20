# -*- coding: utf-8 -*-
# Copyright (c) Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import re
from datetime import datetime, timedelta
from random import randint
from openerp import api, models
import openerp.addons.decimal_precision as dp
from openerp.osv import fields, osv
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT


class SaleOrder(models.Model):
    _inherit = "sale.order"

    _columns = {
        'asn_shipment': fields.char('ASN Number from 856'),
        'edi_error': fields.text('EDI Errors', help="Text that will describe failures to add sale order lines because of failing product lookups."),
        'edi_yes': fields.boolean('From an EDI PO?', help="Is this order from an EDI purchase order, 850 EDI doc."),
        'ack_yes': fields.boolean('855', help="Will this order have an 855?"),
        '855_replace': fields.boolean('Send 855', readonly=True, help="Shall we send an 855 replacement?"),
        'ship_to_code': fields.char('Ship To Warehouse', help="Trading Partner Ship to location code."),
        'supplier_code': fields.char('Supplier Code', help="Supplier code from the 856."),
        'ship_not_before_date': fields.date('Estimated Shipping Date', help="This is the date from the 856."),
        'cancel_after_date': fields.date('Cancel if Shipped After This Date', help="Cancel if Shipped After This Date."),
        'trading_partner_id': fields.many2one('edi.config', 'Trading Partner', help='EDI Configuration information for partner'),
        '855_sent_timestamp': fields.datetime('855 Sent Date', help="The timestamp for when the 855 was sent."),
        '855_check': fields.boolean('855 Sent Already', help="A check to see if 855 has been sent already."),
        'scac_code': fields.char('SCAC Code', help="This is the shipping alpha code from your carrier."),
        'bol_num': fields.char('BoL Number', help="This is bill of lading number from your carrier/shipper."),
        'tracking_num': fields.char('Tracking Number', help="This is the tracking number from your carrier."),
        'tset_purpose_code':fields.char('TsetPurposeCode', help="Code identifying purpose of the document.."),
        'purchase_order_type_code':fields.char('PurchaseOrderTypeCode', help="Code specifying the type of purchase order."),
        'po_type_description':fields.char('POTypeDescription', help="Free form text to describe the type of order."),
        'ship_complete_code':fields.char('ShipCompleteCode', help="Code to identify a specific requirement or agreement of sale. Should only be used to indicate if an item can be placed on backorder."),
        'department':fields.char('Department', help="Name or number identifying an area wherein merchandise is categorized within a store."),
        'division':fields.char('Division', help="Different entities belonging to the same parent company."),
        'promotion_deal_number':fields.char('PromotionDealNumber', help="Number uniquely identifying an agreement for a special offer or price."),
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

    def create_855(self, cr, uid, sale_ids, context=None):
    
        xml_output = '<?xml version="1.0" encoding="utf-8"?><OrderAcks xmlns="http://www.spscommerce.com/RSX"><OrderAck><Meta><Version>testVersion</Version></Meta><Header>'
        
        for sale_id in sale_ids:
        
            # initialize
            csvwriter = None
            sale_obj = self.browse(cr, uid, sale_id, context=context)
            config_obj = sale_obj.trading_partner_id
            OUT_PATH = config_obj.out_path
            sale_lines = sale_obj.order_line          
            sale_name = sale_obj.name        
            num = re.findall('\d+', sale_name)[0]  
            po_num = ''
            
            if sale_obj.client_order_ref:
                po_num = sale_obj.client_order_ref
            
            # create and format dates for ACK
            now = datetime.now()
            today = now.strftime('%Y%m%d')
            time = datetime.now().strftime('%H%M%S')
            po_date = datetime.strptime(sale_obj.date_order, '%Y-%m-%d %H:%M:%S') 
            po_date = po_date.strftime('%m/%d/%Y')
            
            # generate random numbers for the 3 header id numbers in 855
            ISA_num = randint(100000000, 999999999)
            GS_code = randint(1000000, 9999999)
            st_trans_num = randint(100000000, 999999999)

            # Grab the vendor_id and trading_partner_id for EDI in the edi_config.
            trading_partner_code = sale_obj.trading_partner_id.partner_header_string
            trading_partner_padded = trading_partner_code.ljust(15)

            vendor_code = sale_obj.trading_partner_id.vendor_header_string
            vendor_padded = vendor_code.ljust(15)
            OUT_PATH = str(sale_obj.trading_partner_id.out_path)
            
            # header, payment  and date info
            xml_output += '<OrderHeader><TradingPartnerId>' + trading_partner_code + '</TradingPartnerId>'
            xml_output += '<PurchaseOrderNumber>' + po_num + '</PurchaseOrderNumber>'
            xml_output += '<TsetPurposeCode>' + str(sale_obj.tset_purpose_code) + '</TsetPurposeCode>'
            xml_output += '<PurchaseOrderDate>' + po_date + '</PurchaseOrderDate>'
            xml_output += '<PurchaseOrderTypeCode>' + str(sale_obj.purchase_order_type_code) + '</PurchaseOrderTypeCode>'
            xml_output += '<POTypeDescription>' + str(sale_obj.po_type_description) + '</POTypeDescription>'
            xml_output += '<ReleaseNumber>' + po_num + '</ReleaseNumber>'
            xml_output += '<AcknowledgementType>RJ</AcknowledgementType>'
            xml_output += '<AcknowledgementDate>' + today + '</AcknowledgementDate>'
            xml_output += '<ShipCompleteCode>' + str(sale_obj.ship_complete_code) + '</ShipCompleteCode>'
            xml_output += '<BuyersCurrency>' + str(sale_obj.pricelist_id.currency_id.name) + '</BuyersCurrency>'
            xml_output += '<Department>' + str(sale_obj.department) + '</Department>'
            xml_output += '<Division>' + str(sale_obj.division) + '</Division>'
            xml_output += '<CustomerOrderNumber>' + str(sale_obj.name) + '</CustomerOrderNumber>'
            xml_output += '<PromotionDealNumber>' + str(sale_obj.promotion_deal_number) + '</PromotionDealNumber>'
            xml_output += '<Vendor>' + vendor_code + '</Vendor></OrderHeader>'
            xml_output += '<PaymentTerms><TermsType>' + str(sale_obj.terms_type) + '</TermsType>'
            xml_output += '<TermsBasisDateCode>' + str(sale_obj.terms_basis_date_code) + '</TermsBasisDateCode>'
            xml_output += '<TermsDiscountPercentage>' + str(sale_obj.terms_discount_percentage) + '</TermsDiscountPercentage>'
            xml_output += '<TermsDiscountDueDays>' + str(sale_obj.terms_discount_due_days) + '</TermsDiscountDueDays>'
            xml_output += '<TermsNetDueDays>' + str(sale_obj.terms_net_due_days) + '</TermsNetDueDays>'
            xml_output += '<TermsDescription>' + str(sale_obj.payment_term_id.note) + '</TermsDescription>'
            xml_output += '<PaymentMethodCode>' + str(sale_obj.payment_method_code) + '</PaymentMethodCode></PaymentTerms>'
            xml_output += '<Date><DateTimeQualifier1>ORS</DateTimeQualifier1>'
            xml_output += '<Date1>' + today + '</Date1></Date>'
            cust_rec = sale_obj.partner_id
            ship_address_rec = sale_obj.partner_shipping_id
            
            # customer contact details
            xml_output += '<Contact><ContactTypeCode>CH</ContactTypeCode>'
            xml_output += '<ContactName>' + str(cust_rec.name) + '</ContactName>'
            xml_output += '<PrimaryPhone>' + str(cust_rec.phone) + '</PrimaryPhone>'
            xml_output += '<PrimaryFax>' + str(cust_rec.fax) + '</PrimaryFax>'
            xml_output += '<PrimaryEmail>' + str(cust_rec.email) + '</PrimaryEmail></Contact>'

            # contact address details
            xml_output += '<Address><AddressTypeCode>FW</AddressTypeCode>'
            xml_output += '<LocationCodeQualifier>1</LocationCodeQualifier>'
            xml_output += '<AddressLocationNumber>11111</AddressLocationNumber>'
            xml_output += '<AddressName>' + str(ship_address_rec.name) + '</AddressName>'
            xml_output += '<Address1>' + str(ship_address_rec.street) + '</Address1>'
            xml_output += '<Address2>' + str(ship_address_rec.street2) + '</Address2>'
            xml_output += '<City>' + str(ship_address_rec.city) + '</City>'
            xml_output += '<State>' + str(ship_address_rec.state_id.code) + '</State>'
            xml_output += '<PostalCode>' + str(ship_address_rec.zip) + '</PostalCode>'
            xml_output += '<Country>' + str(ship_address_rec.country_id.code) + '</Country>'
            xml_output += '<Contact><ContactTypeCode>CH</ContactTypeCode>'
            xml_output += '<ContactName>' + str(cust_rec.name) + '</ContactName>'
            xml_output += '<PrimaryPhone>' + str(cust_rec.phone) + '</PrimaryPhone>'
            xml_output += '<PrimaryFax>' + str(cust_rec.fax) + '</PrimaryFax>'
            xml_output += '<PrimaryEmail>' + str(cust_rec.email) + '</PrimaryEmail></Contact></Address>'
            
            # FOBRelatedInstruction
            xml_output += '<FOBRelatedInstruction><FOBPayCode>' + str(sale_obj.fob_pay_code) + '</FOBPayCode>'
            xml_output += '<FOBLocationQualifier>' + str(sale_obj.fob_location_qualifier) + '</FOBLocationQualifier>'
            xml_output += '<FOBLocationDescription>' + str(sale_obj.fob_location_description) + '</FOBLocationDescription>'
            xml_output += '<FOBTitlePassageCode>' + str(sale_obj.fob_title_passage_code) + '</FOBTitlePassageCode>'
            xml_output += '<FOBTitlePassageLocation>' + str(sale_obj.fob_title_passage_location) + '</FOBTitlePassageLocation></FOBRelatedInstruction>'
            
            # CarrierInformation
            xml_output += '<CarrierInformation><CarrierTransMethodCode>' + str(sale_obj.carrier_trans_method_code) + '</CarrierTransMethodCode>'
            xml_output += '<CarrierAlphaCode>' + str(sale_obj.carrier_alpha_code) + '</CarrierAlphaCode>'
            xml_output += '<CarrierRouting>' + str(sale_obj.carrier_routing) + '</CarrierRouting>'
            xml_output += '<RoutingSequenceCode>' + str(sale_obj.routing_sequence_code) + '</RoutingSequenceCode>'
            xml_output += '<ServiceLevelCodes><ServiceLevelCode>' + str(sale_obj.service_leve_code) + '</ServiceLevelCode></ServiceLevelCodes></CarrierInformation>'
            
            # Reference
            xml_output += '<Reference><ReferenceQual>' + str(sale_obj.reference_qual) + '</ReferenceQual>'
            xml_output += '<ReferenceID>' + str(sale_obj.reference_id) + '</ReferenceID>'
            xml_output += '<Description>' + str(sale_obj.ref_description) + '</Description></Reference>'
            
            # Notes
            xml_output += '<Notes><NoteCode>' + str(sale_obj.note_code) + '</NoteCode>'
            xml_output += '<NoteInformationField>' + str(sale_obj.note_information_field) + '</NoteInformationField></Notes>'
            
            # ChargesAllowances
            xml_output += '<ChargesAllowances><AllowChrgIndicator>' + str(sale_obj.allow_chrg_indicator) + '</AllowChrgIndicator>'
            xml_output += '<AllowChrgCode>' + str(sale_obj.allow_chrg_code) + '</AllowChrgCode>'
            xml_output += '<AllowChrgAgencyCode>' + str(sale_obj.allow_chrg_agency_code) + '</AllowChrgAgencyCode>'
            xml_output += '<AllowChrgAgency>' + str(sale_obj.allow_chrg_agency) + '</AllowChrgAgency>'
            xml_output += '<AllowChrgAmt>' + str(sale_obj.allow_chrg_amt) + '</AllowChrgAmt>'
            xml_output += '<AllowChrgPercentQual>' + str(sale_obj.allow_chrg_percent_qual) + '</AllowChrgPercentQual>'
            xml_output += '<AllowChrgPercent>' + str(sale_obj.allow_chrg_percent) + '</AllowChrgPercent>'
            xml_output += '<AllowChrgHandlingCode>' + str(sale_obj.allow_chrg_handling_code) + '</AllowChrgHandlingCode>'
            xml_output += '<ReferenceIdentification>' + str(sale_obj.reference_identification) + '</ReferenceIdentification>'
            xml_output += '<AllowChrgHandlingDescription>' + str(sale_obj.allow_chrg_handling_description) + '</AllowChrgHandlingDescription></ChargesAllowances></Header><LineItems>'
            
            total_lines = 0
            total_qty = 0
            total_weight = 0
            # Create the text string for 855 order acknowledgement
            for line in sale_lines:
                total_lines += 1
                est_del_date = ''
                est_ship_date = ''
                accept_code = ''
                
                if line.edi_est_ship_date:
                    est_ship_date = datetime.strptime(line.edi_est_ship_date, '%Y-%m-%d')       
                    est_ship_date = est_ship_date.strftime('%m/%d/%Y')
                        
                if line.edi_line_msg == 'reject':
                    accept_code = 'CC'
                    
                elif line.edi_line_msg == 'backorder':
                    accept_code = 'IB'
                    
                else:
                    accept_code = 'IA'
                    
                uom = line.product_uom.name 
                quantity = int(line.product_uom_qty)
                total_qty += quantity
                total_weight += (line.product_id.weight * quantity)    
                original_po_qty = int(line.edi_line_qty)
                
                if uom == 'Unit(s)':
                    uom = 'EA'
                    
                else:
                    print "*****  UOM is Not EA (Each)  *****"                            
                
                # line items
                xml_output += '<LineItem><OrderLine>'
                xml_output += '<LineSequenceNumber>' + str(line.id) + '</LineSequenceNumber>'
                xml_output += '<BuyerPartNumber>' + str(line.buyer_part_number) + '</BuyerPartNumber>'
                xml_output += '<VendorPartNumber>' + str(line.vendor_part_number) + '</VendorPartNumber>'
                xml_output += '<ConsumerPackageCode>' + str(line.consumer_package_code) + '</ConsumerPackageCode>'
                xml_output += '<GTIN>' + str(line.gtin) + '</GTIN>'
                xml_output += '<UPCCaseCode>' + str(line.upc_case_code) + '</UPCCaseCode>'
                xml_output += '<ProductID><PartNumberQual>MN</PartNumberQual>'
                xml_output += '<PartNumber>' + str(line.product_id.default_code) + '</PartNumber></ProductID>'
                xml_output += '<OrderQty>' + str(uom) + '</OrderQty>'
                xml_output += '<OrderQtyUOM>' + str(line.edi_line_qty) + '</OrderQtyUOM>'
                xml_output += '<PurchasePrice>' + str(line.price_unit) + '</PurchasePrice>'
                xml_output += '<PurchasePriceBasis>' + str(line.purchase_price_basis) + '</PurchasePriceBasis>'
                xml_output += '<BuyersCurrency>' + str(sale_obj.pricelist_id.currency_id.name) + '</BuyersCurrency>'
                xml_output += '<ProductSizeCode>' + str(line.product_size_code) + '</ProductSizeCode>'
                xml_output += '<ProductSizeDescription>' + str(line.product_size_description) + '</ProductSizeDescription>'
                xml_output += '<ProductColorCode>' + str(line.product_color_code) + '</ProductColorCode>'
                xml_output += '<ProductColorDescription>' + str(line.product_color_description) + '</ProductColorDescription>'
                xml_output += '<ProductMaterialCode>' + str(line.product_material_code) + '</ProductMaterialCode>'
                xml_output += '<ProductMaterialDescription>' + str(line.product_material_description) + '</ProductMaterialDescription>'
                xml_output += '<Department>' + str(line.department) + '</Department>'
                xml_output += '<Class>' + str(line.classs) + '</Class></OrderLine>'
                
                # date
                xml_output += '<Date><DateTimeQualifier1>' + str(line.price_unit) + '</DateTimeQualifier1>'
                xml_output += '<Date1>' + today + '</Date1></Date>'
                
                # PriceInformation
                xml_output += '<PriceInformation><PriceTypeIDCode>' + str(line.price_unit) + '</PriceTypeIDCode>'
                xml_output += '<UnitPrice>' + str(line.price_unit) + '</UnitPrice>'
                xml_output += '<Quantity>' + str(quantity) + '</Quantity>'
                xml_output += '<MultiplePriceQuantity>' + str(line.multiple_price_quantity) + '</MultiplePriceQuantity>'
                xml_output += '<ClassOfTradeCode>' + str(line.class_of_trade_code) + '</ClassOfTradeCode></PriceInformation>'
                
                # ProductOrItemDescription
                xml_output += '<ProductOrItemDescription><ItemDescriptionType>' + str(line.item_description_type) + '</ItemDescriptionType>'
                xml_output += '<ProductCharacteristicCode>' + str(line.product_characteristic_code) + '</ProductCharacteristicCode>'
                xml_output += '<AgencyQualifierCode>' + str(line.agency_qualifier_code) + '</AgencyQualifierCode>'
                xml_output += '<ProductDescriptionCode>' + str(line.product_description_code) + '</ProductDescriptionCode>'
                xml_output += '<ProductDescription>' + str(line.name) + '</ProductDescription></ProductOrItemDescription>'
                
                # PhysicalDetails
                xml_output += '<PhysicalDetails><PackQualifier>' + str(line.pack_qualifier) + '</PackQualifier>'
                xml_output += '<PackValue>' + str(line.pack_value) + '</PackValue>'
                xml_output += '<PackSize>' + str(line.pack_size) + '</PackSize>'
                xml_output += '<PackUOM>' + str(line.pack_uom) + '</PackUOM>'
                xml_output += '<PackingMedium>' + str(line.packing_medium) + '</PackingMedium>'
                xml_output += '<PackingMaterial>' + str(line.packing_material) + '</PackingMaterial>'
                xml_output += '<PackWeight>' + str(line.pack_weight) + '</PackWeight>'
                xml_output += '<PackWeightUOM>' + str(line.pack_weight_uom) + '</ProductDescription></PackWeightUOM>'
                
                # Reference
                xml_output += '<Reference><ReferenceQual>' + str(sale_obj.reference_qual) + '</ReferenceQual>'
                xml_output += '<ReferenceID>' + str(sale_obj.reference_id) + '</ReferenceID>'
                xml_output += '<Description>' + str(sale_obj.ref_description) + '</Description></Reference>'
                
                # Notes
                xml_output += '<Notes><NoteCode>' + str(sale_obj.note_code) + '</NoteCode>'
                xml_output += '<NoteInformationField>' + str(sale_obj.note_information_field) + '</NoteInformationField></Notes>'
                
                # contact address details
                xml_output += '<Address><AddressTypeCode>FW</AddressTypeCode>'
                xml_output += '<AddressName>' + str(ship_address_rec.name) + '</AddressName>'
                xml_output += '<Address1>' + str(ship_address_rec.street) + '</Address1>'
                xml_output += '<City>' + str(ship_address_rec.city) + '</City>'
                xml_output += '<State>' + str(ship_address_rec.state_id.code) + '</State>'
                xml_output += '<PostalCode>' + str(ship_address_rec.zip) + '</PostalCode>'
                xml_output += '<Country>' + str(ship_address_rec.country_id.code) + '</Country></Address>'
                
                # ChargesAllowances
                xml_output += '<ChargesAllowances><AllowChrgIndicator>' + str(line.allow_chrg_indicator) + '</AllowChrgIndicator>'
                xml_output += '<AllowChrgCode>' + str(line.allow_chrg_code) + '</AllowChrgCode>'
                xml_output += '<AllowChrgAgencyCode>' + str(line.allow_chrg_agency_code) + '</AllowChrgAgencyCode>'
                xml_output += '<AllowChrgAgency>' + str(line.allow_chrg_agency) + '</AllowChrgAgency>'
                xml_output += '<AllowChrgAmt>' + str(line.allow_chrg_amt) + '</AllowChrgAmt>'
                xml_output += '<AllowChrgPercent>' + str(line.allow_chrg_percent) + '</AllowChrgPercent>'
                xml_output += '<PercentDollarBasis>' + str(line.percent_dollar_basis) + '</PercentDollarBasis>'
                xml_output += '<AllowChrgRate>' + str(line.allow_chrg_rate) + '</AllowChrgRate>'
                xml_output += '<AllowChrgQtyUOM>' + str(line.allow_chrg_qty_uom) + '</AllowChrgQtyUOM>'
                xml_output += '<AllowChrgHandlingCode>' + str(line.allow_chrg_handling_code) + '</AllowChrgHandlingCode>'
                xml_output += '<AllowChrgHandlingDescription>' + str(line.allow_chrg_handling_description) + '</AllowChrgHandlingDescription></ChargesAllowances>'
                
                # line item acknowledgement                
                xml_output += '<LineItemAcknowledgement>'
                xml_output += '<ItemStatusCode>' + str(line.edi_line_msg) + '</ItemStatusCode>'
                xml_output += '<ItemScheduleQty>' + str(quantity) + '</ItemScheduleQty>'
                xml_output += '<ItemScheduleUOM>' + str(uom) + '</ItemScheduleUOM>'
                xml_output += '<ItemScheduleQualifier>002</ItemScheduleQualifier>'
                xml_output += '<ItemScheduleDate>' + str(line.edi_est_ship_date) + '</ItemScheduleDate></LineItemAcknowledgement>'
                    
                xml_output += '<PriceInformation><PriceTypeIDCode>FCP</PriceTypeIDCode>'
                xml_output += '<UnitPrice>' + str(line.price_unit) + '</UnitPrice></PriceInformation>'
                
                for tax in line.tax_id:
                
                    xml_output += '<Tax><TaxTypeCode>H780</TaxTypeCode>'
                    xml_output += '<TaxAmount>' + str(1 + tax.amount / 100 * line.price_unit) + '</TaxAmount>'
                    xml_output += '<TaxPercent>' + str(tax.amount / 100) + '</TaxPercent><TaxExemptCode>0</TaxExemptCode><TaxID>99990000</TaxID></Tax>'
                    
                xml_output += '</LineItem>'
                
            xml_output += '</LineItems>'
            
            # Summary
            xml_output += '<Summary><TotalAmount>' + str(sale_obj.amount_total) + '</TotalAmount>'
            xml_output += '<TotalLineItemNumber>' + str(total_lines) + '</TotalLineItemNumber>'
            xml_output += '<TotalQuantity>' + str(total_qty) + '</TotalQuantity>'
            xml_output += '<TotalWeight>' + str(total_weight) + '</TotalWeight>'
            xml_output += '<TotalWeightUOM>0</TotalWeightUOM>'
            xml_output += '<TotalVolume>0</TotalVolume>'
            xml_output += '<TotalVolumeUOM>0</TotalVolumeUOM></Summary>'
            
            date_format = "%Y-%m-%d %H:%M:%S"
            now = datetime.now()
            today = now.strftime(date_format)  
            sale_obj.write({'855_check':True, '855_sent_timestamp':today})
            print "*****  SUCCESSFULLY STORED  *****"
            
            xml_output += '</OrderAck></OrderAcks>'
                
            # Write ASN doc to text file    
            filename = '855_' + today + '%s.txt' % num
            filename.replace('/', '_')
            fd = open(OUT_PATH + '/' + filename, 'w')
            fd.write(xml_output)
            fd.close()
            
        return True
                   
    def _create_855_wrapper(self, cr, uid, context=None):
    
        # search for invoices that are ack_yes = True, edi_yes = True and 855_sent_timestamp = False
        eligible_orders = self.search(cr, uid, [('ack_yes', '=', True), ('edi_yes', '=', True), ('855_sent_timestamp', '=', False)], context=context)
        
        return eligible_orders and self.create_855(cr, uid, eligible_orders, context=context) or False
          
    def action_send_855(self, cr, uid, ids, context=None):
        """ Creates and new 855 and puts it into the outbox
        """
        if context is None:
            context = {}
        
        # execute the create_855 method
        self.create_855(cr, uid, ids, context=None)              
            
        return True
        
    @api.multi
    def _prepare_order_line_procurement(self, group_id=False):
    
        self.ensure_one()
        res = super(SaleOrder, self)._prepare_order_line_procurement(group_id=group_id)
        
        for sale_line in self.order_line:
        
            res['po_number'] = sale_line.po_number or ''
            res['asn_shipment'] = sale_line.asn_shipment or '' 
            res['sale_line_id'] = sale_line.id or False  
            res['edi_line_num'] = sale_line.edi_line_num or 0      
            res['so_id'] = self.id or False
            res['ship_to_code'] = self.ship_to_code or ''
            res['trading_partner_id'] = self.trading_partner_id and self.trading_partner_id.id or False
            res['edi_yes'] = self.trading_partner_id and self.edi_yes or False
            res['ship_not_before_date'] = self.trading_partner_id and self.ship_not_before_date or False
            res['cancel_after_date'] = self.trading_partner_id and self.cancel_after_date or False
            
        return res

    @api.model
    def _prepare_procurement_group(self):

        res = super(SaleOrder, self)._prepare_procurement_group()       
        res['trading_partner_id'] = self.trading_partner_id and self.trading_partner_id.id or False
        # res['edi_yes'] = self.trading_partner_id and self.edi_yes or False
        res['edi_yes'] = True
        res['asn_shipment'] = self.asn_shipment or 'asn_id'
        res['ship_to_code'] = self.ship_to_code or ''
        res['ship_not_before_date'] = self.trading_partner_id and self.ship_not_before_date or False
        res['cancel_after_date'] = self.trading_partner_id and self.cancel_after_date or False
        res['po_number'] = self.client_order_ref or ''   

        return res
        
    @api.multi        
    def test_edi_status(self):
        
        for line in self.order_line:
        
            if line.edi_yes and not line.edi_line_msg and line.ack_yes:            
                return False
                
        return True
        
    @api.multi
    def _prepare_invoice(self):
        """
        Prepare the dict of values to create the new invoice for a sales order. This method may be
        overridden to implement custom invoice generation (making sure to call super() to establish
        a clean extension chain).
        """
        stock_picking_obj = self.pool['stock.picking']
        pick = False
        
        for pick in self.picking_ids:
            
            if pick.picking_type_id.id == 2:

                break
        
        res = super(SaleOrder, self)._prepare_invoice()       
        res['sale_id'] = self.id or False
        res['bol_num'] = self.picking_ids and pick and pick.bol_num or self.bol_num or ''
        res['picking_ids'] = self.picking_ids
        res['scac_code'] = self.picking_ids and pick and pick.carrier_id.scac_code or self.scac_code or False
        res['tracking_num'] = self.picking_ids and pick and pick.tracking_number or ''
        res['sender_id'] = self.partner_id.sender_id or ''
        res['asn_shipment'] = pick and pick.name or ''       
        res['trading_partner_id'] = self.trading_partner_id.id or False
        res['edi_yes'] = self.edi_yes or False
        res['ship_not_before_date'] = self.ship_not_before_date or False
        res['cancel_after_date'] = self.cancel_after_date or False
        res['supplier_code'] = self.supplier_code or False
        res['ship_to_code'] = self.ship_to_code or False
        res['client_order_ref'] = self.client_order_ref or False
        res['tset_purpose_code'] = self.tset_purpose_code or ''
        res['purchase_order_type_code'] = self.purchase_order_type_code or ''
        res['po_type_description'] = self.po_type_description or ''
        res['ship_complete_code'] = self.ship_complete_code or ''
        res['department'] = self.department or ''
        res['division'] = self.division or ''
        res['promotion_deal_number'] = self.promotion_deal_number or ''
        res['terms_type'] = self.terms_type or ''
        res['terms_basis_date_code'] = self.terms_basis_date_code or ''
        res['terms_discount_percentage'] = self.terms_discount_percentage or ''
        res['terms_discount_due_days'] = self.terms_discount_due_days or ''
        res['terms_net_due_days'] = self.terms_net_due_days or ''
        res['payment_method_code'] = self.payment_method_code or ''
        res['fob_pay_code'] = self.fob_pay_code or ''
        res['fob_location_qualifier'] = self.fob_location_qualifier or ''
        res['fob_location_description'] = self.fob_location_description or ''
        res['fob_title_passage_code'] = self.fob_title_passage_code or ''
        res['fob_title_passage_location'] = self.fob_title_passage_location or ''
        res['carrier_trans_method_code'] = self.carrier_trans_method_code or ''
        res['carrier_alpha_code'] = self.carrier_alpha_code or ''
        res['carrier_routing'] = self.carrier_routing or ''
        res['routing_sequence_code'] = self.routing_sequence_code or ''
        res['service_level_code'] = self.service_level_code or ''
        res['reference_qual'] = self.reference_qual or ''
        res['reference_id'] = self.reference_id or ''
        res['ref_description'] = self.ref_description or ''
        res['note_code'] = self.note_code or ''
        res['note_information_field'] = self.note_information_field or ''
        res['allow_chrg_indicator'] = self.allow_chrg_indicator or ''
        res['allow_chrg_code'] = self.allow_chrg_code or ''
        res['allow_chrg_agency_code'] = self.allow_chrg_agency_code or ''
        res['allow_chrg_agency'] = self.allow_chrg_agency or ''
        res['allow_chrg_amt'] = float(self.allow_chrg_amt) or 0
        res['allow_chrg_percent_qual'] = self.allow_chrg_percent_qual or ''
        res['allow_chrg_percent'] = float(self.allow_chrg_percent) or 0
        res['allow_chrg_handling_code'] = self.allow_chrg_handling_code or ''
        res['reference_identification'] = self.reference_identification or ''
        res['allow_chrg_handling_description'] = self.allow_chrg_handling_description or ''
        return res


class SaleOrderLine(osv.osv):
    _inherit = "sale.order.line"

    @api.multi
    def _prepare_invoice_line(self, qty):
        """
        Prepare the dict of values to create the new invoice line for a sales order line.

        :param qty: float quantity to invoice
        """
        res = super(SaleOrderLine, self)._prepare_invoice_line(qty=qty) 
        res['edi_line_qty'] = self.edi_line_qty
        res['edi_line_num'] = self.edi_line_num
        res['asn_shipment'] = self.asn_shipment
        res['po_number'] = self.po_number
        res['buyer_part_number'] = self.buyer_part_number
        res['vendor_part_number'] = self.vendor_part_number or ''
        res['consumer_package_code'] = self.consumer_package_code or ''
        res['gtin'] = self.gtin or ''
        res['upc_case_code'] = self.upc_case_code or ''
        res['purchase_price_basis'] = self.purchase_price_basis or ''
        res['product_size_code'] = self.product_size_code or ''
        res['product_size_description'] = self.product_size_description or ''
        res['product_color_code'] = self.product_color_code or ''
        res['product_color_description'] = self.product_color_description or ''
        res['product_material_code'] = self.product_material_code or ''
        res['product_material_description'] = self.product_material_description or ''
        res['department'] = self.department or ''
        res['classs'] = self.classs or ''
        res['price_type_id_code'] = self.price_type_id_code or ''
        res['multiple_price_quantity'] = self.multiple_price_quantity or ''
        res['class_of_trade_code'] = self.class_of_trade_code or ''
        res['item_description_type'] = self.item_description_type or ''
        res['product_characteristic_code'] = self.product_characteristic_code or ''
        res['agency_qualifier_code'] = self.agency_qualifier_code or ''
        res['product_description_code'] = self.product_description_code or ''
        res['pack_qualifier'] = self.pack_qualifier or ''
        res['pack_value'] = self.pack_value or ''
        res['pack_size'] = self.pack_size or ''
        res['pack_uom'] = self.pack_uom or ''
        res['packing_medium'] = self.packing_medium or ''
        res['packing_material'] = self.packing_material or ''
        res['pack_weight'] = self.pack_weight or ''
        res['pack_weight_uom'] = self.pack_weight_uom or ''
        res['location_code_qualifier'] = self.location_code_qualifier or ''
        res['location'] = self.location or ''
        res['allow_chrg_indicator'] = self.allow_chrg_indicator or ''
        res['allow_chrg_code'] = self.allow_chrg_code or ''
        res['allow_chrg_agency_code'] = self.allow_chrg_agency_code or ''
        res['allow_chrg_agency'] = self.allow_chrg_agency or ''
        res['allow_chrg_amt'] = float(self.allow_chrg_amt) or 0
        res['allow_chrg_percent'] = self.allow_chrg_percent or ''
        res['percent_dollar_basis'] = self.percent_dollar_basis or ''
        res['allow_chrg_rate'] = self.allow_chrg_rate or ''
        res['allow_chrg_handling_code'] = self.allow_chrg_handling_code or ''
        res['allow_chrg_qty_uom'] = self.allow_chrg_qty_uom or ''
        res['allow_chrg_handling_description'] = self.allow_chrg_handling_description or ''
        return res
        
    def edi_line_status_change(self, cr, uid, ids, order_id, edi_line_msg, order_edi_last_date, context=None):
        res = {'value': {'state':'draft', 'edi_est_ship_date': order_edi_last_date}}
        if ids:
            if edi_line_msg == 'reject':
                res['value']['state'] = 'cancel'
                res['value']['edi_est_ship_date'] = ''
        return res

    _columns = {
        'edi_yes': fields.boolean('From an EDI PO?', help="Is this order from an EDI purchase order, 850 EDI doc?"),
        'asn_shipment': fields.char('ASN Shipment Number from Converted 856'),
        'po_number': fields.char('Line Item PO Number from Converted 856'),
        'buyer_part_number': fields.char(string='Buyer Part Number'),
        'edi_line_num': fields.integer('EDI PO line number'),
        'edi_line_qty': fields.float('Original EDI Quantity', digits_compute=dp.get_precision('Product Unit of Measure')),
        'ack_yes': fields.boolean('855', readonly=True, help="Will this order have an 855?"),
        'edi_est_del_date': fields.date('Est. Del. Date', help="Line Item Estimated Delivery Date"),
        'edi_est_ship_date': fields.date('Est. Ship Date', help="Line Item Estimated Shipping Date"),
        'edi_line_msg': fields.selection((('reject', 'Reject'), ('accept', 'Accept'), ('backorder', 'Backorder')), 'EDI Line Status'),
        'ship_not_before_date': fields.date('Do Not Ship Before This Date', help="Do Not Ship Before This Date."),
        'cancel_after_date': fields.date('Cancel if Shipped After This Date', help="Cancel if Shipped After This Date."),
        'trading_partner_id': fields.many2one('edi.config', 'Trading Partner', help='EDI Configuration information for partner'),
        'edi_intransit_qty': fields.float('Incoming Qty', digits_compute=dp.get_precision('Product Unit of Measure')),
        'edi_outgoing_qty': fields.float('Reserved Qty', digits_compute=dp.get_precision('Product Unit of Measure')),
        'edi_avlforsale_qty': fields.float('Available for Sale', digits_compute=dp.get_precision('Product Unit of Measure')),
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
    
    def _get_commitment_date(self, cr, uid, line, context=None):
        """Compute the estimated delivery date"""
        order = line.order_id[0]
        order_datetime = datetime.strptime(order.date_order, DEFAULT_SERVER_DATETIME_FORMAT)
        dt = order_datetime + timedelta(days=line.delay or 0.0)
        est_del_date = dt.strftime(DEFAULT_SERVER_DATETIME_FORMAT)
        return est_del_date
