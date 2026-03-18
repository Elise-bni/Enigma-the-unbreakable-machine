def enigma_initialization():
    """
    @brief Return raw elements
    @return dict[int,str],dict[int,str],dict[int,str],dict[int,str],str : available reflectors, rotors (their respective reference and notch), reflector
    """
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
    raw_reflectors = {'A':"EJMZALYXVBWFCRQUONTSPIKHGD",
              'B':"YRUHQSLDPXNGOKMIEBFZCWVJAT"}
    reference = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    return raw_rotors,raw_rotors_ref,raw_notches,raw_reflectors,reference

def find_index(L:list[str],e:str):
    """
    @brief Return the index at which the element can be found
    @param L : rotor
    @param e : value to find
    @return int : i such as L[i]=e
    """
    for i in range(len(L)):
        if L[i]==e:
            return i
    return None

def rotate_rotor(rotor:list[str], position:int):
    """
    @brief split rotor at index, swap sublists and concatenate
    @param rotor : rotor
    @param position : 0 <= position < len(rotor)
    @return list[str] : new rotor
    """
    return rotor[position:] + rotor[:position]

def initialize_connection_array(L:list[tuple[str]]):
    """
    @brief creates a new rotor and swap the connected letters    
    @param L : list of connected letters (cables on the actual machine)
    @return list[str] : new rotor
    """
    T=[chr(i) for i in range(65,91)]
    for e in L:
        a,b=e
        j,k=ord(a)-65,ord(b)-65
        T[j],T[k]=T[k],T[j]       
    return ''.join(T)

def used_parts(rotor_orders:str,ini_rotors_position:str,\
    reflector:str,raw_rotors:dict[str],raw_rotors_ref:dict[str],\
    raw_notches:dict[str],raw_reflectors:dict[str]):
    """
    @brief return the selected elements
    @param rotor_orders : order of the rotors in the machine
    @param ini_rotors_position : letter at the top of each rotor in the machine
    @param reflector : used reflector
    @param raw_rotors : set of rotors which can be used
    @param raw_rotors_ref : identical to raw_rotors, used for reference in operations
    @param raw_notches : position at which the rotor turns the one to its left
    @param raw_reflectors : set of reflectors which can be used
    @return list[str],list[str],str,str : used rotors,rotors_ref, reflector and notches
    """
    rotors=[]
    rotors_ref=[]
    lr,mr,rr=int(rotor_orders[0]),int(rotor_orders[1]),int(rotor_orders[2])
    ini_index=\
        {lr:find_index(raw_rotors_ref[lr],ini_rotors_position[0]),
        mr:find_index(raw_rotors_ref[mr],ini_rotors_position[1]),
        rr:find_index(raw_rotors_ref[rr],ini_rotors_position[2])}
    for i in [lr,mr,rr]:
        rotors.append(rotate_rotor(raw_rotors[i],ini_index[i]))
        rotors_ref.append(rotate_rotor(raw_rotors_ref[i],ini_index[i]))
    used_reflector=raw_reflectors[reflector]
    used_notches=\
        raw_notches[int(rotor_orders[0])]+raw_notches[int(rotor_orders[1])]+\
        raw_notches[int(rotor_orders[2])]
    return rotors,rotors_ref,used_reflector,used_notches

def rotation(rotors:list[str],rotors_ref:list[str],notches:dict):
    """
    @brief turn the right rotor (and any driven ones)
    @param rotors : used rotors
    @param rotors_ref : reference rotors of the used ones
    @param notches : position at which the rotor turns the one to its left
    @return tupl[list[list[str]] : new rotors and rotors:ref
    """
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
    """
    @brief Double stepping means that the middle rotor moves forward twice in a row: 
        once because the right rotor pushes it, 
        and then a second time because it is itself 
        in its slot and thus also drives the left rotor.
        This function replicates this principle.
    @param rotors : used rotors
    @param rotors_ref : reference rotors of the used ones
    @param notches : position at which the rotor turns the one to its left
    @return tupl[list[list[str]] : new rotors and rotors:ref    
    """
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

def Enigma(message:str,rotors_order:str,ini_rotors_position:str,reflector:str,\
            connection_array:list[tuple[str]]):
    """
    @brief act as an Enigma machine
    @param message : message to encrypt
    @param rotors_order : order of the rotors in the machine
    @param ini_rotors_position : letter at the top of each rotor in the machine
    @param reflector : used reflector
    @param connection_array : list of connected letters
    @return encoded message
    """
    raw_rotors,raw_rotors_ref,raw_notches,raw_reflectors,reference=enigma_initialization()
    rotors,rotors_ref,reflector,notches=used_parts(rotors_order,ini_rotors_position,\
                        reflector,raw_rotors,raw_rotors_ref,raw_notches,raw_reflectors)
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
            num=ord(reference[index])-65
            char=connections[num]
            code=code+reference[index]
            rotors,rotors_ref=double_stepping(rotors,rotors_ref,notches)
    return code

#############################################################
#                                                           #
#  Example of use :                                         #
#                                                           #
#  print(Enigma("HELLOWORLD","231","EQL","B",[('E','F')]))  #
#                                                           #
#############################################################