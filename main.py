#main function
#r"^.*S\d\dE\d\d" < possible show and episode regex

import os, re
def get_valid_file_types(Directory):
    #all valid video file types
    valid_type =  ["m4v", "flv", "mpeg", "mov", "mpg","mpe", "wmv", "MOV", "mp4"] 
    foundMatch = []
    for dirName, subDirList, fileList in os.walk(Directory): #Walks the given directory and any subdirectory/ies
        for fName in fileList:
            if fName.split('.')[-1] in valid_type: #if the file ending matches any valid file ending, append to the list both the filename, and the full path to the file
                #TODO match show name and season. store differently.
                #possible solution for naming using https://github.com/divijbindlish/parse-torrent-name
                #Requires teacher confirmation before we go further.
                foundMatch.append((fName, os.path.join(dirName, fName)))
                
    
    '''for item in Directory:
        temp = item.split('.')
        print(temp[-1])
        if temp[-1] in valid_type:
            filtered_accepetables.append(item)'''
    print(foundMatch)
    return None

get_valid_file_types("downloads")

def main_func(s):
    return None


