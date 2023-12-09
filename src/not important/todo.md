''' TODO / not important /
parser = argparse.ArgumentParser()
parser.add_argument( '-log',
                     '--loglevel',
                     default='warning',
                     help='Provide logging level. Example --loglevel debug, default=warning. Use debug for more info')

args = parser.parse_args()
levels = {
    'critical': logging.CRITICAL,
    'error': logging.ERROR,
    'warn': logging.WARNING,
    'warning': logging.WARNING,
    'info': logging.INFO,
    'debug': logging.DEBUG
}
# args.loglevel.upper  --> -log "debug"
# levels[args.loglevel.upper()]
'''
'''
# majd külön pkg
logger = logging.getLogger(__name__)
FORMAT = "[%(asctime)s %(filename)s->%(funcName)s():%(lineno)s] %(levelname)s: %(message)s" 
logging.basicConfig(format=FORMAT, level=logging.INFO)
logging.info( 'Logging now setup.' )
'''