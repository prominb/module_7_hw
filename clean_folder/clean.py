import re
import sys
import shutil
from pathlib import Path


CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")

TRANS = {}

dir_names = ('Archives', 'Video', 'Audio', 'Documents', 'Images', 'Others')
jpeg_files, png_files, jpg_files, svg_files = list(), list(), list(), list()

avi_files, mp4_files, mov_files, mkv_files = list(), list(), list(), list()

doc_files, docx_files, txt_files, pdf_files, xlsx_files, pptx_files = list(), list(), list(), list(), list(), list()

mp3_files, ogg_files, wav_files, amr_files = list(), list(), list(), list()

zip_files, gz_files, tar_files = list(), list(), list()

unknown = set()
unknown_files = list()

extensions = set()
folders = list()

registered_extensions = {
    'JPEG': jpeg_files, 'PNG': png_files, 'JPG': jpg_files, 'SVG': svg_files,
    'AVI': avi_files, 'MP4': mp4_files, 'MOV': mov_files, 'MKV': mkv_files,
    'DOC': doc_files, 'DOCX': docx_files, 'TXT': txt_files, 'PDF': pdf_files, 'XLSX': xlsx_files, 'PPTX': pptx_files,
    'MP3': mp3_files, 'OGG': ogg_files, 'WAV': wav_files, 'AMR': amr_files,
    'ZIP': zip_files, 'GZ': gz_files, 'TAR': tar_files
}

dir_for_sorted = {
    'Archives': [],
    'Video': [],
    'Audio': [],
    'Documents': [],
    'Images': [],
    'Others': [],
}

for cyri, lati in zip(CYRILLIC_SYMBOLS, TRANSLATION):
    TRANS[ord(cyri)] = lati
    TRANS[ord(cyri.upper())] = lati.upper()


def normalize(name: str) -> str: # приймає на вхід рядок та повертає рядок
    name, *extension = name.split('.')
    name_translit = name.translate(TRANS) # transliteration
    name_translit = re.sub(r"\W", "_", name_translit) # normalize word
    return f"{name_translit}.{'.'.join(extension)}"


def get_extensions(file_name):
    return Path(file_name).suffix[1:].upper()


def scan(folder):
    for item in folder.iterdir():
        if item.is_dir():
            if item.name not in dir_names:
                folders.append(item)
                scan(item)
            continue

        extension = get_extensions(file_name=item.name)
        new_file_name = folder/item.name

        if not extension:
            unknown_files.append(new_file_name)
        else:
            try:
                container = registered_extensions[extension]
                extensions.add(extension)
                container.append(new_file_name)
            except KeyError:
                unknown.add(extension)
                unknown_files.append(new_file_name)


def handle_file(path, root_folder, destinations):
    target_folder = root_folder/destinations
    target_folder.mkdir(exist_ok=True)
    target_item = path.replace(target_folder/normalize(path.name))
    if destinations == 'Archives':
        dir_for_sorted.get('Archives').append(target_item.name)
    elif destinations == 'Video':
        dir_for_sorted.get('Video').append(target_item.name)
    elif destinations == 'Audio':
        dir_for_sorted.get('Audio').append(target_item.name)
    elif destinations == 'Documents':
        dir_for_sorted.get('Documents').append(target_item.name)
    elif destinations == 'Images':
        dir_for_sorted.get('Images').append(target_item.name)
    elif destinations == 'Others':
        dir_for_sorted.get('Others').append(target_item.name)


def handle_archive(path, root_folder, destinations):
    target_folder = root_folder/destinations
    target_folder.mkdir(exist_ok=True)

    new_name = normalize(path.stem)
    archive_folder = target_folder/new_name
    archive_folder.mkdir(exist_ok=True)

    try:
        shutil.unpack_archive(str(path.resolve()), str(archive_folder.resolve()))
    except shutil.ReadError:
        archive_folder.rmdir()
        return
    except FileNotFoundError:
        archive_folder.rmdir()
        return
    
    path.unlink()


def remove_empty_folders(path):
    for item in path.iterdir():
        if item.is_dir():
            remove_empty_folders(item)

            try:
                item.rmdir()
            except OSError:
                # print("Not Empty")
                pass


def write_to_file(folder_path):
    with open(str(folder_path)+'/log_file', 'w') as fh:
        for key, value in dir_for_sorted.items():
            fh.write(f"{key}: {value}\n")


def main():
    folder_path = Path(sys.argv[1])
    print(f'Start in folder name: {folder_path}')

    scan(folder_path)

    # for file in zip_files:
        # handle_file(file, folder_path, "Archives")
    for file in zip_files:
        handle_archive(file, folder_path, "Archives")

    # for file in gz_files:
        # handle_file(file, folder_path, "Archives")
    for file in gz_files:
        handle_archive(file, folder_path, "Archives")

    # for file in tar_files:
        # handle_file(file, folder_path, "Archives")
    for file in tar_files:
        handle_archive(file, folder_path, "Archives")

    for file in jpeg_files:
        handle_file(file, folder_path, "Images")

    for file in png_files:
        handle_file(file, folder_path, "Images")

    for file in jpg_files:
        handle_file(file, folder_path, "Images")

    for file in svg_files:
        handle_file(file, folder_path, "Images")

    for file in avi_files:
        handle_file(file, folder_path, "Video")

    for file in mp4_files:
        handle_file(file, folder_path, "Video")

    for file in mov_files:
        handle_file(file, folder_path, "Video")
    
    for file in mkv_files:
        handle_file(file, folder_path, "Video")

    for file in doc_files:
        handle_file(file, folder_path, "Documents")

    for file in docx_files:
        handle_file(file, folder_path, "Documents")

    for file in txt_files:
        handle_file(file, folder_path, "Documents")

    for file in pdf_files:
        handle_file(file, folder_path, "Documents")

    for file in xlsx_files:
        handle_file(file, folder_path, "Documents")

    for file in pptx_files:
        handle_file(file, folder_path, "Documents")

    for file in mp3_files:
        handle_file(file, folder_path, "Audio")

    for file in ogg_files:
        handle_file(file, folder_path, "Audio")

    for file in wav_files:
        handle_file(file, folder_path, "Audio")

    for file in amr_files:
        handle_file(file, folder_path, "Audio")

    for file in unknown_files:
        handle_file(file, folder_path, "Others")

    remove_empty_folders(folder_path)

    write_to_file(folder_path)


if __name__ == '__main__':
    main()
