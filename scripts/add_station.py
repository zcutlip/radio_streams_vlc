#! /snap/bin/pypy3
'''`add_station` adds an Internet radio station to the CSV database used by
`radio_streams_vlc`.'''
import csv

CSV_DB = 'stations_test.csv'
COMMA = f'\x1b[1;31m,\x1b[0m'
CYAN = f'\x1b[1;36m'
END = f'\x1b[0m'

print(f'Add radio station data to the CSV database (no commas):')
station_name = input(f'{CYAN}Enter name:{END} ')
station_genre = input(f'{CYAN}Enter genre:{END} ')
station_url = input(f'{CYAN}Enter URL:{END} ')

'''
with open(CSV_DB, 'a') as _file:
    _file.write(f'{station_name},{station_genre},{station_url}')
'''

print(f'Appended to {CYAN}{CSV_DB}{END}:')
print(f'{station_name}{COMMA}{station_genre}{COMMA}{station_url}')
