# -*- coding: utf-8 -*-
import os
import sys
import logging
from datetime import datetime
from tempfile import gettempdir
from argparse import ArgumentParser

os.chdir(os.path.abspath(os.path.dirname(__file__)))

logging.basicConfig(
    level=logging.INFO, stream=sys.stdout,
    format='%(asctime)s %(levelname)-5.5s [%(name)s] %(message)s')
logging.addLevelName(logging.WARNING, "WARN")
logging.addLevelName(logging.CRITICAL, "FATAL")

# FTP client config
FTP_OPTIONS = {
    'host': 'x.x.x.x',
    'port': 21,  # optional 990 for Implicit TLS over FTP
    'username': 'user1',
    'password': '123456',
    'transfer_mode': 'Passive',  # Passive|Active
    'tls_enable': True,
    'tls_protocol': 'Explicit',  # Explicit|Implicit
    'tls_version': 'Auto',       # Auto|TLSv1_2|TLSv1_3
}

FTP_DIR = "/"
FTP_RETRIES = 2


def main():
    logger = logging.getLogger()
    logger.name = 'main'

    try:
        pr = ArgumentParser(prog=None)
        pr.add_argument(
            '-x', dest='debug', action='count', default=0,
            help='set debug modes')
        pr.add_argument(
            '--shell', dest='shell', action='store_true',
            help="use shell ftp client implementation")
        args = pr.parse_args()

        if args.debug > 0:
            logger.setLevel(logging.DEBUG)

        if args.shell:
            from exonutils.services.ftp_shell import FTPClient
        else:
            from exonutils.services.ftp import FTPClient

        # create FTP client handler
        ftp = FTPClient(FTP_OPTIONS, logger=logger)

        tmpdir = gettempdir()

        # create sample data file
        fname = 'test_%s.txt' % datetime.now().strftime("%Y%m%d%H%M%S")
        fpath = os.path.join(tmpdir, fname)
        with open(fpath, 'w+') as f:
            for i in range(500):
                f.write('Sample data, line: %s\n' % i)

        # upload file
        is_uploaded = ftp.upload(fpath, FTP_DIR, retries=FTP_RETRIES)
        os.unlink(fpath)

        if is_uploaded:
            remote_file = '%s/%s' % (FTP_DIR, fname)
            ftp.download(remote_file, tmpdir, retries=FTP_RETRIES)
            os.unlink(fpath)

    except Exception as e:
        logger.fatal(str(e), exc_info=args.debug)
        sys.exit(1)


if __name__ == '__main__':
    main()
