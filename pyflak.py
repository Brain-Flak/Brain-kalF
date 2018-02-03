class Nilad:
    def __init__(self, string):
        self.brack_type = string

    def exec(self, program_state):
        if self.brack_type == "()":
            return 1
        if self.brack_type == "{}":
            return program_state.pop()
        if self.brack_type == "[]":
            return program_state.stack_height()
        if self.brack_type == "<>":
            return program_state.toggle()

    def is_nilad(self):
        return True

class Monad:
    def __init__(self, string, args):
        self.brack_type = string
        self.args = args

    def exec(self, program_state):
        if self.brack_type == "(":
            value = 0
            i = 0 if program_state.ip_dir == 1 else len(self.args) - 1

            while -1 < i < len(self.args):
                value += self.args[i].exec(program_state)
                i += program_state.ip_dir

            program_state.push(value)

            return value

        if self.brack_type == "{":
            value = 0


            while program_state.peek():
                orig_ip_dir = program_state.ip_dir

                i = 0 if program_state.ip_dir == 1 else len(self.args) - 1

                while -1 < i < len(self.args):
                    value += self.args[i].exec(program_state)
                    i += program_state.ip_dir

                if program_state.peek():
                    program_state.ip_dir *= -1

            return value

        if self.brack_type == "[":
            value = 0
            i = 0 if program_state.ip_dir == 1 else len(self.args) - 1

            while -1 < i < len(self.args):
                value += self.args[i].exec(program_state)
                i += program_state.ip_dir

            return value * -1

        if self.brack_type == "<":
            i = 0 if program_state.ip_dir == 1 else len(self.args) - 1

            while -1 < i < len(self.args):
                self.args[i].exec(program_state)
                i += program_state.ip_dir
            
            return 0

    def is_nilad(self):
        return False


class ProgramState:
    def __init__(self):
        self.stacks = [[], []]
        self.stack_index = 0
        self.active_stack = self.stacks[self.stack_index]
        self.ip_dir = 1

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

    def reverse_ip(self):
        self.ip_dir *= -1

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
source = "(()){(()){{}}}(()())"

atoms = parse(source)[0]
i = 0
while -1 < i < len(atoms):
    atoms[i].exec(state)
    i += state.ip_dir

state.print()
