import os, re, PTN, shutil
############################################
#main function
#r"^.*S\d\dE\d\d" < possible show and episode regex
def get_valid_file_types(Directory):
    #all valid video file types
    valid_type =  ["m4v", "flv", "mpeg", "mov", "mpg","mpe", "wmv", "MOV", "mp4"] 
    Unsorted = []
    Shows = []
    fileCounter = 0
    for dirName, subDirList, fileList in os.walk(Directory): #Walks the given directory and any subdirectory/ies
        for fName in fileList:
            if fName.split('.')[-1] in valid_type: #if the file ending matches any valid file ending, append to the list both the filename, and the full path to the file
                #TODO match show name and season. store differently.
                #possible solution for naming using https://github.com/divijbindlish/parse-torrent-name
                #Requires teacher confirmation before we go further.
                fileCounter += 1
                info = PTN.parse(fName)
                if 'episode' not in info: #Catch any movie and bad show filenames
                    Unsorted.append(info)
                elif 'episode' and 'season' in info: #No need to work these any further, keep the info we need and the path so we can move the file to the correct folder
                    Season = "S"+ str(info['season'])
                    Episode = "E"+str(info['episode'])
                    title = info['title'].lower()
                    path = os.path.join(dirName, fName)
                    Shows.append((title, Season, Episode, path))
                else: #shouldn't miss anything, but just in case we add anything else also to the unsorted list.
                    Unsorted.append(info)

    #make sure we've sorted every single file applicable to the valid typing
    if fileCounter == len(Shows) + len(Unsorted):
        pass
    else:
        print("We're missing some files captain")
        return
    print(fileCounter)

    print(len(Shows))
    return Shows

#get_valid_file_types('downloads')

############################################ 
def test_sort_to_new_folder(direct, target):
    lis = get_valid_file_types(direct)
    
    print(lis)

    for show in lis:
        shutil.move(show[-1], target)

test_sort_to_new_folder('downloads', 'downloads/moved')


