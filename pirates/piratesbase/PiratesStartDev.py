from direct.directnotify.DirectNotifyGlobal import directNotify
import __builtin__

notify = directNotify.newCategory('AIBase')

try:
    import wx
except:
    notify.warning('Failed to start injector - wx module missing!')
else:
    try:
        import psutil
    except:
        notify.warning('Failed to start injector - psutil module missing!')
    else:
        from otp.otpbase.OTPInjectorDev import Injector

        notify.info('Starting injector...')
        __builtin__.injector = Injector()

import PiratesStart