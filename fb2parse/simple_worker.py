# -*- coding: utf-8 -*-
import os
from fb2parse import BookFile
from hashlib import md5
from binascii import Error as base64PaddingError
from shutil import move as shumove

# Модуль в одном потоке бежит по файловой системе, читает файлы, перекладывает их в другое место
# сразу же добавляет в базу, упаковывает их

__author__ = 'Andrew'

# todo: 4 проверка дубликатов
# todo: 5 добавение в базу
# todo: 6 упаковка

SOURCE = "d:\\Projects\\proj\\_fb2from\\"
LIBRARY = "d:\\Projects\\proj\\_fb2to\\Root\\Library\\"
COVERS = "d:\\Projects\\proj\\_fb2to\\Root\\Covers\\"


def get_path_elements(path):
    """ Разбираем путь на части """
    _path, _file = os.path.split(path)
    elements = []
    while 1:
        _path, folder = os.path.split(_path)
        if folder != '':
            elements.append(folder)
            if _path == "":
                break
        else:
            if _path != "":
                elements.append(_path)
            break
    elements.reverse()
    return elements


def build_path(book_file):
    """ Строим дерево каталогов """
    name, path = book_file.get_new_name_path()
    start_path = LIBRARY
    elements = get_path_elements(path)
    for el in elements:
        start_path = os.path.join(start_path, el)
        if not os.path.exists(start_path):
            try:
                os.mkdir(start_path)
            except Exception, e:
                return False
    return True


def move_book(book_file):
    # строим путь в ФС для книги
    res = build_path(book_file)
    if res:
        _path = os.path.join(LIBRARY, book_file.new_path)
        try:
            shumove(book_file.file, _path)
        except Exception:
            return False
        return True
    return False


def main():
    for (_dir, sub_dir, files_here) in os.walk(SOURCE):
        for _file in files_here:
            # собираем file-object книгу
            _file_path = os.path.join(_dir, _file)
            book_file = BookFile(_file_path)
            # собираем class-object книгу
            res = book_file.make_book()
            # если не получилось - пропускаем
            if not res:
                continue
            # перемещаем книгу
            res = move_book(book_file)
            if not res:
                continue
            # пока картинки не сохраняем
            if book_file.book.cover is not None:
                covername = book_file.hash
                coverpath = os.path.join(COVERS, covername[:4])
                if not os.path.exists(coverpath):
                    os.mkdir(coverpath)
                with open(os.path.join(coverpath, covername + '.' + book_file.book.cover.extension), 'wb') as coverfile:
                    try:
                        coverfile.write(book_file.book.cover.data.decode('base64'))
                    except base64PaddingError:
                        # todo: fix padding
                        continue

            # res = save_cover(book_file)

if __name__ == "__main__":
    main()