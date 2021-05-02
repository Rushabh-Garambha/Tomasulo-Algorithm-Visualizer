class Config:
    num_of_registers = 4
    inst_win_size = 5
    rob_size = 5
    functional_units = [{"id": 0,
                         "instructions": ["ADD", "SUB"],
                         "cycles": 1},
                        {"id": 1,
                         "instructions": ["ADD", "SUB"],
                         "cycles": 1},
                        {"id": 2,
                         "instructions": ["MUL"],
                         "cycles": 4},
                        {"id": 3,
                         "instructions": ["MUL"],
                         "cycles": 4},
                        {"id": 4,
                         "instructions": ["DIV"],
                         "cycles": 4},
                        {"id": 5,
                         "instructions": ["LD", "BGE", "BNEZ", "BEQZ"],
                         "cycles": 1},
                        {"id": 6,
                         "instructions": ["LD", "BGE", "BNEZ", "BEQZ"],
                         "cycles": 1},
                        ]
    rs_id_mappings = ["A0","A1","M0","M1","D0","L0","L1"]


instructions = [{"address": 0,
                 "op": "LD",
                 "dest": "R0",
                 "s1": "0",
                 "s2": None},
                {"address": 4,
                 "op": "MUL",
                 "dest": "R2",
                 "s1": "R0",
                 "s2": "2"},
                {"address": 8,
                 "op": "MUL",
                 "dest": "R1",
                 "s1": "R0",
                 "s2": "R0"},
                {"address": 12,
                 "op": "SUB",
                 "dest": "R3",
                 "s1": "R1",
                 "s2": "R2"},
                {"address": 16,
                 "op": "DIV",
                 "dest": "R1",
                 "s1": "1",
                 "s2": "16"},
                {"address": 20,
                 "op": "SUB",
                 "dest": "R2",
                 "s1": "R2",
                 "s2": "2"},
                {"address": 24,
                 "op": "ADD",
                 "dest": "R3",
                 "s1": "R3",
                 "s2": "1"},
                {"address": 28,
                 "op": "DIV",
                 "dest": "R2",
                 "s1": "R3",
                 "s2": "R2"},
                {"address": 32,
                 "op": "SUB",
                 "dest": "R0",
                 "s1": "R0",
                 "s2": "R2"},
                {"address": 36,
                 "op": "BEQZ",
                 "dest": "R1",
                 "s1": "4",
                 "s2": None}]

results = []

def get_program(program):
    line = ''
    for inst in program:
        line += "{:<2d}: {:<4s} {:<2s} {:<2s} {:<2s}\n".format(inst['address'], inst['op'], inst['dest'], inst['s1'], '' if inst['s2'] is None else inst['s2'])
    return line

#print(get_program(instructions))