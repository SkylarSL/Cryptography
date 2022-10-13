
# integer to binary
def itob(x, i):
    return format(x, "0"+str(i)+"b")

# binary to integer
def btoi(x):
    return int(x, 2)

# inverse s-box
isBox = [14, 3, 4, 8, 1, 12, 10, 15, 7, 13, 9, 6, 11, 2, 0, 5]


cipherText = open("a2\cipher2.txt", "r")
keyText = open("a2\key.txt", "r")

cipherTextLines = cipherText.readlines()
keyTextLines = keyText.readlines()

deltau = "0000011000000110"
ucount = ("", 0)

keys = []
for key in keyTextLines:
    count = 0
    for line in cipherTextLines:
        x, xprime, y, yprime = line.split(",")
        
        y1 = y[4:8]
        y2 = y[12:16]
        yprime1 = yprime[4:8]
        yprime2 = yprime[12:16]
        key1 = key[0:4]
        key2 = key[4:8]

        y1Int = btoi(y1)
        y2Int = btoi(y2)
        yprime1Int = btoi(yprime1)
        yprime2Int = btoi(yprime2)
        key1Int = btoi(key1)
        key2Int = btoi(key2)

        v1 = y1Int ^ key1Int
        v2 = y2Int ^ key2Int
        vprime1 = yprime1Int ^ key1Int
        vprime2 = yprime2Int ^ key2Int

        u1 = isBox[v1]
        u2 = isBox[v2]
        uprime1 = isBox[vprime1]
        uprime2 = isBox[vprime2]

        deltau1 = u1 ^ uprime1
        deltau2 = u2 ^ uprime2

        deltau1Bin = itob(deltau1, 4)
        deltau2Bin = itob(deltau2, 4)

        deltauTest = "0000" + deltau1Bin + "0000" + deltau2Bin

        if(deltauTest == deltau):
            count += 1

    keys.append(count)
    if(count >= ucount[1]):
        ucount = (key, count)

print(ucount)
keys.sort(reverse=True)
print(keys)
