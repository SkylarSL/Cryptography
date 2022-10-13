from cgitb import reset
from secrets import randbits
import string

map = {
    "_": 0, 
    "A": 1, 
    "B": 2, 
    "C": 3, 
    "D": 4, 
    "E": 5, 
    "F": 6, 
    "G": 7, 
    "H": 8, 
    "I": 9, 
    "J": 10, 
    "K": 11, 
    "L": 12, 
    "M": 13, 
    "N": 14, 
    "O": 15, 
    "P": 16, 
    "Q": 17, 
    "R": 18, 
    "S": 19, 
    "T": 20, 
    "U": 21, 
    "V": 22, 
    "W": 23, 
    "X": 24, 
    "Y": 25, 
    "Z": 26
}

c1 = "POGINSRBXCYVRMXBACWUUXOCLUEOGJUTQKNWYXKVTTGVXTJBWXMJVMMQSGWKZOFYUYTEBOGSZBERFIJJUR__MWLMKZSLKBADUXPBEWRECMYGLZLAHIP_GHNLRCGXBHZVKYS__SYSRUUJQRHSHTSPLAWVYOVPJDRYAOEUQPJ_WCNAOZPTSKJUVZHXRLFHIRAXLIZYZOUIRXXZVAB_M_SDCUCOVKN"
c2 = "TUQMIRBQYCNOQASDWTRUVPSUIUCCAHWCVOARNBGFIVPVJBJ_ZBEAKDBDGDUKSJGMNJ_UXQWKZLATAZGVFQASYC_BZAL_XOXCTUKBUKAIOWZQIYQPJHIENS_FDEFFQVZTQUOVMSXEUOCSBJBRGTFPYBHME_BAJACLPTNHYKBVJJVFCGF_DWLHVNLHZTXGGNLJVCYCZOOMUVQVWMBVGCLNYXKNBUW"
m1 = "YOU_CAN_T_BLAME_THEM_SAID_DUMBLEDORE_GENTLY_WE_VE_HAD_PRECIOUS_LITTLE_TO_CELEBRATE_FOR_ELEVEN_YEARS_I_KNOW_THAT_SAID_PROFESSOR_MCGONAGALL_IRRITABLY_BUT_THAT_S_NO_REASON_TO_LOSE_OUR_HEADS_PEOPLE_ARE_BEING_DOWNRIGHT_CAREL"
m2 = "BUDDY_YOU_RE_A_BOY_MAKE_A_BIG_NOISE_PLAYING_IN_THE_STREET_GONNA_BE_A_BIG_MAN_SOMEDAY_YOU_GOT_MUD_ON_YOUR_FACE_YOU_BIG_DISGRACE_KICKING_YOUR_CAN_ALL_OVER_THE_PLACE_SINGIN_WE_WILL_WE_WILL_ROCK_YOU_WE_WILL_WE_WILL_ROCK_YOU"
k =  "R_MIKRDBDCWJQ_SBHVRHUENUHUAUUHIOMWWRYQFH_HIVAOJGRXEIRMXZNDNWEWFMLE_TXONDZZ_FAGSIAM_UYELHZUXGXBCZTFXBWWGROQYNDYSAPHGWGSWXLYOENQZIHRDMZLXGFULSZIORFHUPJGCVEGUWJLRKMONPPXVMWJZACKXOSWPCVRCWNTFSDCLLGIYGUOSDIJQZRMFMVRLWJU_NDFB"

#used for all parts, a), b), c)
def shift(text:string, i: int) -> string:
    temp = i % len(text)
    res = text[temp : ] + text[ : temp]
    return res

#used for part a)
def enc(text: string, key: string) -> string:
    new_text = ""
    j=0
    for i in text:
        pt_letter_map = map[i]
        key_letter_map = map[key[j]]
        enc_letter = (pt_letter_map + key_letter_map) % 27
        new_letter = [i for i in map if map[i] == enc_letter]
        new_text += new_letter[0]
        j += 1
    return new_text

#used for all parts, a), b), c)
def dec(text: string, key: string) -> string:
    new_text = ""
    j=0
    for i in text:
        pt_letter_map = map[i]
        key_letter_map = map[key[j]]
        enc_letter = (pt_letter_map - key_letter_map)
        if enc_letter < 0:
            enc_letter += 27
        new_letter = [i for i in map if map[i] == enc_letter]
        new_text += new_letter[0]
        j += 1
    return new_text

#used for b), c)
def find_text(m: string, ctext: string) -> string:
    ctext_msg = ctext
    for i in range(len(m)):
        dec_text = dec(ctext_msg, m)
        print(dec_text + "\n")
        ctext_msg = shift(ctext_msg, 1)
    return 0

#used for c)
def find_key(m1: string, c1: string, m2: string, c2: string) -> string:
    c1_msg = c1
    c2_msg = c2
    for i in range(len(m1)):
        dec_text1 = dec(c1_msg, m1)
        dec_text2 = dec(c2_msg, m2)
        print(dec_text1)
        print(dec_text2 + "\n")
        c1_msg = shift(c1_msg, 1)
        c2_msg = shift(c2_msg, 1)
    return 0

#c1_c2 = dec(c1, c2)
#find_text(c1_c2, m1)

#find_key(m1, c1, m2, c2)

#get the key using m
find_text(m2, c2)
#test the key on m1
find_text(k, c1)

#get the key using m
find_text(m1, c1)
#test the key on m1
find_text(k, c2)

'''
c1 = m1 + k
c2 = m2 + k

k = c1 - m1
k = c2 - m2

c1 - m1 = c2 - m2

c1 - c2 = m1 - m2

m2 = m1 - (c1 - c2)


LOSE_OUR_HEADS exists because we got _WILL_WE_WILL_

k = CKXOSWPCVRCWNT


process to decrypt: Realized m2 was lyrics. Fill in the lyrics appropriately for m2. Use a program that get the key using the equation: k = c2 - m2. Using that key, test out with m1 to see if you get coherent text by using: m1 = c1 - k. This is usually completed by trial and error, but since I knew the lyrics and love Queen, it was more efficient.
'''