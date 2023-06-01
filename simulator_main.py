import sys
from collections import OrderedDict

registers = OrderedDict(
    (
        ("000", 0),
        ("001", 0),
        ("010", 0),
        ("011", 0),
        ("100", 0),
        ("101", 0),
        ("110", 0),
        ("111", 0),
    )
)

ram = OrderedDict()  # will store the addressa as keys to values at that mem

PC = 0

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


def dump_mem():
    for mem in ram.values():
        print(mem)


def convert_bin(num, num_bits):
    temp = bin(num)
    while len(temp) < num_bits:
        temp = "0" + temp

    return temp


def bin_to_dec(str):
    powr = 0
    ans = 0
    for i in str:
        ans += int(i) * 2**pow
        powr += 1
    return ans


def print_regs():
    print(convert_bin(PC, 7))

    for reg in registers.values():
        print(convert_bin(reg, 16))


def ex_typeA(op_code, dest, op1, op2):
    if op_code == "00000":  # add the op1 and op2 and store in dest
        sum = registers[op1] + registers[op2]
        if sum <= reg_max and sum >= 0:
            registers[dest] = sum
        registers["111"] = 8
        registers[dest] = 0
        PC += 1

    elif op_code == "00001":  # sub the op1 and op2 and store in dest
        diff = registers[op1] - registers[op2]
        if diff <= reg_max and diff >= 0:
            registers[dest] = diff
        registers["111"] = 8
        registers[dest] = 0
        PC += 1

    elif op_code == "00110":  # mul
        prod = registers[op1] * registers[op2]
        if prod <= reg_max and prod >= 0:
            registers[dest] = prod
        registers["111"] = 8
        registers[dest] = 0
        PC += 1

    elif op_code == "01010":  # xor
        xor_ans=""
        op1_len=len(op1)
        op2_len=len(op2)

        if op1_len>op2_len:
            d=op1_len-op2_len
            p=op2
            q=op1
            
        else:
            d=op2_len-op1_len
            p=op1
            q=op2

        prefix=""
        for i in range(0,d):
            prefix+="0"
            i+=1
        
        new_p=prefix+p
        

        new_len=len(new_p)

        for i in range(0,new_len):
            if new_p[i]=="1" and q[i]=="1":
                xor_ans+="0"
                i+=1
            elif new_p[i]=="1" and q[i]=="0":
                xor_ans+="1"
                i+=1
            elif new_p[i]=="0" and q[i]=="1":
                xor_ans+="1"
                i+=1
            elif new_p[i]=="0" and q[i]=="0":
                xor_ans+="0"
                i+=1

        if xor_ans<=reg_max and xor_ans>=0:          ### CHECK IF REGISTERS ARE CORRECT OR NOT
            registers[dest]=xor_ans

        PC+=1 

    elif op_code == "01011":  # or
        or_ans=""
        op1_len=len(op1)
        op2_len=len(op2)

        if op1_len>op2_len:
            d=op1_len-op2_len
            p=op2
            q=op1
            
        else:
            d=op2_len-op1_len
            p=op1
            q=op2

        prefix=""
        for i in range(0,d):
            prefix+="0"
            i+=1
        
        new_p=prefix+p
        new_len=len(new_p)

        for i in range(0,new_len):
            if new_p[i]=="1" and q[i]=="1":
                or_ans+="1"
                i+=1
            elif new_p[i]=="1" and q[i]=="0":
                or_ans+="1"
                i+=1
            elif new_p[i]=="0" and q[i]=="1":
                or_ans+="1"
                i+=1
            elif new_p[i]=="0" and q[i]=="0":
                or_ans+="0"
                i+=1
        
        if or_ans<=reg_max and or_ans>=0:
            registers[dest]=or_ans
                                             ### CHECK IF REGISTERS ARE CORRECT OR NOT
        PC+=1 

    elif op_code == "01100":  # and
        and_ans=""
        op1_len=len(op1)
        op2_len=len(op2)

        if op1_len>op2_len:
            d=op1_len-op2_len
            p=op2
            q=op1
            
        else:
            d=op2_len-op1_len
            p=op1
            q=op2

        prefix=""
        for i in range(0,d):
            prefix+="0"
            i+=1
        
        new_p=prefix+p
        new_len=len(new_p)

        for i in range(0,new_len):
            if new_p[i]=="1" and q[i]=="1":
                and_ans+="1"
                i+=1
            elif new_p[i]=="1" and q[i]=="0":
                and_ans+="1"
                i+=1
            elif new_p[i]=="0" and q[i]=="1":
                and_ans+="1"
                i+=1
            elif new_p[i]=="0" and q[i]=="0":
                and_ans+="0"
                i+=1

        if and_ans<=reg_max and and_ans>=0:
            registers[dest]=and_ans             ### CHECK IF REGISTERS ARE CORRECT OR NOT 

        PC+=1


def ex_typeB(op_code, dest, imm):
    if op_code == "00010":  # mov the imm valuse in dest
        registers[dest] = bin_to_dec(imm)

    elif op_code == "01000":  # rs           NEEDS TO BE IMPLEMENTED 
        rs_val = registers[dest]/(2**bin_to_dec(imm))
        if rs_val > reg_max or rs_val < 0:
            registers[dest] = rs_val

        registers["111"] = 8
        registers[dest] = 0
        PC += 1
        
    elif op_code == "01001":  # ls           NEEDS TO BE IMPLEMENTED
        ls_val = registers[dest]*(2**bin_to_dec(imm))
        if ls_val > reg_max or ls_val < 0:
            registers[dest] = ls_val

        registers["111"] = 8
        registers[dest] = 0
        PC += 1


def ex_typeC(op_code, dest, op1):
    if op_code == "00011":  # mov the value in op1 to dest
        registers[dest] = registers[op1]

    elif op_code == "00111":  # div
        if registers[op1] != 0:
            quot = registers[dest]/registers[op1]
            remain = registers[dest]/registers[op1]
            registers[dest] = quot
            registers[op1] = remain

        registers["111"] = 8
        registers[dest] = 0
        registers[op1] = 0  
        
    elif op_code == "01101":  # not
        not_ans=""
        len_op1=len(op1)
        for i in range(0,len_op1):
            if op1[i]=="1":
                not_ans+="0"
            elif op1[i]=="0":
                not_ans+="1"
            i+=1

        registers[dest]=not_ans
        PC += 1        
        
    elif op_code == "01110":  # cmp            NEEDS TO BE IMPLEMENTED
        pass


def ex_typeD(op_code, dest, mem):
    if op_code == "00100":  #
        registers[dest] = bin_to_dec(ram[mem])

    elif op_code == "00101":  # st
        ram[mem] = convert_bin(registers[dest], 16)


def ex_typeE(op_code, mem):
    if op_code == "01111":  # jmp
        PC = bin_to_dec(mem)

    elif op_code == "11100":  # jlt
        if registers["111"] == 4:
            PC = bin_to_dec(mem)
            registers["111"] = 0

    elif op_code == "11101":  # jgt
        if registers["111"] == 2:
            PC = bin_to_dec(mem)
            registers["111"] = 0

    elif op_code == "11111":  # je
        if registers["111"] == 1:
            PC = bin_to_dec(mem)
            registers["111"] = 0


def ex_typeF(op_code):
    if op_code == "11010":
        pass


if __name__ == "__main__":
    lines = sys.stdin.readlines()
    count = 0
    for line in lines:
        line = line.strip()
        ram[convert_bin(count, 7)] = lines

    # execution of lines
    line = lines[PC]
    while line != "11010":
        control_unit(line)
        line = lines[PC]
