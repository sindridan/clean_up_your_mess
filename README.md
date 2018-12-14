# clean_up_your_mess
Reykjavík University
Three week course: Python (Group Project)
Fall 2018

A python script to clean up a directory containing downloaded tv-series and movies.
End goal is for us to sort based on the Series name and what season the episode is in.

## Required libraries:
* [Parse-Torrent-Name](https://github.com/divijbindlish/parse-torrent-name#parse-torrent-name-) - Used to parse the filenames

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
