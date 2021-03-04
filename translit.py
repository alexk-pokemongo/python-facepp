from glob import glob
import os
import os.path
from transliterate import translit, get_available_language_codes

dataset_dir = '/dataset/feb_2021'
blacklist = ['css','images','js','photos','video_files']

def is_unicode(s):
    return len(s) != len(s.encode())

def translit_rename(dataset_dir,blacklist):
    #glob directories, rename diorectories
    subdirs = glob(os.path.join(dataset_dir,'*'))

    for s in subdirs:
        if(os.path.isdir(s) and is_unicode(s) and not(s in blacklist)):
            s_translit = translit(s,'ru', reversed=True)
            s_translit = s_translit.replace(' ','_')
            print(s+"->"+s_translit)
            os.rename(s,s_translit)
            

    subdirs = glob(os.path.join(dataset_dir,'*'))
    for s in subdirs:
        if not(s in blacklist):
            subdir_files = glob(os.path.join(s,"*"))    
            for f in subdir_files:
                if(os.path.isfile(f) and is_unicode(f) ):
                    f_translit = translit(f,'ru', reversed=True)
                    f_translit = f_translit.replace(' ','_')
                    print(f+"-->"+f_translit)
                    os.rename(f,f_translit)

    #glob file names, rename file names
    pass

if __name__ == "__main__":
    translit_rename(dataset_dir,blacklist)
