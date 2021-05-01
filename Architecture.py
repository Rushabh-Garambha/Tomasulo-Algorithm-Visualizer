from Components import *
import Config as cfg


class Architecture:
    def __init__(self):
        self.PC = 16
        self.cycle = 0
        self.done = False

        # Initialize Parameters
        self.total_regs = cfg.Config.num_of_registers
        self.len_inst_window = cfg.Config.inst_win_size

        # Create Register File according to params
        self.RF = RegisterFile(self.total_regs)

        # Load Program to memory into dictionary which has keys are the address
        self.program = {}
        for inst in cfg.instructions:
            self.program[inst["address"]] = Instruction(inst["op"], inst["dest"], inst["s1"], inst["s2"])

        # Reservation Stations list
        self.RS = ReservationStation()

        # Instruction Queue
        self.IQ = InstructionQueue(self.len_inst_window, self.program)

        # ReOrder Buffer
        self.ROB = ReOrderBuffer()

        # Common Data Bus
        self.CDB = []

        # Report File
        self.report = open('Output_Report.txt', 'w')

    def start(self):
        while not self.done:
            self.print_cycle()
            self.issue()
            if self.cycle > 0:
                self.execute()
            self.print_CDB()
            if self.cycle > 1:
                self.write_back()
            if self.cycle > 2:
                self.commit()
            self.update_clock()
        self.print_cycle()
        self.report.write('Program has finished')
        self.report.close()

    def print_cycle(self):
        self.report.write('\n------------------------')
        self.report.write('\nCYCLE ' + str(self.cycle) + '\n')

        self.report.write('\nInstruction Window\n')
        self.report.write(str(self.IQ))

        self.report.write('\nRegisters\n')
        self.report.write(str(self.RF))

        self.report.write('\nReservation Stations\n')
        self.report.write(str(self.RS))

        self.report.write('\nReorder Buffer\n')
        self.report.write(str(self.ROB))

    def print_CDB(self):
        self.report.write('\nCommon Data Bus\n')
        if len(self.CDB) != 0:
            self.report.write(str(self.CDB[0]))

    def issue(self):
        if self.IQ.empty():
            return

        if not self.ROB.is_full():
            next_inst = self.IQ.get()

            if self.RS.is_available(next_inst.op):
                inst_id, inst = self.IQ.dequeue()
            else:
                return

            rob_id = self.ROB.list[self.ROB.tail].name

            rs = self.RS.get_rs(inst.op)
            rs.busy = True
            rs.inst_id = inst_id
            rs.op = inst.op
            rs.dest = rob_id

            # Case of Branch
            # Branch Prediction
            if inst.op == 'LD':
                if Instruction.is_operand_reg(inst.s1):
                    if self.RF.is_available(inst.s1):
                        rob_s1 = self.ROB.getby_reg(inst.s1)
                        if rob_s1.ready:
                            rs.vj = rob_s1.value
                            rs.qj = ''
                            self.RF[inst.s1].reorder = rob_id
                            self.RF[inst.s1].busy = True
                        else:
                            rs.qj = rob_id
                    else:
                        rs.vj = self.RF[inst.s1].value
                        rs.qj = ''
                else:
                    rs.vj = int(inst.s1)
                    rs.qj = ''
            elif inst.op in ['BGE','BNEZ','BEQZ']:
                if Instruction.is_operand_reg(inst.d):
                    if not self.RF[inst.d].busy:
                        rob_d = self.ROB.getby_reg(inst.d)
                        if rob_d is not None:
                            if rob_d.ready:
                                rs.vj = rob_d.value
                                rs.qj = ''
                                self.RF[inst.d].reorder = rob_id
                                self.RF[inst.d].busy = True

                            else:
                                rs.qj = rob_d.name
                        else:
                            rs.vj = self.RF[inst.d].value
                            rs.qj = ''
                    else:
                        rob_d = self.ROB.getby_reg(inst.d)
                        if rob_d.name == self.RF[inst.d].reorder:
                            rs.qj = rob_d.name
                        else:
                            rs.vj = self.RF[inst.d].value
                            rs.qj = ''
                else:
                    rs.vj = int(inst.d)
                    rs.qj = ''

                if Instruction.is_operand_reg(inst.s1):
                    if not self.RF[inst.s1].busy:
                        rob_s1 = self.ROB.getby_reg(inst.s1)
                        if rob_s1 is not None:
                            if rob_s1.ready:
                                rs.vk = rob_s1.value
                                rs.qk = ''
                                self.RF[inst.s1].reorder = rob_id
                                self.RF[inst.s1].busy = True
                            else:
                                rs.qk = rob_s1.name
                        else:
                            rs.vk = self.RF[inst.s1].value
                            rs.qk = ''
                    else:
                        rob_s1 = self.ROB.getby_reg(inst.s1)
                        if rob_s1.name == self.RF[inst.s1].reorder:
                            rs.qk = rob_s1.name
                        else:
                            rs.vk = self.RF[inst.s1].value
                            rs.qk = ''
                else:
                    rs.vk = int(inst.s1)
                    rs.qk = ''
            else:
                if Instruction.is_operand_reg(inst.s1):
                    if not self.RF[inst.s1].busy:
                        rob_s1 = self.ROB.getby_reg(inst.s1)
                        if rob_s1 is not None:
                            if rob_s1.ready:
                                rs.vj = rob_s1.value
                                rs.qj = ''
                                self.RF[inst.s1].reorder = rob_id
                                self.RF[inst.s1].busy = True

                            else:
                                rs.qj = rob_s1.name
                        else:
                            rs.vj = self.RF[inst.s1].value
                            rs.qj = ''
                    else:
                        rob_s1 = self.ROB.getby_reg(inst.s1)
                        if rob_s1.name == self.RF[inst.s1].reorder:
                            rs.qj = rob_s1.name
                        else:
                            rs.vj = self.RF[inst.s1].value
                            rs.qj = ''
                else:
                    rs.vj = int(inst.s1)
                    rs.qj = ''

                if Instruction.is_operand_reg(inst.s2):
                    if not self.RF[inst.s2].busy:
                        rob_s2 = self.ROB.getby_reg(inst.s2)
                        if rob_s2 is not None:
                            if rob_s2.ready:
                                rs.vk = rob_s2.value
                                rs.qk = ''
                                self.RF[inst.s2].reorder = rob_id
                                self.RF[inst.s2].busy = True
                            else:
                                rs.qk = rob_s2.name
                        else:
                            rs.vk = self.RF[inst.s2].value
                            rs.qk = ''
                    else:
                        rob_s2 = self.ROB.getby_reg(inst.s2)
                        if rob_s2.name == self.RF[inst.s2].reorder:
                            rs.qk = rob_s2.name
                        else:
                            rs.vk = self.RF[inst.s2].value
                            rs.qk = ''
                else:
                    rs.vk = int(inst.s2)
                    rs.qk = ''
            self.ROB.add(inst_id, inst)
            # if branch: don't add to RF
            if not inst.op.startswith('B'):
                self.RF[inst.d].reorder = rob_id

    def execute(self):
        self.RS.execute(self.CDB)

    def write_back(self):
        if len(self.CDB) != 0:
            rob_id, value = self.CDB.pop(0)

            rob = self.ROB.getby_rob_id(rob_id)
            rob.ready = True
            rob.value = value
            if rob.op.startswith('B') and rob.value == 0:
                self.cycle += 1
                self.print_cycle()
                self.flush()
                self.PC = self.last_branch_PC
            self.RS.update_with_rob(rob_id, value)

    def commit(self):
        head_rob = self.ROB.get_head()
        if head_rob.ready:
            reg = self.RF[head_rob.dest]
            if not head_rob.op.startswith('B'):
                reg.value = head_rob.value
            if head_rob.name == reg.reorder:
                reg.reorder = ''
            head_rob.busy = False
            self.ROB.update_head()
            if self.ROB.getby_reg(reg.name) is None:
                reg.busy = False

    def update_clock(self):
        self.cycle += 1
        try:
            inst_copy = self.program[self.PC].copy()
            self.IQ.enqueue(inst_copy)
            if inst_copy.op.startswith('B'):
                self.last_branch_PC = self.PC + 4
                self.PC = int(inst_copy.s2) if inst_copy.op not in ["BNEZ", "BEQZ"] else int(inst_copy.s1)
            else:
                self.PC += 4
        except:
            if self.ROB.is_empty() and self.IQ.empty():
                self.done = True

    def flush(self):
        rob_list = self.ROB.flush()
        if rob_list is not None:
            for rob in rob_list:
                self.RS.flush(rob.inst_id)
                if self.RF[rob.dest].reorder == rob.name:
                    self.RF[rob.dest].reorder = ''
                    # if this register exists in the updated rob, update it with that rob id
                    reg_rob = self.ROB.getby_reg(rob.dest)
                    if reg_rob is not None:
                        self.RF[rob.dest].reorder = reg_rob.name
                    else:
                        self.RF[rob.dest].busy = False
            self.IQ.flush()
        else:
            return
