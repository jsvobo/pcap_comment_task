# pcap_comment_task

Task is to write a python code, which can either add comments to packets or read the packet and print it out. 
The file format supported is pcapng.
You will find the short script and a dummy file collected by the author with around 800 packets.

## Installation

The script needs the library `pcapng` to work.

```sh
pip install python-pcapng
```

If needed, refer to: [python-pcapng on PyPI](https://pypi.org/project/python-pcapng/)

For a clean environment:

```sh
conda create -n pkt_comments python=3.11 
conda activate pkt_comments
pip install python-pcapng
```

## Description

The script can either read the content of a packet with a specified number (which is the order of the packets in the file) or add a comment to the packet with the specified number. The selected mode depends on the provided arguments (whether "comment" is provided on the command line).

- If `--output` or `-o` is not specified, the file is saved as `X_changed_Y.pcapng`, where `X` is the original input file name and `Y` is the packet number changed.
- If no comment is provided, the script reads the packet content and prints it as JSON in the console. You can specify the output file even for the read-only mode, but then no file is created.

The script verifies if the input file has the correct file suffix ".pcapng". Output file can have arbitrary suffix.

The script prints an error and fails, when the packet with the specified number is not found in the file.

## Usage

```sh
python commenter.py "input file" "packet number" "comment" -o "output file name"
```

Refer to `python commenter.py -h` for more details.

### Examples

```sh
python commenter.py dummy.pcapng 10 "lalala" -o out.pcapng
python commenter.py out.pcapng 10 -o out.pcapng # having -o here changes nothing since we are reading only
python commenter.py out.pcapng 10 



python commenter.py dummy.pcapng 666 "testing testing lalala" #produces file dummy_changed_666.pcapng since no -o was added
python commenter.py dummy_changed_666.pcapng 666 #read the packet and the comment inserted

python commenter.py dummy.pcapng 900 "lalala" # fails, since there is no packet 900
python commenter.py out.cpp 10  # fails, since input file has wrong type
``` 
