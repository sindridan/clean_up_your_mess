import os, re, PTN, shutil
import string

def filterFiles(unsorted):
    movies = []
    tvShows = []
    unknown = []
    samples = []
    #Run through each file in the unsorted list, sorting it into seperated lists so that we can arrange them correctly in the new folder
    for tup in unsorted:
        info = tup[0]
        splitDir = tup[1].split('/')
        #filtering out sample files, not very useful at this point but will be sorted to special folder if user needs them
        if 'sample' in splitDir[-1].lower():
            samples.append((tup[1]))
        #Missing season in info
        elif 'episode' in info and 'season' not in info: #search for s+digit in filename, else default to Season 1
            season = re.search(r'[sS]\d{1,2}', splitDir[-1])
            episode = info['episode']
            title = info['title']
            if season is not None: #found some season marker in filename, using it
                season = season.group(0)
                tvShows.append((title.lower(), season, episode, tup[1]))
            else: #nothing to indicate season in filename, defaulting to 1
                season = "Season 1"
                tvShows.append((title.lower(), season, episode, tup[1]))
        #both season and episode in info
        elif 'season' and 'episode' in info:
            season = info['season']
            episode = info['episode']
            title = info['title']
            if title == '':
                title = splitDir[1]
            tvShows.append((title.lower(), season, episode, tup[1]))
        #only season in info
        elif 'season' in info and 'episode' not in info:
            episode = re.search(r'[Ee]?\d{1,2}', info['title'])
            #check if we can find the episode number in the title
            season = str(info['season'])
            title = info['title']
            tvShows.append((title.lower(), season, episode, tup[1]))
        #Before we start checking for any digits in the filenames, sort out any files we can be confident belong in movies
        elif 'year' and 'resolution' in info:
            title = info['title']
            movies.append((title.lower(), tup[1]))
        #the rest are filenames the parser couldn't work out if they were part of a tv series or a movie

        #Most tvShows are in structured folders, let's use that to our advantage
        elif len(splitDir) > 3:
            #show folders are usually structured as 'downloads/showName/Season/episode
            #check if there's any indication of "season" in the 2nd folder
            if 'season' or 'sería' in splitDir[2].lower():
                season = splitDir[2]
                title = splitDir[1]
                episode = None
                tvShows.append((title.lower(), season, episode, tup[1]))
            #check if there's a single digit season marker(i.e S1 or similar)
            elif re.fullmatch(r'[sS]\d', splitDir[2]) is not None:
                season = splitDir[2]
                title = splitDir[1]
                episode = None
                tvShows.append((title.lower(), season, episode, tup[1]))
            #expected season folder is only 1-2 digits
            elif splitDir[2].isdigit() and len(splitDir[2]) < 3:
                season = "Season " + splitDir[2]
                title = splitDir[1]
                episode = None
                tvShows.append((title.lower(), season, episode, tup[1]))
            else: #I'm not sure how to exit a nested if statement, so this is here on leftover duty
                unknown.append(tup)
        #Some movies managed to slip through the parser, find any file with 19** or 20** in the name
        elif re.search(r'(19\d{2}|20\d{2})', splitDir[-1]) is not None:
            title = info['title']
            movies.append((title.lower(), tup[1]))
        #final attempt at sorting out more difficult tv shows, grabbing any show whos title ends with 3 digits
        elif  'quality' in info:
            tmp = info['title'].split(' ')
            if tmp[-1].isdigit():
                title = ' '.join(tmp[0:len(tmp)-1])
                season = tmp[-1][0]
                episode = tmp[-1][1:]
                tvShows.append((title.lower(), season, episode, tup[1]))
            else: #Same as the else statement above, leftovers
                unknown.append(tup)
        else: #Hungry hungry hippo
            unknown.append(tup)
    #check to make sure we've got every path that got sent into the function sorted into one of the four lists
    listSum = len(tvShows) + len(unknown) + len(movies) + len(samples)
    if len(unsorted) == listSum:
        pass
    else:
        print("Uh-oh, some files appear to have gotten lost in the filtering")
        return

    return tvShows, movies, unknown, samples

def get_valid_file_types(Directory):
    #all valid video file types
    valid_type =  ["3gp", "3g2", "asf", "amv", "avi", "drc", "flv", "f4v", "f4p", "f4a", "f4b", "gif", "m4v", "mxf", "mkv", "mts", "m2ts", "mpg", "mpeg", "m2v", "mp4", "m4p", "mng", "ogv", "ogg", "mov", "qt", "rm", "vob", "wmv", "srt"]
    Unsorted = []
    for dirName, subDirList, fileList in os.walk(Directory): #Walks the given directory and any subdirectory/ies
        for fName in fileList:
            if fName.split('.')[-1].lower() in valid_type: #only check if the file ends in a file-format we're looking for
                info = PTN.parse(fName) #extract all available information from filename via Parse-Torrent-Name library
                path = os.path.join(dirName, fName)
                Unsorted.append((info, path))

    return Unsorted


#get_valid_file_types("downloads")

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
#delete any empty folders left behind after sorting
def delete_empty_folders(directory):
  if not os.path.isdir(directory):
    return

  #traverses sub directories and deletes them
  files = os.listdir(directory)
  if len(files):
    for f in files:
      totalpath = os.path.join(directory, f)
      if os.path.isdir(totalpath):
        delete_empty_folders(totalpath)

  #checks the mmain dir and if empty, trashes it
  files = os.listdir(directory)
  if len(files) == 0:
    os.rmdir(directory)

############################################ 
def delete_sample_file(directory):
    return None

############################################ 
#returns a folder name fosr the file to be placed in
#creating an appropriate directory targetFolder + '/NameOfShow/..'
def get_series_name(name_of_file):
    showName = name_of_file[0]

    showName = re.sub('[^0-9a-zA-Z\']+', ' ', showName)
    showName = showName.strip()
    return string.capwords(showName)

############################################ 
#returns a folder name for the file to be placed in
#creating an appropriate directory targetFolder + '/NameOfShow/Seasons XX/..'
def get_season(name_of_file):
    seasonMatch = re.search(r'\d?\d', str(name_of_file[1]))
    if seasonMatch is not None:
        seasonVal = "Season " + str(seasonMatch.group(0))
        return seasonVal
    else:
        return "Other"

############################################ 
#returns the movie name
def get_movie_title(name_of_file):
    movie_title = name_of_file[0]

    movie_title = re.sub('[^0-9a-zA-Z\']+', ' ', movie_title)
    movie_title = movie_title.strip()
    return string.capwords(movie_title)

############################################ 
#1 helper function for sort_to_new_folder
#checks the path and if it doesn't exist, it creates the directory and moves item into it
#else just moves into it and overwrites duplicates
def sort_pathing_samples(item, newPath):
    if not os.path.exists(newPath):
        os.makedirs(newPath)
        shutil.move(item, newPath)
    else:
        dst_filename = os.path.join(newPath, os.path.basename(item))
        shutil.move(item, dst_filename)

############################################ 
#2 helper function for sort_to_new_folder
#checks the path and if it doesn't exist, it creates the directory and moves item into it
#else just moves into it and overwrites duplicates
#only works for files that are going to be in subdirectories like seasons and movies alongside .srt files etc.
def sort_pathing_precise(item, newPath):
    if not os.path.exists(newPath):
        os.makedirs(newPath)
        shutil.move(item[-1], newPath)
    else:
        #if duplicates, overwrite
        dst_filename = os.path.join(newPath, os.path.basename(item[-1]))
        shutil.move(item[-1], dst_filename)

############################################ 
#places all valid files into a new folder based on their name, and then into a specific season folder
def sort_to_new_folder(directFolder, targetFolder):
    if os.name == 'nt':
        #Windows-based system
        delim = '\\'
    else:
        #Linux or Unix
        delim = '/'

    listedFiles = get_valid_file_types(directFolder)
    tvShows, movies, unknown, samples = filterFiles(listedFiles)

    samples_path = targetFolder + delim + 'Samples'

    for samp in samples:
        #same as the unknown, the sample files with be moved to this specific folder
        #a reason why we keep these files is because some shows might include 'sample'
        #in their title but doesn't define it as a sample file
        sort_pathing_samples(samp, samples_path)

    for show in tvShows:
        name_folder_path = get_series_name(show)
        season_folder_path = get_season(show)
        str_folder_path = targetFolder + delim + 'TV' + delim + name_folder_path + delim + season_folder_path
        #this checks the file name of show and checks for corresponding folder name,
        #if it doesn't exists, it'll create a new one and be moved there
        #this has been commented out to test the trash function, it works perfectly otherwise
        sort_pathing_precise(show, str_folder_path)

    for movie in movies:
        movie_folder_path = get_movie_title(movie)
        movie_folder_path = targetFolder + delim + 'Movies' + delim + movie_folder_path
        #creates a directory for the movie itself instead of having each file directly in the movie directory
        #this causes issues when working with .srt files (subtitles), we want those files 
        sort_pathing_precise(movie, movie_folder_path)

    unknown_folder_path = targetFolder + delim + 'Unknown'   
    for unsort in unknown:
        #there will be no special folders for items in the unknown
        sort_pathing_precise(unsort, unknown_folder_path)

    #trash function for unrelated files after sorting
    delete_trash_files(directFolder)
    delete_empty_folders(directFolder)

    return None

sort_to_new_folder('downloads', 'structured')
