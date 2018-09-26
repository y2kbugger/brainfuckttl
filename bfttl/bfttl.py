class Memory():
    def __init__(self):
        self._mem = [0 for x in range(2 ** 16)]
        self._ptr = 0
        self._ptr_min = 0
        self._ptr_max = 0

    @property
    def ptr(self):
        return self._ptr

    @ptr.setter
    def ptr(self, n):
        diff = self._ptr - n
        if abs(diff) > 1:
            print(self._ptr, n)
            raise ValueError("Memory ptr can only be incremented or decremented")

        self._ptr_max = max(self._ptr_max, n)
        self._ptr_min = min(self._ptr_min, n)

        self._ptr = n

    @property
    def mem(self):
        return self._mem[self._ptr_min:self._ptr_max + 1]

    @property
    def value(self):
        return self._mem[self.ptr]

    @value.setter
    def value(self, n):
        self._mem[self.ptr] = n

class ProgMemory(Memory):
    def __init__(self, progtxt):
        super().__init__()
        self.loadprog(progtxt)

    def __str__(self):
        out = [NME[c] for c in self.mem]
        return ''.join(out)

    def loadprog(self, progtxt):
        for c in progtxt:
                try:
                    self.value = OPS[c]
                    self._ptr += 1
                except KeyError:
                    continue
        self.ptr -= 1
        self._ptr = 0

class DataMemory(Memory):
    def __init__(self):
        super().__init__()

    def __str__(self):
        out = [chr(c) for c in self.mem]
        return ''.join(out)

    def hex(self):
        out = [f'{c:02X}' for c in self.mem]
        return ' '.join(out)

    @Memory.value.setter
    def value(self, n):
        diff = self._mem[self.ptr] - n
        if abs(diff) > 1:
            raise ValueError("DataMemory value can only be incremented or decremented")
        self._mem[self.ptr] = n

    def set_value(self, n):
        self._mem[self.ptr] = n

class Decoder():
    def __init__(self, pmem, dmem):
        self.pmem = pmem
        self.dmem = dmem

# opcodes
OPS = {
    '>': 0b10000000,
    '<': 0b01000000,
    '+': 0b00100000,
    '-': 0b00010000,
    '.': 0b00001000,
    ',': 0b00000100,
    '[': 0b00000010,
    ']': 0b00000001,
        }

# nmemonics
NME = {op: nme for nme, op in OPS.items()}

# microcode
def op_no(p, d):
    pass
def op_dm_right(p, d):
    d.ptr += 1
def op_dm_left(p, d):
    d.ptr -= 1
def op_dm_inc(p, d):
    d.value += 1
def op_dm_dec(p, d):
    d.value -= 1
def op_out(p, d):
    global output
    # print(chr(d.value), end='')
    print(chr(d.value))
    output += chr(d.value)
def op_in(p, d):
    d.set_value(ord(input()))
def op_open(p, d):
    if d.value:
        return
    while NME[p.value] != ']':
        p.ptr += 1
def op_close(p, d):
    if not d.value:
        return
    while NME[p.value] != '[':
        p.ptr -= 1

MC = {
    '>': op_dm_right,
    '<': op_dm_left,
    '+': op_dm_inc,
    '-': op_dm_dec,
    '.': op_out,
    ',': op_in,
    '[': op_open,
    ']': op_close,
    }
output = ""
def test1():
    inputstr = """
    ++       Cell c0 = 2
> +++++  Cell c1 = 5

[        Start your loops with your cell pointer on the loop counter (c1 in our case)
< +      Add 1 to c0
> -      Subtract 1 from c1
]        End your loops with the cell pointer on the loop counter

At this point our program has added 5 to 2 leaving 7 in c0 and 0 in c1
but we cannot output this value to the terminal since it is not ASCII encoded!

To display the ASCII character "7" we must add 48 to the value 7!
48 = 6 * 8 so let's use another loop to help us!

++++ ++++  c1 = 8 and this will be our loop counter again
[
< +++ +++  Add 6 to c0
> -        Subtract 1 from c1
]
< .        Print out c0 which has the value 55 which translates to "7"!
"""

    # inputstr = "+" * ord('q') + ".>..>>+." + '+'*51 + '.'
    inputstr = """
++       Cell c0 = 2
> +++++  Cell c1 = 5

[        Start your loops with your cell pointer on the loop counter (c1 in our case)
< +      Add 1 to c0
> -      Subtract 1 from c1
]        End your loops with the cell pointer on the loop counter

At this point our program has added 5 to 2 leaving 7 in c0 and 0 in c1
but we cannot output this value to the terminal since it is not ASCII encoded!

To display the ASCII character "7" we must add 48 to the value 7!
48 = 6 * 8 so let's use another loop to help us!

++++ ++++  c1 = 8 and this will be our loop counter again
[
< +++ +++  Add 6 to c0
> -        Subtract 1 from c1
]
< .        Print out c0 which has the value 55 which translates to "7"!
Hello World!	Edit
The following program prints "Hello World!" and a newline to the screen:

[ This program prints "Hello World!" and a newline to the screen its
  length is 106 active command characters. [It is not the shortest.]

  This loop is an "initial comment loop" a simple way of adding a comment
  to a BF program such that you don't have to worry about any command
  characters. Any  characters are simply
  ignored the "[" and "]" characters just have to be balanced. This
  loop and the commands it contains are ignored because the current cell
  defaults to a value of 0; the 0 value causes this loop to be skipped.
]
++++++++               Set Cell #0 to 8
[
    >++++               Add 4 to Cell #1; this will always set Cell #1 to 4
    [                   as the cell will be cleared by the loop
        >++             Add 2 to Cell #2
        >+++            Add 3 to Cell #3
        >+++            Add 3 to Cell #4
        >+              Add 1 to Cell #5
        <<<<-           Decrement the loop counter in Cell #1
    ]                   Loop till Cell #1 is zero; number of iterations is 4
    >+                  Add 1 to Cell #2
    >+                  Add 1 to Cell #3
    >-                  Subtract 1 from Cell #4
    >>+                 Add 1 to Cell #6
    [<]                 Move back to the first zero cell you find; this will
                        be Cell #1 which was cleared by the previous loop
    <-                  Decrement the loop Counter in Cell #0
]                       Loop till Cell #0 is zero; number of iterations is 8

The result of this is:
Cell No :   0   1   2   3   4   5   6
Contents:   0   0  72 104  88  32   8
Pointer :   ^

>>.                     Cell #2 has value 72 which is 'H'
>---.                   Subtract 3 from Cell #3 to get 101 which is 'e'
+++++++..+++.           Likewise for 'llo' from Cell #3
>>.                     Cell #5 is 32 for the space
<-.                     Subtract 1 from Cell #4 for 87 to give a 'W'
<.                      Cell #3 was set to 'o' from the end of 'Hello'
+++.------.--------.    Cell #3 for 'rl' and 'd'
>>+.                    Add 1 to Cell #5 gives us an exclamation point
>++.                    And finally a newline from Cell #6
"""
    inputstr = """
++++++++[>++++[>++>+++>+++>+<<<<-]>+>+>->>+[<]<-]>>.>---.+++++++..+++.>>.<-.<.+++.------.--------.>>+.>++.
"""
    inputstr = "++++++++++[>+++++++>++++++++++>+++>+<<<<-]>++.>+.+++++++..+++.>++.<<+++++++++++++++.>.+++.------.--------.>+.>."

    # inputstr = """,."""
    pmem = ProgMemory(inputstr)
    print(pmem)
    dmem = DataMemory()
    print(dmem)
    # return
    op = pmem.value
    while op != 0:
        MC[NME[op]](pmem, dmem)
        print(dmem.hex())

        pmem.ptr += 1
        op = pmem.value

    pmem._ptr_max -= 1
    print('\n\n\n', output)
    print(f"\npmem:\n{pmem}")
    print(f"\nfinal dmem:\n{dmem.hex()}")

if __name__ == "__main__":
    test1()
