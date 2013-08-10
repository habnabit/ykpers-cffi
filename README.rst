=============
 ykpers-cffi
=============


Extremely small bindings to `libykpers`_ for communicating with a `YubiKey`_
over USB. The features are currently "whatever I need at the time." Feel free
to make suggestions about what to do next. Here's approximately what it can do
at the moment::

  from ykpers import YubiKey

  yk = YubiKey.open_first_key()
  print 'yubikey {0.versionMajor}.{0.versionMinor}'.format(yk.get_status())
  print 'slot 1:', yk.hmac_challenge_response('hi').encode('hex')
  print 'slot 2:', yk.hmac_challenge_response('hi', slot=2).encode('hex')


Why not `python-yubico`_?
=========================

It only runs on linux and reimplements what libykpers already does.


.. _libykpers: https://github.com/Yubico/yubikey-personalization
.. _YubiKey: http://www.yubico.com/
.. _python-yubico: https://github.com/Yubico/python-yubico
