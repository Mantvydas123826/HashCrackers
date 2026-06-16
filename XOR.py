#!/usr/bin/env python3
"""
XOR Debugger v3 - Encrypt / Decrypt Mode
"""

import sys
import argparse
from itertools import cycle

def xor(data: bytes, key: bytes) -> bytes:
    """XOR operation (same for encrypt and decrypt)"""
    return bytes(a ^ b for a, b in zip(data, cycle(key)))

def main():
    parser = argparse.ArgumentParser(description="XOR Debugger with Encrypt/Decrypt")
    parser.add_argument("-k", "--key", required=True, help="Key (string or 0xHEX)")
    parser.add_argument("-d", "--data", help="Data as hex string, \\x format, or text")
    parser.add_argument("-i", "--input", help="Input file")
    parser.add_argument("-o", "--output", help="Output file")
    parser.add_argument("--mode", choices=["encrypt", "decrypt"], default="encrypt",
                        help="Mode: encrypt or decrypt (XOR is symmetric)")
    parser.add_argument("--tohex", action="store_true", help="Output as hex")
    parser.add_argument("--text", action="store_true", help="Try to show as text")

    args = parser.parse_args()

    # Parse key
    if args.key.startswith("0x"):
        key = bytes.fromhex(args.key[2:])
    else:
        key = args.key.encode('utf-8', errors='replace')

    print(f"Key     : {key} (len={len(key)})", file=sys.stderr)
    print(f"Mode    : {args.mode.upper()}", file=sys.stderr)

    # Get input data
    if args.data:
        # Clean and detect hex
        raw = args.data.strip()
        clean = raw.replace(" ", "").replace("\\x", "").replace("0x", "").lower()
        if all(c in '0123456789abcdef' for c in clean):
            try:
                data = bytes.fromhex(clean)
                print(f"Input   : {len(data)} bytes (hex parsed)", file=sys.stderr)
            except ValueError:
                data = raw.encode()
        else:
            data = raw.encode()
    elif args.input:
        with open(args.input, "rb") as f:
            data = f.read()
        print(f"Input   : {len(data)} bytes from file", file=sys.stderr)
    else:
        data = sys.stdin.buffer.read()

    # Perform XOR
    result = xor(data, key)

    # Output
    if args.output:
        with open(args.output, "wb") as f:
            f.write(result)
        print(f"✅ Saved {len(result)} bytes to: {args.output}", file=sys.stderr)
    else:
        if args.tohex:
            print(result.hex())
        else:
            try:
                text = result.decode('utf-8', errors='replace')
                if args.text or '\0' not in text[:100]:
                    print(text)
                else:
                    print(result.hex())
            except:
                print(result.hex())

if __name__ == "__main__":
    main()
