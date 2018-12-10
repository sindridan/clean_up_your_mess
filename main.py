#main function

def get_valid_file_types(files):
    valid_type = ['avi', 'mkv', 'mp4']
    
    filtered_accepetables = []
    formatted_file_name = []
    for item in files:
        temp = item.split('.')
        print(temp[-1])
        if temp[-1] in valid_type:
            filtered_accepetables.append(item)


    print(filtered_accepetables)
    return None

get_valid_file_types(['My Girl 1 1991 DvDrip[Eng]-greenbud1969.avi', 'Modern.Family.S07E05.720p.HDTV.x264-KILLERS.mkv', 'New.Girl.S03E03.720p.HDTV.X264-DIMENSION.mkv', 'A.Quiet.Place.2018.1080p.BluRay.x264.DD5.1.Isl.Texti.mkv.torrent' ])

def main_func(s):
    return None


