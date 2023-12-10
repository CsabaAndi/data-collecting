# data-collecting


## Összefoglaló

Jelmondat : A csigák csúsznak csak mint a szakdolgozat.

A program lényege : [SOCCERWAY](https://us.soccerway.com) oldalon található adatok kigyüjtése. 
Akár 1901/1902-es szezonig visszamenőleg.


Leszedésre kerülő adatok (more info : [data-plan.md](./data-plan/data-plan.md)) :

Competitions (E.g. England - Premier League): <br>


| Táblázat/Statisztika | Jelenlegi Állapot | 
|--------------|-----------|
| League Table (Team name + Last-5-matches) |[implemented]|
| Wide Table |[implemented]|
| Topscorers (top 15 for now) Table | [implemented]|
| Over/Under Table | [implemented]|


Team specific data (E.g. Arsenal):

| Táblázat/Statisztika | Jelenlegi Állapot | 
|--------------|-----------|
| Match History | [90% done - not uploaded for the moment] |
| newest season competition general statistic Table | [75% done - not uploaded for the moment] |
| newest season competition scoring minutes charts | [75% done - not uploaded for the moment] |


Végső cél : Teljes autoamtizálás és napi szinten legfrissebb adatok gyüjtése (szakdolgozat szempontjából nem fontos)

Jelenlegi Állapot : felsorolt adatok/táblázatok jelenleg félig-automatizálva leszedhetőek 

Az adatleszedés jelenleg másodpercekben mérhető 

## own modules/packages 
(currently it's working but the whole file structure / import structure is a mess)

constans_pkg: constans változók E.g Links / Folder paths <br>
debug_pkg (logs):  logger for debugging + context manager for runtime measuring <br>
resource_blocking_pgk : 
   - browser page : image, fonts, ads, tracking, request, google, facebook -  blocks useless, resource/time consuming data


## Requirements : 

Python - 3.12.0 (not tested on lower versions)

Playwright : 

   - pip install --upgrade pip
   - pip install playwright
   - playwright install chromium

Beautiful Soup :

   - pip install beautifulsoup4


Pandas :

   - pip install pandas


tabulate :

   - pip install tabulate


## Debug : 

first run --> after the first run let the browser load the extensions then rerun the program

page wont load some elements or waits for something forever --> rerun the program (probably some chaching problem with cookies [WIP] )


## Todo

Important : 

   - automatize scraper to download fresh data daily (szakdolgozat szempontjából nem fontos)
   - scrape data for Thesis database [WIP]

Not important : 

   - arguments for debug (argparse)
   - moving code parts to modules/packages
   - clean code [Szakdolgozat szempontjából nem fontos]
   


## preview for one of the data [wide table form of league statistic] 

example : England - Premier League | Week 15 - Total

T - Total <br/>
H - Home <br/>
A - Against <br/>

|Column name|Meaning|
|--------------|-----------|
| MP: | Matches Played |
| D: | Draw |
| L: | Lost |
| GF: | Goals For |
| GA: | Goals Against |
| GD: | Goal Difference |
| p: | Points |

<br/>

|   index | team            |   MP-T |   W-T |   D-T |   L-T |   GF-T |   GA-T |   MP-H |   W-H |   D-H |   L-H |   GF-H |   GA-H |   MP-A |   W-A |   D-A |   L-A |   GF-A |   GA-A |   GD |   P |
|--------:|:----------------|-------:|------:|------:|------:|-------:|-------:|-------:|------:|------:|------:|-------:|-------:|-------:|------:|------:|------:|-------:|-------:|-----:|----:|
|       1 | Arsenal         |     15 |    11 |     3 |     1 |     33 |     14 |      8 |     6 |     2 |     0 |     20 |      8 |      7 |     5 |     1 |     1 |     13 |      6 |  +19 |  36 |
|       2 | Liverpool       |     15 |    10 |     4 |     1 |     34 |     14 |      7 |     7 |     0 |     0 |     21 |      5 |      8 |     3 |     4 |     1 |     13 |      9 |  +20 |  34 |
|       3 | Aston Villa     |     15 |    10 |     2 |     3 |     34 |     20 |      7 |     7 |     0 |     0 |     24 |      5 |      8 |     3 |     2 |     3 |     10 |     15 |  +14 |  32 |
|       4 | Manchester City |     15 |     9 |     3 |     3 |     36 |     17 |      7 |     5 |     2 |     0 |     20 |      7 |      8 |     4 |     1 |     3 |     16 |     10 |  +19 |  30 |
|       5 | Tottenham H…    |     14 |     8 |     3 |     3 |     28 |     20 |      6 |     4 |     0 |     2 |     10 |      8 |      8 |     4 |     3 |     1 |     18 |     12 |   +8 |  27 |
|       6 | Manchester …    |     15 |     9 |     0 |     6 |     18 |     18 |      8 |     5 |     0 |     3 |     10 |     11 |      7 |     4 |     0 |     3 |      8 |      7 |   +0 |  27 |
|       7 | Newcastle U…    |     14 |     8 |     2 |     4 |     32 |     14 |      8 |     7 |     0 |     1 |     19 |      4 |      6 |     1 |     2 |     3 |     13 |     10 |  +18 |  26 |
|       8 | Brighton & …    |     15 |     7 |     4 |     4 |     32 |     27 |      8 |     4 |     3 |     1 |     17 |     11 |      7 |     3 |     1 |     3 |     15 |     16 |   +5 |  25 |
|       9 | West Ham United |     14 |     6 |     3 |     5 |     24 |     24 |      7 |     3 |     2 |     2 |     12 |     10 |      7 |     3 |     1 |     3 |     12 |     14 |   +0 |  21 |
|      10 | Chelsea         |     15 |     5 |     4 |     6 |     26 |     24 |      8 |     2 |     3 |     3 |     13 |     13 |      7 |     3 |     1 |     3 |     13 |     11 |   +2 |  19 |
|      11 | Brentford       |     15 |     5 |     4 |     6 |     23 |     21 |      8 |     3 |     3 |     2 |     15 |     12 |      7 |     2 |     1 |     4 |      8 |      9 |   +2 |  19 |
|      12 | Fulham          |     15 |     5 |     3 |     7 |     21 |     26 |      7 |     4 |     0 |     3 |     12 |      9 |      8 |     1 |     3 |     4 |      9 |     17 |   -5 |  18 |
|      13 | Wolverhampt…    |     15 |     5 |     3 |     7 |     20 |     25 |      7 |     3 |     2 |     2 |     10 |     12 |      8 |     2 |     1 |     5 |     10 |     13 |   -5 |  18 |
|      14 | Crystal Palace  |     15 |     4 |     4 |     7 |     14 |     21 |      7 |     1 |     2 |     4 |      6 |     10 |      8 |     3 |     2 |     3 |      8 |     11 |   -7 |  16 |
|      15 | AFC Bournemouth |     15 |     4 |     4 |     7 |     18 |     30 |      8 |     2 |     3 |     3 |      8 |     12 |      7 |     2 |     1 |     4 |     10 |     18 |  -12 |  16 |
|      16 | Nottingham …    |     15 |     3 |     4 |     8 |     16 |     27 |      7 |     2 |     3 |     2 |     10 |      9 |      8 |     1 |     1 |     6 |      6 |     18 |  -11 |  13 |
|      17 | Luton Town      |     15 |     2 |     3 |    10 |     16 |     30 |      7 |     1 |     2 |     4 |      9 |     12 |      8 |     1 |     1 |     6 |      7 |     18 |  -14 |   9 |
|      18 | Everton         |     14 |     5 |     2 |     7 |     15 |     20 |      7 |     1 |     1 |     5 |      5 |      9 |      7 |     4 |     1 |     2 |     10 |     11 |   -5 |   7 |
|      19 | Burnley         |     15 |     2 |     1 |    12 |     15 |     33 |      8 |     1 |     0 |     7 |     10 |     20 |      7 |     1 |     1 |     5 |      5 |     13 |  -18 |   7 |
|      20 | Sheffield U…    |     15 |     1 |     2 |    12 |     11 |     41 |      8 |     1 |     1 |     6 |      7 |     21 |      7 |     0 |     1 |     6 |      4 |     20 |  -30 |   5 |