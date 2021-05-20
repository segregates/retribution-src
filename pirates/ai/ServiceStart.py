from panda3d.core import loadPrcFile, loadPrcFileData
import __builtin__
import argparse
import os
import gc

gc.disable()

parser = argparse.ArgumentParser()
parser.add_argument('--base-channel', help='The base channel that the server may use.')
parser.add_argument('--max-channels', help='The number of channels the server may use.')
parser.add_argument('--stateserver', help="The control channel of this AI's designated State Server.")
parser.add_argument('--district-name', help="What this AI Server's district will be named.")
parser.add_argument('--astron-ip', help="The IP address of the Astron Message Director to connect to.")
parser.add_argument('--eventlogger-ip', help="The IP address of the Astron Event Logger to log to.")
parser.add_argument('--mongodb-ip', help="The IP address of the MongoDB Server to connect to.")
parser.add_argument('--splunk-ip', help='The IP address of the Splunk Server to connect to.')
parser.add_argument('--splunk-token', help='The Splunk token to authenticate to Splunk with.')
parser.add_argument('config', nargs='*', default=['config/general.prc', 'config/dev.prc', 'config/server.prc'], help="PRC file(s) to load.")
args = parser.parse_args()

for prc in args.config:
    loadPrcFile(prc)

localConfig = 'config/%s.prc' % args.district_name

if os.path.isfile(localConfig):
    loadPrcFile(localConfig)

if os.path.isfile('config/local.prc'):
    loadPrcFile('config/local.prc')

localconfig = ''
if args.base_channel: localconfig += 'air-base-channel %s\n' % args.base_channel
if args.max_channels: localconfig += 'air-channel-allocation %s\n' % args.max_channels
if args.stateserver: localconfig += 'air-stateserver %s\n' % args.stateserver
if args.district_name: localconfig += 'district-name %s\n' % args.district_name
if args.astron_ip: localconfig += 'air-connect %s\n' % args.astron_ip
if args.eventlogger_ip: localconfig += 'eventlog-host %s\n' % args.eventlogger_ip
if args.mongodb_ip: localconfig += 'mongodb-url %s\n' % args.mongodb_ip
if args.splunk_ip: localconfig += 'splunk-host %s\n' % args.splunk_ip
if args.splunk_token: localconfig += 'splunk-token %s\n' % args.splunk_token
loadPrcFileData('Command-line', localconfig)

from otp.ai.AIBaseGlobal import *

from pirates.ai.PiratesAIRepository import PiratesAIRepository
simbase.air = PiratesAIRepository(config.GetInt('air-base-channel', 401000000),
                                   config.GetInt('air-stateserver', 1100),
                                   config.GetString('district-name', 'Pirates'))
host = config.GetString('air-connect', '25.91.142.158')
port = 7100
if ':' in host:
    host, port = host.split(':', 1)
    port = int(port)
simbase.air.connect(host, port)

gc.enable()

try:
    run()
except SystemExit:
    raise
except Exception:
    info = describeException()
    simbase.air.writeServerEvent('ai-exception', avId=simbase.air.getAvatarIdFromSender(), accountId=simbase.air.getAccountIdFromSender(), exception=info)
    with open(config.GetString('ai-crash-log-name', 'ai-crash.log'), 'w+') as file:
        # w+ empties log and writes fresh (meaning 1 exception at a time).
        file.write(info + "\n")
    raise
