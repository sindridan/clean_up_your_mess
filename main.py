import os, re, PTN, shutil
############################################
#main function
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
    
    #print(tvShows)
    return tvShows, movies, unknown

def get_valid_file_types(Directory):
    #all valid video file types
    valid_type =  ["3gp", "3g2", "asf", "amv", "avi", "drc", "flv", "f4v", "f4p", "f4a", "f4b", "gif", "m4v", "mxf", "mkv", "mts", "m2ts", "mpg", "mpeg", "m2v", "mp4", "m4p", "mng", "ogv", "ogg", "mov", "qt", "rm", "vob", "wmv", "srt"]
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

    #will return more later
    return tvShows

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
    seasonVal = name_of_file[1]
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


