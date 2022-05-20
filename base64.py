alphabets = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"

MASK = 63  # 0b111111


def encode(bytes: bytearray):
    pad = 0
    output = ""
    for i in range(0, len(bytes), 3):
        triplet = bytes[i:i+3]
        if len(triplet) == 3:
            n = (triplet[0] << 16) + (triplet[1] << 8) + triplet[2]
        elif len(triplet) == 2:
            n = (triplet[0] << 16) + (triplet[1] << 8)
            pad = 1
        else:
            n = triplet[0] << 16
            pad = 2

        output += alphabets[(n >> 18) & MASK]
        output += alphabets[(n >> 12) & MASK]
        output += alphabets[(n >> 6) & MASK]
        output += alphabets[n & MASK]

    output = (output[0:len(output) - pad] + '='*pad)

    return output


def decode(text: str):
    output = ""
    for i in range(0, len(text), 4):
        quad = text[i:i+4]
        indexes = [alphabets.index(b) for b in quad if b != '=']
        l = len(indexes)
        if l == 4:
            n = (indexes[0] << 18) \
                ^ (indexes[1] << 12) \
                ^ (indexes[2] << 6) \
                ^ indexes[3]
            output += chr(n >> 16)
            output += chr((n >> 8) & 255)
            output += chr(n & 255)
        elif l == 3:
            n = (indexes[0] << 12) \
                ^ (indexes[1] << 6) \
                ^ (indexes[2])
            output += chr(n >> 10)
            output += chr((n >> 2) & 255)
        elif l == 2:
            n = (indexes[0] << 6) ^ indexes[1]
            print(bin(n))
            output += chr(n >> 4)

    return output


if __name__ == '__main__':
    from sys import argv
    if argv[1] == 'encode':
        print(encode(argv[2].encode()))
    elif argv[1] == 'decode':
        print(decode(argv[2]))
