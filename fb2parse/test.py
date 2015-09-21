# -*- coding: utf-8 -*-

from fb2parse import *
import os

def main():
    path = "D:\\Projects\\proj\\_fb2bak"
    for
    id = '225713'  #raw_input("book id:")
    bookfile = BookFile(os.path.join(path, id + '.fb2'))
    book = bookfile.make_book()
    print book


if __name__ == "__main__":
    main()