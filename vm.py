import sys, time
from ascii import ascii_table

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

def jmp(line) -> None:
	if line in registers:
		registers["pc"] = registers[line] -1
	else:
		registers["pc"] = int(line) -1

def jmpeq(line, cmp1, cmp2) -> None: # jump to line if equal
	if cmp1 in registers:
		if registers[cmp1] == int(cmp2):
			jmp(line=int(line))
	elif cmp2 in registers:
		if int(cmp1) == registers[cmp2]:
			jmp(line=int(line))
	else:
		if int(cmp1) == int(cmp2):
			jmp(line=int(line))

def jmpneq(line, cmp1, cmp2) -> None: # jump to line if NOT equal
	if cmp1 in registers:
		if registers[cmp1] != int(cmp2):
			jmp(line=int(line))
	elif cmp2 in registers:
		if int(cmp1) != registers[cmp2]:
			jmp(line=int(line))
	else:
		if int(cmp1) != int(cmp2):
			jmp(line=int(line))

def execute_instruction(instruction: str) -> None:
	parts = instruction.split()
	
	match parts[0]:
		case "mov":
			if len(parts) != 3: halt("malformed instruction mov")
			else: mov(dest=parts[1], s=parts[2])

		case "add":
			if len(parts) != 4: halt("malformed instruction add")
			else: add(dest=parts[1], s1=parts[2], s2=parts[3])

		case "sub":
			if len(parts) != 4: halt("malformed instruction sub")
			else: sub(dest=parts[1], s1=parts[2], s2=parts[3])
		
		case "jmp":
			if len(parts) != 2: halt("malformed instruction jmp")
			else: jmp(line=parts[1])
		
		case "jmpeq":
			if len(parts) != 4: halt("malformed instruction jmpeq")
			else: jmpeq(line=parts[1], cmp1=parts[2], cmp2=parts[3])
		
		case "jmpneq":
			if len(parts) != 4: halt("malformed instruction jmpneq")
			else: jmpneq(line=parts[1], cmp1=parts[2], cmp2=parts[3])

		case "halt":
			halt("received instruction")

		case _:
			halt(f"unknown instruction: ({instruction})")

	print(registers)
			

fallback_program = [
	"mov r1 1",
	"mov r2 1",
	"add r1 r1 r2",
	"jmpneq 2 r1 3",
]

program: list[str]
if len(sys.argv) <= 1:
	print("no program provided")
	print("usage: pass argv[1] as program path")
	exit(1)
else:
	print(f"using program {sys.argv[1]}")
	with open(sys.argv[1], "r") as f:
		program = f.read().strip().split("\n")

while registers["pc"] < len(program):
	execute_instruction(program[registers["pc"]])
	registers["pc"] += 1
	time.sleep(0.5)
print("successfully executed program")
