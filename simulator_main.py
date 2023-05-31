import sys
from collections import OrderedDict

registers = {"000": 0, "001": 0, "010": 0, "011": 0,
             "100": 0, "101": 0, "110": 0, "111": 0}

variables = {}


OP_code_typeA = {
    "add": "00000",
    "sub": "00001",
    "mul": "00110",
    "xor": "01010",
    "or": "01011",
    "and": "01100",
}

OP_code_typeB = {"mov": "00010", "rs": "01000", "ls": "01001"}
OP_code_typeC = {"mov": "00011", "div": "00111",
                 "not": "01101", "cmp": "01110"}
OP_code_typeD = {"ld": "00100", "st": "00101"}
OP_code_typeE = {"jmp": "01111", "jlt": "11100", "jgt": "11101", "je": "11111"}
OP_code_typeF = {"hlt": "11010"}

reg_max = 2**16 - 1


def control_unit(inst):
    # read the instruction and detect the opcode, call the function accordingly
    op_code = inst[:5]

    if op_code in OP_code_typeA.values():
        dest = inst[7:10]
        op1 = inst[10:13]
        op2 = inst[13:]

        ex_typeA(op_code, dest, op1, op2)

    elif op_code in OP_code_typeB.values():
        dest = inst[6:9]
        imm = inst[9:]

        ex_typeB(op_code, dest, imm)

    elif op_code in OP_code_typeC.values():
        dest = inst[10:13]
        op1 = inst[13:]

        ex_typeC(op_code, dest, op1)

    elif op_code in OP_code_typeD.values():
        dest = inst[6:9]
        mem = inst[9:]

        ex_typeD(op_code, dest, mem)

    elif op_code in OP_code_typeE.values():
        mem = inst[9:]

        ex_typeE(op_code, mem)

    elif op_code in OP_code_typeB.values():
        ex_typeF(op_code)


def print_mem():
    pass


def ex_typeA(op_code, dest, op1, op2):
    if op_code == "00000":  # add the op1 and op2 and store in dest
        pass
    elif op_code == "00001":  # sub the op1 and op2 and store in dest
        pass
    elif op_code == "00110":  # mul
        pass
    elif op_code == "01010":  # xor
        pass
    elif op_code == "01011":  # or
        pass
    elif op_code == "01100":  # and
        pass


def ex_typeB(op_code, dest, imm):
    if op_code == "00010":  # mov the imm valuse in dest
        pass
    elif op_code == "01000":  # rs
        pass
    elif op_code == "01001":  # ls
        pass


def ex_typeC(op_code, dest, op1):
    if op_code == "00011":  # mov the value in op1 to dest
        pass
    elif op_code == "00111":  # div
        pass
    elif op_code == "01101":  # not
        pass
    elif op_code == "01110": # cmp 
        pass


def ex_typeD(op_code, dest, mem):
    if op_code == "00100":  # ld
        pass
    elif op_code == "00101":  # st
        pass

def ex_typeE(op_code, mem):
    if op_code == "01111":  # jmp
        pass
    elif op_code == "11100":  # jlt
        pass
    elif op_code == "11101":  # jgt
        pass
    elif op_code == "11111":  # je
        pass



def ex_typeF(op_code):
    if op_code == "11010":
        pass


if __name__ == "__main__":
    lines = sys.stdin.readlines()
    for line in lines:
        pass
    pass
