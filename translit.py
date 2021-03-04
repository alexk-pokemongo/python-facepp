from glob import iglob
import os
dataset_dir = '/dataset/feb_2021'
blacklist = ['css','images','js','photos','video_files']

def is_unicode(s):
    return len(s) != len(s.encode())

def translit(dataset_dir,blacklist):
    #glob directories, rename diorectories
    subdirs = iglob(os.path.join(dataset_dir,'*'))
    print(subdirs)
    #glob file names, rename file names
    pass

if __name__ == "__main__":
    translit()
