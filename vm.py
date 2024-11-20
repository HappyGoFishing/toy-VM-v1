import sys, time

registers = {
	"pc": 0, # program  counter
	"r1": 0,
	"r2": 0,
	"r3": 0,
	"r4": 0,
}

def halt(message="no reason provided") -> None:
	print(f"halted: {message}")
	exit()

def mov(dest, s) -> None:	
	if s in registers:
		registers[dest] = registers[s]
	else:
		registers[dest] = int(s)


def add(dest, s1, s2) -> None:
	if s1 in registers and s2 in registers:
		registers[dest] = registers[s1] + registers[s2]

	elif s1 in registers:
		registers[dest] = registers[s1] + int(s2)

	elif s2 in registers:
		registers[dest] = int(s1) + registers[s2]
	else:
		registers[dest] = int(s1) + int(s2)
	

def sub(dest, s1, s2) -> None:
	if s1 in registers and s2 in registers:
		registers[dest] = registers[s1] - registers[s2]

	elif s1 in registers:
		registers[dest] = registers[s1] - int(s2)

	elif s2 in registers:
		registers[dest] = int(s1) - registers[s2]
	else:
		registers[dest] = int(s1) + int(s2)
	
def execute_instruction(instruction: str) -> None:
	parts = instruction.split()
	
	match parts[0]:
		case "mov":
			if len(parts) != 3:
				halt("malformed instruction move")
			else:
				mov(dest=parts[1], s=parts[2])

		case "add":
			if len(parts) != 4:
				halt("malformed instruction add")
			else:
				add(dest=parts[1], s1=parts[2], s2=parts[3])

		case "sub":
			if len(parts) != 4:
				halt("malformed instruction sub")
			else:
				sub(dest=parts[1], s1=parts[2], s2=parts[3])

		case "halt":
			halt("received instruction")

		case _:
			halt("unknown instruction")

	print(registers)
			


program: list[str]
with open(sys.argv[1], "r") as f:
	program = f.read().strip().split("\n")

while registers["pc"] < len(program):
	execute_instruction(program[registers["pc"]])
	registers["pc"] += 1
	time.sleep(0.5)