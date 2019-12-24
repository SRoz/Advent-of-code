class IntcodeComputer:
    def __init__(self, bits):
        self.bits = bits.copy() + [0]* 100_000
        self.i = 0
        self.outputs = []
        self.output = []
        self.inputs = []
        self.input_i = 0
        self.relative_base = 0 
        self.state = 'Not Started'

        
    def _apply_mode(self, instruction, i):
        mode = int(instruction[-2-i])
        loc = self.i + i
        
        if mode == 0:
            return self.bits[self.bits[loc]]
        elif mode == 1:
            return self.bits[loc]
        elif mode ==2:
            return self.bits[self.relative_base + self.bits[loc]]
    
    def _write_mode(self, instruction, i, write):
        if instruction[-2-i] == '0':
            self.bits[self.bits[self.i+i]] = write
        else:
            self.bits[self.bits[self.i+i] + self.relative_base] = write
    
    def run(self, inputs=[]):
        self.output = []
        if isinstance(inputs, list):
            self.inputs += inputs
        else:
            self.inputs += [inputs]

        while True:
            instruction = ("00000" + str(self.bits[self.i]))[-6:]
            opcode = int(instruction[-2:])
                        
            if opcode == 99:
                self.state = 'Finished'
                return int(self.outputs[-1])
            elif opcode == 1:
                p1 = self._apply_mode(instruction, 1)
                p2 = self._apply_mode(instruction, 2)
                
                self._write_mode(instruction, 3, p1+p2)
                self.i = self.i+4
            elif opcode == 2:
                p1 = self._apply_mode(instruction, 1)
                p2 = self._apply_mode(instruction, 2)
                
                self._write_mode(instruction, 3, p1*p2)
                self.i = self.i+4
            elif opcode == 3:
                if len(self.inputs) <= self.input_i:
                    self.state = 'Paused'
                    if len(self.outputs) > 0:
                        return int(self.outputs[-1])
                    else:
                        return None
                
                self._write_mode(instruction, 1, self.inputs[self.input_i])                
                self.input_i += 1
                self.i = self.i+2
            elif opcode == 4:
                output_val = self._apply_mode(instruction, 1)
                self.outputs += [output_val]
                self.output += [output_val]
                self.i = self.i+2
            elif opcode == 5:
                p1 = self._apply_mode(instruction, 1)
                p2 = self._apply_mode(instruction, 2)

                if p1 > 0:
                    self.i = p2
                else:
                    self.i = self.i+3
            elif opcode == 6:
                p1 = self._apply_mode(instruction, 1)
                p2 = self._apply_mode(instruction, 2)

                if p1 == 0:
                    self.i = p2
                else:
                    self.i = self.i+3
            elif opcode == 7:
                p1 = self._apply_mode(instruction, 1)
                p2 = self._apply_mode(instruction, 2)
                p3 = self._apply_mode(instruction, 3)
                if p1 < p2:
                    self._write_mode(instruction, 3, 1)
                    #self.bits[self.bits[self.i+3]] = 1
                else:
                    self._write_mode(instruction, 3, 0)
                    #self.bits[self.bits[self.i+3]] = 0
                self.i = self.i+4
            elif opcode == 8:
                p1 = self._apply_mode(instruction, 1)
                p2 = self._apply_mode(instruction, 2)
                p3 = self._apply_mode(instruction, 3)
                if p1 == p2:
                    self._write_mode(instruction, 3, 1)
                    #self.bits[self.bits[self.i+3]] = 1
                else:
                    self._write_mode(instruction, 3, 0)
                    #self.bits[self.bits[self.i+3]] = 0
                self.i = self.i+4            
            elif opcode == 9:
                self.relative_base = self.relative_base + self._apply_mode(instruction, 1)
                self.i = self.i+2