import os, re, PTN, shutil

def filterFiles(Unordered):
    movies = []
    tvShows = []
    unknown = []
    for tup in Unordered:
        info = tup[0]
        splitDir = tup[1].split('/')
        #Missing season in info
        if 'episode' in info and 'season' not in info: #Default to Season 01
            season = "Season 01"
            episode = info['episode']
            title = info['title'].lower()
            tvShows.append((title, season, episode, tup[1]))
        #both season and episode in info
        elif 'season' and 'episode' in info:
            season = info['season']
            episode = info['episode']
            title = info['title'].lower()
            if title == '':
                title = splitDir[1]
            tvShows.append((title, season, episode, tup[1]))
        #only season in info
        elif 'season' in info and 'episode' not in info:
            episode = re.search(r'[Ee]?\d{1,2}', info['title'])
            #check if we can find the episode number in the title
            if episode != None:
                episode = info['episode']
                title = info['title'].lower()
                tvShows.append((title, season, episode, tup[1]))
            else:
                season = str(info['season'])
                title = info['title'].lower()
                tvShows.append((title, season, episode, tup[1]))
        #Before we start checking for any digits in the filenames, sort out any files we can be confident belong in movies
        elif 'year' and 'resolution' in info:
            title = info['title'].lower()
            movies.append((title, tup[1]))
        elif re.search(r'[1-2]\d{3}', splitDir[-1]) is not None:
            title = info['title'].lower()
            movies.append((title, tup[1]))
        elif re.search(r'[1-9]\d\d', info['title']) is not None:
            tmp = re.search(r'[1-9]\d\d', info['title'])
            tmp = tmp.group(0)
            season = "Season " + tmp[0]
            episode = tmp[1:len(tmp)]
            title = info['title'].split()
            title  = " ".join(title[0:len(title)-1])
            tvShows.append((title.strip('- '), season, episode, tup[1]))
        elif len(splitDir) > 3:
            if 'season' or 'sería' in splitDir[2].lower():
                season = splitDir[2]
                title = splitDir[1]
                episode = None
                tvShows.append((title, season, episode, tup[1]))
            elif re.fullmatch(r'[sS]\d', splitDir[2]) is not None:
                print(splitDir[2])
                season = splitDir[2]
                title = splitDir[1]
                episode = None
                tvShows.append((title, season, episode, tup[1]))
            elif splitDir[2].isdigit():
                season = "Season " + splitDir[2]
                title = splitDir[1]
                episode = None
                tvShows.append((title, season, episode, tup[1]))
            else:
                unknown.append(tup)
        else: #TODO filter more!
            unknown.append(tup)

    return tvShows, movies, unknown

def get_valid_file_types(Directory):
    #all valid video file types
    valid_type =  ["3gp", "3g2", "asf", "amv", "avi", "drc", "flv", "f4v", "f4p", "f4a", "f4b", "gif", "m4v", "mxf", "mkv", "mts", "m2ts", "mpg", "mpeg", "m2v", "mp4", "m4p", "mng", "ogv", "ogg", "mov", "qt", "rm", "vob", "wmv", "srt"]
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
        print("Uh-oh, some files appear to have gotten lost in the filtering")
        return
    for x in tvShows:
        print(x)
    print(len(unknown))
    #will return more later
    return tvShows

get_valid_file_types("downloads")
############################################ 
#cleans up the folder, removing any unnecessary files like .torrent and .nfo etc.
def delete_trash_files(directory):
    trash = []
    valid_type =  ["3gp", "3g2", "asf", "amv", "avi", "drc", "flv", "f4v", "f4p", "f4a", "f4b", "gif", "m4v", "mxf", "mkv", "mts", "m2ts", "mpg", "mpeg", "m2v", "mp4", "m4p", "mng", "ogv", "ogg", "mov", "qt", "rm", "vob", "wmv", "srt"]
    for dirName, subDirList, fileList in os.walk(directory): #Walks the given directory and any subdirectory/ies
        for fName in fileList:
            if fName.split('.')[-1] not in valid_type: #only check if the file ends in a file-format we're looking for
                #info = PTN.parse(fName) #extract all available information from filename via Parse-Torrent-Name library
                path = os.path.join(dirName, fName)
                trash.append(path)
    for pls_delete in trash:
        os.remove(pls_delete)

############################################ 
#delete any empty folders left behind after sorting -- virkar ekki 
def delete_empty_folders(directory):
    if not os.listdir(directory):
        os.rmdir(directory)

############################################ 
#returns a folder name for the file to be placed in
#creating an appropriate directory targetFolder + '/NameOfShow/..'
def get_series_name(name_of_file):

    showName = name_of_file[0]
    return str(showName)

############################################ 
#returns a folder name for the file to be placed in
#creating an appropriate directory targetFolder + '/NameOfShow/Seasons XX/..'
def get_season(name_of_file):
    seasonMatch = re.search(r'\d?\d', name_of_file[1])
    seasonVal = "Season " + seasonMatch.group(0)
    return str(seasonVal)

############################################ 
#places all valid files into a new folder based on their name, and then into a specific season folder
def sort_to_new_folder(directFolder, targetFolder):
    lis = get_valid_file_types(directFolder)

    for show in lis:
        name_folder_path = get_series_name(show)
        season_folder_path = get_season(show)
        str_folder_path = targetFolder + '/' + name_folder_path + '/' + season_folder_path
        #this checks the file name of show and checks for corresponding folder name,
        #if it doesn't exists, it'll create a new one and be moved there
        #this has been commented out to test the trash function, it works perfectly otherwise
        if not os.path.exists(str_folder_path):
            os.makedirs(str_folder_path)
            shutil.move(show[-1], str_folder_path)
        else:
            shutil.move(show[-1], str_folder_path)
        
        #trash function for unrelated files after sorting
        delete_trash_files(directFolder)
        delete_empty_folders(directFolder)

    return None

#sort_to_new_folder('from_folder', 'to_folder')


