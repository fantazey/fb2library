# -*- coding: utf-8 -*-
__author__ = 'Andrew'



#from zipfile import *
from fb2 import *
from book.models import *
import os
import shutil

LIB_ROOT = '/home/andy/Projects/mylib/lib_root/'
CURR = '/home/andy/Projects/mylib/utils/24-30559/'
UTF = '/home/andy/Projects/mylib/utils/books/utf/'
CP1251 = '/home/andy/Projects/mylib/utils/books/cp1251/'


#zipwork('1.zip')
split_by_encoding(CURR)
#decode2utf(CP1251)

# чтобы сохранить картинку нужно к блоку данных binary применить команды:
# imgData - кусок binary
#fh = open("imageToSave.png", "wb")
#fh.write(imgData.decode('base64'))
#fh.close()