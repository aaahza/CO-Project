import sys
from collections import OrderedDict

# binary code of operations
OP_code_typeA = {
    "add": "00000",
    "sub": "00001",
    "mul": "00110",
    "xor": "01010",
    "or": "01011",
    "and": "01100",
    "addf": "10000",
    "subf": "10001"
}
OP_code_typeB = {"mov": "00010", "rs": "01000", "ls": "01001", "movf": "10010"}
OP_code_typeC = {"mov": "00011", "div": "00111",
                 "not": "01101", "cmp": "01110"}
OP_code_typeD = {"ld": "00100", "st": "00101"}
OP_code_typeE = {"jmp": "01111", "jlt": "11100", "jgt": "11101", "je": "11111"}
OP_code_typeF = {"hlt": "11010"}


# binary code of registers
reg_address = {
    "R0": "000",
    "R1": "001",
    "R2": "010",
    "R3": "011",
    "R4": "100",
    "R5": "101",
    "R6": "110",
    "FLAGS": "111",
}

labels = OrderedDict()  # dict of all labels and there addresss

variables = OrderedDict()  # dict of all variables and there addresss

max_imm = 127
max_float = 0b11_111_100
min_float = 0b1
counter = 0b0_000_000  # counter to address the lables and variables
# stores data(dict) about the instructions like op type, and oparands
instructions = []
machine_code = []  # will store the final binary code

# helpers
# functions to find type of the instertion
# these functions may call other functions to check errors

def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False

def is_var(instruction: str) -> bool:
    instruction = instruction.split()
    if len(instruction) != 2:
        return False
    instruction[0].strip()
    if instruction[0] == "var":
        return True
    return False


def is_label(instruction: str) -> bool:
    instruction = instruction.split()
    instruction[0].strip()
    if instruction[0][-1] == ":":
        return True
    return False


def is_typeA(instruction: str) -> bool:
    instruction = instruction.split()
    if len(instruction) != 4:
        return False
    for j, i in enumerate(instruction):
        instruction[j] = i.strip()

    if instruction[0] in OP_code_typeA.keys():
        if instruction[1] == "FLAGS":
            print("ERROR: Illegal use of FLAGS register")
            exit()
        elif instruction[1] in reg_address.keys():
            if instruction[2] == "FLAGS":
                print("ERROR: Illegal use of FLAGS register")
                exit()
            elif instruction[2] in reg_address.keys():
                if instruction[3] == "FLAGS":
                    print("ERROR: Illegal use of FLAGS register")
                    exit()
                elif instruction[3] in reg_address.keys():
                    return True
                else:
                    print("ERROR: Typos in register name")
                    exit()
            else:
                print("ERROR: Typos in register name")
                exit()

        else:
            print("ERROR: Typos register name")
            exit()
    return False


def is_typeB(instruction: str) -> bool:
    instruction = instruction.split()

    if len(instruction) != 3:
        return False
    for j, i in enumerate(instruction):
        instruction[j] = i.strip()

    if instruction[0] in OP_code_typeB.keys():
        if instruction[1] == "FLAGS":
            print("ERROR: Illegal use of FLAGS register")
            exit()
        elif instruction[1] in reg_address.keys():
            if instruction[2][0] == "$":
                if instruction[2][1:].isdigit():
                    instruction[2] = int(instruction[2][1:])
                    if instruction[2] <= max_imm:
                        return True
                    else:
                        print("ERROR: Illegal Immediate values")
                        exit()
                elif isfloat(instruction[2][1:]):
                    instruction[2] = float(instruction[2][1:])
                    if min_float <= instruction[2] <= max_float:
                        return True
                    else:
                        print("ERROR: Illegal Immediate values")
                        exit()
                else:
                    print("ERROR: Illegal Immediate values")
                    exit()
            elif instruction[2] in reg_address.keys():
                return False
            else:
                print("ERROR: Typos in register name")
                exit()
        else:
            print("ERROR: Typos register name")
            exit()
    return False


def is_typeC(instruction: str) -> bool:
    instruction = instruction.split()

    if len(instruction) != 3:
        return False
    for j, i in enumerate(instruction):
        instruction[j] = i.strip()

    if instruction[0] in OP_code_typeC.keys():
        if instruction[1] == "FLAGS":
            print("ERROR: Illegal use of FLAGS register")
            exit()
        elif instruction[1] in reg_address.keys():
            if instruction[2] in reg_address.keys():
                return True
            else:
                print("ERROR: Typos in register name")
                exit()
        else:
            print("ERROR: Typos in register name")
            exit()
    return False


def is_typeD(instruction: str) -> bool:
    instruction = instruction.split()

    if len(instruction) != 3:
        return False
    for j, i in enumerate(instruction):
        instruction[j] = i.strip()

    if instruction[0] in OP_code_typeD.keys():
        if instruction[1] == "FLAGS":
            print("ERROR: Illegal use of FLAGS register")
            exit()
        elif instruction[1] in reg_address.keys():
            if instruction[2] in labels:
                print("ERROR: Misuse of labels as variables")
                exit()
            elif instruction[2] in variables:
                return True
            else:
                print("ERROR: Use of undefined variables")
                exit()
        else:
            print("ERROR: Typos in register name")
            exit()
    return False


def is_typeE(instruction: str) -> bool:
    instruction = instruction.split()

    if len(instruction) != 2:
        return False
    for j, i in enumerate(instruction):
        instruction[j] = i.strip()

    if instruction[0] in OP_code_typeE.keys():
        if instruction[1] in labels:
            return True
        elif instruction[1] in variables:
            print("ERROR: Misuse of variable as label")
            exit()
        else:
            print("ERROR: Use of undefined labels")
            exit()
    return False


def is_typeF(instruction: str) -> bool:
    if instruction.split()[0] in OP_code_typeF.keys():
        return True
    else:
        return False


def handle_variable(instruction: str):  # add the variable to the odered dict
    instruction = instruction.split()
    for i in instruction:
        i.strip()
    variables[instruction[1]] = None


def address_variables():  # add address to variables in orderd dict
    tmp_counter = counter
    for i in variables:
        tmp = bin(tmp_counter)[2:]
        while len(tmp) < 7:
            tmp = "0" + tmp
        variables[i] = tmp
        tmp_counter += 1


# add the label and its address to the odered dict
def handle_label(instruction: str) -> None:
    instruction = instruction.split()
    for j, i in enumerate(instruction):
        instruction[j] = i.strip()
    tmp = bin(counter)[2:]
    while len(tmp) < 7:
        tmp = "0" + tmp
    labels[instruction[0][:-1]] = tmp


# write the binary of instrucgtion to machine code list
def make_instructions():
    for i in instructions:
        mcode = ""
        if i["type"] == "A":
            mcode += OP_code_typeA[i["inst"]]
            mcode += "0" * 2
            mcode += reg_address[i["r1"]]
            mcode += reg_address[i["r2"]]
            mcode += reg_address[i["r3"]]
        elif i["type"] == "B":
            mcode += OP_code_typeB[i["inst"]]
            if len(i["imm"]) == 7:
                mcode += "0"
            mcode += reg_address[i["r1"]]
            mcode += i["imm"]
        elif i["type"] == "C":
            mcode += OP_code_typeC[i["inst"]]
            mcode += "0" * 5
            mcode += reg_address[i["r1"]]
            mcode += reg_address[i["r2"]]
        elif i["type"] == "D":
            mcode += OP_code_typeD[i["inst"]]
            mcode += "0"
            mcode += reg_address[i["r1"]]
            mcode += variables[i["mem_addr"]]
        elif i["type"] == "E":
            mcode += OP_code_typeE[i["inst"]]
            mcode += "0" * 4
            mcode += labels[i["mem_addr"]]
        elif i["type"] == "F":
            mcode += OP_code_typeF[i["inst"]]
            mcode += "0" * 11
        machine_code.append(mcode+'\n')


# adds data(dict) about the instruction to instructions list
def handle_instruction(instruction):
    # inst_dict = {'type': '', 'inst': '', 'r1': '', 'r2': '', 'r3': ''}
    # Parse the instruction string to get the instruction type and operands
    inst_parts = instruction.split()
    for j, i in enumerate(inst_parts):
        inst_parts[j] = i.strip()

    operands = inst_parts[1:]

    inst_dict = {}
    if is_typeA(instruction) == True:
        inst_type = "A"
        inst_dict["type"] = inst_type
        inst_dict["inst"] = inst_parts[0]
        inst_dict["r1"] = operands[0]
        inst_dict["r2"] = operands[1]
        inst_dict["r3"] = operands[2]

    elif is_typeB(instruction) == True:
        words = instruction.split()
        imm = words[-1].replace("$", "")
        if imm.isdigit():
            imm = bin(int(imm))[2:]
            while len(imm) < 7:
                imm = "0" + imm
        elif isfloat(imm):

            imm = float(imm)
            inti = int(imm)
            frac = imm - inti
            imm = bin(inti)[2:]
            pow = len(imm) - 1
            while len(imm) < 6:
                frac = frac*2
                imm +=  str(int(frac))
                frac = frac - int(frac)
            pow = bin(pow)[2:]
            while len(pow) < 3:
                pow = "0" + pow
            imm = pow + imm[1:]
        inst_type = "B"
        inst_dict["type"] = inst_type
        inst_dict["inst"] = inst_parts[0]
        inst_dict["r1"] = operands[0]
        inst_dict["imm"] = imm

    elif is_typeC(instruction) == True:
        inst_type = "C"
        inst_dict["type"] = inst_type
        inst_dict["inst"] = inst_parts[0]
        inst_dict["r1"] = operands[0]
        inst_dict["r2"] = operands[1]

    elif is_typeD(instruction) == True:
        inst_type = "D"
        inst_dict["type"] = inst_type
        inst_dict["inst"] = inst_parts[0]
        inst_dict["r1"] = operands[0]
        inst_dict["mem_addr"] = operands[1]

    elif is_typeE(instruction) == True:
        inst_type = "E"
        inst_dict["type"] = inst_type
        inst_dict["inst"] = inst_parts[0]
        inst_dict["mem_addr"] = operands[0]

    elif is_typeF(instruction) == True:
        inst_type = "F"
        inst_dict["type"] = inst_type
        inst_dict["inst"] = inst_parts[0]

    else:
        print("ERROR: Typos in instruction name")
        exit()

    # Append the instruction dictionary to the instructions list
    instructions.append(inst_dict)


def strip_label(instruction: str) -> str:
    instruction = instruction.split()
    for i in instruction:
        i.strip()
    new_instruction = ""
    for i in instruction[1:]:
        new_instruction += " " + i
    return new_instruction.strip()


if __name__ == "__main__":
    # with open('in.txt', 'r') as rfile:
    variables_end_index = 0
    # lines = rfile.readlines()
    lines = sys.stdin.readlines()
    for line in lines:
        line = line.strip("\n")
        line = line.strip()
        # print(line.split())
        if line == "":
            continue
        if is_var(line):
            handle_variable(line)
        else:
            break
        variables_end_index += 1
    # print(variables_end_index)
    for line in lines[variables_end_index:]:
        line = line.strip("/n")
        line = line.strip()
        # print(line.split())
        if line == "":
            continue
        if is_var(line):
            print("declare all variables at the start")
            exit()
        if is_label(line):
            handle_label(line)
        counter += 1
    address_variables()
    for line in lines[variables_end_index:-1]:
        line = line.strip("\n")
        line = line.strip()
        # print(line.split())
        if line == "":
            continue
        if is_label(line):
            line = strip_label(line)
        if line == "hlt":
            print("hlt not being used as the last instruction")
            exit()
        handle_instruction(line)
    if is_label(lines[-1]):
        line = strip_label(lines[-1])
        if line == "hlt":
            handle_instruction(line)
        else:
            print("Missing hlt instruction")
            exit()
    elif lines[-1].strip("\n").strip() != "hlt":
        print("Missing hlt instruction")
        exit()
    else:
        handle_instruction(lines[-1].strip("\n").strip())
    make_instructions()

    # print(variables)
    # print(labels)
    # print(instructions)
    # print(machine_code)

    # with open("out.txt", "w") as wfile:
    #     wfile.truncate()
    #     wfile.writelines(machine_code)

    sys.stdout.writelines(machine_code)
