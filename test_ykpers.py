# Copyright (c) Aaron Gallagher <_@habnab.it>
# See COPYING for details.

import struct

import mock  # fuck me, right?
import pytest

import ykpers


@mock.patch('ykpers.C')
def test_get_status(C):
    yk = ykpers.YubiKey.open_first_key()
    def fill_in_status(key, status):
        assert key is C.yk_open_first_key()
        ykpers.ffi.buffer(status)[:] = '123456'
        return 1
    C.yk_get_status = fill_in_status
    status = yk.get_status()
    assert status.versionMajor == ord('1')
    assert status.versionMinor == ord('2')
    assert status.versionBuild == ord('3')
    assert status.pgmSeq == ord('4')
    assert struct.pack('H', status.touchLevel) == '56'


def cstring(s):
    c = ykpers.ffi.new('unsigned char[]', len(s))
    ykpers.ffi.buffer(c)[:] = s
    return c

@mock.patch('ykpers.C')
def test_get_status_error(C):
    yk = ykpers.YubiKey.open_first_key()
    C.yk_errno = 2
    C.yk_strerror.return_value = cstring('error')
    C.yk_get_status.return_value = 0
    with pytest.raises(ykpers.YubiKeyError) as excinfo:
        yk.get_status()
    assert excinfo.value.args == (2, 'error')


@mock.patch('ykpers.C')
def test_hmac_challenge_response(C):
    yk = ykpers.YubiKey.open_first_key()
    def fill_in_response(key, op, may_block, challenge_length, challenge,
                         response_length, response):
        assert key is C.yk_open_first_key()
        assert op is C.SLOT_CHAL_HMAC1
        assert challenge_length == 2
        assert challenge == 'hi'
        ykpers.ffi.buffer(response)[:response_length] = '\1' * response_length
        return 1
    C.yk_challenge_response = fill_in_response
    assert yk.hmac_challenge_response('hi') == '\1' * 20


@mock.patch('ykpers.C')
def test_hmac_challenge_slot_1(C):
    yk = ykpers.YubiKey.open_first_key()
    called = []
    def fill_in_response(key, op, may_block, challenge_length, challenge,
                         response_length, response):
        assert op is C.SLOT_CHAL_HMAC1
        called.append(True)
        return 1
    C.yk_challenge_response = fill_in_response
    yk.hmac_challenge_response('', slot=1)
    assert called


@mock.patch('ykpers.C')
def test_hmac_challenge_slot_2(C):
    yk = ykpers.YubiKey.open_first_key()
    called = []
    def fill_in_response(key, op, may_block, challenge_length, challenge,
                         response_length, response):
        assert op is C.SLOT_CHAL_HMAC2
        called.append(True)
        return 1
    C.yk_challenge_response = fill_in_response
    yk.hmac_challenge_response('', slot=2)
    assert called


@mock.patch('ykpers.C')
def test_hmac_challenge_response_error(C):
    yk = ykpers.YubiKey.open_first_key()
    C.yk_errno = 3
    C.yk_strerror.return_value = cstring('another-error')
    C.yk_challenge_response.return_value = 0
    with pytest.raises(ykpers.YubiKeyError) as excinfo:
        yk.hmac_challenge_response('')
    assert excinfo.value.args == (3, 'another-error')
