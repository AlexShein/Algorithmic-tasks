test = require("./test");

// Returns [operation, operand, optional_parameter]
function parseProgram(program) {
  return program.map((rawCommand) => {
    const commandArr = rawCommand.split(" ");
    return {
      op: commandArr[0],
      arg: isNaN(parseInt(commandArr[1]))
        ? commandArr[1]
        : parseInt(commandArr[1]),
      param:
        commandArr.length === 3
          ? isNaN(parseInt(commandArr[2]))
            ? commandArr[2]
            : parseInt(commandArr[2])
          : null,
    };
  });
}
/*
function receives list of strings which include following commands:
mov x y - copies y (either a constant value or the content of a register) into register x
inc x - increases the content of the register x by one
dec x - decreases the content of the register x by one
jnz x y - jumps to an instruction y steps away if x is not zero
*/
function simpleAssembler(rawProgram) {
  // return a dictionary with the registers
  const program = parseProgram(rawProgram);
  const commandsCount = program.length;
  let currentCommand = 0;
  const registers = {};

  while (true) {
    if (currentCommand >= commandsCount) break;
    command = program[currentCommand];
    switch (command.op) {
      case "mov": {
        registers[command.arg] =
          typeof command.param === "string"
            ? registers[command.param]
            : command.param;
        currentCommand += 1;
        break;
      }
      case "inc": {
        registers[command.arg] += 1;
        currentCommand += 1;
        break;
      }
      case "dec": {
        registers[command.arg] -= 1;
        currentCommand += 1;
        break;
      }
      case "jnz": {
        const condition =
          typeof command.arg === "string" ? registers[command.arg] : command.arg;
        if (condition !== 0) {
          currentCommand += command.param;
        } else currentCommand += 1;
        break;
      }
    }
  }
  return registers;
}

test.Assert(
  "First program",
  simpleAssembler(["mov a 5", "inc a", "dec a", "dec a", "jnz a -1", "inc a"]),
  { a: 1 }
);

test.Assert(
  "Second program",
  simpleAssembler(["mov a -10", "mov b a", "inc a", "dec b", "jnz a -2"]),
  { a: 0, b: -20 }
);
