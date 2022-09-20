import os
from time import sleep
from image_decoder import get_image_from_url
from ruamel import yaml
from pathlib import Path

EXTENSIONS = ('.jpeg', '.jpg')


def get_next_name(path_dir, filename_mask, suffix, extension):
    result_path = path_dir / f'{filename_mask}_{suffix}{extension}'
    while result_path.is_file():
        suffix += 1
        result_path = path_dir / f'{filename_mask}_{suffix}{extension}'
    return result_path, suffix


if __name__ == '__main__':
    with open('config.yaml') as _stream:
        config = yaml.safe_load(_stream.read())
    url = config.get('url')
    filename_mask = config.get('filename_mask')
    for ext in EXTENSIONS:
        if filename_mask.endswith(ext):
            filename_mask = filename_mask[:-(len(ext))]
            break  # saving ext
    path_dir = config.get('dir', None)
    if path_dir:
        path_dir = Path(path_dir)
        if not path_dir.is_dir():
            os.makedirs(path_dir, exist_ok=True)

    sleep_time = config.get('sleep')
    suffix = 0
    while True:
        result_path, suffix = get_next_name(path_dir, filename_mask, suffix, ext)
        with open(result_path, 'wb') as im_stream:
            im_stream.write(get_image_from_url(url))
        sleep(sleep_time)
