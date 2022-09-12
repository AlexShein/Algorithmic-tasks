test = require("./test");

/*
function receives list of strings which include following commands:
mov x y - copies y (either a constant value or the content of a register) into register x
inc x - increases the content of the register x by one
dec x - decreases the content of the register x by one
jnz x y - jumps to an instruction y steps away if x is not zero
*/
function simpleAssembler2(program) {
  // return a dictionary with the registers
  let currInd = 0;
  const reg = {};
  const getVal = (x) => (isNaN(x) ? reg[x] : +x);

  cmdMap = {
    mov: (x, y) => {
      reg[x] = getVal(y);
      currInd += 1;
    },
    inc: (x, _) => {
      reg[x] += 1;
      currInd += 1;
    },
    dec: (x, _) => {
      reg[x] -= 1;
      currInd += 1;
    },
    jnz: (x, y) => {
      if (getVal(x) !== 0) currInd += getVal(y);
      else currInd += 1;
    },
  };

  while (true) {
    if (currInd >= program.length) break;
    const [op, a, b] = program[currInd].split(" ");
    cmdMap[op](a, b);
  }
  return reg;
}

test.Assert(
  "First program",
  simpleAssembler2(["mov a 5", "inc a", "dec a", "dec a", "jnz a -1", "inc a"]),
  { a: 1 }
);

test.Assert(
  "Second program",
  simpleAssembler2(["mov a -10", "mov b a", "inc a", "dec b", "jnz a -2"]),
  { a: 0, b: -20 }
);
