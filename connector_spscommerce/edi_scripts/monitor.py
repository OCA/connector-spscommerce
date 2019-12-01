#!/usr/bin/python
# Copyright (c) Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import ftplib
import logging
import os
import re
import shutil
import time

HOST = ''  # IP Address
PORT = 22
UNAME = ''
PW = ''

SOURCE_DIR = '/out/'
DEST_DIR = '/in/'
REMOTE_ARCHIVE = '/Archive/'
LOCAL_DEST_DIR = '/var/log/_edi/Inbox/'
LOCAL_SOURCE_DIR = '/var/log/_edi/Outbox/'
ARCHIVE = '/var/log/_edi/Archive'

log_path = '/var/log/_edi/Logs'

count = 0

print "Current date & time " + time.strftime("%c")


def ftp_connect(HOST, UNAME, PW):
    ftp = ftplib.FTP(HOST)
    try:
        ftp.login(UNAME, PW)
        logging.info('Successfully connected to the remote site.')

    except Exception:
        logging.error('Error logging into ftp server.')

    return ftp


def process_files(ftp, SOURCE_DIR, LOCAL_SOURCE_DIR, DEST_DIR, LOCAL_DEST_DIR):
    in_data = []
    out_data = []
    in_file_list = []
    out_file_list = []

    ftp.dir(SOURCE_DIR, in_data.append)

    for in_file in in_data:

        file = re.split('\s+', in_file)
        filename = file[len(file) - 1]
        filename.replace(" ", "")

        if filename not in ['.', '..', 'Archive']:
            in_file_list.append(filename)

    out_data = os.listdir(LOCAL_SOURCE_DIR)

    for out_file in out_data:

        file = re.split('\s+', out_file)
        filename = file[len(file) - 1]
        filename.replace(" ", "")

        if filename not in ['.', '..', 'Archive']:
            out_file_list.append(filename)

    logging.info('Found this list of incoming files: %s' % str(in_file_list))
    logging.info('Found this list of outgoing files: %s' % str(out_file_list))

    # Create lists of each file type for outgoing and incoming files
    incoming_files = [fle for fle in in_file_list]
    outgoing_files = [fle for fle in out_file_list]

    get = transfer_files(ftp, incoming_files, SOURCE_DIR,
                         LOCAL_DEST_DIR, 'RETR')

    if get:
        for filename in in_file_list:

            try:
                ftp.rename(SOURCE_DIR + filename, REMOTE_ARCHIVE + filename)
                logging.info('Successfully transfered %s' %
                             filename + 'from remote host')
                print 'Successful Transfer of: ' + filename + \
                      ' from remote host'
            except Exception:
                logging.error(
                    'Failed to archive %s on remote server' % filename)

    send = transfer_files(ftp, outgoing_files,
                          LOCAL_SOURCE_DIR, DEST_DIR, 'STOR')

    if send:
        for filename in out_file_list:

            try:
                shutil.move(LOCAL_SOURCE_DIR + filename, ARCHIVE)
                logging.info('Successfully transfered %s' %
                             filename + 'to remote host')
                print 'Successful Transfer of: ' + filename + ' to remote host'
            except Exception:
                logging.error(
                    'Failed to archive %s on local server' % filename)

    ftp.quit()


def transfer_files(ftp, files, SOURCE_DIR, DEST_DIR, transfer_type):
    res = True

    for filename in files:

        try:

            if transfer_type == 'RETR':
                outfile = open(DEST_DIR + filename, 'w')
                ftp.retrlines('RETR' + ' ' + SOURCE_DIR + filename,
                              lambda s, w=outfile.write: w(s + '\n'))
                outfile.close()
            if transfer_type == 'STOR':
                ftp.cwd(DEST_DIR)
                ftp.storbinary("STOR " + filename,
                               open(SOURCE_DIR + filename, "rb"))

        except Exception:

            res = False
            logging.error('Error transferring ' + filename +
                          ' using transfer type: ' + transfer_type)

    return res


def main():
    ftp = ftp_connect(HOST, UNAME, PW)
    process_files(ftp, SOURCE_DIR, LOCAL_SOURCE_DIR, DEST_DIR, LOCAL_DEST_DIR)


if __name__ == '__main__':
    print 'Starting'
    main()
    print 'Sleeping'
    time.sleep(5)
