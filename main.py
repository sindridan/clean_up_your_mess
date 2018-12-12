#main function

import os, re, PTN

def sort_Unordered(Unordered):
    movies = []
    tvShows = []
    unknown = []
    for tup in Unordered:
        info = tup[0]
        #print(info)
        if 'episode' in info and 'season' not in info: #Default to Season 01
            season = "S01"
            episode = "E"+str(info['episode'])
            title = info['title'].lower()
            tvShows.append((title, season, episode, tup[1]))
        elif 'season' and 'episode' in info:
            season = "S"+ str(info['season'])
            episode = "E"+str(info['episode'])
            title = info['title'].lower()
            tvShows.append((title, season, episode, tup[1]))
        #Should have covered most of the tv-shows excluding oddly named ones
        elif 'year' in info: 
            title = info['title'].lower()
            movies.append((title, tup[1]))
        else: #these files require further checking, for now we put them into unknowns
            unknown.append(tup)

    return tvShows, movies, unknown




def get_valid_file_types(Directory):
    #all valid video file types
    valid_type =  ["m4v", "flv", "mpeg", "mov", "mpg","mpe", "wmv", "MOV", "mp4"] 
    Unsorted = []
    fileCounter = 0
    for dirName, subDirList, fileList in os.walk(Directory): #Walks the given directory and any subdirectory/ies
        for fName in fileList:
            if fName.split('.')[-1] in valid_type: #only check if the file ends in a file-format we're looking for
                fileCounter += 1 #counter to make sure we're listing every file we check
                info = PTN.parse(fName) #extract all available information from filename via Parse-Torrent-Name library
                path = os.path.join(dirName, fName)
                Unsorted.append((info, path))
    tvShows, movies, unknown = sort_Unordered(Unsorted)
    #make sure we've sorted every single file applicable to the valid typing
    listSum = len(tvShows) + len(unknown) + len(movies)
    if fileCounter == listSum:
        pass
    else:
        print("We're missing some files captain")
        return
    '''Other = [] #list of items we could not sort, sort into it's own folder and must be dealt with manually
    for item in Unsorted:
        if re.fullmatch(r'\d\d\d', item[0]['title'].split(' ')[-1]):
            tmp = item[0]['title'].split(' ')
            title = ' '.join(tmp[0:len(tmp)-1]).lower()
            season = "S0"+ tmp[-1][0]
            Episode = "E"+ tmp[-1][1:]
            tvShows.append((title, season, Episode, item[1]))
            Unsorted.remove(item) #not sure this currently does anything?
        else:
            #TODO find title and serie in directory path?
            #Set default season 01 if only r'E\d\d' in filename
            #further filtering
            Other.append(item)'''
    Unsorted.clear() #empty unsorted as we have no need for it further
    #print(movies)
    #print(tvShows)
    print(unknown)
    return None

get_valid_file_types("downloads")

def main_func(s):
    return None


