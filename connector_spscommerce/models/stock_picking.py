# Copyright (c) Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import re
import dicttoxml
from datetime import datetime
from odoo import api, fields, models
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DSD
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DS
from odoo.exceptions import UserError


class StockPicking(models.Model):
    _inherit = "stock.picking"

    ship_not_before_date = fields.Date(
        'Do Not Ship Before This Date',
        help="Do Not Ship Before This Date."
    )
    cancel_after_date = fields.Date(
        'Cancel if Shipped After This Date',
        help="Cancel if Shipped After This Date."
    )
    client_order_ref = fields.Text(
        'Customer PO #',
        help="Customer PO #"
    )
    edi_yes = fields.Boolean(
        'From an EDI PO',
        readonly=True,
        help="Is this order from an EDI purchase order, 850 EDI doc."
    )
    est_del_date = fields.Date(
        'Estimated Delivery Date',
        help="Calculated based on shipping method."
    )
    trading_partner_id = fields.Many2one(
        'edi.config',
        'Trading Partner',
        help='EDI Configuration information for partner'
    )
    sent_timestamp = fields.Datetime(
        '856 Sent Date',
        help="The timestamp for when the 856 was sent."
    )
    check = fields.Boolean(
        '856 Created',
        help="A check to see if 856 has been sent."
    )
    bol_num = fields.Char(
        'BoL',
        help="BoL Number."
    )
    tracking_number = fields.Char(
        'Tracking Number',
        help="Tracking Number"
    )
    ship_to_code = fields.Char(
        'Ship To Warehouse',
        help="Trading Partner Ship to location code."
    )
    package_code = fields.Selection(
        [('PLT71', 'PLT71'), ('CTN25', 'CTN25')],
        'Package Code',
        help="Pkg Code Qualifier.",
        default="PLT71"
    )
    tset_purpose_code = fields.Char(
        'Tset Purpose Code',
        help="Code identifying purpose of the document.."
    )
    purchase_order_type_code = fields.Char(
        'Purchase Order TypeCode',
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
        help="Number uniquely identifying an agreement for"
        "a special offer or price."
    )
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
        help="Number of days until total invoice amount is"
        "due[discount not applicable."
    )
    payment_method_code = fields.Char(
        'Payment Method Code',
        help="Indication of the instrument of payment."
    )
    fob_pay_code = fields.Char(
        'FOB Pay Code',
        help="Code identifying payment terms for transportation charges."
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
        'Carrier Alpha Code',
        help="Standard Carrier Alpha Code[SCAC] - "
    )
    carrier_routing = fields.Char(
        'Carrier Routing',
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
        help="Code specifying the type of data in the "
        "ReferenceID/ReferenceDescription."
    )
    ref_description = fields.Char(
        'Description',
        help="Free-form textual description to clarify the related data"
        "elements and their content."
    )
    note_code = fields.Char(
        'Note Code',
        help="Code specifying the type of note."
    )
    note_information_field = fields.Char(
        'Note Information Field',
        help="Free-form textual description of the note."
    )
    allow_chrg_indicator = fields.Char(
        'Allow Chrg Indicator',
        help="Code which indicates an allowance or charge for"
        "the service specified."
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
    allow_chrg_percent_qual = fields.Char(
        'Allow Chrg Percent Qual',
        help="Code indicating on what basis an allowance or charge percent"
        "is calculated.."
    )
    allow_chrg_percent = fields.Float(
        'Allow Chrg Percent',
        help='''Percentage of allowance or charge. Percentages should be
        represented as real numbers[0% through 100% should be normalized to
        0.0 through 100.00]..'''
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
    appointment_number = fields.Char('Appointment Number')
    asn_structure_code = fields.Char('ASN Structure Code')
    address_type_code = fields.Char('Address Type Code')
    location_code_qualifier = fields.Char('Location Code Qualifier')
    address_location_number = fields.Char('Address Location Number')
    status_code = fields.Char('Status Code')
    equipment_description_code = fields.Char('Equipment Description Code')
    carrier_equipment_initial = fields.Char('Carrier Equipment Initial')
    carrier_equipment_number = fields.Char('Carrier Equipment Number')
    seal_number = fields.Char('Seal Number')
    allow_chrg_rate = fields.Char('Allow Chrg Rate')

    def put_in_pack(self):
        stock_move_line_obj = self.env['stock.move.line']
        for pick in self:
            operations = pick.move_line_ids.\
                filtered(lambda o: o.qty_done > 0 and not o.result_package_id)
            for operation in operations:

                # assign edi_line_num and po_number to
                # pack operation, move by move.
                link_ids = stock_move_line_obj.\
                    search([('picking_id', '=', pick.id)]) or []
                move = False
                for link_id in link_ids:
                    if link_id and link_id.move_id:
                        move = link_id.move_id
                        break
                    op_write = move and link_id and link_id.operation_id and\
                        link_id.move_id.write({
                            'edi_line_num': move.edi_line_num,
                            'po_number': move.po_number
                        }) or False
        return super(StockPicking, self).put_in_pack()

    @api.model
    def create(self, vals):
        res = super(StockPicking, self).create(vals)
        if res.origin:
            sale_obj = self.env['sale.order']
            sale_id = sale_obj.search([('name', '=', res.origin)])

            # look back to the sale order and get the edi field values and
            # write them to the picking
            if sale_id:
                data = {
                    'ship_not_before_date': sale_id.ship_not_before_date,
                    'cancel_after_date': sale_id.cancel_after_date,
                    'client_order_ref': sale_id.client_order_ref,
                    'edi_yes': sale_id.edi_yes,
                    'trading_partner_id': sale_id.trading_partner_id.id,
                    'bol_num': sale_id.bol_num,
                    # 'tracking_number': sale_id.tracking_number,
                    'scac_code': sale_id.scac_code,
                    'ship_to_code': sale_id.ship_to_code,
                }
                res.write(data)
        return res

#    def _get_invoice_vals(self, key, inv_type, journal_id, move):
#        res = super(StockPicking, self
#                    )._get_invoice_vals(key, inv_type, journal_id, move)
#        res['so_id'] = move.picking_id.sale_id or False
#        res['trading_partner_id'] =\
#            move.picking_id.trading_partner_id.id or False
#        res['edi_yes'] = move.picking_id.edi_yes or False
#        res['ship_not_before_date'] =\
#            move.picking_id.ship_not_before_date or False
#        res['cancel_after_date'] = move.picking_id.cancel_after_date or False
#        res['bol_num'] = move.picking_id.bol_num or ''
#        res['tracking_number'] = move.picking_id.carrier_tracking_ref or ''
#        res['scac_code'] = move.picking_id.carrier_id.scac_code or ''
#        res['ship_to_code'] = move.picking_id.ship_to_code or ''
#        return res

    @api.multi
    def get_operations(self):
        operations_dict = []
        for move in self.move_lines:
            if move.picking_id:
                operations_dict.append(move or False)
            for line in move.move_line_ids:
                if not line.result_package_id:
                        continue
                package = line.result_package_id
        return operations_dict

    @api.multi
    def create_text_856(self):
        today = str(datetime.now().strftime(DS)) or ''
        processed = 0
        name = ''

        # for each picking
        shipments_list = {'Shipments': []}
        for picking in self:
            name += picking.name

            # Grab the vendor_id and trading_partner_id for
            # EDI in the edi_config.
            trading_partner_code =\
                picking.trading_partner_id.partner_header_string
            vendor_code = picking.trading_partner_id.vendor_header_string

            # ship_date
            if picking.scheduled_date:
                ship_date = picking.scheduled_date
                dateship_object = datetime.strptime(ship_date, DSD)
                ship_date = dateship_object.date()
                ship_date = str(ship_date)

            # ship_time
                ship_time = picking.scheduled_date
                dateship_object = datetime.strptime(ship_time, DSD)
                ship_time = dateship_object.time()
                ship_time = str(ship_time)

            # Schedule_date
            schedule_date = picking.est_del_date
            if not schedule_date:
                schedule_date = picking.scheduled_date
                dateship_object = datetime.strptime(schedule_date, DSD)
            else:
                dateship_object = datetime.strptime(schedule_date, DS)
            schedule_date = dateship_object.date()
            schedule_date = str(schedule_date)

            # Schedule_time
            schedule_time = picking.est_del_date
            if not schedule_time:
                schedule_time = picking.scheduled_date
                dateship_object = datetime.strptime(schedule_time, DSD)
            else:
                dateship_object = datetime.strptime(schedule_time, DS)
            schedule_time = dateship_object.time()
            schedule_time = str(schedule_time)

            # Notice_date
            notice_date = picking.ship_not_before_date
            if not notice_date:
                notice_date = picking.date
                dateship_object = datetime.strptime(notice_date, DSD)
            else:
                dateship_object = datetime.strptime(notice_date, DS)
            notice_date = dateship_object.date()
            notice_date = str(notice_date)

            # get total packages and weight for the entire order
            total_weight = 0
            total_qty = 0

            for move in picking.move_lines:
                total_qty += move.product_qty
                total_weight += move.product_id.weight * move.product_qty

            # initialize
            shipment_dict = {'Shipment': {}}
            # 1. Header Line - one line for the order
            meta_dict = {'Meta': {'Version': '1.0'}}
            header_dict = {'Header': {'ShipmentHeader': {
                'TradingPartnerId': trading_partner_code,
                'ShipmentIdentification': str(picking.name),
                'ShipmentDate': ship_date,
                'TsetPurposeCode': picking.tset_purpose_code,
                'ShipNoticeDate': notice_date,
                'ShipNoticeTime': '00:00:00',
                'ASNStructureCode': picking.asn_structure_code,
                'BillOfLadingNumber': picking.bol_num,
                'CarrierProNumber': picking.carrier_tracking_ref,
                'AppointmentNumber': picking.appointment_number,
                'CurrentScheduledDeliveryDate': schedule_date,
                'CurrentScheduledDeliveryTime': schedule_time,
            },
                'Date': {
                    'DateTimeQualifier1': '945',
                    'Date1': ship_date,
                    'Time1': ship_time,
                    'DateTimePeriod': '',
                },
                'Reference': {
                    'ReferenceQual': picking.reference_qual,
                    'ReferenceID': picking.reference_id,
                    'Description': picking.ref_description,
                },
                'Notes': {
                    'NoteCode': picking.note_code,
                    'NoteInformationField': picking.note_information_field,
                },
                'Contact': {
                    'ContactTypeCode': 'BD',
                    'ContactName':
                    picking.partner_id and picking.partner_id.name or '',
                    'PrimaryPhone':
                    picking.partner_id and picking.partner_id.phone or '',
                    # 'PrimaryFax':
                    # picking.partner_id and picking.partner_id.fax or '',
                    'PrimaryEmail':
                    picking.partner_id and picking.partner_id.email or '',
                },
                'Address': {
                    'AddressTypeCode': picking.address_type_code,
                    'LocationCodeQualifier': picking.location_code_qualifier,
                    'AddressLocationNumber': picking.address_location_number,
                    'AddressName': picking.partner_id.name,
                    'Address1': picking.partner_id.street,
                    'Address2': picking.partner_id.street2,
                    'City': picking.partner_id.city,
                    'State': picking.partner_id.state_id.name,
                    'PostalCode': picking.partner_id.zip,
                    'Country': picking.partner_id.country_id.name,
                    'Contact': {
                        'ContactTypeCode': 'BD',
                        'ContactName':
                        picking.partner_id and picking.partner_id.name or '',
                        'PrimaryPhone':
                        picking.partner_id and picking.partner_id.phone or '',
                        # 'PrimaryFax':
                        # picking.partner_id and picking.partner_id.fax or '',
                        'PrimaryEmail':
                        picking.partner_id and picking.partner_id.email or '',
                    },
                },
                'CarrierInformation': {
                    'StatusCode': picking.status_code,
                    'CarrierTransMethodCode':
                    picking.carrier_trans_method_code,
                    'CarrierAlphaCode': picking.carrier_alpha_code,
                    'CarrierRouting': picking.carrier_routing,
                    'EquipmentDescriptionCode':
                    picking.equipment_description_code,
                    'CarrierEquipmentInitial':
                    picking.carrier_equipment_initial,
                    'CarrierEquipmentNumber':
                    picking.carrier_equipment_number,
                    'SealNumber': picking.seal_number,
                    'RoutingSequenceCode': picking.routing_sequence_code
                },
                'QuantityAndWeight': {
                    'LadingQuantity': total_qty,
                    'WeightQualifier': 'G',
                    'Weight': total_weight,
                    'WeightUOM': 'AD',
                },
                'ChargesAllowances': {
                    'AllowChrgIndicator': picking.allow_chrg_indicator,
                    'AllowChrgCode': picking.allow_chrg_code,
                    'AllowChrgAmt': picking.allow_chrg_amt,
                    'AllowChrgPercentQual': picking.allow_chrg_percent_qual,
                    'AllowChrgPercent': picking.allow_chrg_percent,
                    'AllowChrgHandlingCode': picking.allow_chrg_handling_code,
                    'AllowChrgHandlingDescription':
                    picking.allow_chrg_handling_description,
                    'AllowChrgRate': picking.allow_chrg_rate
                },
                'FOBRelatedInstruction': {
                    'FOBPayCode': picking.fob_pay_code,
                    'FOBLocationQualifier': picking.fob_location_qualifier,
                    'FOBLocationDescription': picking.fob_location_description,
                },
            }
            }
            orderlevel_dict = {'OrderLevel': {'OrderHeader': {
                'InternalOrderNumber': picking.name,
                'InternalOrderDate': ship_date,
                'InvoiceNumber': '99999-123',
                'InvoiceDate': '',
                'PurchaseOrderNumber': picking.origin,
                'ReleaseNumber': picking.name,
                'PurchaseOrderDate': ship_date,
                'Department': picking.department,
                'Vendor': picking.partner_id.id,
                'CustomerOrderNumber': ''
            },
                'QuantityAndWeight': {
                    'LadingQuantity': total_qty,
                    'WeightQualifier': 'G',
                    'Weight': total_weight,
                    'WeightUOM': 'AD',
                },
                'CarrierInformation': {
                    'StatusCode': picking.status_code,
                    'CarrierTransMethodCode':
                    picking.carrier_trans_method_code,
                    'CarrierAlphaCode': picking.carrier_alpha_code,
                    'CarrierRouting': picking.carrier_routing,
                    'EquipmentDescriptionCode':
                    picking.equipment_description_code,
                    'CarrierEquipmentInitial':
                    picking.carrier_equipment_initial,
                    'CarrierEquipmentNumber': picking.carrier_equipment_number,
                    'SealNumber': picking.seal_number,
                    'RoutingSequenceCode': picking.routing_sequence_code
                },
                'Reference': {
                    'ReferenceQual': picking.reference_qual,
                    'ReferenceID': picking.reference_id,
                    'Description': picking.ref_description,
                },
                'Notes': {
                    'NoteCode': picking.note_code,
                    'NoteInformationField': picking.note_information_field,
                },
                'ChargesAllowances': {
                    'AllowChrgIndicator': picking.allow_chrg_indicator,
                    'AllowChrgCode': picking.allow_chrg_code,
                    'AllowChrgAmt': picking.allow_chrg_amt,
                    'AllowChrgPercentQual': picking.allow_chrg_percent_qual,
                    'AllowChrgPercent': picking.allow_chrg_percent,
                    'AllowChrgHandlingCode': picking.allow_chrg_handling_code,
                    'AllowChrgHandlingDescription':
                    picking.allow_chrg_handling_description,
                    'AllowChrgRate': picking.allow_chrg_rate
                },
            }
            }
            packlevel_dict = {
                'PackLevel': {},
                'Itemlevel': {'ShipmentLine': {}}}

            for operation in self.get_operations():
                package_id = operation.move_line_ids.\
                    mapped('package_id') | operation.move_line_ids.\
                    mapped('result_package_id')
                packlevel_dict['PackLevel'] = {'Pack': {
                    'PackLevelType': 'P',
                    'ShippingSerialID': '9996999',
                    'CarrierPackageID': package_id or False,
                },
                    'PhysicalDetails': {
                        'PackQualifier': operation.pack_qualifier,
                        'PackValue': operation.pack_value,
                        'PackSize': operation.pack_size,
                        'PackUOM': operation.pack_uom,
                        'PackingMedium': operation.packing_medium,
                        'PackingMaterial': operation.packing_material,
                    },
                    'Date': {
                        'DateTimeQualifier1': '619',
                        'Date1': ship_date,
                        'Time1': ship_time,
                    },
                    'Reference': {
                        'ReferenceQual': operation.reference_qual,
                        'ReferenceID': operation.reference_id,
                        'Description': operation.ref_description,
                    },
                    'Notes': {
                        'NoteCode': operation.note_code,
                        'NoteInformationField':
                        operation.note_information_field,
                    },
                }
                """packlevel_dict['ItemLevel']['ShipmentLine'] = {
                    'LineSequenceNumber': '01',
                    'BuyerPartNumber': '9999-SPS',
                    'VendorPartNumber': '',
                    'ConsumerPackageCode': 'FW',
                    'EAN': 'testReferenceID',
                    'GTIN': 'New products only. Do not reuse packaging',
                    'UPCCaseCode': 'FW',
                    'NatlDrugCode': 'testReferenceID',
                    'InternationalStandardBookNumber': '',
                    'ProductID': {
                        'PartNumberQual': 'STAEV',
                        'PartNumber': 'REPEAT LOGO PREVIOUS ORDER',
                    },
                    'OrderQty': '01',
                    'OrderQtyUOM': 'P',
                    'PurchasePrice': '9999-SPS',
                    'ItemStatusCode': '',
                    'ShipQty': '',
                    'ShipQtyUOM': 'H1',
                    'ProductSizeCode': 'S-800',
                    'ProductSizeDescription': 'Small',
                    'ProductColorCode': 'C-999',
                    'ProductColorDescription': 'Fire Truck Red',
                    'ProductMaterialDescription': '',
                    'NRFStandardColorAndSize': {
                        'NRFColorCode': '600',
                        'NRFSizeCode': '42-10651',
                    },
                    'PhysicalDetails': {
                        'PackQualifier': 'Small',
                        'PackValue': 'C-999',
                        'PackSize': '',
                        'PackUOM': '',
                    },
                    'PriceInformation': {
                        'PriceTypeIDCode': 'PRP',
                        'UnitPrice': '5.48',
                    },
                    'ProductOrItemDescription': {
                        'ItemDescriptionType': '74',
                        'ProductDescription': 'Super comfortable',
                    },
                    'Date': {
                        'DateTimeQualifier1': '945',
                        'Date1': ship_date,
                        'Time1': ship_time,
                    },
                    'Reference': {
                        'ReferenceQual': 'PJ',
                        'ReferenceID': 'testReferenceID',
                        'Description':
                        'New products only. Do not reuse packaging',
                    },
                    'Notes':{
                        'NoteCode': 'DSCSA',
                        'NoteInformationField': 'REPEAT LOGO PREVIOUS ORDER',
                    },
                    'ChargesAllowances': {
                        'AllowChrgIndicator': 'C',
                        'AllowChrgCode': 'C310',
                        'AllowChrgAmt': '85.02',
                        'AllowChrgPercentQual': '4',
                        'AllowChrgPercent': '5.0',
                        'AllowChrgHandlingCode': '02',
                        'AllowChrgHandlingDescription':
                        'This will cover the cost of shipping',
                    },
                }"""
            shipment_dict.get('Shipment').update(meta_dict)
            shipment_dict.get('Shipment').update(header_dict)
            shipment_dict.get('Shipment').update(orderlevel_dict)
            shipment_dict.get('Shipment'
                              ).get('OrderLevel').update(packlevel_dict)

            # Sublines
            sublines_list = {'Sublines': []}
            total_lines = 0
            total_qty = 0
            total_weight = 0

            # for each sub line
            for line in picking.move_lines:
                total_lines += 1
                total_qty += line.product_qty
                total_weight += (line.product_id.weight * line.product_qty)
                subline_dict = {'Subline': {}}
                pickingline_dict = {'ShipmentLine': {
                    'LineSequenceNumber': int(line.id),
                    'BuyerPartNumber': line.product_id.default_code or '',
                    'VendorPartNumber': line.product_id.default_code or '',
                    'ConsumerPackageCode': line.consumer_package_code,
                    'EAN': line.product_id.barcode,
                    'GTIN': line.gtin,
                    'UPCCaseCode': line.upc_case_code,
                    'NatlDrugCode': line.natl_drug_code,
                    'InternationalStandardBookNumber':
                    line.international_standard_book_number,
                    'ProductID': {
                        'PartNumberQual': 'IT',
                        'PartNumber': line.product_id.default_code,
                    },
                    'PurchasePrice': line.price_unit,
                    'ShipQty': line.product_qty,
                    'ShipQtyUOM': 'P4',
                    'ProductSizeDescription': line.product_size_description,
                    'ProductColorDescription': line.product_color_description,
                    'ProductMaterialDescription':
                    line.product_material_description,
                }
                }
                subline_dict.get('Subline').update(pickingline_dict)
                sublines_list.get('Sublines').append(subline_dict)

            # shipment_dict.get('Shipment').get('OrderLevel').get('PackLevel'
            # ).get('ItemLevel').update(sublines_list)
            shipment_dict.get('Shipment'
                              ).get('OrderLevel').update(sublines_list)

            # summary
            summary_dict = {
                'Summary': {
                    'TotalLineItems': total_lines or '',
                    'TotalQuantity': total_qty,
                }
            }
            shipment_dict.get('Shipment').update(summary_dict)

            # update invoice
            today = datetime.now().strftime(DSD)
            picking.write({'sent_timestamp': today})
            shipments_list.get('Shipments').append(shipment_dict)
            processed += 1

        # convert dictionary to xml
        xml = dicttoxml.dicttoxml(shipments_list, attr_type=False, root=False)
        xml = xml.decode("utf-8")
        xml = xml.replace('<item>', '').replace('</item>', '')
        xml = xml.replace('<item>', '').\
            replace('<Shipments>',
                    '<?xml version="1.0" encoding="utf-8"?>' +
                    '<Shipments xmlns="http://www.spscommerce.com/RSX">')

        print("*****  SUCCESSFULLY STORED  *****")
        # Write ASN doc to text file
        name = re.findall('\d+', name)[0]
        filename = '856_' + today + '%s.xml' % name
        filename.replace('/', '_')
        if not picking.trading_partner_id.out_path:
            raise UserError('Add out path in Trading Partner')
        fd = open(picking.trading_partner_id.out_path + filename,
                  'w')
        fd.write(xml)
        fd.close()
        return processed

    def _create_856_wrapper(self):
        # search for invoices that are edi_yes = True
        # and sent_timestamp = False
        eligible_pickings = self.search([
            ('edi_yes', '=', True),
            ('sent_timestamp', '=', False)
        ])
        return eligible_pickings and self.create_text_856() or False

    # done as a server action
    @api.multi
    def action_create_text_856(self):
        """ Creates and new 856, ASN and puts it into the outbox
        """
        # number of orders to process
        toprocess = len(self.ids)

        # process orders to write 856
        processed = self.create_text_856()
        return (toprocess - processed)
