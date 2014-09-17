import unittest
import sys
from ecdsa.util import number_to_string

from ..bitcoin import (
    generator_secp256k1, point_to_ser, public_key_to_bc_address, EC_KEY,
    bip32_root, bip32_public_derivation, bip32_private_derivation, pw_encode,
    pw_decode, Hash, public_key_from_private_key, address_from_private_key,
    is_valid, is_private_key, xpub_from_xprv)

try:
    import ecdsa
except ImportError:
    sys.exit("Error: python-ecdsa does not seem to be installed. Try 'sudo pip install ecdsa'")


class Test_bitcoin(unittest.TestCase):

    def test_crypto(self):
        for message in ["Chancellor on brink of second bailout for banks", chr(255)*512]:
            self._do_test_crypto(message)

    def _do_test_crypto(self, message):
        G = generator_secp256k1
        _r = G.order()
        pvk = ecdsa.util.randrange(pow(2, 256)) %_r

        Pub = pvk*G
        pubkey_c = point_to_ser(Pub, True)
        #pubkey_u = point_to_ser(Pub,False)
        addr_c = public_key_to_bc_address(pubkey_c)
        #addr_u = public_key_to_bc_address(pubkey_u)

        #print "Private key            ", '%064x'%pvk
        eck = EC_KEY(number_to_string(pvk, _r))

        #print "Compressed public key  ", pubkey_c.encode('hex')
        enc = EC_KEY.encrypt_message(message, pubkey_c)
        dec = eck.decrypt_message(enc)
        assert dec == message

        #print "Uncompressed public key", pubkey_u.encode('hex')
        #enc2 = EC_KEY.encrypt_message(message, pubkey_u)
        dec2 = eck.decrypt_message(enc)
        assert dec2 == message

        signature = eck.sign_message(message, True, addr_c)
        #print signature
        EC_KEY.verify_message(addr_c, signature, message)

    def test_bip32(self):
        # see https://en.bitcoin.it/wiki/BIP_0032_TestVectors
        xpub, xprv = self._do_test_bip32("000102030405060708090a0b0c0d0e0f", "m/0'/1/2'/2/1000000000", testnet=False)
        assert xpub == "xpub6G57jZrwk73raTVL6vAFwbv2pV2TwNuBodmQfB6MpxYfwNJ9V8cQ3SC7ujwahk413MmFb6yXPzQq34vkeJ2tNwb2v6bfEu6kZnEd7Zksjrh"
        assert xprv == "xprvA35mL4L3ujVZMyQrztdFaTyJGTByXvBLSQqorngkGd1h4ZxzwbJ9Vdse4UHoYsWGdoe6cMJQNDbka6cxrbPnhzoh89FCCfLQA6ejFDpQubQ"

        xpub, xprv = self._do_test_bip32("fffcf9f6f3f0edeae7e4e1dedbd8d5d2cfccc9c6c3c0bdbab7b4b1aeaba8a5a29f9c999693908d8a8784817e7b7875726f6c696663605d5a5754514e4b484542",
                                         "m/0/2147483647'/1/2147483646'/2", testnet=False)
        assert xpub == "xpub6GesmaqrUhnzgqk5wxBBH8NhV5qMXbb7969ThVyh2BKPBzSZJix1dyFN6eJTW5gpWrFyXyNvMsawmJVrB4xpBvJWybUcuVC97AhqZehEcJb"
        assert xprv == "xprvA3fXN5JxeLEhUMfcqveAuzRxw3zs88sFmsDru7a5TqnQKC7QmBdm6AvtFN17RVwoFt354TTaNy7ZQodWSzffzXmcJxYc41pxqCDK7Cryi7r"

    def test_bip32_testnet(self):
        xpub, xprv = self._do_test_bip32("000102030405060708090a0b0c0d0e0f", "m/0'/1/2'/2/1000000000", testnet=True)
        assert xpub == "tpubDGSkFogdTP1JrFgBZ79M9XFQ9c87vmQFMGMi1j9WAsJZgexrZMTVBsrx9n2NEF1EqGJACgVPw6EsjFRN39t8GP3KyhLxvRkz9jq2seaqhyE"
        assert xprv == "tprv8jki7PePK1KdxnePfTUkk7bHaacBmSDLmxkvjD7CkbWArAi5vxdu1PF5yeTTZEtb1FAscSvAXaBZ2xAhyojjX45HenTVs24T5CQ9gsWp48F"

        xpub, xprv = self._do_test_bip32("fffcf9f6f3f0edeae7e4e1dedbd8d5d2cfccc9c6c3c0bdbab7b4b1aeaba8a5a29f9c999693908d8a8784817e7b7875726f6c696663605d5a5754514e4b484542",
                                         "m/0/2147483647'/1/2147483646'/2", testnet=True)
        assert xpub == "tpubDH2WHpfYBykSxdvwQ9AGV3i4pCw1Wz6Agijm442qN65GwH7GNwo6nQvCLgPF2ae4Jknt9YtntyQzTUzTZvp45Mkp3CDvb1rNh8JFKg19W1E"
        assert xprv == "tprv8kLU9QdJ3c4n5Au9WVVg5e3xFBR5MeuG7R8ymXzXwpGt6nrVkYyWbvJLAYAmRsL7dKZr4Z5LYKhMsfBFaD1cob3CqbkuiNZ1kHxjYwwjePJ"

    def _do_test_bip32(self, seed, sequence, testnet):
        xprv, xpub = bip32_root(seed.decode('hex'), testnet)
        assert sequence[0:2] == "m/"
        path = 'm'
        sequence = sequence[2:]
        for n in sequence.split('/'):
            child_path = path + '/' + n
            if n[-1] != "'":
                xpub2 = bip32_public_derivation(xpub, path, child_path, testnet)
            xprv, xpub = bip32_private_derivation(xprv, path, child_path, testnet)
            if n[-1] != "'":
                assert xpub == xpub2
            path = child_path

        return xpub, xprv

    def test_aes_homomorphic(self):
        """Make sure AES is homomorphic."""
        payload = u'\u66f4\u7a33\u5b9a\u7684\u4ea4\u6613\u5e73\u53f0'
        password = u'secret'
        enc = pw_encode(payload, password)
        dec = pw_decode(enc, password)
        self.assertEqual(dec, payload)

    def test_aes_encode_without_password(self):
        """When not passed a password, pw_encode is noop on the payload."""
        payload = u'\u66f4\u7a33\u5b9a\u7684\u4ea4\u6613\u5e73\u53f0'
        enc = pw_encode(payload, None)
        self.assertEqual(payload, enc)

    def test_aes_deencode_without_password(self):
        """When not passed a password, pw_decode is noop on the payload."""
        payload = u'\u66f4\u7a33\u5b9a\u7684\u4ea4\u6613\u5e73\u53f0'
        enc = pw_decode(payload, None)
        self.assertEqual(payload, enc)

    def test_aes_decode_with_invalid_password(self):
        """pw_decode raises an Exception when supplied an invalid password."""
        payload = u"blah"
        password = u"uber secret"
        wrong_password = u"not the password"
        enc = pw_encode(payload, password)
        self.assertRaises(Exception, pw_decode, enc, wrong_password)

    def test_hash(self):
        """Make sure the Hash function does sha256 twice"""
        payload = u"test"
        expected = '\x95MZI\xfdp\xd9\xb8\xbc\xdb5\xd2R&x)\x95\x7f~\xf7\xfalt\xf8\x84\x19\xbd\xc5\xe8"\t\xf4'

        result = Hash(payload)
        self.assertEqual(expected, result)

    def test_xpub_from_xprv(self):
        """We can derive the xpub key from a xprv."""
        # Taken from test vectors in https://en.bitcoin.it/wiki/BIP_0032_TestVectors
        xpub = "xpub6H1LXWLaKsWFhvm6RVpEL9P4KfRZSW7abD2ttkWP3SSQvnyA8FSVqNTEcYFgJS2UaFcxupHiYkro49S8yGasTvXEYBVPamhGW6cFJodrTHy"
        xprv = "xprvA41z7zogVVwxVSgdKUHDy1SKmdb533PjDz7J6N6mV6uS3ze1ai8FHa8kmHScGpWmj4WggLyQjgPie1rFSruoUihUZREPSL39UNdE3BBDu76"

        result = xpub_from_xprv(xprv)
        self.assertEqual(result, xpub)

    def test_xpub_from_xprv_testnet(self):
        """We can derive the xpub key from a xprv using testnet headers."""
        xpub = "tpubDHNy3kAG39ThyiwwsgoKY4iRenXDRtce8qdCFJZXPMCJg5dsCUHayp84raLTpvyiNA9sXPob5rgqkKvkN8S7MMyXbnEhGJMW64Cf4vFAoaF"
        xprv = "tprv8kgvuL81tmn36Fv9z38j8f4K5m1HGZRjZY2QxnXDy5PuqbP6a5TzoKWCgTcGHBu66W3TgSbAu2yX6sPza5FkHmy564Sh6gmCPUNeUt4yj2x"
        result = xpub_from_xprv(xprv, testnet=True)
        self.assertEqual(result, xpub)


class Test_keyImport(unittest.TestCase):
    """ The keys used in this class are TEST keys from
        https://en.bitcoin.it/wiki/BIP_0032_TestVectors"""

    private_key = "UyCikgbdBb36n5EZLCW4sxea5jX3ByPCaVRGn8kiBNsg3LTAoQUG"
    public_key_hex = "020826026689880c7bfcdb56a96b166cb9cf6241662b371ff9110b99f92b59239f"
    main_address = "RqAahY1pTk1q417ALF4ScYGLWthphAGaHW"

    def test_public_key_from_private_key(self):
        result = public_key_from_private_key(self.private_key)
        self.assertEqual(self.public_key_hex, result)

    def test_address_from_private_key(self):
        result = address_from_private_key(self.private_key)
        self.assertEqual(self.main_address, result)

    def test_is_valid_address(self):
        self.assertTrue(is_valid(self.main_address))
        self.assertFalse(is_valid("not an address"))

    def test_is_private_key(self):
        self.assertTrue(is_private_key(self.private_key))
        self.assertFalse(is_private_key(self.public_key_hex))
