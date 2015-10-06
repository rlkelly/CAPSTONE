import sys
from pyechonest import song
from pyechonest import config

config.ECHO_NEST_API_KEY="2PSC0QWFJLYNM4XA6"

song_ids = ['SOBSLVH12A8C131F38', 'SOXMSGY1338A5D5873', 'SOJPHZO1376210AFE5', 'SOBHNKR12AB0186218', 'SOSJAHD13770F4D40C']

rowlst = []
import time
counter = 0

while counter < 9899:
   if counter %9 == 0:
       time.sleep(6)
   song_id = list(song_analysis_df['track_id'])[counter*10:counter*10+10]
   songlst = song.profile(song_ids, buckets=['audio_summary'])
   rows = map(lambda x: x.audio_summary.values(), songlst)
   rowlst.extend(rows)
   counter+=1
   print counter
   