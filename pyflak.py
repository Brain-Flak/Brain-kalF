PARENTHESIS = 0
SQUIGGLY = 1
SQUARE = 2
ANGLED = 3

class Nilad:
    def __init__(self, string):
        self.brack_type = ["()", "{}", "[]", "<>"].index(string)

    def exec(self, program_state):
        if self.brack_type == PARENTHESIS:
            return 1
        if self.brack_type == SQUIGGLY:
            return program_state.pop()
        if self.brack_type == SQUARE:
            return program_state.stack_height()
        if self.brack_type == ANGLED:
            return program_state.toggle()

    def is_nilad(self):
        return True

class Monad:
    def __init__(self, string, args):
        self.brack_type = "({[<".find(string)
        self.args = args

    def exec(self, program_state):
        if self.brack_type == PARENTHESIS:
            value = 0
            for atom in self.args:
                value += atom.exec(program_state)
            program_state.push(value)

            return value

        if self.brack_type == SQUIGGLY:
            value = 0
            while program_state.peek():
                for atom in self.args:
                    value += atom.exec(program_state)

            return value

        if self.brack_type == SQUARE:
            value = 0
            for atom in self.args:
                value += atom.exec(program_state)

            return value * -1

        if self.brack_type == ANGLED:
            for atom in self.args:
                atom.exec(program_state)
            
            return 0

    def is_nilad(self):
        return False


class ProgramState:
    def __init__(self):
        self.stacks = [[], []]
        self.stack_index = 0
        self.active_stack = self.stacks[self.stack_index]

    def pop(self):
        return self.active_stack.pop()

    def stack_height(self):
        return len(self.active_stack)

    def toggle(self):
        self.stack_index ^= 1
        self.active_stack = self.stacks[self.stack_index]

    def push(self, value):
        self.active_stack.append(value)

    def peek(self):
        return self.active_stack[-1] if len(self.active_stack) else 0

    def print(self):
        print("\n".join(str(n) for n in self.active_stack[::-1]))

def parse(source):
    i = 0
    depth = 0
    commands = []
    while i < len(source):
        if source[i:i+2] in ("()", "{}", "[]", "<>"):
            commands.append(Nilad(source[i:i+2]))
            i += 2
        elif source[i] in "({[<":
            sub_commands, read = parse(source[i+1:])
            commands.append(Monad(source[i], sub_commands))
            i += read + 2
        elif source[i] in ")}]>":
            return commands, i

    return commands, i

state = ProgramState()
source = "(()()()())({({})({}[()])}{})"

for atom in parse(source)[0]:
    atom.exec(state)

state.print()
