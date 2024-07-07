# File To Image Converter

Convert any file to an image representing the binary data. The script can also decode the generated images.

![README_converted](https://github.com/mrusse/file-to-image/assets/38119333/4d80f69d-95b4-43b2-935a-234005712b7b)

The example above is this README file represented as an image (so meta).

# Setup

Install the requirements:
```
pip install -r requirements.txt
```

# Usage

To encode a file use the `-e` flag:
```
python file-to-image.py -e file.txt
```
If you encode with the `-r` flag the "high" bits will be a random colour instead of being black (see the above picture for an example).

To decode an image use the `-d` flag. `-d` needs the filename and the extension of the original file:
```
python file-to-image.py -d file_converted.png txt
```

By default one bit is represented by one pixel. This can be changed with the `-s` flag:
```
python file-to-image.py -e file.txt -s 10
```
This will make an image where each bit is 10x10 pixels. It is important to note that if you are decoding a scaled image you need to pass the same value in through `-s`.

<sup><sub>ps if you are looking to decode the example image... scale is 10</sub></sup>
