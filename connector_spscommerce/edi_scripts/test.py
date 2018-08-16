#!/usr/bin/python
# Copyright (c) Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import csv
import itertools
import xmlrpclib
import edi_850
from connect_info import ERP_WWW, DBNAME, USERNAME, PWD, IN_PATH


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

    # CSV COLUMNS
    cols = [
        'partner',
        'po_num',
        'date', 'ship_to_code',
        'sku',
        'upc',
        'product_desc',
        'product_qty',
        'product_uom',
        'price_unit',
        'third_party',
        'address1',
        'address2',
        'city',
        'state',
        'zip',
        'country',
        'billing_contact',
        'billing_address1',
        'billing_address2',
        'billing_city',
        'billing_state',
        'billing_zip',
        'billing_country',
        'ship_not_before',
        'cancel_after',
        'po_line'
    ]

    csv_obj = open(file, 'rb')
    data = csv.reader(csv_obj, delimiter='\t')
    count = 1
    record = {}
    record['sku'] = []
    record['upc'] = []
    record['po_line'] = []

    for col in itertools.islice(cols, 6, 10):
        record[col] = []

    for row in data:

        if count == 1 and row[0] != 'H':

            print "INFO: FAILURE - YOUR FILE DOES NOT HAVE THE REQUIRED FIRST" \
                  " ROW WITH COLUMN HEADINGS:" \
                  " EDI Loop  | Order line | Partner | PO # | Date/UPC |" \
                  " code?/product desc | quantity | UOM	Price *****"
            break

        if count > 2 and row[0] == '':
            # sale_id, sale_name = process_record(sock, uid, record)
            break

        if row[0] == 'H':

            if record['sku']:
                print record
                edi_850.main(sock, uid, record, IN_PATH)
                record['sku'] = []
                record['upc'] = []
                record['po_line'] = []

                for col in itertools.islice(cols, 6, 10):
                    record[col] = []

            record['ship_to_code'] = row[14]
            record['ship_not_before'] = row[31]
            record['cancel_after'] = row[32]

            # get partner, PO#, date
            i = 2
            for col in itertools.islice(cols, 0, 3):
                record[col] = row[i]
                i += 1

            # get thirdparty info
            i = 7
            for col in itertools.islice(cols, 10, 17):
                record[col] = row[i]
                i += 1

            # get billing address info
            i = 15
            for col in itertools.islice(cols, 17, 24):
                record[col] = row[i]
                i += 1

        elif row[0] == 'I':

            record['sku'].append(row[2])
            record['upc'].append(row[4])
            record['po_line'].append(row[1])
            # get sale line data: sku, asin, product description, quantity,
            # uom, price
            i = 5
            for col in itertools.islice(cols, 6, 10):
                record[col].append(row[i])
                i += 1

        count += 1

    status = edi_850.main(sock, uid, record, IN_PATH)

    csv_obj.close()

    return status, record['partner']


def main():
    sock, uid = connect_oerp()
    o_id = 33382
    orders = sock.execute(DBNAME, uid, PWD, 'stock.picking', 'read', o_id)
    print orders


if __name__ == '__main__':
    print 'Process: EDI Orders Read - Starting'
    main()
    print 'Process: EDI Orders Read - Ending'
