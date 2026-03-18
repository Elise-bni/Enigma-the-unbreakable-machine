import encryption
import time
   
permutations=["123","213","312","132","231","321","124","214","412","142","241","421","125","215","512","152","251","521","134","314","413","143","341","431","135","315","513","153","351","531","145","415","514","154","451","541","234","324","423","243","342","432","235","325","523","253","352","532","245","425","524","254","452","542","345","435","534","354","453","543"] 
   
def ascending_counter(lc:int,mc:int,rc:int,n):
    """
    @brief increase the base n counter
    @param lc : left counter
    @param mc : middle counter
    @param rc : right counter
    @param n : counter base
    @return int : new state of the counter
    """
    if rc==n:
        if mc==n:
            lc+=1
        mc+=1
    rc+=1
    return lc%(n+1),mc%(n+1),rc%(n+1)   
   
def descending_counter(lc:int,mc:int,rc:int,n):
    """
    @brief decrease the base n counter
    @param lc : left counter
    @param mc : middle counter
    @param rc : right counter
    @param n : counter base
    @return int : new state of the counter
    """
    if lc==0 and mc==0 and rc==0:
        lc,mc,rc=n,n,n
    elif mc==0 and rc==0:
        lc-=1
        mc,rc=n,n
    elif rc==0:
        mc-=1
        rc=n
    else:
        rc-=1
    return lc,mc,rc

def get_ini_rotors_settings(rotor_code:str,message_length:int,magic_word_length:int): 
    """
    @brief return the initial setting of the machine before the encryption of the message
    @param rotor_code : rotor setting read on the machine after message encryption
    @param message_length : length of the crypted message
    @param magic_word_length : length of the word for which the decrypted version is known
    @return str : rotor setting
    """
    counter=(ord(rotor_code[0])-65,ord(rotor_code[1])-65,ord(rotor_code[2])-65)
    for _ in range(message_length-magic_word_length):
        counter=descending_counter(counter[0],counter[1],counter[2],25)
    return chr(counter[0]+65)+chr(counter[1]+65)+chr(counter[2]+65)

def decryption(message:str,decryption_mode:int,permutations:list[int]):
    """
    @brief decrypt the message using the chosen mode
    @param message : message to decode
    @param decryption_mode : method used to parse the permutation list :
            1: from beginning to end
            2: from end to beginning
            3: from the edges to the center
    @param permutations : List of all permutations with 5 rotors and 3 slots
    @return float : time to find the encryption key    
    """
    initial_time=time.perf_counter()
    if decryption_mode == 1 or decryption_mode == 3:
        txt1=""
        initial_magic_word=message.split()[0]
    if decryption_mode == 2 or decryption_mode == 3:
        txt2=""
        final_magic_word=message.split()[-1]
        chain_length=len(message.replace(" ",""))
        final_magic_word_length=len(final_magic_word) 
    for order in range(len(permutations)):
        lc,mc,rc=0,0,0
        while (lc,mc,rc)!=(25,25,25):
            rotors_code=chr(65+lc)+chr(65+mc)+chr(65+rc)      
            if decryption_mode == 1 or decryption_mode == 3:
                txt1=encryption.Enigma(initial_magic_word,permutations[order],\
                    rotors_code,"B",[],encryption.initialisation_enigma())
                if txt1 == "METEO":
                    final_time=time.perf_counter()-initial_time
                    return final_time
            if decryption_mode == 2 or decryption_mode == 3:
                txt2=encryption.Enigma(final_magic_word,permutations[-order-1],\
                    rotors_code,"B",[],encryption.initialisation_enigma())
                if txt2 == "CHANCELIER":
                    final_time=time.perf_counter()-initial_time
                    rotor_encryption_position=get_ini_rotors_settings(rotors_code,chain_length,final_magic_word_length)
                    return final_time
            lc,mc,rc=ascending_counter(lc,mc,rc,25)
    return None

def graph_values_generation(mode:int): # This function takes a LOT of time to generate all the values so they are provided directly in the graph.py file.
    """
    @brief generate the y values to plot a graph of the decryption time
    @param mode : mode of decryption
    @return list[float] : decryption times    
    """
    y=[]
    for i in range(len(permutations)):
        message = encryption.Enigma("WETTER KANZLER",permutations[i],"AAA","B",[])
        t = decryption(message,mode)
        y.append(t)
    return y