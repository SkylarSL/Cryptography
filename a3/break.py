import hashlib

hash = "ceb1cd859c180e8f7f7b2d325d1c3e32d096be04c36a0bf6652052720ad149b4"

for i in range(0, 999999):
    s = "69908278" + str(i)
    tmphash = hashlib.sha256(s.encode()).hexdigest()
    if(tmphash == hash):
        print(s)
        break

#alice's password 69908278759669


hash = "aa841766218cbfe1c4e165c022047b9cc8bef364c3c184b4b496908f91c2f6f8"

wordlist = open("wordlist.txt", "r")
wordlist = wordlist.readlines()
count = 0
for word in wordlist:
    length = len(word)-1
    minnumlength = pow(10, (11-length-1))-1
    maxnumlength = pow(10, (11-length))
    for i in range(minnumlength, maxnumlength):
        for j in ("!", "?", "$", "#", "&"):
            s = word.capitalize()[:-1] + str(i) + j
            s = "74364533" + s
            tmphash = hashlib.sha256(s.encode()).hexdigest()
            if(tmphash == hash):
                print(s)
                print(count)
                break
            count += 1

#alice's password: 74364533Offshore696&
#count: 43900249

'''
d)
worst case scenario an attacker would have the bruteforce, and a brute force attack
would take 20000*20000*9*9*9*6 = 1,749,600,000,000 possible combinations. My program
in part c took about 43,900,249 hashes to find Alice's password. This new strategy
is better for Alice because it is much harder to bruteforce; assuming that Alice's
new password can not be patternized and is completely random.

e)
it would take 0.01 seconds to crack Alices password, using the strategy in part d)

f)
Look at password hashing slides.
'''