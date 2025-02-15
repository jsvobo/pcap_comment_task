import json
import os
import sys
from argparse import ArgumentParser
from datetime import datetime

import pcapng.blocks as blocks
from pcapng import FileScanner
from pcapng.blocks import EnhancedPacket


def read_comment(filename, packet_number):
    with open(filename, "rb") as fp:
        scanner = FileScanner(fp)
        count = 0
        for block in scanner:
            if isinstance(block, blocks.BasePacketBlock):
                if count == int(packet_number):
                    try:
                        # print(block.options["opt_comment"])
                        packet = block
                        packet_json = {
                            "interface_id": packet.interface_id,
                            "timestamp": datetime.utcfromtimestamp(  # parsed timestamp to human readable format
                                block.timestamp
                            ).strftime(
                                "%Y-%m-%d %H:%M:%S.%f UTC"
                            ),
                            "packet_length": len(packet.packet_data),
                            "raw_data": packet.packet_data.hex(),  # raw bytes to hex
                            "options": {
                                key: value
                                for key, value in block.options.items()  # finally, the options, which contain the comment
                            },
                        }

                        print(json.dumps(packet_json, indent=4))

                    except KeyError:
                        print("No comment found")
                        sys.exit(1)

                    return True

                count += 1

    return False


def write_comment(filename, packet_number, comment, output):
    changed = False
    with open(filename, "rb") as fp, open(output, "wb") as out_fp:
        scanner = FileScanner(fp)
        count = 0
        for block in scanner:
            if isinstance(block, blocks.BasePacketBlock):
                if count == int(packet_number):
                    block.options["opt_comment"] = comment
                    changed = True

                count += 1
            block._write(out_fp)
            if count > 1:
                break

    return changed


if __name__ == "__main__":
    parser = ArgumentParser(description="PCAPNG Commenter")
    parser.add_argument("filename", help="PCAPNG file to process")
    parser.add_argument("packet_number", help="Packet number to read or comment")
    parser.add_argument("comment", nargs="?", help="Comment to add to the packet")
    parser.add_argument("-o", "--output", help="Output file name")

    args = parser.parse_args()

    arg_dict = {
        "filename": args.filename,
        "packet number": args.packet_number,
        "comment": args.comment,
        "read": args.comment is None,
        "output": args.output,
    }

    # check if file is in correct format
    if arg_dict["filename"].split(".")[-1] != "pcapng":
        print(
            f'Error: wrong file format - need .pcapng with no  - filename provided: {arg_dict["filename"]}'
        )
        sys.exit(1)

    # compose savefile name by adding _changed_X where X is the number of packet
    if arg_dict["output"] is None:
        split_filename = arg_dict["filename"].rsplit(".", 1)
        packet_number = arg_dict["packet number"]
        savefile_name = (
            split_filename[0] + f"_changed_{packet_number}." + split_filename[1]
        )
    else:
        savefile_name = arg_dict["output"]

    # does the correct operation, then prints success or error message
    success = False
    if arg_dict["read"]:
        success = read_comment(arg_dict["filename"], arg_dict["packet number"])
    else:
        success = write_comment(
            arg_dict["filename"],
            arg_dict["packet number"],
            arg_dict["comment"],
            savefile_name,
        )

    if not success:
        print(f"Error: operation failed, packet not found")
        if not arg_dict["read"]:
            os.remove(
                savefile_name
            )  # I dont like it here, but it is the only way to remove the file
        sys.exit(1)
    else:
        print("Success")
