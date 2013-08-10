# Copyright (c) Aaron Gallagher <_@habnab.it>
# See COPYING for details.

from ykpers import YubiKey

yk = YubiKey.open_first_key()
print 'yubikey {0.versionMajor}.{0.versionMinor}'.format(yk.get_status())
print 'slot 1:', yk.hmac_challenge_response('hi').encode('hex')
print 'slot 2:', yk.hmac_challenge_response('hi', slot=2).encode('hex')
