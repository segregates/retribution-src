from direct.directnotify import DirectNotifyGlobal
#import requests, time, json

class AnalyticsManagerAI:
    notify = DirectNotifyGlobal.directNotify.newCategory('AnalyticsManagerAI')

    def __init__(self):
        self.host = config.GetString('splunk-host', '')
        self.enabled = False
           
        if not self.host:
            self.notify.info('Not using analytics.')
            return

        self.applicationName = config.GetString('splunk-application', 'por-production')
        self.headers = {'Authorization': 'Splunk ' + config.GetString('splunk-token', '')}
        self.host = 'http://' + self.host + '/services/collector/event'
        self.enabled = True
        self.notify.info('Connected to Splunk.')

    def isReady(self):
        return self.enabled

    def track(self, eventName, props={}):
        if not self.enabled:
            return False

        data = json.dumps({
            'time': int(time.time()),
            'source': eventName,
            'sourcetype': self.applicationName,
            'event': props
        })
        
        requests.post(self.host, data=data, headers=self.headers)
        return True