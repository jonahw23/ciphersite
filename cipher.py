"""
CSAPX Lab 1: Ciphers

A program that encodes/decodes a message by applying a set of transformation operations.
The transformation operations are:
    shift - Sa[,n] changes letter at index a by moving it n letters fwd in the alphabet. A negative
        value for n shifts the letter backward in the alphabet.
    rotate - R[n] rotates the string n positions to the right. A negative value for n rotates the string
        to the left.
    duplicate - Da[,n] follows character at index a with n copies of itself.
    trade - Ta,b swap the places of the a-th and b-th characters.
    
-------------------------------------------------------------------------
Note: There are optional experimental features included in this project.
Toggle the boolean variables to allow/disallow them.

duplicate_undoable (bool): allows for the "duplicate" transformation to be undone in the decrypting process. Project default: True
sanitized_input (bool): tests whether the user-input message and transformation strings are roughly in correct form. Project default: True
-------------------------------------------------------------------------

All indices numbers (the subscript parameters) are 0-based.

author: Jonah Witte
"""

def shift(msg, index, amount):
    """
    shift():
        Changes the letter at index "index" by shifting it "amount" places forward in the alphabet.

    Args:
        msg (str): the message string
        index (int): the index to be shifted
        amount (int): the amount to be shifted (negative shifts backward in the alphabet)

    Returns:
        str: the message with one character shifted
    """
    if index == len(msg) - 1:
        return msg[0:index] + chr((ord(msg[index]) - 65 + amount) % 26 + 65)
    return msg[:index] + chr((ord(msg[index]) - 65 + amount) % 26 + 65) + msg[index + 1 : ]

def rotate(msg, amount):
    """
    rotate():
        rotates the string "amount" places to the right

    Args:
        msg (str): the message string
        amount (int): the amount to be rotated (negative rotates to the left)

    Returns:
        str: the message after "amount" rotations
    """
    for i in range(abs(amount)):
        if(amount > 0):
            msg = msg[-1] + msg[0:-1]
        else:
            msg = msg[1:] + msg[0]
    return msg

def duplicate(msg, index, amount):
    """
    duplicate():
        duplicates the character at index "index" "amount" times

    Args:
        msg (str): the message string
        index (int): the index of the character to be duplicated
        amount (int): the number of times to duplicate the character (or remove characters if negative)

    Raises:
        Exception: if undoing the duplicate operation is not allowed, it throws an error

    Returns:
        str: the string after duplications
    """
    duplicate_undoable = True # change to False if duplicates cannot be decrypted
    if amount < 1:
        if duplicate_undoable:
            for i in range(abs(amount)):
                msg = msg[:index] + msg[index + 1:]
            return msg
        else:
            raise Exception("Can't decode duplicate")
    if index == len(msg) - 1:
        return msg + msg[-1]
    return msg[:index] + msg[index] * amount + msg[index:]

def trade(msg, index1, index2):
    """
    trade():
        swaps places of the characters at "index1" and "index2"

    Args:
        msg (str): the message string
        index1 (int): the first index to be swapped
        index2 (int): the second index to be swapped

    Returns:
        str: the string after the two characters have been swapped
    """
    strmsg = [*msg]
    strmsg[index1] = msg[index2]
    strmsg[index2] = msg[index1]
    return "".join(strmsg)

def id_operation(opp):
    """
    id_operation():
        takes a operation str "opp" and parses it to determine the operation + any arguments

    Args:
        opp (str): an operation str in the form given by the assignment (ex: 'S1,2')

    Returns:
        tuple: a tuple where tuple[0] is the operation name, and other even-numbered indexes are arguments for that operation (as strings)
    """
    opp_name = None
    index = None
    amount = None
    if opp[0] == "S":
        opp_name = "shift"
        if(opp.find(",") > -1):
            index = opp[1:opp.find(",")]
            amount = opp[opp.find(",") + 1:]
        else:
            index = opp[1:]
            amount = 1
        return opp_name, "index", index, "by amount", amount 
    elif opp[0] == "R":
        opp_name = "rotate"
        amount = 1
        if(len(opp) > 1):
            amount = opp[1:]
        return opp_name, "by amount", amount 
    elif opp[0] == "D":
        opp_name = "duplicate"
        if(opp.find(",") > -1):
            index = opp[1:opp.find(",")]
            amount = opp[opp.find(",") + 1:]
        else:
            index = opp[1:]
            amount = 1
        return opp_name, "index", index, "by amount", amount
    elif opp[0] == "T":
        opp_name = "trade"
        index1 = opp[1:opp.find(",")]
        index2 = opp[opp.find(",") + 1:]
        return opp_name, "index1", index1, "index2", index2
    
def transform(dir, msg, cmd):
    """
    transform():
        given a message string "msg", a direction "dir" and a list of transformations "cmd", it executes the given transformations on the "msg" string

    Args:
        dir (str): should be either "D" or "E", controls whether the function decrypts or encrypts
        msg (str): the message string
        cmd (str): the list of transfomations in the form given by the lab (ex: 'T2,4;S4;R')

    Returns:
        str: the message string after all transformations are executed
    """
    cmds = cmd.split(";")
    if dir == "D":
        # Decrypting mode, run transformations in reverse
        cmds.reverse()
        for trans in cmds:
            opplist = id_operation(trans)
            if opplist[0] == "shift":
                msg = shift(msg, int(opplist[2]), -int(opplist[4]))
            if opplist[0] == "rotate":
                msg = rotate(msg, -int(opplist[2]))
            if opplist[0] == "duplicate":
                msg = duplicate(msg, int(opplist[2]), -int(opplist[4]))
            if opplist[0] == "trade":
                msg = trade(msg, int(opplist[2]), int(opplist[4]))
    if dir == "E":
        # Encrypting mode
        for trans in cmds:
            opplist = id_operation(trans)
            if opplist[0] == "shift":
                msg = shift(msg, int(opplist[2]), int(opplist[4]))
            if opplist[0] == "rotate":
                msg = rotate(msg, int(opplist[2]))
            if opplist[0] == "duplicate":
                msg = duplicate(msg, int(opplist[2]), int(opplist[4]))
            if opplist[0] == "trade":
                msg = trade(msg, int(opplist[2]), int(opplist[4]))
    return msg

def check_well_formed_msg(str):
    """
    check_well_formed_msg():
        tests whether or not the message input is in the correct form

    Args:
        str (str): the message string

    Returns:
        bool: True if the string contains only capital letters, otherwise False
    """
    for s in str:
        if ord(s) > 90 or ord(s) < 65:
            return False
    return True

def check_well_formed_trans(str):
    """
    check_well_formed_trans
        tests whether or not the transformation is in the correct form

    Args:
        str (str): the message string

    Returns:
        bool: True if the transformation contains only allowed characters, otherwise False. 
    """
    cmds = str.split(";")
    for trans in cmds:
        # print(trans)
        if len(trans) < 1:
            return False
        if trans[0] not in ("S", "R", "D", "T"):
            return False
        if trans.find(",") > 1:
            # If there's a comma
            if trans[0] == "R":
                return False
            if (not (trans[1:trans.find(",")].isnumeric())) and not(trans[2:trans.find(",")].isnumeric() and trans[1] == "-"):
                # Between the letter and the comma is not a number
                return False
            if (not (trans[trans.find(",") + 1:].isnumeric())) and not(trans[trans.find(",") + 2:].isnumeric() and trans[trans.find(",") + 1] == "-"):
                # Between the comma and the end is not a number
                return False
        elif (not (trans[1:].isnumeric())) and not(trans[2:].isnumeric() and trans[1] == "-"):
            return False
    return True

def main() -> None:
    """
    The main loop responsible for getting the input details from the user
    and printing in the standard output the results
    of encrypting or decrypting the message after applying the transformations
    
    Returns: 
        None
    """
    sanitized_input = False # If input is guaranteed to be sanitized, can be set to True for time-saving
    live = True
    while(live):
        direction = input("Enter operation: (E)ncrypt, (D)ecrypt or (Q)uit? ")
        well_formed = False
        if direction == "E" or direction == "D":
            while(not well_formed):
                message = input("Enter message to be encryped/decrypted: ")
                if(not check_well_formed_msg(message) and not(sanitized_input)):
                    print("Please enter a message consisting of only capital letters.")
                else:
                    well_formed = True
            commands = input("Enter encryption/decryption transformations: ")
            if(not sanitized_input):
                well_formed = check_well_formed_trans(commands)
            while(not well_formed):
                print("Please see transformation string guidelines for correct input syntax.")
                commands = input("Enter encryption/decryption transformations: ")
                well_formed = check_well_formed_trans(commands)
            new_msg = transform(direction, message, commands)
            print("Transformed message:", new_msg)
        if(direction == "Q"):
            live = False
            print("Exiting")


if __name__ == '__main__':
    main()
