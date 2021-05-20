from panda3d.core import Datagram, Thread
from direct.distributed.AstronInternalRepository import msgpack_encode
from direct.distributed.PyDatagram import PyDatagram
from direct.directnotify.DirectNotifyGlobal import directNotify
from threading import Thread
import traceback

class SplunkThreadAI(Thread):
    notify = directNotify.newCategory('SplunkThreadAI')
    
    def run(self):
        while True:
            item = simbase.air.logQueue.get()

            if not simbase.air.analyticsMgr.isReady():
                if simbase.air.eventSocket is not None:
                    dg = PyDatagram()
                    msgpack_encode(dg, item)
                    simbase.air.eventSocket.Send(dg.getMessage())
            else:
                logType = item.pop('type')
                
                try:
                    simbase.air.analyticsMgr.track(logType, item)
                except Exception as e:
                    self.notify.warning('Exception happened while sending log to Splunk:\n%s' % traceback.format_exc())

            simbase.air.logQueue.task_done()