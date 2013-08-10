# Copyright (c) Aaron Gallagher <_@habnab.it>
# See COPYING for details.

"""libykpers bindings for python via cffi."""

from cffi import FFI


ffi = FFI()
ffi.cdef("""

typedef void YK_KEY;

struct status_st {
    unsigned char versionMajor;
    unsigned char versionMinor;
    unsigned char versionBuild;
    unsigned char pgmSeq;
    unsigned short touchLevel;
    ...;
};
typedef struct status_st YK_STATUS;

enum yk_slot {
    SLOT_CHAL_HMAC1, SLOT_CHAL_HMAC2, ...
};

int yk_init(void);
int yk_release(void);
YK_KEY *yk_open_first_key(void);
int yk_close_key(YK_KEY *k);

int yk_get_status(YK_KEY *k, YK_STATUS *status);
int yk_challenge_response(YK_KEY *yk, uint8_t yk_cmd, int may_block,
                          unsigned int challenge_len, const unsigned char *challenge,
                          unsigned int response_len, unsigned char *response);

int yk_errno;
const char *yk_strerror(int);

""")

C = ffi.verify("""

#include "ykpers-1/ykdef.h"
#include "ykpers-1/ykcore.h"

""", libraries=['ykpers-1'])


class YubiKeyError(Exception):
    pass

def _yubi_error_wrap(f, *a, **kw):
    ret = f(*a, **kw)
    if not ret:
        errno = C.yk_errno
        raise YubiKeyError(errno, ffi.string(C.yk_strerror(errno)))
    return ret


_yubi_error_wrap(C.yk_init)

class YubiKey(object):
    """A YubiKey.

    Don't call ``YubiKey()`` directly; instead, use
    ``YubiKey.open_first_key()``.

    """

    @classmethod
    def open_first_key(cls):
        """Open the first YubiKey available."""

        key = _yubi_error_wrap(C.yk_open_first_key)
        inst = cls()
        inst._key = key
        return inst

    def get_status(self):
        """Get the status of this YubiKey.

        Returns a struct with ``versionMajor``, ``versionMinor``,
        ``versionBuild``, ``pgmSeq``, and ``touchLevel`` attributes.

        """

        status = ffi.new('YK_STATUS *')
        _yubi_error_wrap(C.yk_get_status, self._key, status)
        return status[0]

    def hmac_challenge_response(self, challenge, may_block=True, slot=1):
        """Issue an HMAC-SHA1 challenge to the YubiKey.

        ``may_block`` can be set to False to not wait for the YubiKey button to
        be pressed, if it's configured that way. ``slot`` can be either 1 or 2.

        Returns a string of 20 bytes.

        """

        if slot == 1:
            op = C.SLOT_CHAL_HMAC1
        elif slot == 2:
            op = C.SLOT_CHAL_HMAC2
        else:
            raise ValueError('invalid slot', slot)
        response = ffi.new('unsigned char[64]')
        _yubi_error_wrap(
            C.yk_challenge_response, self._key, op, may_block,
            len(challenge), challenge, 64, response)
        return ffi.buffer(response)[:20]
