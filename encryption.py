raw_rotors = {1:"EKMFLGDQVZNTOWYHXUSPAIBRCJ",
       2:"AJDKSIRUXBLHWTMCQGZNPYFVOE",
       3:"BDFHJLCPRTXVZNYEIWGAKMUSQO",
       4:"ESOVPZJAYQUIRHXLNFTGKDCMWB",
       5:"VZBRGITYUPSDNHLXAWMJQOFECK"}

raw_rotors_ref={1:"ABCDEFGHIJKLMNOPQRSTUVWXYZ",
       2:"ABCDEFGHIJKLMNOPQRSTUVWXYZ",
       3:"ABCDEFGHIJKLMNOPQRSTUVWXYZ",
       4:"ABCDEFGHIJKLMNOPQRSTUVWXYZ",
       5:"ABCDEFGHIJKLMNOPQRSTUVWXYZ"}

raw_notches={1:'Q',
       2:'E',
       3:'V',
       4:'J',
       5:'Z'}

reference = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

raw_reflectors = {'A':"EJMZALYXVBWFCRQUONTSPIKHGD",
              'B':"YRUHQSLDPXNGOKMIEBFZCWVJAT"}

def find_index(L:list[str],e:str):
    for i in range(len(L)):
        if L[i]==e:
            return i
    return None

def rotate_rotor(rotor:list[str], position:int):
    return rotor[position:] + rotor[:position]

def initialize_connection_array(L:list[tuple[str]]):
    T=[chr(i) for i in range(65,91)]
    for e in L:
        a,b=e
        j,k=ord(a)-65,ord(b)-65
        T[j],T[k]=T[k],T[j]       
    return ''.join(T)

def used_parts(rotor_orders:str,ini_rotors_position:str,reflector:str,raw_rotors:dict[str],raw_rotors_ref:dict[str],raw_notches:dict[str],raw_reflectors:dict[str]):
    rotors=[]
    rotors_ref=[]
    r1,r2,r3=int(rotor_orders[0]),int(rotor_orders[1]),int(rotor_orders[2])
    ini_index={r1:find_index(raw_rotors_ref[r1],ini_rotors_position[r1-1]),
                r2:find_index(raw_rotors_ref[r2],ini_rotors_position[r2-1]),
                r3:find_index(raw_rotors_ref[r3],ini_rotors_position[r3-1])}
    for i in range(3):
        rotors.append(rotate_rotor(raw_rotors[int(rotor_orders[i])],ini_index[i+1]))
        rotors_ref.append(rotate_rotor(raw_rotors_ref[int(rotor_orders[i])],ini_index[i+1]))
    used_reflector=raw_reflectors[reflector]
    used_notches=raw_notches[int(rotor_orders[0])]+raw_notches[int(rotor_orders[1])]+raw_notches[int(rotor_orders[2])]
    return rotors,rotors_ref,used_reflector,used_notches

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

def double_stepping(rotors:list[str],rotors_ref:list[str],notches:dict[str]):
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

def Enigma(message:str,rotors_order:str,ini_rotors_position:str,reflector:str,raw_rotors:dict[str],raw_rotors_ref:dict[str],raw_notches:dict[str],raw_reflectors:dict[str],connection_array:list[tuple[str]],reference:str):
    rotors,rotors_ref,reflector,notches=used_parts(rotors_order,ini_rotors_position,reflector,raw_rotors,raw_rotors_ref,raw_notches,raw_reflectors)
    connections=initialize_connection_array(connection_array)
    code=""
    for k in range(len(message)):
        char=message[k]
        if char==' ':
            code=code+' '
        else:
            rotors,rotors_ref=rotation(rotors,rotors_ref,notches)
            num=ord(char)-65
            char=connections[num]
                       
            index=find_index(reference,char)
            for i in range(2,-1,-1):
                letter=rotors[i][index]
                index=find_index(rotors_ref[i],letter)              
            letter=reflector[index]
            index=find_index(reference,letter)
            for i in range(3):
                letter=rotors_ref[i][index]
                index=find_index(rotors[i],letter)
            print(rotors_ref, reference[index])   
            
            num=ord(reference[index])-65
            char=connections[num]
            
            code=code+reference[index]
            rotors,rotors_ref=double_stepping(rotors,rotors_ref,notches)
    return code

print(Enigma("HELLO WORLD","231","EQL","B",raw_rotors,raw_rotors_ref,raw_notches,raw_reflectors,[('E','F')],reference))

"""
TODO
Encoding the position of the rings: rotating the reference lists without rotating the base lists?
"""