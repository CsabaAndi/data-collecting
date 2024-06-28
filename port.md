# Currently working on a typescript version for performance optimalization: 
- Playwright for NodeJS (Typescript)
- Cheerio
- saving only the html during scraping then processing it later for relevant data,    <br> instead of processing it during scraping (performance / stability)

## [Done]:
- Most of the code has been sucesfully ported
- Program works as intended but currently unusable due to the bugs

## [Bugs]:
- Unable to install playwright for NodeJS on Fedora linux :
   - Fedora linux unsupported
   - The fallback ubuntu version could be installed with pip for playwright for python but npm/yarn/pnmp fails to install the fallback version 
- chromium browser not loading requested resources for soccerway (other browser dont have this problem)
- firefox browser works but add-ons (adblock) aren't supported


## [Env]:
- Currently tested on Desktop Windows 11


## [Possible solutions]:
- testing the chrome browser in a Ubuntu linux vm
- solving the Resource requests blocking and bugs 


