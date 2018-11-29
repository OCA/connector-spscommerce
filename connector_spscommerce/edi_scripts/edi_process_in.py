#!/usr/bin/python
# Copyright (c) Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import os
import shutil
import xmlrpclib
from datetime import datetime

import xmltodict

import edi_850
from connect_info import ERP_WWW, DBNAME, USERNAME, PWD, DEBUG, IN_PATH

test_me = """<?xml version="1.0" encoding='utf-8'?>
<Orders>
  <Order>
    <Meta>
      <Version>testVersion</Version>
    </Meta>
    <Header>
      <OrderHeader>
        <TradingPartnerId>000ALLTESTID</TradingPartnerId>
        <PurchaseOrderNumber>1010101010101</PurchaseOrderNumber>
        <TsetPurposeCode>00</TsetPurposeCode>
        <PurchaseOrderTypeCode>OS</PurchaseOrderTypeCode>
        <POTypeDescription>This is a test. Do not ship</POTypeDescription>
        <ReleaseNumber>XYZ999999</ReleaseNumber>
        <PurchaseOrderDate>2013-08-29</PurchaseOrderDate>
        <PurchaseOrderTime>21:05:49-06:00</PurchaseOrderTime>
        <ShipCompleteCode>Y</ShipCompleteCode>
        <BuyersCurrency>testBuyersCurrency</BuyersCurrency>
        <Department>026</Department>
        <Vendor>99999999</Vendor>
        <Division>Sam's Club</Division>
        <PromotionDealNumber>55555555</PromotionDealNumber>
      </OrderHeader>
      <PaymentTerms>
        <TermsType>09</TermsType>
        <TermsBasisDateCode>8</TermsBasisDateCode>
        <TermsDiscountPercentage>5.62</TermsDiscountPercentage>
        <TermsDiscountDate>2013-11-28</TermsDiscountDate>
        <TermsDiscountDueDays>60</TermsDiscountDueDays>
        <TermsNetDueDate>2013-11-15</TermsNetDueDate>
        <TermsNetDueDays>90</TermsNetDueDays>
        <TermsDiscountAmount>1845.08</TermsDiscountAmount>
        <TermsDescription>Must be paid in full by end of year</TermsDescription>
        <PaymentMethodCode>AB</PaymentMethodCode>
        <PaymentMethodID>999888777</PaymentMethodID>
      </PaymentTerms>
      <Date>
        <DateTimeQualifier1>043</DateTimeQualifier1>
        <Date1>2012-10-31</Date1>
        <Time1>16:13:03-05:00</Time1>
      </Date>
      <Contact>
        <ContactTypeCode>IC</ContactTypeCode>
        <ContactName>SPS Commerce</ContactName>
        <PrimaryPhone>866-245-8100</PrimaryPhone>
        <PrimaryFax>612-435-9401</PrimaryFax>
        <PrimaryEmail>info@spscommerce.com</PrimaryEmail>
      </Contact>
      <Address>
        <AddressTypeCode>FW</AddressTypeCode>
        <LocationCodeQualifier>9</LocationCodeQualifier>
        <AddressLocationNumber>11111</AddressLocationNumber>
        <AddressName>SPS Commerce</AddressName>
        <AddressAlternateName>ATTN: Marketing</AddressAlternateName>
        <Address1>333 South 7th Street</Address1>
        <Address2>ATTN: The President</Address2>
        <City>Washington</City>
        <State>MN</State>
        <PostalCode>55402</PostalCode>
        <Country>USA</Country>
        <Contact>
          <ContactTypeCode>BI</ContactTypeCode>
          <ContactName>SPS Commerce</ContactName>
          <PrimaryPhone>866-245-8100</PrimaryPhone>
          <PrimaryFax>612-435-9401</PrimaryFax>
          <PrimaryEmail>info@spscommerce.com</PrimaryEmail>
        </Contact>
      </Address>
      <FOBRelatedInstruction>
        <FOBPayCode>RS</FOBPayCode>
        <FOBLocationQualifier>MI</FOBLocationQualifier>
        <FOBLocationDescription>Minnesota</FOBLocationDescription>
      </FOBRelatedInstruction>
      <CarrierInformation>
        <CarrierTransMethodCode>SB</CarrierTransMethodCode>
        <CarrierAlphaCode>EMSY</CarrierAlphaCode>
        <CarrierRouting>ONTRAC</CarrierRouting>
      </CarrierInformation>
      <Reference>
        <ReferenceQual>GD</ReferenceQual>
        <ReferenceID>testReferenceID</ReferenceID>
        <Description>New products only. Do not reuse packaging</Description>
      </Reference>
      <Notes>
        <NoteCode>GEN</NoteCode>
        <NoteInformationField>REPEAT LOGO PREVIOUS ORDER</NoteInformationField>
      </Notes>
      <Tax>
        <TaxTypeCode>EV</TaxTypeCode>
        <TaxAmount>1845.08</TaxAmount>
        <TaxPercent>8.50</TaxPercent>
        <JurisdictionQual>CC</JurisdictionQual>
        <JurisdictionCode>07034</JurisdictionCode>
        <TaxExemptCode>0</TaxExemptCode>
        <TaxID>99990000</TaxID>
      </Tax>
      <ChargesAllowances>
        <AllowChrgIndicator>A</AllowChrgIndicator>
        <AllowChrgCode>F330</AllowChrgCode>
        <AllowChrgAmt>85.02</AllowChrgAmt>
        <AllowChrgPercentQual>1</AllowChrgPercentQual>
        <AllowChrgPercent>5.0</AllowChrgPercent>
        <AllowChrgHandlingCode>02</AllowChrgHandlingCode>
        <AllowChrgHandlingDescription>This will cover the cost of shipping</AllowChrgHandlingDescription>
      </ChargesAllowances>
    </Header>
    <LineItems>
      <LineItem>
        <OrderLine>
          <LineSequenceNumber>01</LineSequenceNumber>
          <BuyerPartNumber>9999-SPS</BuyerPartNumber>
          <VendorPartNumber>11155-559999</VendorPartNumber>
          <ConsumerPackageCode>093597609541</ConsumerPackageCode>
          <EAN>1234567890123</EAN>
          <GTIN>12345678901234</GTIN>
          <UPCCaseCode>98765432101</UPCCaseCode>
          <NatlDrugCode>51456-299</NatlDrugCode>
          <InternationalStandardBookNumber>999-0-555-22222-0</InternationalStandardBookNumber>
          <ProductID>
            <PartNumberQual>VC</PartNumberQual>
            <PartNumber>ABC-456789</PartNumber>
          </ProductID>
          <OrderQty>125</OrderQty>
          <OrderQtyUOM>DA</OrderQtyUOM>
          <PurchasePrice>5.85</PurchasePrice>
          <BuyersCurrency>testBuyersCurrency</BuyersCurrency>
          <ProductSizeCode>S-800</ProductSizeCode>
          <ProductSizeDescription>Small</ProductSizeDescription>
          <ProductColorCode>C-999</ProductColorCode>
          <ProductColorDescription>Fire Truck Red</ProductColorDescription>
          <ProductMaterialDescription>Faux Fabric</ProductMaterialDescription>
          <Department>026</Department>
          <Class>testClass</Class>
          <NRFStandardColorAndSize>
            <NRFColorCode>600</NRFColorCode>
            <NRFSizeCode>42-10651</NRFSizeCode>
          </NRFStandardColorAndSize>
        </OrderLine>
        <Date>
          <DateTimeQualifier1>069</DateTimeQualifier1>
          <Date1>2012-10-31</Date1>
          <Time1>16:13:03-05:00</Time1>
        </Date>
        <PriceInformation>
          <PriceTypeIDCode>RPC</PriceTypeIDCode>
          <UnitPrice>5.48</UnitPrice>
        </PriceInformation>
        <ProductOrItemDescription>
          <ItemDescriptionType>RE</ItemDescriptionType>
          <ProductDescription>Super comfortable</ProductDescription>
        </ProductOrItemDescription>
        <PhysicalDetails>
          <PackQualifier>CP</PackQualifier>
          <PackValue>6</PackValue>
          <PackSize>18</PackSize>
          <PackUOM>BO</PackUOM>
        </PhysicalDetails>
        <Reference>
          <ReferenceQual>BY</ReferenceQual>
          <ReferenceID>testReferenceID</ReferenceID>
          <Description>New products only. Do not reuse packaging</Description>
        </Reference>
        <Notes>
          <NoteCode>CAFA3</NoteCode>
          <NoteInformationField>REPEAT LOGO PREVIOUS ORDER</NoteInformationField>
        </Notes>
        <FloorReady>
          <FloorReadyRequired>N</FloorReadyRequired>
          <FloorReadyTypeCode>S</FloorReadyTypeCode>
          <FloorReadyDescription>Hanger with clips</FloorReadyDescription>
          <FloorReadyID>A-112233</FloorReadyID>
        </FloorReady>
        <Sublines>
          <Subline>
            <SublineItemDetail>
              <LineSequenceNumber>02</LineSequenceNumber>
              <BuyerPartNumber>9999-SPS</BuyerPartNumber>
              <VendorPartNumber>11155-559999</VendorPartNumber>
              <ConsumerPackageCode>093597609541</ConsumerPackageCode>
              <EAN>1234567890123</EAN>
              <GTIN>12345678901234</GTIN>
              <UPCCaseCode>98765432101</UPCCaseCode>
              <NatlDrugCode>51456-299</NatlDrugCode>
              <InternationalStandardBookNumber>999-0-555-22222-0</InternationalStandardBookNumber>
              <ProductID>
                <PartNumberQual>N5</PartNumberQual>
                <PartNumber>ABC-456789</PartNumber>
              </ProductID>
              <ProductSizeCode>S-800</ProductSizeCode>
              <ProductSizeDescription>Small</ProductSizeDescription>
              <ProductColorCode>C-999</ProductColorCode>
              <ProductColorDescription>Fire Truck Red</ProductColorDescription>
              <ProductMaterialDescription>Faux Fabric</ProductMaterialDescription>
              <QtyPer>5</QtyPer>
              <QtyPerUOM>PP</QtyPerUOM>
              <PurchasePrice>5.85</PurchasePrice>
              <NRFStandardColorAndSize>
                <NRFColorCode>600</NRFColorCode>
                <NRFSizeCode>42-10651</NRFSizeCode>
              </NRFStandardColorAndSize>
            </SublineItemDetail>
            <PriceInformation>
              <PriceTypeIDCode>RTL</PriceTypeIDCode>
              <UnitPrice>5.48</UnitPrice>
            </PriceInformation>
            <ProductOrItemDescription>
              <ItemDescriptionType>74</ItemDescriptionType>
              <ProductDescription>Super comfortable</ProductDescription>
            </ProductOrItemDescription>
            <FloorReady>
              <FloorReadyRequired>Y</FloorReadyRequired>
              <FloorReadyTypeCode>H</FloorReadyTypeCode>
              <FloorReadyDescription>Hanger with clips</FloorReadyDescription>
              <FloorReadyID>A-112233</FloorReadyID>
            </FloorReady>
          </Subline>
        </Sublines>
        <QuantitiesSchedulesLocations>
          <TotalQty>100</TotalQty>
          <TotalQtyUOM>P9</TotalQtyUOM>
          <Date>
            <DateTimeQualifier1>097</DateTimeQualifier1>
            <Date1>2013-12-21</Date1>
            <Time1>16:13:03-05:00</Time1>
          </Date>
        </QuantitiesSchedulesLocations>
        <Tax>
          <TaxTypeCode>CA</TaxTypeCode>
          <TaxAmount>1845.08</TaxAmount>
          <TaxPercent>8.50</TaxPercent>
          <JurisdictionQual>CC</JurisdictionQual>
          <JurisdictionCode>07034</JurisdictionCode>
          <TaxExemptCode>2</TaxExemptCode>
          <TaxID>99990000</TaxID>
        </Tax>
        <ChargesAllowances>
          <AllowChrgIndicator>C</AllowChrgIndicator>
          <AllowChrgCode>D550</AllowChrgCode>
          <AllowChrgAmt>85.02</AllowChrgAmt>
          <AllowChrgPercentQual>1</AllowChrgPercentQual>
          <AllowChrgPercent>5.0</AllowChrgPercent>
          <AllowChrgHandlingCode>01</AllowChrgHandlingCode>
          <AllowChrgHandlingDescription>This will cover the cost of shipping</AllowChrgHandlingDescription>
        </ChargesAllowances>
      </LineItem>
    </LineItems>
    <Summary>
      <TotalAmount>4058.92</TotalAmount>
      <TotalLineItemNumber>3</TotalLineItemNumber>
      <TotalQuantity>90</TotalQuantity>
    </Summary>
  </Order>
</Orders>"""


def connect_oerp():
    '''
    Function that will make a connection to OpenERP using XML-RPC.
    @return1: socket that is connected to OpenERP
    @return2: An id that shows that you have been validated
    '''
    sock = xmlrpclib.ServerProxy(ERP_WWW + '/xmlrpc/object')
    sock_common = xmlrpclib.ServerProxy(ERP_WWW + '/xmlrpc/common')
    uid = sock_common.login(DBNAME, USERNAME, PWD)

    print "XMLRPC Connection: SUCCESS - SERVER HAS AUTHENTICATED A LOGIN"

    return sock, uid


def parse_csv(sock, uid, file):
    # note xmltodict.unparse(file) will convert it back to xml.  It will also
    # convert any dict to xml.
    orders = xmltodict.parse(test_me)
    #     order_dict = xmltodict.parse(test_me)
    record = {}

    # improve process in
    for order in orders['Orders']:
        record['address_type_code'] = order['Order']['Header']['Address'][
            'AddressTypeCode']
        record['location_code_qualifier'] = \
            order['Order']['Header']['Address']['LocationCodeQualifier']
        record['address_location_number'] = \
            order['Order']['Header']['Address']['AddressLocationNumber']
        record['address_name'] = order['Order']['Header']['Address'][
            'AddressName']
        record['address_alternate_name'] = order['Order']['Header']['Address'][
            'AddressAlternateName']
        record['address1'] = order['Order']['Header']['Address']['Address1']
        record['address2'] = order['Order']['Header']['Address']['Address2']
        record['city'] = order['Order']['Header']['Address']['City']
        record['state'] = order['Order']['Header']['Address']['State']
        record['postal_code'] = order['Order']['Header']['Address'][
            'PostalCode']
        record['country'] = order['Order']['Header']['Address']['Country']
        record['contact'] = {}
        record['contact']['contact_type_code'] = \
            order['Order']['Header']['Address']['Contact']['ContactTypeCode']
        record['contact']['contact_name'] = \
            order['Order']['Header']['Address']['Contact']['ContactName']
        record['contact']['primary_phone'] = \
            order['Order']['Header']['Address']['Contact']['PrimaryPhone']
        record['contact']['primary_fax'] = \
            order['Order']['Header']['Address']['Contact']['PrimaryFax']
        record['contact']['primary_email'] = \
            order['Order']['Header']['Address']['Contact']['PrimaryEmail']
        record['date'] = order['Order']['Header']['Date']['Date1']
        record['time'] = order['Order']['Header']['Date']['Time1']
        record['edi_error'] = False
        record['edi_yes'] = False
        record['ack_yes'] = True
        record['855_replace'] = True
        record['supplier_code'] = '123'
        record['ship_not_before_date'] = datetime.now().strftime('%Y-%m-%d')
        record['cancel_after_date'] = datetime.now().strftime('%Y-%m-%d')
        record['trading_partner_id'] = order['Order']['Header']['OrderHeader'][
            'TradingPartnerId']
        record['scac_code'] = ''
        record['bol_num'] = ''
        record['asn_shipment'] = ''
        record['tracking_num'] = ''
        record['tset_purpose_code'] = order['Order']['Header']['OrderHeader'][
            'TsetPurposeCode']
        record['purchase_order_number'] = \
            order['Order']['Header']['OrderHeader']['PurchaseOrderNumber']
        record['purchase_order_type_code'] = \
            order['Order']['Header']['OrderHeader']['PurchaseOrderTypeCode']
        record['po_type_description'] = \
            order['Order']['Header']['OrderHeader']['POTypeDescription']
        record['ship_complete_code'] = order['Order']['Header']['OrderHeader'][
            'ShipCompleteCode']
        record['department'] = order['Order']['Header']['OrderHeader'][
            'Department']
        record['division'] = order['Order']['Header']['OrderHeader'][
            'Division']
        record['promotion_deal_number'] = \
            order['Order']['Header']['OrderHeader']['PromotionDealNumber']
        record['terms_type'] = order['Order']['Header']['PaymentTerms'][
            'TermsType']
        record['terms_basis_date_code'] = \
            order['Order']['Header']['PaymentTerms']['TermsBasisDateCode']
        record['terms_discount_percentage'] = \
            order['Order']['Header']['PaymentTerms']['TermsDiscountPercentage']
        record['terms_discount_due_days'] = \
            order['Order']['Header']['PaymentTerms']['TermsDiscountDueDays']
        record['terms_net_due_days'] = \
            order['Order']['Header']['PaymentTerms']['TermsNetDueDays']
        record['payment_method_code'] = \
            order['Order']['Header']['PaymentTerms']['PaymentMethodCode']
        record['fob_pay_code'] = \
            order['Order']['Header']['FOBRelatedInstruction']['FOBPayCode']
        record['fob_location_qualifier'] = \
            order['Order']['Header']['FOBRelatedInstruction'][
                'FOBLocationQualifier']
        record['fob_location_description'] = \
            order['Order']['Header']['FOBRelatedInstruction'][
                'FOBLocationDescription']
        record['fob_title_passage_code'] = ''
        record['fob_title_passage_location'] = ''
        record['carrier_trans_method_code'] = \
            order['Order']['Header']['CarrierInformation'][
                'CarrierTransMethodCode']
        record['carrier_alpha_code'] = \
            order['Order']['Header']['CarrierInformation']['CarrierAlphaCode']
        record['carrier_routing'] = \
            order['Order']['Header']['CarrierInformation']['CarrierRouting']
        record['routing_sequence_code'] = ''
        record['service_level_code'] = ''
        record['reference_qual'] = order['Order']['Header']['Reference'][
            'ReferenceQual']
        record['reference_id'] = order['Order']['Header']['Reference'][
            'ReferenceID']
        record['ref_description'] = order['Order']['Header']['Reference'][
            'Description']
        record['note_code'] = order['Order']['Header']['Notes']['NoteCode']
        record['note_information_field'] = order['Order']['Header']['Notes'][
            'NoteInformationField']
        record['allow_chrg_indicator'] = \
            order['Order']['Header']['ChargesAllowances']['AllowChrgIndicator']
        record['allow_chrg_code'] = \
            order['Order']['Header']['ChargesAllowances']['AllowChrgCode']
        record['allow_chrg_agency_code'] = ''
        record['allow_chrg_agency'] = ''
        record['allow_chrg_amt'] = \
            order['Order']['Header']['ChargesAllowances']['AllowChrgAmt']
        record['allow_chrg_percent_qual'] = \
            order['Order']['Header']['ChargesAllowances'][
                'AllowChrgPercentQual']
        record['allow_chrg_percent'] = \
            order['Order']['Header']['ChargesAllowances']['AllowChrgPercent']
        record['allow_chrg_handling_code'] = \
            order['Order']['Header']['ChargesAllowances'][
                'AllowChrgHandlingCode']
        record['reference_identification'] = ''
        record['allow_chrg_handling_description'] = \
            order['Order']['Header']['ChargesAllowances'][
                'AllowChrgHandlingDescription']

        record['order_line'] = {}
        for line in orders['Orders']['Order']['LineItems']:
            order_line_data = {
                'product_qty':
                    orders['Orders']['Order']['LineItems'][line]['OrderLine'][
                        'OrderQty'],
                'product_uom':
                    orders['Orders']['Order']['LineItems'][line]['OrderLine'][
                        'OrderQtyUOM'],
                'sku':
                    orders['Orders']['Order']['LineItems'][line]['OrderLine'][
                        'VendorPartNumber'],
                'edi_yes': False,
                'asn_shipment': '123',
                'po_number': '123',
                'buyer_part_number':
                    orders['Orders']['Order']['LineItems'][line]['OrderLine'][
                        'BuyerPartNumber'],
                'edi_line_num':
                    orders['Orders']['Order']['LineItems'][line]['OrderLine'][
                        'LineSequenceNumber'],
                'edi_line_qty': '123',
                'ack_yes': '123',
                'edi_est_del_date': datetime.now().strftime('%Y-%m-%d'),
                'edi_est_ship_date': datetime.now().strftime('%Y-%m-%d'),
                'edi_line_msg': '123',
                'ship_not_before_date': datetime.now().strftime('%Y-%m-%d'),
                'cancel_after_date': datetime.now().strftime('%Y-%m-%d'),
                'trading_partner_id':
                    orders['Orders']['Order']['Header']['OrderHeader'][
                        'TradingPartnerId'],
                'edi_intransit_qty': 0,
                'edi_outgoing_qty': 0,
                'edi_avlforsale_qty': 0,
                'vendor_part_number':
                    orders['Orders']['Order']['LineItems'][line]['OrderLine'][
                        'VendorPartNumber'],
                'consumer_package_code':
                    orders['Orders']['Order']['LineItems'][line]['OrderLine'][
                        'ConsumerPackageCode'],
                'gtin':
                    orders['Orders']['Order']['LineItems'][line]['OrderLine'][
                        'GTIN'],
                'upc_case_code':
                    orders['Orders']['Order']['LineItems'][line]['OrderLine'][
                        'UPCCaseCode'],
                'purchase_price_basis':
                    orders['Orders']['Order']['LineItems'][line]['OrderLine'][
                        'PurchasePrice'],
                'product_size_code':
                    orders['Orders']['Order']['LineItems'][line]['OrderLine'][
                        'ProductSizeCode'],
                'product_size_description':
                    orders['Orders']['Order']['LineItems'][line]['OrderLine'][
                        'ProductSizeDescription'],
                'product_color_code':
                    orders['Orders']['Order']['LineItems'][line]['OrderLine'][
                        'ProductColorCode'],
                'product_color_description':
                    orders['Orders']['Order']['LineItems'][line]['OrderLine'][
                        'ProductColorDescription'],
                #                                'product_material_code':orders['Orders']['Order']['LineItems'][line]['OrderLine']['ProductMaterialCode'],
                'product_material_description':
                    orders['Orders']['Order']['LineItems'][line]['OrderLine'][
                        'ProductMaterialDescription'],
                'department':
                    orders['Orders']['Order']['LineItems'][line]['OrderLine'][
                        'Department'],
                'classs':
                    orders['Orders']['Order']['LineItems'][line]['OrderLine'][
                        'Class'],
                'price_type_id_code':
                    orders['Orders']['Order']['LineItems'][line][
                        'PriceInformation']['PriceTypeIDCode'],
                'edi_line_num':
                    orders['Orders']['Order']['LineItems'][line]['OrderLine'][
                        'LineSequenceNumber'],
                #                                 'multiple_price_quantity':orders['Orders']['Order']['LineItems'][line]['PriceInformation']['MultiplePriceQuantity'],
                #                                 'class_of_trade_code':orders['Orders']['Order']['LineItems'][line]['PriceInformation']['ClassOfTradeCode'],
                'item_description_type':
                    orders['Orders']['Order']['LineItems'][line][
                        'ProductOrItemDescription']['ItemDescriptionType'],
                'product_characteristic_code': '',
                'agency_qualifier_code': '',
                'product_description_code': '',
                'pack_qualifier': orders['Orders']['Order']['LineItems'][line][
                    'PhysicalDetails']['PackQualifier'],
                'pack_value': orders['Orders']['Order']['LineItems'][line][
                    'PhysicalDetails']['PackValue'],
                'pack_size': orders['Orders']['Order']['LineItems'][line][
                    'PhysicalDetails']['PackSize'],
                'pack_uom': orders['Orders']['Order']['LineItems'][line][
                    'PhysicalDetails']['PackUOM'],
                'packing_medium': '',
                'packing_material': '',
                'pack_weight': 0,
                'pack_weight_uom': '',
                'location_code_qualifier': '',
                'location': '',
                'allow_chrg_indicator':
                    orders['Orders']['Order']['LineItems'][line][
                        'ChargesAllowances']['AllowChrgIndicator'],
                'allow_chrg_code':
                    orders['Orders']['Order']['LineItems'][line][
                        'ChargesAllowances']['AllowChrgCode'],
                'allow_chrg_agency_code': '',
                'allow_chrg_agency': '',
                'allow_chrg_amt': orders['Orders']['Order']['LineItems'][line][
                    'ChargesAllowances']['AllowChrgAmt'],
                'allow_chrg_percent':
                    orders['Orders']['Order']['LineItems'][line][
                        'ChargesAllowances']['AllowChrgPercent'],
                'percent_dollar_basis': 0,
                'allow_chrg_rate': 0,
                'allow_chrg_handling_code':
                    orders['Orders']['Order']['LineItems'][line][
                        'ChargesAllowances']['AllowChrgHandlingCode'],
                'allow_chrg_qty_uom': '',
                #                                 'allow_chrg_handling_description':orders['Orders']['Order']['LineItems'][line]['ChargesAllowances']['allow_chrg_handling_description'],
            }
            record['order_line'].update(order_line_data)
    print "Stop", record
    sale_id = create_sale_order(sock, uid, record)
    print "Successfully created ORDER IMPORTED!!!!", sale_id
    line_ids = create_so_lines(sock, uid, sale_id, record['order_line'])
    print "Successfully created ORDER LINES IMPORTED!!!!", line_ids
    return parse_csv


def get_order_header(order_header):
    """Inputs:
        order_header = "
          <OrderHeader>
            <TradingPartnerId>000ALLTESTID</TradingPartnerId>
            <PurchaseOrderNumber>1010101010101</PurchaseOrderNumber>
            <TsetPurposeCode>00</TsetPurposeCode>
            <PurchaseOrderTypeCode>OS</PurchaseOrderTypeCode>
            <POTypeDescription>This is a test. Do not ship</POTypeDescription>
            <ReleaseNumber>XYZ999999</ReleaseNumber>
            <PurchaseOrderDate>2013-08-29</PurchaseOrderDate>
            <PurchaseOrderTime>21:05:49-06:00</PurchaseOrderTime>
            <ShipCompleteCode>Y</ShipCompleteCode>
            <BuyersCurrency>testBuyersCurrency</BuyersCurrency>
            <Department>026</Department>
            <Vendor>99999999</Vendor>
            <Division>Sam's Club</Division>
            <PromotionDealNumber>55555555</PromotionDealNumber>
          </OrderHeader>"
        Output: dictionary with values for header to be used in sale order
         import
    """
    return \
        order_header['Department'], \
        order_header['PurchaseOrderNumber'], \
        order_header['TradingPartnerId'], \
        order_header['PurchaseOrderDate']


def get_state(sock, uid, state):
    args = [('name', '=', state)]
    ids = sock.execute(DBNAME, uid, PWD, 'res.country.state', 'search', args)

    try:
        state_id = ids[0]
        return state_id

    except Exception:
        "There are no states matching the code"
        return False


def get_country(sock, uid, country):
    args = [('name', '=', country)]
    ids = sock.execute(DBNAME, uid, PWD, 'res.country', 'search', args)

    try:
        country_id = ids[0]
        return country_id

    except Exception:
        "There are no states matching the code"
        return False


def get_partner_info(
        sock,
        uid,
        partner_contact,
        address1='',
        address2='',
        city='',
        state='',
        postal_code='',
        country=''):
    fields = [
        'is_company',
        'city',
        'country_id',
        'company_id',
        'email',
        'fax',
        'name',
        'phone',
        'state_id',
        'street',
        'street2',
        'website',
        'zip',
        'ship_to_code',
        'user_id',
        'property_product_pricelist']

    try:
        # check for existing partner if not then create
        print "LOOK FOR THIS", partner_contact['contact_name']
        args = [('name', '=', partner_contact['contact_name'])]
        ids = sock.execute(DBNAME, uid, PWD, 'res.partner', 'search', args)
        if ids:
            result = sock.execute(
                DBNAME, uid, PWD, 'res.partner', 'read', ids[0], fields)
        else:
            partner_data = {
                'name': partner_contact['contact_name'],
                'phone': partner_contact['primary_phone'],
                'email': partner_contact['primary_email'],
                'fax': partner_contact['primary_fax'],
                'street': address1,
                'street2': address2,
                'city': city,
                'zip': postal_code,
                'state_id': get_state(sock, uid, state),
                'country_id': get_country(sock, uid, country),
                'user_id': uid,
            }
            partner_id = sock.execute(
                DBNAME, uid, PWD, 'res.partner', 'create', partner_data)
            result = sock.execute(
                DBNAME, uid, PWD, 'res.partner', 'read', partner_id, fields)
        return result

    except Exception:
        "There are no partners to process"
        pass


def search_product(sock, uid, product_sku):
    args = [('default_code', '=', product_sku)]
    ids = sock.execute(DBNAME, uid, PWD, 'product.product', 'search', args)
    try:
        product_id = ids[0]
    except Exception:
        product_id = 'no_exist'
        print 'product does not exist'

    return product_id


def create_sale_order(sock, uid, order_data):
    partner_info = get_partner_info(
        sock,
        uid,
        order_data['contact'],
        order_data['address1'],
        order_data['address2'],
        order_data['city'],
        order_data['state'],
        order_data['postal_code'],
        order_data['country'])
    user_id = False
    if partner_info['user_id']:
        user_id = partner_info['user_id'][0]

    pricelist_id = False
    if partner_info['property_product_pricelist']:
        pricelist_id = partner_info['property_product_pricelist'][0]

    # based on partner's billing address, look up in partner record to find
    # billing contact
    if partner_info['id']:
        partner_invoice_id = partner_info['id']
        partner_shipping_id = partner_info['id']
    print "datetime.now().strftime('%Y-%m-%d %H:%M:%S')", \
        datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    sale_hash = {
        'incoterm': 14,  # hardcoded to "Delivery at Place"
        'date_order': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'client_order_ref': order_data['purchase_order_number'],
        'origin': False,
        'note': '',
        'user_id': user_id or 1,
        'team_id': 1,
        'warehouse_id': 9,
        'partner_id': partner_info['id'] or False,
        # 'carrier_id': carrier_id,
        'pricelist_id': pricelist_id or 1,
        'project_id': 1,
        'currency_id': 1,
        # 'payment_term': payment_term,
        'company_id': 1,
        'order_policy': 'picking',  # hardcoded to "On Delivery",
        'picking_policy': 'direct',
        'partner_invoice_id': partner_invoice_id,
        'partner_shipping_id': partner_shipping_id,
        'edi_yes': True,
        'ack_yes': True,
        'ack_sent': False,
        'ship_to_code': partner_info['ship_to_code'],
        'trading_partner_id': partner_info['id'],
        'edi_est_so_ship_date': datetime.now().strftime('%Y-%m-%d'),
        'tset_purpose_code': order_data['tset_purpose_code'],
        'purchase_order_type_code': order_data['purchase_order_type_code'],
        'po_type_description': order_data['po_type_description'],
        'ship_complete_code': order_data['ship_complete_code'],
        'department': order_data['department'],
        'division': order_data['division'],
        'promotion_deal_number': order_data['promotion_deal_number'],
        'terms_type': order_data['terms_type'],
        'terms_basis_date_code': order_data['terms_basis_date_code'],
        'terms_discount_percentage': order_data['terms_discount_percentage'],
        'terms_discount_due_days': order_data['terms_discount_due_days'],
        'terms_net_due_days': order_data['terms_net_due_days'],
        'payment_method_code': order_data['payment_method_code'],
        'fob_pay_code': order_data['fob_pay_code'],
        'fob_location_qualifier': order_data['fob_location_qualifier'],
        'fob_location_description': order_data['fob_location_description'],
        'fob_title_passage_code': order_data['fob_title_passage_code'],
        'fob_title_passage_location': order_data['fob_title_passage_location'],
        'carrier_trans_method_code': order_data['carrier_trans_method_code'],
        'carrier_alpha_code': order_data['carrier_alpha_code'],
        'carrier_routing': order_data['carrier_routing'],
        'routing_sequence_code': order_data['routing_sequence_code'],
        'service_level_code': order_data['service_level_code'],
        'reference_qual': order_data['reference_qual'],
        'reference_id': order_data['reference_id'],
        'ref_description': order_data['ref_description'],
        'note_code': order_data['note_code'],
        'note_information_field': order_data['note_information_field'],
        'allow_chrg_indicator': order_data['allow_chrg_indicator'],
        'allow_chrg_code': order_data['allow_chrg_code'],
        'allow_chrg_agency_code': order_data['allow_chrg_agency_code'],
        'allow_chrg_agency': order_data['allow_chrg_agency'],
        'allow_chrg_amt': order_data['allow_chrg_amt'],
        'allow_chrg_percent_qual': order_data['allow_chrg_percent_qual'],
        'allow_chrg_percent': order_data['allow_chrg_percent'],
        'allow_chrg_handling_code': order_data['allow_chrg_handling_code'],
        'reference_identification': order_data['reference_identification'],
        'allow_chrg_handling_description':
            order_data['allow_chrg_handling_description'],
    }

    print "Attempting to create %s" % sale_hash
    sale_id = sock.execute(DBNAME, uid, PWD, 'sale.order', 'create', sale_hash)
    print "sale_idddddddddddddddddddddddd", sale_id
    return sale_id


def search_uom(sock, uid, uom):
    uom_id = ''

    args = [('name', 'ilike', uom)]
    ids = sock.execute(DBNAME, uid, PWD, 'product.uom', 'search', args)
    try:
        uom_id = ids[0]
    except Exception:
        pass

    return uom_id


def create_so_lines(sock, uid, sale_id, order_lines):
    sale_line_ids = []

    for line in order_lines:
        p_id = search_product(sock, uid, order_lines['sku'])

        order_line_hash = {
            'name': p_id.default_code,
            'edi_line_num': line['edi_line_num'],
            'product_uos_qty': int(line['product_qty']),
            'product_uom_qty': int(line['product_qty']),
            'edi_line_qty': int(line['product_qty']),
            'state': 'draft',
            'order_id': sale_id,  # from sale order we just created
            'invoiced': False,
            'th_weight': 0,  # lookup from product
            'product_id': p_id,
            # passed in from PO
            'price_unit': line['purchase_price_basis'],
            # lookup from product
            'purchase_price': line['purchase_price_basis'],
            'product_uom': line['product_uom'],  # lookup from product
            'product_qty': int(line['product_qty']),
            'sku': line['sku'],
            'edi_yes': line['edi_yes'],
            'asn_shipment': line['asn_shipment'],
            'po_number': line['po_number'],
            'buyer_part_number': line['buyer_part_number'],
            'ack_yes': line['ack_yes'],
            'edi_est_del_date': line['edi_est_del_date'],
            'edi_est_ship_date': line['edi_est_ship_date'],
            'edi_line_msg': line['edi_line_msg'],
            'ship_not_before_date': line['ship_not_before_date'],
            'cancel_after_date': line['cancel_after_date'],
            'trading_partner_id': line['trading_partner_id'],
            'edi_intransit_qty': line['edi_intransit_qty'],
            'edi_outgoing_qty': line['edi_outgoing_qty'],
            'edi_avlforsale_qty': line['edi_avlforsale_qty'],
            'vendor_part_number': line['vendor_part_number'],
            'consumer_package_code': line['consumer_package_code'],
            'gtin': line['gtin'],
            'upc_case_code': line['upc_case_code'],
            'purchase_price_basis': line['purchase_price_basis'],
            'product_size_code': line['product_size_code'],
            'product_size_description': line['product_size_description'],
            'product_color_code': line['product_color_code'],
            'product_color_description': line['product_color_description'],
            'product_material_description':
                line['product_material_description'],
            'department': line['department'],
            'classs': line['classs'],
            'price_type_id_code': line['price_type_id_code'],
            'item_description_type': line['item_description_type'],
            'product_characteristic_code': line['product_characteristic_code'],
            'agency_qualifier_code': line['agency_qualifier_code'],
            'product_description_code': line['product_description_code'],
            'pack_qualifier': line['pack_qualifier'],
            'pack_value': line['pack_value'],
            'pack_size': line['pack_size'],
            'pack_uom': line['pack_uom'],
            'packing_medium': line['packing_medium'],
            'packing_material': line['packing_material'],
            'pack_weight': line['pack_weight'],
            'pack_weight_uom': line['pack_weight_uom'],
            'location_code_qualifier': line['location_code_qualifier'],
            'location': line['location'],
            'allow_chrg_indicator': line['allow_chrg_indicator'],
            'allow_chrg_code': line['allow_chrg_code'],
            'allow_chrg_agency_code': line['allow_chrg_agency_code'],
            'allow_chrg_agency': line['allow_chrg_agency'],
            'allow_chrg_amt': line['allow_chrg_amt'],
            'allow_chrg_percent': line['allow_chrg_percent'],
            'percent_dollar_basis': line['percent_dollar_basis'],
            'allow_chrg_rate': line['allow_chrg_rate'],
            'allow_chrg_handling_code': line['allow_chrg_handling_code'],
            'allow_chrg_qty_uom': line['allow_chrg_qty_uom'],
        }
        try:
            line_id = sock.execute(
                DBNAME, uid, PWD, 'sale.order.line', 'create', order_line_hash)
            sale_line_ids.append(line_id)
        except BaseException:
            pass
    return sale_line_ids


def main():
    # connect to openerp
    sock, uid = connect_oerp()
    company_id = False

    if not company_id:
        company_id = edi_850.get_current_company(sock, uid)
    # read in incoming EDI, parse through and create dictionary with EDI info
    files = os.listdir(IN_PATH)
    # loop through files
    for fle in files:
        status, partner = parse_csv(sock, uid, IN_PATH + fle)
        # get edi_config_id from company record
        edi_id = edi_850.edi_config_id(sock, uid, company_id, partner)
        # print 'EDI: ' + str(edi_id)
        config = edi_850.get_config(sock, uid, edi_id)
        # move processed file to archive folder
        if not DEBUG and status:
            if config['archive_path']:
                shutil.move(IN_PATH + fle, config['archive_path'] + '/' + fle)


if __name__ == '__main__':
    print 'Process: EDI Orders Read - Starting'
    main()
    print 'Process: EDI Orders Read - Ending'
