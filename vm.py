import argparse

class VM:
    MAX_STACK_SIZE = 1024*1024*1024

    def __init__(self, stack_size=1024, bitwidth=0):
        self.stack_size = stack_size
        self.data = [0] * self.stack_size
        self.p = 0
        self.pc = 0
        self.buffer = []
        self.active_loops = []
        self.MAX_INT = (1<<bitwidth-1) - 1 if bitwidth else None
        self.MIN_INT = - self.MAX_INT - 1 if bitwidth else None

    def check_bound(self):
        if self.p < 0:
            raise RuntimeError('Data Pointer Out of Bound')
        elif self.p > self.stack_size:
            raise RuntimeError('Stack Overflow')

    def rshift(self):   # >
        self.p += 1
        if self.p >= self.MAX_STACK_SIZE:
            raise RuntimeError('Segmentation Fault')
        if self.p >= self.stack_size and self.stack_size < self.MAX_STACK_SIZE:
            extend_size = min(self.MAX_STACK_SIZE - self.stack_size, self.stack_size)
            self.data.extend([0] * extend_size)
            self.stack_size += extend_size

    def lshift(self):   # <
        self.p -= 1

    def incr(self):     # +
        self.check_bound()
        self.data[self.p] += 1
        if self.MAX_INT and self.data[self.p] > self.MAX_INT:
            self.data[self.p] = self.MIN_INT

    def decr(self):     # -
        self.check_bound()
        self.data[self.p] -= 1
        if self.MIN_INT and self.data[self.p] < self.MIN_INT:
            self.data[self.p] = self.MAX_INT

    def putch(self):    # .
        self.check_bound()
        print(chr(self.data[self.p]), end='', flush=True)

    def getch(self):    # ,
        while not self.buffer:
            self.buffer += input() + '\n'
        self.data[self.p] = ord(self.buffer.pop(0))

    def jloop_in(self, code):   # [
        self.check_bound()
        if self.data[self.p] != 0: # enter loop
            self.active_loops.append(self.pc)
            return
        # skip loop
        depth = 0
        self.pc += 1
        while self.pc < len(code):
            if code[self.pc] == '[':
                depth += 1
            elif code[self.pc] == ']':
                if depth:
                    depth -=1
                else:
                    return
            self.pc += 1
        raise RuntimeError(f'Unexpected End of Code at: {self.pc}')

    def jloop_out(self, code):  # ]
        self.check_bound()
        if self.data[self.p] == 0: # end loop
            self.active_loops.pop()
            return
        self.pc = self.active_loops[-1]

    def nop(self):
        pass

    def run(self, code: str):
        op_table = {
            '>': self.rshift,
            '<': self.lshift,
            '+': self.incr,
            '-': self.decr,
            '.': self.putch,
            ',': self.getch,
            '[': self.jloop_in,
            ']': self.jloop_out,
        }

        while self.pc < len(code):
            c = code[self.pc]
            op = op_table.get(c, self.nop)
            op(code) if c in '[]' else op()
            self.pc += 1


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='The Brainfuck Virtual Machine')
    parser.add_argument('-c', '--code', help='code to run directly')
    parser.add_argument('-b', '--bitwidth', type=int, help='bitwidth of machine', default=0)
    parser.add_argument('file', nargs='?', help='the source code file')
    args = parser.parse_args()
    if args.file:
        with open(args.file) as f:
            code = f.read()
    else:
        code = args.code
    vm = VM(bitwidth=args.bitwidth)
    vm.run(code)
