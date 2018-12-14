# clean_up_your_mess
Reykjavík University
Three week course: Python (Group Project)
Fall 2018

A python script to clean up a directory containing downloaded tv-series and movies.
End goal is for us to sort based on the Series name and what season the episode is in.

## Required libraries:
* [Parse-Torrent-Name](https://github.com/divijbindlish/parse-torrent-name#parse-torrent-name-) - Used to parse the filenames

## How to run:
* Fork or clone this repo to your local machine
* Locate your source downloads folder
* Open up your terminal (MacOS) or command prompt (Windows) in the directory containing the source folder
* Run the following command: python3 main.py 'Source folder name' 'Target folder name'
* The two arguements in the bottom of the main.py script: sys.argv[1], sys.argv[2], read the path to the directory
* from the user and gathers the files from sys.argv[1] (source directory), sorts it and structures the files in sys.arg[2] (target directory).
* This can be run anywhere but make sure that you're using the correct directories: For example: (MacOS) SindriDan/pyFinalProject/main.py ../Downloads ../StructuredDownloads
 


## Developers
* Arnar Pálmi Elvarsson - *arnare15* - [github](https://github.com/arnarish)
* Sindri Dan Garðarsson - *sindrig17* - [github](https://github.com/sindridan)

## Built with
* [VS Code](https://code.visualstudio.com/Download) - Code editor
* [Python](https://www.python.org/) - Programming language

## Known issues / bugs
* Struggles with inconsistent naming
* Similarly does not sort shows with extended names with their shorter selves(e.g. QI and QI XL are sorted into seperate folders)
* .str files have a small tendency to end up in their own directory for tv shows
* Could do some file & directory name cleanup
* Unknown folder could do some sorting on it's own, making the manual work required less tedious

## Notes:
* Our script has only been tested on a Mac but with our OS check function, it should be able to run on other operating systems
* Terminal of choice for the developers was the iTerm for MacOS