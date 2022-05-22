import binascii
import hashlib
import os
import datetime
import time


def rc4crypt(data, key):
    x = 0
    box = range(256)
    for i in range(256):
        x = (x + box[i] + ord(key[i % len(key)])) % 256
        box[i], box[x] = box[x], box[i]
    x = 0
    y = 0
    out = []
    for char in data:
        x = (x + 1) % 256
        y = (y + box[x]) % 256
        box[x], box[y] = box[y], box[x]
        out.append(chr(ord(char) ^ box[(box[x] + box[y]) % 256]))
    return ''.join(out)


def hasher(data, algorithm="md5"):
    h = hashlib.new(algorithm)
    # print(type(data))
    h.update(data.encode('utf-8'))
    return h.hexdigest()


def getDate():
    dt = str(datetime.datetime.now()).split(' ')[0]
    dstash = dt.split('-')
    dd = dstash[2]
    mm = dstash[1]
    yyyy = dstash[0]
    return int(dd), int(mm), int(yyyy)


def generateSeed(a1, a2, a3):
    result = ''
    v4 = ''
    v5 = 0
    v6 = 0
    v7 = 0
    v8 = "1F1C1F1E1F1E1F1F1E1F1E1F"
    v8 = bytes(bytearray.fromhex(v8))
    # print(v8)
    result = 0
    if (a1 > 0):
        if ((a2 - 1) <= 0xB):
            if ((a3 - 1) <= 0x1E):
                v4 = (a1 & 0x80000003) == 0
                if ((a1 & 0x80000003) < 0):
                    v4 = (((a1 & 0x80000003) - 1) | 0xFFFFFFFC) == -1
                if (v4):
                    v8[11] = chr(0x1D)
                v5 = 0
                if (a2 > 1):
                    v7 = "1F1C1F1E1F1E1F1F1E1F1E1F"  # &v8
                    v6 = a2 - 1
                    i7 = 0
                    while (v6):
                        # print(v7)
                        # print(v7[i7])
                        v5 += ord(str(v7[i7]))  # *v7
                        i7 += 1
                        v6 -= 1
                ecx = 365 * (a1 - (a1 / 4))
                eax = 366 * (a1 / 4)
                result = a3 + v5 + ecx + eax

    return result


def generateString(salt, seed):
    buf = ''
    tmp = "%08x" % seed
    tmp = bytes(bytearray.fromhex(tmp))
    # print(tmp)
    for i in range(4):
        # print(tmp[i])
        buf = str(tmp[i]) + buf
    return buf


def generateDomain(mdhash, length):
    buf = ''
    # print('mdhash:',mdhash)
    for c in mdhash:
        if len(buf) > length:
            return buf
        bl = ord(str(c))
        v1 = "aiou"
        v2 = "aeiouy"
        c1 = "bcdfghjklmnpqrstvwxz"
        c2 = "zxtsrqpnmlkgfdcb"
        edx = 0
        eax = bl
        edi = 0x13
        edx = eax % edi
        bl += 1
        edi = 5
        al = c1[edx]
        buf += al
        eax = bl
        edx = 0
        edx = eax % edi
        bl += 1
        al = v2[edx]
        buf += al
        eax = 2

        if ord(al) == 0x65:

            if bl & 0x07:
                eax = bl
                edi = 3
                edx = 0
                edx = eax % edi
                al = v1[edx]
                buf += al
        else:
            if (bl & 1):
                bl += 1
                eax = bl
                edi = 0x0F
                edx = 0
                edx = eax % edi
                al = c2[edx]
                buf += al
        bl += 1

    return buf


def initDGA(salt, domain_num):
    domains = []
    day, month, year = getDate()
    seed = generateSeed(year, month, day)
    # print(seed)
    seed = generateString(salt, int(seed))  # .decode("hex")
    for i in range(domain_num):
        hashit = hasher(seed)
        domain = generateDomain(hashit, 0x0A)
        seed = ("%08x" % (int(hashit[:8], 16) + 0x01000000))
        domains.append(domain)
        # time.sleep(1)
    return domains


if __name__ == '__main__':
    domain_num = 1000
    domains = initDGA(0, domain_num,)
    for domain in domains:
        print(domain + ".ru")

