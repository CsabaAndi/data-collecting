from debug_pkg.logs import log as debuglog
import browser


def main(debug_slow_down=0, lgs=1):
    browser.main(debug_slow_down, lgs)
 
    
if __name__ == "__main__":
  with debuglog.timed():
    main(0, 11)