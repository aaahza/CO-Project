import sys
from collections import OrderedDict

registers = {"000": 0, "001": 0, "010": 0, "011": 0, "100": 0, "101": 0, "110": 0, "111": 0}

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
OP_code_typeC = {"mov": "00011", "div": "00111", "not": "01101", "cmp": "01110"}
OP_code_typeD = {"ld": "00100", "st": "00101"}
OP_code_typeE = {"jmp": "01111", "jlt": "11100", "jgt": "11101", "je": "11111"}
OP_code_typeF = {"hlt": "11010"}

reg_max = 2**16 - 1

def control_unit(inst):
    #read the instruction and detect the opcode, call the function accordingly
    op_code = inst[:5]

    if op_code in OP_code_typeA.values():
        dest = inst[7:10]
        op1 = inst[10:13]
        op2 = inst[13:]

        ex_typeA(op_code, dest, op1, op2 )

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

        ex_typeE(op_code,mem)

    elif op_code in OP_code_typeB.values():
        ex_typeF(op_code)

def print_mem():
    pass

def ex_typeA(op_code, dest , op1, op2):
    pass
def ex_typeB(op_code, dest , imm):
    pass
def ex_typeC(op_code, dest , op1):
    pass
def ex_typeD(op_code, dest ,mem):
    pass
def ex_typeE(op_code, mem):
    pass
def ex_typeF(op_code):
    pass
    

if __name__ == "__main__":
    lines = sys.stdin.readlines()
    for line in lines:
        pass
    pass