import typer

import aes_encryption


def main(
    command: str = typer.Argument(
        default="encrypt", help="Command: encrypt/decrypt"
    ),
    aes_type_str: str = typer.Argument(
        default="256", help="Key size: 128, 192 or 256"
    ),
    key_file: str = typer.Argument(
        default="key.txt", help="Path to key file"
    ),
    in_file: str = typer.Argument(
        default="input.txt", help="Path to input file"
    ),
    out_file: str = typer.Argument(
        default="output.txt", help="Path to output file"
    ),
):
    if command not in ["encrypt", "decrypt"]:
        raise ValueError("Invalid command.")

    try:
        aes_type = aes_encryption.AES_Type[f"AES_{aes_type_str}"]
    except KeyError:
        raise ValueError("Invalid AES type.")

    with open(key_file, "rb") as k:
        key = k.read()
    if len(key) != aes_type.value.key_length * 4:
        raise ValueError("Invalid key length.")

    with open(in_file, "rb") as f:
        input_string = f.read()

    if command == "encrypt":
        output_text = aes_encryption.encrypt(
            input_string,
            key,
            aes_type,
        )
    elif command == "decrypt":
        output_text = aes_encryption.decrypt(
            input_string,
            key,
            aes_type,
        )
    else:
        raise ValueError("Invalid command.")

    with open(out_file, "wb") as w:
        w.write(output_text)


if __name__ == "__main__":
    typer.run(main)
