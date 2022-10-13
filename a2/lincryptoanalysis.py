
# keyFile = open("a2\key2.txt", "w")
# for i in range(65536):
#     keyFile.write(format(i, "08b") + "\n")

# convert binary to int: int("<bin>", 2)

# integer to binary
def itob(x, i):
    return format(x, "0"+str(i)+"b")

# binary to integer
def btoi(x):
    return int(x, 2)

# s-box
sBox = [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7]
# inverse s-box
isBox = [14, 3, 4, 8, 1, 12, 10, 15, 7, 13, 9, 6, 11, 2, 0, 5]

plainTextFile = open("a2\plain.txt", "r")
cipherTextFile = open("a2\cipher.txt", "r")
keyTextFile = open("a2\key.txt", "r")

plainText = plainTextFile.readlines()
cipherText = cipherTextFile.readlines()
keyText = keyTextFile.readlines()

key = "01110110"

counter = [0, 0]

for (ptext, ctext) in zip(plainText, cipherText):

    subKey1 = key[0:4]
    subKey2 = key[4:8]
    subCiph1 = ctext[4:8]
    subCiph2 = ctext[12:16]

    subKey1Int = btoi(subKey1)
    subKey2Int = btoi(subKey2)
    subCiph1Int = btoi(subCiph1)
    subCiph2Int = btoi(subCiph2)

    v1Int = subKey1Int ^ subCiph1Int
    v2Int = subKey2Int ^ subCiph2Int

    u1Int = isBox[v1Int]
    u2Int = isBox[v2Int]

    u1Bin = itob(u1Int, 4)
    u2Bin = itob(u2Int, 4)

    uValue = u1Bin[1] + u1Bin[3] + u2Bin[1] + u2Bin[3]

    bias = int(ptext[4]) ^ \
        int(ptext[6]) ^ \
        int(ptext[7]) ^ \
        int(uValue[0]) ^ \
        int(uValue[1]) ^ \
        int(uValue[2]) ^ \
        int(uValue[3])

    counter[bias] += 1

print(counter)
print(abs(counter[0]/20000))

keyBias = [-1, -1]
for key in keyText:
    counter = [0, 0]
    
    for (ptext, ctext) in zip(plainText, cipherText):

        subKey1 = key[0:4]
        subKey2 = key[4:8]
        subCiph1 = ctext[4:8]
        subCiph2 = ctext[12:16]

        subKey1Int = btoi(subKey1)
        subKey2Int = btoi(subKey2)
        subCiph1Int = btoi(subCiph1)
        subCiph2Int = btoi(subCiph2)

        v1Int = subKey1Int ^ subCiph1Int
        v2Int = subKey2Int ^ subCiph2Int

        u1Int = isBox[v1Int]
        u2Int = isBox[v2Int]

        u1Bin = itob(u1Int, 4)
        u2Bin = itob(u2Int, 4)

        uValue = u1Bin[1] + u1Bin[3] + u2Bin[1] + u2Bin[3]

        bias = int(ptext[4]) ^ \
            int(ptext[6]) ^ \
            int(ptext[7]) ^ \
            int(uValue[0]) ^ \
            int(uValue[1]) ^ \
            int(uValue[2]) ^ \
            int(uValue[3])

        counter[bias] += 1
    
    bias = counter[0]/20000
    if(bias > keyBias[1]):
        keyBias = [key, bias]

print(keyBias)


keyBias = ["", -1]
for key in keyText:
    counter = [0, 0]
    
    for (ptext, ctext) in zip(plainText, cipherText):

        subKey1 = key[0:4]
        subKey2 = "0000"
        subKey3 = key[4:8]
        subKey4 = "1111"

        subCiph1 = ctext[0:4]
        subCiph2 = ctext[4:8]
        subCiph3 = ctext[8:12]
        subCiph4 = ctext[12:16]

        subKey1Int = btoi(subKey1)
        subKey2Int = btoi(subKey2)
        subKey3Int = btoi(subKey3)
        subKey4Int = btoi(subKey4)
        subCiph1Int = btoi(subCiph1)
        subCiph2Int = btoi(subCiph2)
        subCiph3Int = btoi(subCiph3)
        subCiph4Int = btoi(subCiph4)

        v1Int = subKey1Int ^ subCiph1Int
        v2Int = subKey2Int ^ subCiph2Int
        v3Int = subKey3Int ^ subCiph3Int
        v4Int = subKey4Int ^ subCiph4Int

        u1Int = isBox[v1Int]
        u2Int = isBox[v2Int]
        u3Int = isBox[v3Int]
        u4Int = isBox[v4Int]

        u1Bin = itob(u1Int, 4)
        u2Bin = itob(u2Int, 4)
        u3Bin = itob(u3Int, 4)
        u4Bin = itob(u4Int, 4)

        uValue = u1Bin[1] + u2Bin[1] + u3Bin[1] + u4Bin[1]

        bias = int(ptext[0]) ^ \
            int(ptext[3]) ^ \
            int(ptext[8]) ^ \
            int(ptext[11]) ^ \
            int(uValue[0]) ^ \
            int(uValue[1]) ^ \
            int(uValue[2]) ^ \
            int(uValue[3])
            
        counter[bias] += 1
    
    bias = counter[0]/20000
    if(bias > keyBias[1]):
        keyBias = [key, bias]

print(keyBias)