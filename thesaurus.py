# myfile = open('thesaurus.txt')
# reader = myfile.readlines()
# reader = filter(lambda x: x[0] not in map(lambda x: str(x), range(10)),reader)
# reader = filter(lambda x: x[0]!='=', reader)
# reader = map(lambda x: x.replace('\r', ''), reader)
# reader = map(lambda x: x.strip(), reader)
# reader = filter(lambda x: x!='',reader)


# deflines = []
# for i,each in enumerate(reader):
#     try:
#         if each.split()[1] in ['v.', 'adj.', 'n.']:
#             deflines.append(i)
#     except:
#         continue

# thesaurus = []
# for each in range(len(deflines)-1):
#     thesaurus.append(''.join(reader[deflines[each]:deflines[each+1]]))

# print thesaurus

# for each in thesaurus[1:2]:
#     split = each.split('--')
#     temp = []
#     for each in split:
#         temp.append(''.join(each).split(':')[0])
#     split = temp

#     if len(each)>1:
#         pass
#         #do stuff

#     print split[0]
#     print {each.split()[0]:{each.split()[1]:each.split(',')[1:]}}




import spotipy

spotify = spotipy.Spotify()

print spotify.search(q='song:'+'stairway to heaven'+' artist:'+'led zeppelin', type = 'track')['tracks']['items'][0]['id']
