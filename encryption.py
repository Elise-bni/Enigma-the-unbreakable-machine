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

reflectors = {'A':"EJMZALYXVBWFCRQUONTSPIKHGD",
              'B':"YRUHQSLDPXNGOKMIEBFZCWVJAT"}

def find_index(L:list[str],e:str):
    for i in range(len(L)):
        if L[i]==e:
            return i
    return None

def rotate_rotor(rotor:list[str], position:int):
    return rotor[position:] + rotor[:position]

def used_parts(rotor_orders:str,initialization:str,ref:str,notches:dict):
    rotors=[]
    rotors_ref=[]
    index_ini={1:find_index(rotor_ref[1],initialization[0]),
                2:find_index(rotor_ref[2],initialization[1]),
                3:find_index(rotor_ref[3],initialization[2])}
    for i in range(1,4):
        rotors.append(rotate_rotor(rotor[i],index_ini[i]))
        rotors_ref.append(rotate_rotor(rotor_ref[i],index_ini[i]))
    reflector=reflectors[ref]
    notches=notches[int(rotor_orders[0])]+notches[int(rotor_orders[1])]+notches[int(rotor_orders[2])]
    return rotors,rotors_ref,reflector,notches

def rotation(rotors:list[str],rotors_ref:list[str],notches:dict):
    mn,rn=notches[1],notches[2] # middle and right notches
    LR=rotors[0] # left rotor
    MR=rotors[1] # middle rotor
    RR=rotors[2] # right rotor
    LR_ref=rotors_ref[0]
    MR_ref=rotors_ref[1]
    RR_ref=rotors_ref[2]
    RR=rotate_rotor(RR,1)
    RR_ref=rotate_rotor(RR_ref,1)
    if RR_ref[-1]==rn:
        MR=rotate_rotor(MR,1)
        MR_ref=rotate_rotor(MR_ref,1)
        if MR_ref[-1]==mn:
            LR=rotate_rotor(LR,1)
            LR_ref=rotate_rotor(LR_ref,1)
    return [LR,MR,RR],[LR_ref,MR_ref,RR_ref]

def double_stepping(rotors:list[str],rotors_ref:list[str],notches:dict):
    LR=rotors[0]
    MR=rotors[1]
    RR=rotors[2]
    LR_ref=rotors_ref[0]
    MR_ref=rotors_ref[1]
    RR_ref=rotors_ref[2]
    if MR_ref[0]==notches[1]:
        MR=rotate_rotor(MR,1)
        MR_ref=rotate_rotor(MR_ref,1)
        LR=rotate_rotor(LR,1)
        LR_ref=rotate_rotor(LR_ref,1)
    return [LR,MR,RR],[LR_ref,MR_ref,RR_ref]

def Enigma(message:str,rotors_order:str,initialization:str,ref:str,notches:dict):
    rotors,rotors_ref,reflector,notches=used_parts(rotors_order,initialization,ref,notches)  
    code=""
    for k in range(len(message)):
        rotors,rotors_ref=rotation(rotors,rotors_ref,notches)
                
        carac=message[k]
        index=find_index(reference,carac)

        for i in range(2,-1,-1):
            letter=rotors[i][index]
            index=find_index(rotors_ref[i],letter)
            
        letter=reflector[index]
        index=find_index(reference,letter)

        for i in range(3):
            letter=rotors_ref[i][index]
            index=find_index(rotors[i],letter)
            
        # print(rotors_ref, reference[index])
        
        code=code+reference[index]

        rotors,rotors_ref=double_stepping(rotors,rotors_ref,notches)
        
    return code

print(Enigma("HELLOWORLD","123","MDS",'B',notches))

"""
TODO
Ensure that any rotor can be placed in any order:
    A string containing the rotor numbers in order (rotor_order), with two options—see which one works:
        - Loop over j to access rotor_order[j]: unlikely to work for long messages
        - j counter modulo 3 (number of rotors) incremented with each letter encoding to access rotor_order[j]
"""

"""
TODO
Ensure that spaces can be used
"""

"""
TODO
Implement the connection table
"""