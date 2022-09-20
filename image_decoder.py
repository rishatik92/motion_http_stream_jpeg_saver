from urllib.request import urlopen

JPEG_EOF = b'\xff\xd9'
START_STRING = b'--BoundaryString\r\nContent-type: image/jpeg\r\nContent-Length:     '
END_STRING = b'\r\n\r\n'


def get_image_from_url(http_stream_url):
    stream = urlopen(http_stream_url)
    image = b''
    data = stream.read(1024)
    count_from_web, data = data.replace(START_STRING, b'').split(END_STRING)
    count_from_web = int(count_from_web)
    read_count = 0
    while read_count < count_from_web:
        add_count = len(data)
        if add_count + read_count > count_from_web:
            add_count = count_from_web - read_count
        image += data[:add_count]
        read_count += add_count
        request_count = 1024
        if count_from_web - read_count < 1024:
            request_count = count_from_web - read_count
        data = stream.read(request_count)
        if not data:
            break

    return image
