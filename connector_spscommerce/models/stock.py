# -*- coding: utf-8 -*-
# Copyright (c) Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from datetime import datetime
import re
import dicttoxml
from openerp.osv import fields, osv
from openerp.tools.misc import DEFAULT_SERVER_DATETIME_FORMAT, DEFAULT_SERVER_DATE_FORMAT


class product_pricelist(osv.osv):
    _inherit= 'product.pricelist'
     
    def price_get_wrapper(self, cr, uid, ids, prod_id, qty, partner=None, context=None):
        price = self.price_rule_get(cr, uid, ids, prod_id, qty, partner=partner, context=context)[ids][0]       
        return price


class stock_pack_operation(osv.osv):
    _inherit = "stock.pack.operation"

    _columns = {
        'tracking_number': fields.char('Tracking Number', help="Tracking Number"),
        'bol': fields.char('Bill of Lading Number', help="Bill of Lading Number"),
        'package_code': fields.selection((('PLT71', 'PLT71'), ('CTN25', 'CTN25')), 'Package Code', help="Pkg Code Qualifier.", default="PLT71"),
        'po_number': fields.char('PO Number from EDI 850', help="PO Number from EDI 850."),
        'edi_line_num': fields.char('Line Number from EDI 850', help="Line Number from EDI 850."),
        'reference_qual':fields.char('ReferenceQual', help="Code specifying the type of data in the ReferenceID/ReferenceDescription."),
        'reference_id':fields.char('ReferenceID', help="Code specifying the type of data in the ReferenceID/ReferenceDescription."),
        'ref_description':fields.char('Description', help="Free-form textual description to clarify the related data elements and their content."),
        'note_code':fields.char('NoteCode', help="Code specifying the type of note."),
        'note_information_field':fields.char('NoteInformationField', help="Free-form textual description of the note."),
        'pack_qualifier':fields.char('PackQualifier', help=""),
        'pack_value':fields.char('PackValue', help=""),
        'pack_size':fields.char('PackSize', help=""),
        'pack_uom':fields.char('PackUOM', help=""),
        'packing_medium':fields.char('PackingMedium', help=""),
        'packing_material':fields.char('PackingMaterial', help=""),
    } 


class stock_quant(osv.osv):
    _inherit = "stock.quant"

    _columns = {
        'tracking_number': fields.char('Tracking Number', help="Tracking Number"),
        'bol': fields.char('Bill of Lading Number', help="Bill of Lading Number"),
        'package_code': fields.selection((('PLT71', 'PLT71'), ('CTN25', 'CTN25')), 'Package Code', help="Pkg Code Qualifier.", default="PLT71"),
        }  


class stock_quant_package(osv.osv):
    _inherit = "stock.quant.package"

    _columns = {
        'tracking_number': fields.char('Tracking Number', help="Tracking Number"),
        'bol': fields.char('Bill of Lading Number', help="Bill of Lading Number"),
        'package_code': fields.selection((('PLT71', 'PLT71'), ('CTN25', 'CTN25')), 'Package Code', help="Pkg Code Qualifier.", default="PLT71"),
    }


class delivery_carrier(osv.osv):
    _inherit = "delivery.carrier"

    _columns = {
        'scac_code': fields.char('SCAC Ship Method Code', help="Shipping carrier code."),
    }


class stock_move(osv.osv):
    _inherit = "stock.move"

    _columns = {
        'product_material_description': fields.char('ProductMaterialDescription', help="ProductMaterialDescription"),
        'consumer_package_code': fields.char('ConsumerPackageCode', help="ConsumerPackageCode"),
        'gtin': fields.char('GTIN', help="GTIN"),
        'upc_case_code': fields.char('UPCCaseCode', help="UPCCaseCode"),
        'natl_drug_code': fields.char('NatlDrugCode', help="NatlDrugCode"),
        'international_standard_book_number': fields.char('InternationalStandardBookNumber', help="InternationalStandardBookNumber"),
        'product_size_description': fields.char('ProductSizeDescription', help="ProductSizeDescription"),
        'product_color_description': fields.char('ProductColorDescription', help="ProductColorDescription"),
    }


class stock_picking(osv.osv):
    _inherit = "stock.picking"
    
    _columns = {
        'ship_not_before_date': fields.date('Do Not Ship Before This Date', help="Do Not Ship Before This Date."),
        'cancel_after_date': fields.date('Cancel if Shipped After This Date', help="Cancel if Shipped After This Date."),
        'client_order_ref': fields.text('Customer PO #', help="Customer PO #"),
        'edi_yes': fields.boolean('From an EDI PO', readonly=True, help="Is this order from an EDI purchase order, 850 EDI doc."),
        'est_del_date': fields.date('Estimated Delivery Date', help="Calculated based on shipping method."),
        'trading_partner_id': fields.many2one('edi.config', 'Trading Partner', help='EDI Configuration information for partner'),
        '856_sent_timestamp': fields.datetime('856 Sent Date', help="The timestamp for when the 856 was sent."),
        '856_check': fields.boolean('856 Created', help="A check to see if 856 has been sent."),
        'bol_num': fields.char('BoL', help="BoL Number."),
        'tracking_number': fields.char('Tracking Number', help="Tracking Number"),
        'ship_to_code': fields.char('Ship To Warehouse', help="Trading Partner Ship to location code."),
        'package_code': fields.selection((('PLT71', 'PLT71'), ('CTN25', 'CTN25')), 'Package Code', help="Pkg Code Qualifier.", default="PLT71"),
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
        'appointment_number':fields.char('AppointmentNumber', help=""),
        'asn_structure_code':fields.char('ASNStructureCode', help=""),
        'address_type_code':fields.char('AddressTypeCode', help=""),
        'location_code_qualifier':fields.char('LocationCodeQualifier', help=""),
        'address_location_number':fields.char('AddressLocationNumber', help=""),
        'status_code':fields.char('StatusCode', help=""),
        'equipment_description_code':fields.char('EquipmentDescriptionCode', help=""),
        'carrier_equipment_initial':fields.char('CarrierEquipmentInitial', help=""),
        'carrier_equipment_number':fields.char('CarrierEquipmentNumber', help=""),
        'seal_number':fields.char('SealNumber', help=""),
        'allow_chrg_rate':fields.char('AllowChrgRate', help=""),
    }
    
    def put_in_pack(self, cr, uid, ids, context=None):
        
        stock_move_obj = self.pool["stock.move"]
        stock_operation_obj = self.pool["stock.pack.operation"]
        stock_move_op_link_obj = self.pool['stock.move.operation.link']
        package_obj = self.pool["stock.quant.package"]
        package_id = False        
        context = context or {}
        
        for pick in self.browse(cr, uid, ids, context=context):
            operations = [x for x in pick.pack_operation_ids]
            
            for operation in operations:
            
                #assign edi_line_num and po_number to pack operation, move by move.
                link_ids = stock_move_op_link_obj.search(cr, uid, [('operation_id','=',operation.id)], context=context) or []
                move = False
                
                for link_id in link_ids:
                    
                    link = stock_move_op_link_obj.browse(cr, uid, link_id, context=context)
                    
                    if link and link.move_id:
                    
                        move = link.move_id
                        break
                        
                op_write = move and link and link.operation_id and stock_operation_obj.write(cr, uid, [link.operation_id.id], {'edi_line_num': move.edi_line_num, 'po_number':move.po_number}, context=context) or False
        
        return super(stock_picking, self).put_in_pack(cr, uid, ids, context=context)
    
    def create(self, cr, uid, vals, context=None):
        
        context = context or {}
        res = super(stock_picking, self).create(cr, uid, vals, context=context)
        picking = self.browse(cr, uid, res, context=context)


     
        if picking.origin:
            
            sale_obj = self.pool['sale.order']
            sale_id = sale_obj.search(cr, uid, [('name','=',picking.origin)], context=context)
            
            #look back to the sale order and get the edi field values and write them to the picking            
            if sale_id:
            
                sale_order = sale_obj.browse(cr, uid, sale_id[0], context=context)
                data = {
                    'ship_not_before_date': sale_order.ship_not_before_date,
                    'cancel_after_date': sale_order.cancel_after_date,
                    'client_order_ref': sale_order.client_order_ref,    
                    'edi_yes': sale_order.edi_yes,
                    'trading_partner_id': sale_order.trading_partner_id.id,
                    'bol_num': sale_order.bol_num,
                    #'tracking_number': sale_order.tracking_number,
                    'scac_code': sale_order.scac_code,
                    'ship_to_code': sale_order.ship_to_code,                   
                }
                
                picking.write(data)
        
        return res
    
    def _get_invoice_vals(self, cr, uid, key, inv_type, journal_id, move, context=None):
        res = super(stock_picking, self)._get_invoice_vals(cr, uid, key, inv_type, journal_id, move, context)
        
        if context is None:
            context = {}
            
        res['so_id'] = move.picking_id.sale_id or False        
        res['trading_partner_id'] = move.picking_id.trading_partner_id.id or False
        res['edi_yes'] = move.picking_id.edi_yes or False
        res['ship_not_before_date'] = move.picking_id.ship_not_before_date or False
        res['cancel_after_date'] = move.picking_id.cancel_after_date or False
        res['bol_num'] = move.picking_id.bol_num or ''
        res['tracking_number'] = move.picking_id.carrier_tracking_ref or ''
        res['scac_code'] = move.picking_id.carrier_id.scac_code or ''
        res['ship_to_code'] = move.picking_id.ship_to_code or ''   
        return res

    def get_operations(self, cr, uid, picking_ids, context=None):
    
        operations_dict = {}
        stock_move_op_link_obj = self.pool['stock.move.operation.link']
        operation_obj = self.pool['stock.pack.operation']
        
        for picking_id in picking_ids:
        
            #find links between this move and pack operations
            pack_op_ids = operation_obj.search(cr, uid, [('picking_id', '=', picking_id)], context=context)
            operations = operation_obj.browse(cr, uid, pack_op_ids, context=context)           
            operations_dict[picking_id] = operations
            
            #loop through quants found in packages for this particular move                   
            for operation in operations:                    
                
                if not operation.result_package_id:
                    continue

                #assign edi_line_num and po_number to pack operation, move by move.
                link_id = operation.qty_done and stock_move_op_link_obj.search(cr, uid, [('operation_id','=',operation.id)], context=context) or []
                move = link_id and stock_move_op_link_obj.browse(cr, uid, link_id, context=context).move_id or False   
                
                package = operation.result_package_id
            
        return operations_dict
   
    def create_text_856(self, cr, uid, picking_ids, context=None):
        
        today = str(datetime.now().strftime('%Y%m%d')) or ''
        processed = 0
        name = ''
        # for each picking
        shipments_list = {'Shipments':[]}
        for picking in self.browse(cr, uid, picking_ids, context=context):
            name += picking.name
            
            #Grab the vendor_id and trading_partner_id for EDI in the edi_config.
            trading_partner_code = picking.trading_partner_id.partner_header_string
            vendor_code = picking.trading_partner_id.vendor_header_string
            
            #ship_date
            ship_date = picking.date_done
            dateship_object = datetime.strptime(ship_date, DEFAULT_SERVER_DATETIME_FORMAT)
            ship_date = dateship_object.date()
            ship_date = str(ship_date)
            
            #ship_time
            ship_time = picking.date_done
            dateship_object = datetime.strptime(ship_time, DEFAULT_SERVER_DATETIME_FORMAT)
            ship_time = dateship_object.time()
            ship_time = str(ship_time)
            
            #Schedule_date
            schedule_date = picking.est_del_date
            if not schedule_date:
                schedule_date = picking.max_date
                dateship_object = datetime.strptime(schedule_date, DEFAULT_SERVER_DATETIME_FORMAT)
            else:
                dateship_object = datetime.strptime(schedule_date, DEFAULT_SERVER_DATE_FORMAT)
            schedule_date = dateship_object.date()
            schedule_date = str(schedule_date)
            
            #Schedule_time
            schedule_time = picking.est_del_date
            if not schedule_time:
                schedule_time = picking.max_date
                dateship_object = datetime.strptime(schedule_time, DEFAULT_SERVER_DATETIME_FORMAT)
            else:
                dateship_object = datetime.strptime(schedule_time, DEFAULT_SERVER_DATE_FORMAT)
            schedule_time = dateship_object.time()
            schedule_time = str(schedule_time)
            
            #Notice_date
            notice_date = picking.ship_not_before_date
            if not notice_date:
                notice_date = picking.min_date
                dateship_object = datetime.strptime(notice_date, DEFAULT_SERVER_DATETIME_FORMAT)
            else:
                dateship_object = datetime.strptime(notice_date, DEFAULT_SERVER_DATE_FORMAT)
            notice_date = dateship_object.date()
            notice_date = str(notice_date)
            
            # get total packages and weight for the entire order
            total_weight = 0
            total_qty = 0
            
            for move in picking.move_lines:
                total_qty += move.product_qty
                total_weight += move.product_id.weight * move.product_qty

            # initialize
            shipment_dict = {'Shipment':{}}
            # 1. Header Line - one line for the order
            meta_dict = {'Meta': {'Version': '1.0'}}
            header_dict = {'Header': {'ShipmentHeader': {
                'TradingPartnerId': trading_partner_code,
                'ShipmentIdentification': str(picking.name),
                'ShipmentDate':ship_date,
                'TsetPurposeCode':picking.tset_purpose_code,
                'ShipNoticeDate':notice_date,
                'ShipNoticeTime':'00:00:00',
                'ASNStructureCode':picking.asn_structure_code,
                'BillOfLadingNumber':picking.bol_num,
                'CarrierProNumber':picking.carrier_tracking_ref,
                'AppointmentNumber':picking.appointment_number,
                'CurrentScheduledDeliveryDate':schedule_date,
                'CurrentScheduledDeliveryTime':schedule_time,
            },
                'Date': {
                    'DateTimeQualifier1':'945',
                    'Date1':ship_date,
                    'Time1':ship_time,
                    'DateTimePeriod':'',
                },
                'Reference':{
                    'ReferenceQual':picking.reference_qual,
                    'ReferenceID':picking.reference_id,
                    'Description':picking.ref_description,
                },
                'Notes':{
                    'NoteCode':picking.note_code,
                    'NoteInformationField':picking.note_information_field,
                },
                'Contact':{
                    'ContactTypeCode':'BD',
                    'ContactName':picking.partner_id and picking.partner_id.name or '',
                    'PrimaryPhone':picking.partner_id and picking.partner_id.phone or '',
                    'PrimaryFax':picking.partner_id and picking.partner_id.fax or '',
                    'PrimaryEmail':picking.partner_id and picking.partner_id.email or '',
                },
                'Address':{
                    'AddressTypeCode':picking.address_type_code,
                    'LocationCodeQualifier':picking.location_code_qualifier,
                    'AddressLocationNumber':picking.address_location_number,
                    'AddressName':picking.partner_id.name,
                    'Address1':picking.partner_id.street,
                    'Address2':picking.partner_id.street2,
                    'City':picking.partner_id.city,
                    'State':picking.partner_id.state_id.name,
                    'PostalCode':picking.partner_id.zip,
                    'Country':picking.partner_id.country_id.name,
                    'Contact':{
                        'ContactTypeCode':'BD',
                        'ContactName':picking.partner_id and picking.partner_id.name or '',
                        'PrimaryPhone':picking.partner_id and picking.partner_id.phone or '',
                        'PrimaryFax':picking.partner_id and picking.partner_id.fax or '',
                        'PrimaryEmail':picking.partner_id and picking.partner_id.email or '',
                    },
                },
                'CarrierInformation':{
                    'StatusCode':picking.status_code,
                    'CarrierTransMethodCode':picking.carrier_trans_method_code,
                    'CarrierAlphaCode':picking.carrier_alpha_code,
                    'CarrierRouting':picking.carrier_routing,
                    'EquipmentDescriptionCode':picking.equipment_description_code,
                    'CarrierEquipmentInitial':picking.carrier_equipment_initial,
                    'CarrierEquipmentNumber':picking.carrier_equipment_number,
                    'SealNumber':picking.seal_number,
                    'RoutingSequenceCode': picking.routing_sequence_code
                },
                'QuantityAndWeight':{
                    'LadingQuantity':total_qty,
                    'WeightQualifier':'G',
                    'Weight':total_weight,
                    'WeightUOM':'AD',
                },
                'ChargesAllowances':{
                    'AllowChrgIndicator':picking.allow_chrg_indicator,
                    'AllowChrgCode':picking.allow_chrg_code,
                    'AllowChrgAmt':picking.allow_chrg_amt,
                    'AllowChrgPercentQual':picking.allow_chrg_percent_qual,
                    'AllowChrgPercent':picking.allow_chrg_percent,
                    'AllowChrgHandlingCode':picking.allow_chrg_handling_code,
                    'AllowChrgHandlingDescription':picking.allow_chrg_handling_description,
                    'AllowChrgRate':picking.allow_chrg_rate
                },
                'FOBRelatedInstruction':{
                    'FOBPayCode':picking.fob_pay_code,
                    'FOBLocationQualifier':picking.fob_location_qualifier,
                    'FOBLocationDescription':picking.fob_location_description,
                },
            }
            }
            orderlevel_dict = {'OrderLevel': {'OrderHeader': {
                'InternalOrderNumber': picking.name,
                'InternalOrderDate': ship_date,
                'InvoiceNumber':'99999-123',
                'InvoiceDate':'',
                'PurchaseOrderNumber':picking.origin,
                'ReleaseNumber':picking.name,
                'PurchaseOrderDate':ship_date,
                'Department':picking.department,
                'Vendor':picking.vendor,
                'CustomerOrderNumber':''
            },
                'QuantityAndWeight':{
                    'LadingQuantity':total_qty,
                    'WeightQualifier':'G',
                    'Weight':total_weight,
                    'WeightUOM':'AD',
                },
                'CarrierInformation':{
                    'StatusCode':picking.status_code,
                    'CarrierTransMethodCode':picking.carrier_trans_method_code,
                    'CarrierAlphaCode':picking.carrier_alpha_code,
                    'CarrierRouting':picking.carrier_routing,
                    'EquipmentDescriptionCode':picking.equipment_description_code,
                    'CarrierEquipmentInitial':picking.carrier_equipment_initial,
                    'CarrierEquipmentNumber':picking.carrier_equipment_number,
                    'SealNumber':picking.seal_number,
                    'RoutingSequenceCode': picking.routing_sequence_code
                },
                'Reference':{
                    'ReferenceQual':picking.reference_qual,
                    'ReferenceID':picking.reference_id,
                    'Description':picking.ref_description,
                },
                'Notes':{
                    'NoteCode':picking.note_code,
                    'NoteInformationField':picking.note_information_field,
                },
                'ChargesAllowances':{
                    'AllowChrgIndicator':picking.allow_chrg_indicator,
                    'AllowChrgCode':picking.allow_chrg_code,
                    'AllowChrgAmt':picking.allow_chrg_amt,
                    'AllowChrgPercentQual':picking.allow_chrg_percent_qual,
                    'AllowChrgPercent':picking.allow_chrg_percent,
                    'AllowChrgHandlingCode':picking.allow_chrg_handling_code,
                    'AllowChrgHandlingDescription':picking.allow_chrg_handling_description,
                    'AllowChrgRate':picking.allow_chrg_rate
                },
            }
            }
            packlevel_dict = {'PackLevel':{}, 'Itemlevel':{'ShipmentLine':{}}}

            for operation in self.get_operations(cr, uid, picking_ids, context=context):
            
                packlevel_dict['PackLevel'] = {'Pack':{
                    'PackLevelType':'P',
                    'ShippingSerialID':'9996999',
                    'CarrierPackageID':operation.package_id and operation.package_id.id or False,
                },
                    'PhysicalDetails': {
                        'PackQualifier':operation.pack_qualifier,
                        'PackValue':operation.pack_value,
                        'PackSize':operation.pack_size,
                        'PackUOM':operation.pack_uom,
                        'PackingMedium':operation.packing_medium,
                        'PackingMaterial':operation.packing_material,
                    },
                    'Date': {
                        'DateTimeQualifier1':'619',
                        'Date1':ship_date,
                        'Time1':ship_time,
                    },
                    'Reference':{
                        'ReferenceQual':operation.reference_qual,
                        'ReferenceID':operation.reference_id,
                        'Description':operation.ref_description,
                    },
                    'Notes':{
                        'NoteCode':operation.note_code,
                        'NoteInformationField':operation.note_information_field,
                    },
                }
                """packlevel_dict['ItemLevel']['ShipmentLine'] = {
                    'LineSequenceNumber':'01',
                    'BuyerPartNumber':'9999-SPS',
                    'VendorPartNumber':'',
                    'ConsumerPackageCode':'FW',
                    'EAN':'testReferenceID',
                    'GTIN':'New products only. Do not reuse packaging',
                    'UPCCaseCode':'FW',
                    'NatlDrugCode':'testReferenceID',
                    'InternationalStandardBookNumber':'',
                    'ProductID':{
                        'PartNumberQual':'STAEV',
                        'PartNumber':'REPEAT LOGO PREVIOUS ORDER',
                    },
                    'OrderQty':'01',
                    'OrderQtyUOM':'P',
                    'PurchasePrice':'9999-SPS',
                    'ItemStatusCode':'',
                    'ShipQty':'',
                    'ShipQtyUOM':'H1',
                    'ProductSizeCode':'S-800',
                    'ProductSizeDescription':'Small',
                    'ProductColorCode':'C-999',
                    'ProductColorDescription':'Fire Truck Red',
                    'ProductMaterialDescription':'',
                    'NRFStandardColorAndSize':{
                        'NRFColorCode':'600',
                        'NRFSizeCode':'42-10651',
                    },
                    'PhysicalDetails':{
                        'PackQualifier':'Small',
                        'PackValue':'C-999',
                        'PackSize':'',
                        'PackUOM':'',
                    },
                    'PriceInformation':{
                        'PriceTypeIDCode':'PRP',
                        'UnitPrice':'5.48',
                    },
                    'ProductOrItemDescription':{
                        'ItemDescriptionType':'74',
                        'ProductDescription':'Super comfortable',
                    },
                    'Date': {
                        'DateTimeQualifier1':'945',
                        'Date1':ship_date,
                        'Time1':ship_time,
                    },
                    'Reference':{
                        'ReferenceQual':'PJ',
                        'ReferenceID':'testReferenceID',
                        'Description':'New products only. Do not reuse packaging',
                    },
                    'Notes':{
                        'NoteCode':'DSCSA',
                        'NoteInformationField':'REPEAT LOGO PREVIOUS ORDER',
                    },
                    'ChargesAllowances':{
                        'AllowChrgIndicator':'C',
                        'AllowChrgCode':'C310',
                        'AllowChrgAmt':'85.02',
                        'AllowChrgPercentQual':'4',
                        'AllowChrgPercent':'5.0',
                        'AllowChrgHandlingCode':'02',
                        'AllowChrgHandlingDescription':'This will cover the cost of shipping',
                    },
                }"""                                         
                                                                                                             
            shipment_dict.get('Shipment').update(meta_dict)
            shipment_dict.get('Shipment').update(header_dict)
            shipment_dict.get('Shipment').update(orderlevel_dict)
            shipment_dict.get('Shipment').get('OrderLevel').update(packlevel_dict)
            
            #Sublines
            sublines_list = {'Sublines': []}
            total_lines = 0
            total_qty = 0
            total_weight = 0
                    
            #for each sub line
            for line in picking.move_lines:
                total_lines += 1
                total_qty += line.product_qty
                total_weight += (line.product_id.weight * line.product_qty)            
                subline_dict = {'Subline':{}}
                pickingline_dict = {'ShipmentLine': {
                    'LineSequenceNumber':int(line.id),
                    'BuyerPartNumber':line.product_id.default_code or '',
                    'VendorPartNumber':line.product_id.default_code or '',
                    'ConsumerPackageCode':line.consumer_package_code,
                    'EAN':line.product_id.barcode,
                    'GTIN':line.gtin,
                    'UPCCaseCode':line.upc_case_code,
                    'NatlDrugCode':line.natl_drug_code,
                    'InternationalStandardBookNumber':line.international_standard_book_number,
                    'ProductID':{
                        'PartNumberQual':'IT',
                        'PartNumber':line.product_id.default_code,
                    },
                    'PurchasePrice':line.price_unit,
                    'ShipQty':line.product_qty,
                    'ShipQtyUOM':'P4',
                    'ProductSizeDescription':line.product_size_description,
                    'ProductColorDescription':line.product_color_description,
                    'ProductMaterialDescription':line.product_material_description,
                }
                }
                subline_dict.get('Subline').update(pickingline_dict)
                sublines_list.get('Sublines').append(subline_dict)
             
            #shipment_dict.get('Shipment').get('OrderLevel').get('PackLevel').get('ItemLevel').update(sublines_list)
            shipment_dict.get('Shipment').get('OrderLevel').update(sublines_list)
            
            # summary
            summary_dict = {'Summary': {
                'TotalLineItems':total_lines or '',
                'TotalQuantity':total_qty,
            }
            }
            shipment_dict.get('Shipment').update(summary_dict)
            # update invoice
            today = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  
            picking.write({'856_sent_timestamp':today})
            shipments_list.get('Shipments').append(shipment_dict)
            processed += 1
            
        #convert dictionary to xml
        xml = dicttoxml.dicttoxml(shipments_list, attr_type=False, root=False)
        xml = xml.replace('<item>','').replace('</item>','')
        xml = xml.replace('<item>','').replace('<Shipments>','<?xml version="1.0" encoding="utf-8"?><Shipments xmlns="http://www.spscommerce.com/RSX">')
        #Write ASN doc to text file
        name = re.findall('\d+', name)[0]
        filename = '856_' + today + '%s.xml' % name
        filename.replace('/', '_')
        fd = open(picking.trading_partner_id.out_path + filename, 'w')
        fd.write(xml)
        fd.close()
        return processed
        
    def _create_856_wrapper(self, cr, uid, context=None):
    
        #search for invoices that are edi_yes = True and 856_sent_timestamp = False
        eligible_pickings = self.search(cr, uid, [('edi_yes','=',True),('856_sent_timestamp','=',False)], context=context)       
        return eligible_pickings and self.create_text_856(cr, uid, eligible_pickings, context=context) or False

    # done as a server action        
    def action_create_text_856(self, cr, uid, ids, context=None):
        """ Creates and new 856, ASN and puts it into the outbox
        """
        if context is None:
            context = {}
        
        # number of orders to process
        toprocess = len(ids)
        
        # process orders to write 856 
        processed = self.create_text_856(cr, uid, ids, context=context)              
            
        return (toprocess - processed)