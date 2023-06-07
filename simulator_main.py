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
    "addf": "10000",
    "subf": "10001"
}
OP_code_typeB = {"mov": "00010", "rs": "01000", "ls": "01001", "movf": "10010"}
OP_code_typeC = {"mov": "00011", "div": "00111",
                 "not": "01101", "cmp": "01110"}
OP_code_typeD = {"ld": "00100", "st": "00101"}
OP_code_typeE = {"jmp": "01111", "jlt": "11100", "jgt": "11101", "je": "11111"}
OP_code_typeF = {"hlt": "11010"}

reg_max = 2**16 - 1
max_float = 0b11_111_100
min_float = 0b1


def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False


def control_unit(inst):
    # read the instruction and detect the opcode, call the function accordingly
    op_code = inst[:5]

    if op_code in OP_code_typeA.values():
        dest = inst[7:10]
        op1 = inst[10:13]
        op2 = inst[13:]

        ex_typeA(op_code, dest, op1, op2)

    elif op_code in OP_code_typeB.values():
        if op_code == "10010":
            dest = inst[5:8]
            imm = inst[8:]
        else:
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

    elif op_code in OP_code_typeF.values():
        ex_typeF(op_code)


def dump_mem():
    for mem in ram.values():
        print(mem)


def convert_bin(num, num_bits):
    temp = bin(num)[2:]
    while len(temp) < num_bits:
        temp = "0" + temp
    return temp


def convert_float(num):
    flt = float(num)
    inti = int(num)
    frac = flt - inti
    flt = bin(inti)[2:]
    pow = len(flt) - 1
    while len(flt) < 6:
        frac = frac*2
        flt += str(int(frac))
        frac = frac - int(frac)
    pow = bin(pow)[2:]
    while len(pow) < 3:
        pow = "0" + pow
    flt = pow + flt[1:]
    return "00000000"+flt


def bin_to_dec(str):
    powr = 0
    ans = 0
    for i in str[-1::-1]:
        ans += int(i) * 2**powr
        powr += 1
    return ans


def bin_to_float(num_str):
    powr = bin_to_dec(num_str[:3])
    inti = bin_to_dec("1"+num_str[3:3+powr])
    frac = 0
    factor = 1/2
    for i in num_str[3+powr:]:
        frac += int(i)*factor
        factor /= 2
    out = inti + frac
    return out


def print_regs():
    print(convert_bin(PC, 7), end = "        ")
    for reg in registers.values():
        if type(reg) == int:
            print(convert_bin(reg, 16), end=" ")
        else:
            print(convert_float(reg), end = " ")
    print()


def ex_typeA(op_code, dest, op1, op2):
    global PC  # do this for all functions dumb asses
    if op_code == "00000":  # add the op1 and op2 and store in dest
        sum = registers[op1] + registers[op2]
        if sum <= reg_max and sum >= 0:
            registers[dest] = sum
            registers["111"] = 0

        else:
            registers["111"] = 8
            registers[dest] = 0
        print_regs()
        PC += 1

    elif op_code == "00001":  # sub the op1 and op2 and store in dest
        diff = registers[op1] - registers[op2]
        if diff <= reg_max and diff >= 0:
            registers[dest] = diff
            registers["111"] = 0

        else:
            registers["111"] = 8
            registers[dest] = 0

        print_regs()
        PC += 1

    elif op_code == "00110":  # mul
        prod = registers[op1] * registers[op2]
        if prod <= reg_max and prod >= 0:
            registers[dest] = prod
            registers["111"] = 0

        else:
            registers["111"] = 8
            registers[dest] = 0

        print_regs()
        PC += 1

    elif op_code == "01010":  # xor
        registers[dest] = registers[op1] ^ registers[op2]
        registers["111"] = 0

        print_regs()
        PC += 1

    elif op_code == "01011":  # or
        registers[dest] = registers[op1] | registers[op2]
        registers["111"] = 0

        print_regs()
        PC += 1

    elif op_code == "01100":  # and
        registers[dest] = registers[op1] & registers[op2]
        registers["111"] = 0

        print_regs()
        PC += 1
    elif op_code == "10000":
        sum = registers[op1] + registers[op2]
        if sum <= max_float and sum >= min_float:
            registers[dest] = sum
            registers["111"] = 0
        else:
            registers["111"] = 8
            registers[dest] = 0
        print_regs()
        PC += 1

    elif op_code == "10001":  # sub the op1 and op2 and store in dest
        diff = registers[op1] - registers[op2]
        if diff <= max_float and diff >= min_float:
            registers[dest] = diff
            registers["111"] = 0
        else:
            registers["111"] = 8
            registers[dest] = 0
        print_regs()
        PC += 1


def ex_typeB(op_code, dest, imm):
    global PC
    if op_code == "00010":  # mov the imm valuse in dest
        registers[dest] = bin_to_dec(imm)
        registers["111"] = 0

        print_regs()
        PC += 1

    elif op_code == "01000":  # rs           NEEDS TO BE IMPLEMENTED
        rs_val = registers[dest] / (2 ** bin_to_dec(imm))
        if rs_val > reg_max or rs_val < 0:
            registers[dest] = rs_val
            registers["111"] = 0
        else:
            registers["111"] = 8  # else tera baap likhega
            registers[dest] = 0
        print_regs()
        PC += 1

    elif op_code == "01001":  # ls           NEEDS TO BE IMPLEMENTED
        ls_val = registers[dest] * (2 ** bin_to_dec(imm))
        if ls_val > reg_max or ls_val < 0:
            registers[dest] = ls_val
            registers["111"] = 0
        else:
            registers["111"] = 8
            registers[dest] = 0
        print_regs()
        PC += 1

    elif op_code == "10010":
        registers[dest] = bin_to_float(imm)
        registers["111"] = 0
        print_regs()
        PC += 1


def ex_typeC(op_code, dest, op1):
    global PC
    if op_code == "00011":  # mov the value in op1 to dest
        registers[dest] = registers[op1]
        registers["111"] = 0

        print_regs()
        PC += 1

    elif op_code == "00111":  # div
        if registers[op1] != 0:
            quot = registers[dest] / registers[op1]
            remain = registers[dest] / registers[op1]
            registers[dest] = quot
            registers[op1] = remain
            registers["111"] = 0

        else:
            registers["111"] = 8
            registers[dest] = 0
            registers[op1] = 0

        print_regs()
        PC += 1

    elif op_code == "01101":  # not
        temp = convert_bin(registers[op1], 16)
        out = ""
        for i in range(len(temp)):
            if temp[i] == "0": out += "1"
            else: out += "0"
        registers[dest] = bin_to_dec(out)
        print_regs()
        PC += 1

    elif op_code == "01110":  # cmp

        if registers[dest] == registers[op1]:
            registers["111"] = 1
        elif registers[dest] > registers[op1]:
            registers["111"] = 2
        else:
            registers["111"] = 4

        print_regs()
        PC += 1


def ex_typeD(op_code, dest, mem):
    global PC
    if op_code == "00100":  # ld
        if type(registers[dest]) == int:
            registers[dest] = bin_to_dec(ram[mem])
        else:
            registers[dest] = bin_to_float(ram[mem])
        registers["111"] = 0

        print_regs()
        PC += 1

    elif op_code == "00101":  # st
        if type(registers[dest]) == int:
            ram[mem] = convert_bin(registers[dest], 16)
        else:
            ram[mem] = convert_float(registers[dest])
        registers["111"] = 0

        print_regs()
        PC += 1


def ex_typeE(op_code, mem):
    global PC
    if op_code == "01111":  # jmp
        registers["111"] = 0

        print_regs()
        PC = bin_to_dec(mem)

    elif op_code == "11100":  # jlt
        if registers["111"] == 4:
            registers["111"] = 0
            print_regs()
            PC = bin_to_dec(mem)
        else:
            registers["111"] = 0

            print_regs()
            PC += 1

    elif op_code == "11101":  # jgt
        if registers["111"] == 2:
            registers["111"] = 0
            print_regs()
            PC = bin_to_dec(mem)
        else:
            registers["111"] = 0

            print_regs()
            PC += 1

    elif op_code == "11111":  # je
        if registers["111"] == 1:
            registers["111"] = 0
            print_regs()
            PC = bin_to_dec(mem)
        else:
            registers["111"] = 0

            print_regs()
            PC += 1


def ex_typeF(op_code):
    global PC
    if op_code == "11010":
        registers["111"] = 0

        print_regs()
        PC += 1
        dump_mem()
        exit()


if __name__ == "__main__":
    lines = sys.stdin.readlines()
    count = 0
    for line in lines:
        line = line.strip()
        ram[convert_bin(count, 7)] = line
        count += 1
    while count < 128:
        ram[convert_bin(count, 7)] = convert_bin(0, 16)
        count += 1

    # print(lines, ram, PC, sep="\n")
    # execution of lines
    cmd = ram[convert_bin(PC, 7)]

    while 1:
        control_unit(cmd)
        cmd = ram[convert_bin(PC, 7)]
