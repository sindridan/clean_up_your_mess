#main function

import os, re, PTN
def get_valid_file_types(Directory):
    #all valid video file types
    valid_type =  ["m4v", "flv", "mpeg", "mov", "mpg","mpe", "wmv", "MOV", "mp4"] 
    Unsorted = []
    Movies = []
    Shows = []
    fileCounter = 0
    for dirName, subDirList, fileList in os.walk(Directory): #Walks the given directory and any subdirectory/ies
        for fName in fileList:
            if fName.split('.')[-1] in valid_type: #only check if the file ends in a file-format we're looking for
                fileCounter += 1 #counter to make sure we're listing every file we check
                info = PTN.parse(fName) #extract all available information from filename via Parse-Torrent-Name library
                if  'year' in info and 'season' and 'episode' not in info: #Catch most movies, identified by having year and title 
                    path = os.path.join(dirName, fName)
                    Movies.append((info, path))
                elif 'episode' and 'season' in info: #No need to work these any further, keep the info we need and the path so we can move the file to the correct folder
                    Season = "S"+ str(info['season'])
                    Episode = "E"+str(info['episode'])
                    title = info['title'].lower()
                    path = os.path.join(dirName, fName)
                    Shows.append((title, Season, Episode, path))
                else: #anything that doesn't match the prior categories
                    path = os.path.join(dirName, fName)
                    Unsorted.append((info, path))

    #make sure we've sorted every single file applicable to the valid typing
    listSum = len(Shows) + len(Unsorted) + len(Movies)
    if fileCounter == listSum:
        pass
    else:
        print("We're missing some files captain")
        return
    Other = [] #list of items we could not sort, sort into it's own folder and must be dealt with manually
    for item in Unsorted:
        if re.fullmatch(r'\d\d\d', item[0]['title'].split(' ')[-1]):
            tmp = item[0]['title'].split(' ')
            title = ' '.join(tmp[0:len(tmp)-1]).lower()
            season = "S0"+ tmp[-1][0]
            Episode = "E"+ tmp[-1][1:]
            Shows.append((title, season, Episode, item[1]))
            Unsorted.remove(item) #not sure this currently does anything?
        else:
            #TODO find title and serie in directory path?
            #Set default season 01 if only r'E\d\d' in filename
            #further filtering
            else:
                Other.append(item)
    Unsorted.clear() #empty unsorted as we have no need for it further
    #print(Movies)
    #print(Shows)
    #print(Other)
    return None

get_valid_file_types("downloads")

def main_func(s):
    return None


