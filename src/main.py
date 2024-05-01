from debug_pkg.logs import log as debuglog
import browser

def main(lgs=1):
    browser.main(lgs)

    
if __name__ == "__main__":
  with debuglog.timed():
    main(11)