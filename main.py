#main function

import os, re, PTN

def filterFiles(Unordered):
    movies = []
    tvShows = []
    unknown = []
    for tup in Unordered:
        info = tup[0]
        #Missing season in info
        if 'episode' in info and 'season' not in info: #Default to Season 01
            season = "S01"
            episode = str(info['episode'])
            title = info['title'].lower()
            title = title.strip('.| ')
            tvShows.append((title, season, episode, tup[1]))
        #both season and episode in info
        elif 'season' and 'episode' in info:
            season = str(info['season'])
            episode = str(info['episode'])
            title = info['title'].lower()
            title = title.strip('.| ')
            tvShows.append((title, season, episode, tup[1]))
        elif 'year' and ('quality' or 'resolution') in info: 
            title = info['title'].lower()
            movies.append((title, tup[1]))
        #only season in info
        elif 'season' in info and 'episode' not in info:
            episode = re.search(r'[Ee]?\d{1,2}', info['title'])
            #check if we can find the episode number in the title
            if episode != None:
                episode = str(info['episode'])
                title = info['title'].lower()
                title = title.strip('.| ')
                tvShows.append((title, season, episode, tup[1]))
            else:
                season = str(info['season'])
                title = info['title'].lower()
                title = title.strip('.| ')
                tvShows.append((title, season, episode, tup[1]))
        #Should have covered most of the tv-shows excluding ones too difficult to handle with a simple program like this one
        else: #TODO filter more! this is 
            unknown.append(tup)

    return tvShows, movies, unknown




def get_valid_file_types(Directory):
    #all valid video file types
    valid_type =  ["3gp", "3g2", "asf", "amv", "avi", "drc", "flv", "f4v", "f4p", "f4a", "f4b", "gif", "m4v", "mxf", "mkv", "mts", "m2ts", "mpg", "mpeg", "m2v", "mp4", "m4p", "mng", "ogv", "ogg", "mov", "qt", "rm", "vob", "wmv"] 
    Unsorted = []
    fileCounter = 0
    for dirName, subDirList, fileList in os.walk(Directory): #Walks the given directory and any subdirectory/ies
        for fName in fileList:
            if fName.split('.')[-1].lower() in valid_type: #only check if the file ends in a file-format we're looking for
                fileCounter += 1 #counter to make sure we're listing every file we check
                info = PTN.parse(fName) #extract all available information from filename via Parse-Torrent-Name library
                path = os.path.join(dirName, fName)
                Unsorted.append((info, path))
                
    tvShows, movies, unknown = filterFiles(Unsorted)
    #make sure we've sorted every single file applicable to the valid typing
    listSum = len(tvShows) + len(unknown) + len(movies)
    if fileCounter == listSum:
        pass
    else:
        print("We're missing some files captain")
        #return
    Unsorted.clear() #empty unsorted as we have no need for it further
    print(movies)
    #print(tvShows)
    #print(unknown)
    return None

get_valid_file_types("downloads")

def main_func(s):
    return None


