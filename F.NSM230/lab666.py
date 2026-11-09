
from pathlib import Path
from typing import Callable

# S-DES tables use zero-based bit positions.
P10 = (2, 4, 1, 6, 3, 9, 0, 8, 7, 5)
P8 = (5, 2, 6, 3, 7, 4, 9, 8)
IP = (1, 5, 2, 0, 3, 7, 4, 6)
IP_INV = (3, 0, 2, 4, 6, 1, 7, 5)
EP = (3, 0, 1, 2, 1, 2, 3, 0)
P4 = (1, 3, 2, 0)
S0 = ((1, 0, 3, 2), (3, 2, 1, 0), (0, 2, 1, 3), (3, 1, 3, 2))
S1 = ((0, 1, 2, 3), (2, 0, 1, 3), (3, 0, 1, 0), (2, 1, 0, 3))


def permute(bits: str, table: tuple[int, ...]) -> str:
    return "".join(bits[i] for i in table)


def xor_bits(left: str, right: str) -> str:
    return format(int(left, 2) ^ int(right, 2), f"0{len(left)}b")


def rotate_left(bits: str, count: int) -> str:
    count %= len(bits)
    return bits[count:] + bits[:count]


def generate_keys(key: str) -> tuple[str, str]:
    """Generate the two 8-bit subkeys from a 10-bit binary key."""
    if len(key) != 10 or set(key) - {"0", "1"}:
        raise ValueError("Key must be exactly 10 binary digits.")
    permuted = permute(key, P10)
    left, right = permuted[:5], permuted[5:]
    left, right = rotate_left(left, 1), rotate_left(right, 1)
    first = permute(left + right, P8)
    left, right = rotate_left(left, 2), rotate_left(right, 2)
    second = permute(left + right, P8)
    return first, second


def f_function(right: str, subkey: str) -> str:
    mixed = xor_bits(permute(right, EP), subkey)
    output = ""
    for box, chunk in zip((S0, S1), (mixed[:4], mixed[4:])):
        row = int(chunk[0] + chunk[3], 2)
        column = int(chunk[1:3], 2)
        output += format(box[row][column], "02b")
    return permute(output, P4)


def _crypt_block(value: int, keys: tuple[str, str]) -> int:
    if not 0 <= value <= 255:
        raise ValueError("Block must be a byte (0..255).")
    bits = permute(format(value, "08b"), IP)
    left, right = bits[:4], bits[4:]
    for key in keys:
        left, right = right, xor_bits(left, f_function(right, key))
    return int(permute(left + right, IP_INV), 2)


def encrypt_block(value: int, keys: tuple[str, str]) -> int:
    return _crypt_block(value, keys)


def decrypt_block(value: int, keys: tuple[str, str]) -> int:
    return _crypt_block(value, keys[::-1])


def ecb(data: bytes, keys: tuple[str, str], decrypt: bool = False) -> bytes:
    operation = decrypt_block if decrypt else encrypt_block
    return bytes(operation(byte, keys) for byte in data)


def cbc(data: bytes, keys: tuple[str, str], decrypt: bool = False, iv: int = 0x5A) -> bytes:
    result = bytearray()
    previous = iv
    for byte in data:
        if decrypt:
            plain = decrypt_block(byte, keys) ^ previous
            result.append(plain)
            previous = byte
        else:
            cipher = encrypt_block(byte ^ previous, keys)
            result.append(cipher)
            previous = cipher
    return bytes(result)


def cfb(data: bytes, keys: tuple[str, str], decrypt: bool = False, iv: int = 0x5A) -> bytes:
    result = bytearray()
    previous = iv
    for byte in data:
        output = byte ^ encrypt_block(previous, keys)
        result.append(output)
        previous = byte if decrypt else output
    return bytes(result)


def ofb(data: bytes, keys: tuple[str, str], decrypt: bool = False, iv: int = 0x5A) -> bytes:
    del decrypt  # OFB uses the same operation to encrypt and decrypt.
    result = bytearray()
    stream = iv
    for byte in data:
        stream = encrypt_block(stream, keys)
        result.append(byte ^ stream)
    return bytes(result)


def ctr(data: bytes, keys: tuple[str, str], decrypt: bool = False, nonce: int = 0x12) -> bytes:
    del decrypt  # CTR uses the same operation to encrypt and decrypt.
    return bytes(byte ^ encrypt_block((nonce + i) % 256, keys) for i, byte in enumerate(data))


Mode = Callable[[bytes, tuple[str, str], bool], bytes]
MODES: dict[str, Mode] = {"ECB": ecb, "CBC": cbc, "CFB": cfb, "OFB": ofb, "CTR": ctr}


def process_file(path: Path, mode_name: str, keys: tuple[str, str]) -> bool:
    data = path.read_bytes()
    mode = MODES[mode_name]
    encrypted = mode(data, keys)
    decrypted = mode(encrypted, keys, True)
    encrypted_path = Path(f"encrypted_{mode_name.lower()}.bin")
    decrypted_path = Path(f"decrypted_{mode_name.lower()}.txt")
    encrypted_path.write_bytes(encrypted)
    decrypted_path.write_bytes(decrypted)
    print(f"{mode_name}: encrypted -> {encrypted_path}; decrypted -> {decrypted_path}; match: {data == decrypted}")
    return data == decrypted


def main() -> None:
    key = "1010000010"
    while True:
        keys = generate_keys(key)
        print("\nS-DES Lab")
        print(f"Key: {key} | K1: {keys[0]} | K2: {keys[1]}")
        print("1. Change key\n2. Create Cyrillic sample file\n3. Process one mode\n4. Compare all five modes\n5. Exit")
        choice = input("Select (1-5): ").strip()
        if choice == "1":
            candidate = input("Enter a 10-bit binary key: ").strip()
            try:
                generate_keys(candidate)
            except ValueError as error:
                print(error)
            else:
                key = candidate
        elif choice == "2":
            sample = "S-DES.\n" * 700
            Path("plaintext.txt").write_text(sample, encoding="utf-8")
            size = Path("plaintext.txt").stat().st_size
            print(f"Created Cyrillic plaintext.txt ({size} bytes). Requirement met: {size >= 30 * 1024}.")
        elif choice in {"3", "4"}:
            path_text = input("Input file [plaintext.txt]: ").strip() or "plaintext.txt"
            path = Path(path_text)
            if not path.is_file():
                print(f"File not found: {path}")
                continue
            if choice == "3":
                print("Modes: " + ", ".join(f"{i}. {name}" for i, name in enumerate(MODES, 1)))
                selected = input("Select mode (1-5): ").strip()
                names = list(MODES)
                if not selected.isdigit() or not 1 <= int(selected) <= len(names):
                    print("Invalid mode selection.")
                    continue
                process_file(path, names[int(selected) - 1], generate_keys(key))
            else:
                for name in MODES:
                    process_file(path, name, generate_keys(key))
        elif choice == "5":
            print("Goodbye.")
            return
        else:
            print("Invalid selection. Choose 1 through 5.")


if __name__ == "__main__":
    main()
