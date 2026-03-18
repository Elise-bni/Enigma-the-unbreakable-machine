def find_index(L,e):
    for i in range(len(L)):
        if L[i]==e:
            return i
    return None

def rotate_rotor(rotor, position):
    return rotor[position:] + rotor[:position]

rotor = {1:"EKMFLGDQVZNTOWYHXUSPAIBRCJ",
       2:"AJDKSIRUXBLHWTMCQGZNPYFVOE",
       3:"BDFHJLCPRTXVZNYEIWGAKMUSQO",
       4:"ESOVPZJAYQUIRHXLNFTGKDCMWB",
       5:"VZBRGITYUPSDNHLXAWMJQOFECK"}

rotor_ref={1:"ABCDEFGHIJKLMNOPQRSTUVWXYZ",
       2:"ABCDEFGHIJKLMNOPQRSTUVWXYZ",
       3:"ABCDEFGHIJKLMNOPQRSTUVWXYZ",
       4:"ABCDEFGHIJKLMNOPQRSTUVWXYZ",
       5:"ABCDEFGHIJKLMNOPQRSTUVWXYZ"}

notches={1:'Q',
       2:'E',
       3:'V',
       4:'J',
       5:'Z'}

reference = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

reflector = "YRUHQSLDPXNGOKMIEBFZCWVJAT"

rotor_order="123"
initialisation= "MCL"

index_ini={1:find_index(rotor_ref[1],initialisation[0]),
            2:find_index(rotor_ref[2],initialisation[1]),
            3:find_index(rotor_ref[3],initialisation[2])}

for i in range(1,4):
    rotor[i]=rotate_rotor(rotor[i],index_ini[i])
    print(rotor[i])
    rotor_ref[i]=rotate_rotor(rotor_ref[i],index_ini[i])
    print(rotor_ref[i])

message="HELLO"
trad=""

for k in range(len(message)):
    carac=message[k]

    index=find_index(reference,carac)
    # print(index)

    for i in range(3,0,-1):
        letter=rotor[i][index]
        # print(letter)
        index=find_index(rotor_ref[i],letter)
        # print(index)
        
    letter=reflector[index]
    # print(letter)
    index=find_index(reference,letter)
    # print(index)

    for i in range(1,4):
        letter=rotor_ref[i][index]
        # print(letter)
        index=find_index(rotor[i],letter)
        # print(index)
        
    trad=trad+reference[index]
    
    rotor[3]=rotate_rotor(rotor[3],1)
    rotor_ref[3]=rotate_rotor(rotor_ref[3],1)
    
print(trad)

"""
TODO
Code the section involving rotor rotations at the beginning of the loop:
    - Rotate the right rotor systematically
    - Check if the target position has been reached to rotate the middle rotor and, if necessary, the left rotor
"""

"""
TODO
Ensure that any rotor can be placed in any order:
    A string containing the rotor numbers in order (rotor_order), with two options—see which one works:
        - Loop over j to access rotor_order[j]: unlikely to work for long messages
        - j counter modulo 3 (number of rotors) incremented with each letter encoding to access rotor_order[j]
"""
