# -*- coding: utf-8 -*-
# Copyright (c) Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import csv
import itertools

CSV_PATH = '/tmp/csv_import/'
OUT_PATH = '/tmp/csv_export/'


def parse_csv(file):
    # CSV COLUMNS
    cols = [
        'partner',
        'po_num',
        'date',
        'ship_to_code',
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
        'cancel_after'
    ]

    csv_obj = open(CSV_PATH + file, 'rb')
    data = csv.reader(csv_obj, delimiter=',')
    count = 1
    record = {}
    record['sku'] = []
    record['upc'] = []

    for col in itertools.islice(cols, 6, 9):
        record[col] = []

    for row in data:

        if count == 1 and row[0] != 'H':
            print """INFO: ***** FAILURE - YOUR FILE DOES NOT HAVE THE REQUIRED
             FIRST ROW WITH COLUMN HEADINGS:
              EDI Loop  | Order line | Partner | PO # | Date/UPC |
              code?/product desc | quantity | UOM	Price *****
              """
            break

        if count > 2 and row[0] == '':
            # sale_id, sale_name = process_record(sock, uid, record)
            break

        if row[0] == 'H':

            if record['sku']:

                sale_id, sale_name = process_record(sock, uid, record)
                record['sku'] = []
                record['upc'] = []

                for col in itertools.islice(cols, 6, 9):
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
            for col in itertools.islice(cols, 10, 16):
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

            # get sale line data: sku, asin, product description, quantity,
            # uom, price
            i = 6
            for col in itertools.islice(cols, 6, 9):
                record[col].append(row[i])
                i += 1

        count += 1

    sale_id, sale_name = process_record(sock, uid, record)

    csv_obj.close()
