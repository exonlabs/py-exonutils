# -*- coding: utf-8 -*-
import time
from argparse import ArgumentParser
from traceback import format_exc
from utils import valid_msg, fail_msg, red_text, print_data

from exonutils.crypto import xcipher


def TestAES128_Encryption() -> bool:
    chk = True

    secret = "123456_secret"
    aes = xcipher.AES128(secret)

    txt_in = "### INPUT TEXT FOR ENCRYPTION ###"
    b_ciphered = aes.encrypt(txt_in.encode("utf8"))

    b_out = aes.decrypt(b_ciphered)
    txt_out = b_out.decode("utf8")

    print(">> input: %s" % print_data(txt_in))
    if txt_in == txt_out:
        print(valid_msg())
    else:
        chk = False
        print(red_text("FAILED check of decrypted message: %s" % txt_out))

    return chk


def TestAES256_Encryption() -> bool:
    chk = True

    secret = "123456_secret"
    aes = xcipher.AES256(secret)

    txt_in = "### INPUT TEXT FOR ENCRYPTION ###"
    b_ciphered = aes.encrypt(txt_in.encode("utf8"))

    b_out = aes.decrypt(b_ciphered)
    txt_out = b_out.decode("utf8")

    print(">> input: %s" % print_data(txt_in))
    if txt_in == txt_out:
        print(valid_msg())
    else:
        chk = False
        print(red_text("FAILED check of decrypted message: %s" % txt_out))

    return chk


def main():
    tests = [
        TestAES128_Encryption,
        TestAES256_Encryption,
    ]

    pr = ArgumentParser(prog=None)
    pr.add_argument(
        "--run", dest="test_case", metavar="TEST_CASE_NAME",
        help="select test case to run")
    args = pr.parse_args()

    if args.test_case:
        for t in tests:
            if t.__name__ == args.test_case:
                tests = [t]
                break
        else:
            print("\nwarning: no tests to run\nPASS\n")
            return

    for t in tests:
        print("\n=== RUN   %s" % t.__name__)
        chk = "FAIL"
        ts = time.time()
        try:
            if t():
                chk = "PASS"
        except Exception:
            print(format_exc().strip() + "\n" + fail_msg())
        ts = (time.time() - ts) * 1000
        print("--- %s: %s (%.3f ms)" % (chk, t.__name__, ts))
        print(chk)

    print()


main()
