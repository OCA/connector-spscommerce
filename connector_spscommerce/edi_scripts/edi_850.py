#!/usr/bin/python
# Copyright (c) Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import sys
from datetime import datetime
from connect_info import DBNAME, PWD


def get_state(sock, uid, state):
    args = [('code', '=', state)]
    ids = sock.execute(DBNAME, uid, PWD, 'res.country.state', 'search', args)

    try:
        state_id = ids[0]
        return state_id

    except Exception:
        "There are no states matching the code"
        pass


def get_country(sock, uid, country):
    args = [('code', '=', country)]
    ids = sock.execute(DBNAME, uid, PWD, 'res.country', 'search', args)

    try:
        country_id = ids[0]
        return country_id

    except Exception:
        "There are no states matching the code"
        pass


def get_current_company(sock, uid):

    args = [('partner_id', '=', 1)]
    ids = sock.execute(DBNAME, uid, PWD, 'res.company', 'search', args)

    try:
        company_id = ids[0]
        return company_id

    except Exception:
        "There is no company with partner_id = 1"
        pass


def edi_config_id(
        sock,
        uid,
        company_id,
        partner_header_string,
        vendor_header_string):

    args = [('partner_header_string', '=', partner_header_string),
            ('vendor_header_string', '=', vendor_header_string)]
    ids = sock.execute(DBNAME, uid, PWD, 'edi.config', 'search', args)
    edi = []

    try:
        edi = ids[0]

    except Exception:
        print "There are no trading partners to process"
        pass

    return edi


def get_config(sock, uid, edi):

    fields = [
        'partner_header_string',
        'vendor_header_string',
        'salesperson',
        'edi_company_id',
        'in_path',
        'out_path',
        'log_path',
        'archive_path',
        'trading_partner_id',
        'ack_855',
        'auto_workflow']
    record = sock.execute(DBNAME, uid, PWD, 'edi.config', 'read', edi, fields)
    try:
        rec = record['trading_partner_id']
        rec = record['out_path']
        rec = record['archive_path']
        return record
    except Exception:
        print "There are no trading partners to process, paths not set or EOL" \
              " marker not defined."
        pass


def get_partner_info(sock, uid, partner_id):

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
        result = sock.execute(
            DBNAME, uid, PWD, 'res.partner', 'read', partner_id, fields)
        return result

    except Exception:
        "There are no partners to process"
        pass


def get_shipping_partner(sock, uid, partner_id, ship_to_code):
    args = [('parent_id', '=', partner_id),
            ('ship_to_code', '=', ship_to_code)]
    ids = sock.execute(DBNAME, uid, PWD, 'res.partner', 'search', args)
    shipping_id = False
    try:
        shipping_id = ids[0]
    except Exception:
        "There are no shipping partners to process"
        pass

    return shipping_id


def get_billing_partner(sock, uid, partner_id):
    args = [('parent_id', '=', partner_id), ('type', '=', 'invoice')]
    ids = sock.execute(DBNAME, uid, PWD, 'res.partner', 'search', args)
    billing_id = False
    try:
        billing_id = ids[0]
    except Exception:
        "There are no billing partners to process"
        pass

    return billing_id


def search_uom(sock, uid, uom):

    uom_id = ''

    args = [('name', 'ilike', uom)]
    ids = sock.execute(DBNAME, uid, PWD, 'product.uom', 'search', args)
    try:
        uom_id = ids[0]
    except Exception:
        pass

    return uom_id


def search_pmt_terms(sock, uid, payment_terms):

    pmt_id = ''

    args = [('name', 'ilike', payment_terms)]
    ids = sock.execute(
        DBNAME, uid, PWD, 'account.payment.term', 'search', args)
    try:
        pmt_id = ids[0]
    except Exception:
        pass

    return pmt_id


def search_incoterm(sock, uid, code):

    incoterm_id = ''

    args = [('code', 'ilike', code)]
    ids = sock.execute(DBNAME, uid, PWD, 'stock.incoterms', 'search', args)
    try:
        incoterm_id = ids[0]
    except Exception:
        pass

    return incoterm_id


def get_sale_name(sock, uid, sale_id):

    fields = ['name']
    result = sock.execute(DBNAME, uid, PWD, 'sale.order',
                          'read', sale_id, fields)
    return result


def search_cust_id(sock, uid, partner_name):

    cust_id = ''

    args = [('name', 'ilike', partner_name)]
    ids = sock.execute(DBNAME, uid, PWD, 'res.partner', 'search', args)
    try:
        cust_id = ids[0]
    except Exception:
        pass
    return cust_id


def search_channel_id(sock, uid):

    channel_id = False

    args = [('code', '=', 'edi')]
    ids = sock.execute(DBNAME, uid, PWD, 'sale.channel', 'search', args)
    try:
        channel_id = ids[0]
    except Exception:
        pass
    return channel_id


def search_user_id(sock, uid, user_name):

    user_id = ''

    args = [('name', 'ilike', user_name)]
    ids = sock.execute(DBNAME, uid, PWD, 'res.users', 'search', args)
    try:
        user_id = ids[0]
    except Exception:
        pass
    return user_id


def get_shop_location(sock, uid, warehouse_id):

    src_location_id = sock.execute(
        DBNAME,
        uid,
        PWD,
        'stock.warehouse',
        'read',
        warehouse_id,
        ['lot_stock_id'])

    print 'shop stock loc: ' + str(src_location_id)

    return src_location_id


def search_pricelist_id(sock, uid, pricelist):

    pricelist_id = ''

    args = [('name', '=', pricelist_id)]
    ids = sock.execute(DBNAME, uid, PWD, 'product.pricelist', 'search', args)
    try:
        pricelist_id = ids[0]
    except Exception:
        pass
    return pricelist_id


def rename_picking_pol(picking_policy):

    pick_pol = 'one'
    if (picking_policy == 'Deliver each product when available'):
        pick_pol = 'direct'
    return pick_pol


def rename_order_pol(order_policy):
    order_pol = ''
    order_pol_1 = ['manual', 'picking', 'prepaid']
    order_pol_2 = ['On Demand', 'On Delivery Order', 'Before Delivery']
    i = 0
    for pol in order_pol_2:
        if order_policy == pol:
            order_pol = order_pol_1[i]
            break
        i += 1
    if order_pol:
        return order_pol
    else:
        print "FAILURE - ORDER POLICY MUST BE: On Demand, On Delivery Order," \
              " OR Before Delivery"


def check_po_number(sock, uid, client_order_ref, partner_id):

    result = False
    # If PO number is found in EDI
    if client_order_ref:

        sale_ids = sock.execute(DBNAME,
                                uid,
                                PWD,
                                'sale.order',
                                'search',
                                [('partner_id',
                                  '=',
                                  partner_id),
                                 ('state',
                                    '!=',
                                    'cancel'),
                                    ('client_order_ref',
                                     '=',
                                     client_order_ref)])

        # if sale_ids from the above search, then po number is duplicated, warn
        # user, and do not input the sale order
        if sale_ids:
            print "This is a duplicate PO and will not be pushed into the" \
                  " system."
            result = True

    return result


def create_sale_order(
        sock,
        uid,
        date,
        po_num,
        partner_id,
        partner_invoice_id,
        partner_shipping_id,
        third_party,
        address1,
        address2,
        city,
        state,
        zip,
        country,
        ship_to_code,
        trading_partner_id,
        ack_bool,
        automatic_workflow_id):

    partner_info = get_partner_info(sock, uid, partner_id)

    user_id = False
    if partner_info['user_id']:
        user_id = partner_info['user_id'][0]

    pricelist_id = False
    if partner_info['property_product_pricelist']:
        pricelist_id = partner_info['property_product_pricelist'][0]

    src_location_id = ''

    # based on partner's billing address, look up in partner record to find
    # billing contact
    if partner_id:

        if get_billing_partner(sock, uid, partner_id):
            partner_invoice_id = get_billing_partner(sock, uid, partner_id)

    # based on ship_to_code, look up in partner record to find shipping contact
    if ship_to_code:

        if get_shipping_partner(sock, uid, partner_id, ship_to_code):
            partner_shipping_id = get_shipping_partner(
                sock, uid, partner_id, ship_to_code)
    sale_hash = {
        'incoterm': 14,  # hardcoded to "Delivery at Place"
        'date_order': date,
        'client_order_ref': po_num,
        'origin': '',
        'note': '',
        'user_id': user_id,
        'partner_id': partner_id,
        # 'carrier_id': carrier_id,
        'pricelist_id': pricelist_id,
        # 'payment_term': payment_term,
        'company_id': 1,
        'order_policy': 'picking',  # hardcoded to "On Delivery"
        'partner_invoice_id': partner_invoice_id,
        'partner_shipping_id': partner_shipping_id,
        'edi_yes': 'TRUE',
        'ack_yes': ack_bool,
        'ack_sent': 'FALSE',
        'ship_to_code': ship_to_code,
        'trading_partner_id': trading_partner_id,
        'auto_workflow': automatic_workflow_id[0],
        'edi_est_so_ship_date': datetime.now().strftime('%Y-%m-%d')
    }

    print "Attempting to create %s" % sale_hash
    sale_id = sock.execute(DBNAME, uid, PWD, 'sale.order', 'create', sale_hash)
    return sale_id, src_location_id, pricelist_id


def search_product(sock, uid, product_upc, product_sku):

    args = [('default_code', '=', product_sku)]
    ids = sock.execute(DBNAME, uid, PWD, 'product.product', 'search', args)
    try:
        product_id = ids[0]
    except Exception:
        product_id = 'no_exist'
        print 'product does not exist'

    return product_id


def get_product(sock, uid, product_id):

    fields = ['available_sale', 'uom_id',
              'weight', 'standard_price', 'default_code']
    record = sock.execute(
        DBNAME, uid, PWD, 'product.product', 'read', product_id, fields)
    try:
        return record
    except Exception:
        pass


def rename_order_type(order_type):

    order_type_1 = ['from stock', 'on order']
    order_type_2 = ['make_to_stock', 'make_to_order']
    i = 0
    for otype in order_type_1:
        if order_type == otype:
            order_type = order_type_2[i]
            break
        i += 1
    return order_type


def create_so_lines(
        sock,
        uid,
        sale_id,
        product_upcs,
        product_skus,
        product_descs,
        qtys,
        uoms,
        prices,
        src_location_id,
        ack_bool,
        po_lines,
        config_rec,
        pricelist_id):

    sale_line_ids = []
    p_ids = []
    products_not_found = ''

    product_codes = product_upcs
    if product_skus:
        product_codes = product_skus

    for x in xrange(len(product_codes)):

        qty = qtys[x]
        uom = uoms[x]
        # price = prices[x]
        uom_id = search_uom(sock, uid, uom)
        product_code = product_codes[x]
        product_sku = product_skus[x]
        product_upc = product_upcs[x]
        po_line = po_lines[x]
        p_id = search_product(sock, uid, product_upc, product_sku)
        partner_id = config_rec['trading_partner_id'][0]

        if p_id is not 'no_exist':

            price = sock.execute(
                DBNAME,
                uid,
                PWD,
                'product.pricelist',
                'price_get_wrapper',
                pricelist_id,
                p_id,
                qty,
                partner_id)
            product_info = get_product(sock, uid, p_id)
            uom_id = product_info['uom_id']
            weight = product_info['weight']
            p_ids.append(p_id)

            order_hash = {
                'name': product_info['default_code'],
                'edi_line_num': po_line,
                'product_uos_qty': int(qty),
                'product_uom_qty': int(qty),
                'edi_line_qty': int(qty),
                'state': 'draft',
                'order_id': sale_id,  # from sale order we just created
                'invoiced': False,
                'th_weight': weight,  # lookup from product
                'product_id': p_id,
                'edi_yes': 'TRUE',
                'ack_yes': ack_bool,
                'price_unit': price,  # passed in from PO
                # lookup from product
                'purchase_price': product_info['standard_price'],
                'product_uom': uom_id[0],  # lookup from product
            }

            try:
                line_id = sock.execute(
                    DBNAME, uid, PWD, 'sale.order.line', 'create', order_hash)
                sale_line_ids.append(line_id)

            except Exception:
                print "Could not add the order line", sys.exc_info()[0]

        else:

            print "INFO: ***** FAILURE TO FIND PRODUCT WITH UPC CODE: " + \
                str(product_code)
            products_not_found = products_not_found + '\n Line not input: ' + \
                qty + ' ' + uom + ' of ' + product_code

        if products_not_found:
            sock.execute(DBNAME, uid, PWD, 'sale.order', 'write',
                         sale_id, {'edi_error': products_not_found})

    return p_ids, sale_line_ids


def process_record(sock, uid, record, partner_rec, config_rec):

    ack_bool = config_rec['ack_855']

    # We're using fullfillment_channel to store Sale Automatic Workflow ID per
    # customer, this is attached to the order
    print "Automatic workflow is: " + str(config_rec['auto_workflow'])
    automatic_workflow_id = config_rec['auto_workflow']
    # use the 850 PO info to create a sales order
    sale_id, src_location_id, pricelist_id =\
        create_sale_order(sock, uid,
                          record['date'],
                          record['po_num'],
                          record['partner_id'],
                          record['partner_invoice_id'],
                          record['partner_shipping_id'],
                          record['third_party'],
                          record['address1'],
                          record['address2'],
                          record['city'],
                          record['state'],
                          record['zip'],
                          record['country'],
                          record['ship_to_code'],
                          config_rec['id'],
                          ack_bool,
                          automatic_workflow_id)

    # get the sale name from the order you just created
    sale_name = get_sale_name(sock, uid, sale_id)

    # create SO LINE from dictionary we just created
    product_ids, sale_line_ids =\
        create_so_lines(sock, uid, sale_id,
                        record['upc'],
                        record['sku'],
                        record['product_desc'],
                        record['product_qty'],
                        record['product_uom'],
                        record['price_unit'],
                        src_location_id,
                        ack_bool,
                        record['po_line'],
                        config_rec,
                        pricelist_id)

    return sale_id, sale_name, product_ids


def main(sock, uid, order_dict, in_path):

    sale_id = False
    company_id = False

    if not company_id:
        company_id = get_current_company(sock, uid)

    # get edi_config_id from company record
    edi_id = edi_config_id(sock, uid, company_id,
                           order_dict['partner'], order_dict['vendor'])
    # print 'EDI: ' + str(edi_id)

    # get configuration settings from trading_partner

    if edi_id:

        config = get_config(sock, uid, edi_id)

        # get edi trading partner info
        partner_rec = get_partner_info(
            sock, uid, config['trading_partner_id'][0])
        order_dict['partner_id'] = partner_rec['id']
        order_dict['partner_invoice_id'] = partner_rec['id']
        order_dict['partner_shipping_id'] = partner_rec['id']

        # process record and input sale order with multiple order lines in
        # OpenERP

        print "Processing PO#: " + str(order_dict['po_num'])
        if not check_po_number(
                sock,
                uid,
                order_dict['po_num'],
                order_dict['partner_id']):

            try:
                sale_id, sale_name, product_ids = process_record(
                    sock, uid, order_dict, partner_rec, config)

            except Exception:
                print "Cannot process order.  Sale order or order lines not" \
                      " created. ", sys.exc_info()

            print "Sale added id: " + str(sale_id)
    else:
        print 'There is no trading partner that matches the partner header' \
              ' string in the 850 file.'
        print 'Please verify that there are trading partners defined and that' \
              ' the header strings are correctly defined on them.'

    return sale_id


if __name__ == '__main__':
    print 'Process: EDI In - Starting'
    main()
    print 'Process: EDI In - Ending'
