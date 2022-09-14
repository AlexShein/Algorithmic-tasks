test = require("./test");

function assemblerInterpreter(rawProgram) {
  const labels = {};
  const reg = {};

  let [currInd, cmpRes] = [0, 0];
  let execStack = [0];
  let outBuff = "";

  const getVal = (x) => (isNaN(x) ? reg[x] : +x);

  cmdMap = {
    mov: (x, y) => {
      reg[x] = getVal(y);
      execStack[currInd] += 1;
    },
    inc: (x) => {
      reg[x] += 1;
      execStack[currInd] += 1;
    },
    dec: (x) => {
      reg[x] -= 1;
      execStack[currInd] += 1;
    },
    add: (x, y) => {
      reg[x] += getVal(y);
      execStack[currInd] += 1;
    },
    sub: (x, y) => {
      reg[x] -= getVal(y);
      execStack[currInd] += 1;
    },
    mul: (x, y) => {
      reg[x] *= getVal(y);
      execStack[currInd] += 1;
    },
    div: (x, y) => {
      reg[x] = (reg[x] / getVal(y)) | 0;
      execStack[currInd] += 1;
    },
    jmp: (label) => {
      execStack[currInd] = labels[label];
    },
    cmp: (x, y) => {
      cmpRes = getVal(x) === getVal(y) ? 0 : getVal(x) > getVal(y) ? 1 : -1;
      execStack[currInd] += 1;
    },
    jne: (label) => {
      if (cmpRes !== 0) execStack[currInd] = labels[label];
      else execStack[currInd] += 1;
    },
    je: (label) => {
      if (cmpRes === 0) execStack[currInd] = labels[label];
      else execStack[currInd] += 1;
    },
    jge: (label) => {
      if (cmpRes >= 0) execStack[currInd] = labels[label];
      else execStack[currInd] += 1;
    },
    jg: (label) => {
      if (cmpRes > 0) execStack[currInd] = labels[label];
      else execStack[currInd] += 1;
    },
    jle: (label) => {
      if (cmpRes <= 0) execStack[currInd] = labels[label];
      else execStack[currInd] += 1;
    },
    jl: (label) => {
      if (cmpRes < 0) execStack[currInd] = labels[label];
      else execStack[currInd] += 1;
    },
    call: (label) => {
      execStack[currInd + 1] = labels[label];
      currInd += 1;
    },
    ret: () => {
      execStack.pop(currInd);
      currInd -= 1;
      execStack[currInd] += 1;
    },
    msg: (...args) => {
      args.map((arg) => {
        if (arg[0] === "'") outBuff += arg.slice(1, -1);
        else {
          outBuff += getVal(arg);
        }
      });
      execStack[currInd] += 1;
    },
  };

  // Execution of program starts here

  function lineParser(line, lineNumber) {
    let [isString, isComment, isArgs] = [false, false, false];
    let [op, argBuff] = ["", ""];
    const args = [];

    for (let i = 0; i < line.length; i++) {
      const currChar = line[i];
      switch (currChar) {
        case "'":
          isString = !isString;
          argBuff += currChar;
          break;
        case ":":
          if (!isString) {
            labels[op] = lineNumber;
            op = "";
          } else argBuff += currChar;
          break;
        case ";":
          if (!isString) {
            isComment = true;
          }
          break;
        case " ":
          if (isString) argBuff += currChar;
          else if (!isArgs && op !== "") isArgs = true;
          break;
        case "\t":
          break;
        case ",":
          if (!isString && argBuff !== "") {
            args.push(argBuff);
            argBuff = "";
          } else if (isString) argBuff += currChar;
          break;
        default:
          if (!isArgs) op += currChar;
          else argBuff += currChar;
      }
      if (isComment) break;
    }
    if (argBuff !== "") args.push(argBuff);

    return { op: op, args: args };
  }
  const program = rawProgram.split("\n").map(lineParser);

  while (true) {
    if (execStack[currInd] >= program.length) return -1;

    const { op, args } = program[execStack[currInd]];
    switch (op) {
      case "end":
        return outBuff || -1;
      case "":
        execStack[currInd] += 1;
        continue;
      default:
        cmdMap[op](...args);
        break;
    }
  }
}

const program = `
; My first program
mov  a, 5
inc  a
call function
msg  '(5+1)/2 = ', a    ; output message
end

function:
    div  a, 2
    ret`;
test.Assert("First program", assemblerInterpreter(program), "(5+1)/2 = 3");

const program_factorial = `
mov   a, 5
mov   b, a
mov   c, a
call  proc_fact
call  print
end

proc_fact:
    dec   b
    mul   c, b
    cmp   b, 1
    jne   proc_fact
    ret

print:
    msg   a, '! = ', c ; output text
    ret`;

test.Assert("Factorial", assemblerInterpreter(program_factorial), "5! = 120");

const program_fibonacci = `
mov   a, 8            ; value
mov   b, 0            ; next
mov   c, 0            ; counter
mov   d, 0            ; first
mov   e, 1            ; second
call  proc_fib
call  print
end

proc_fib:
    cmp   c, 2
    jl    func_0
    mov   b, d
    add   b, e
    mov   d, e
    mov   e, b
    inc   c
    cmp   c, a
    jle   proc_fib
    ret

func_0:
    mov   b, c
    inc   c
    jmp   proc_fib

print:
    msg   'Term ', a, ' of Fibonacci series is: ', b        ; output text
    ret`;

test.Assert(
  "Fibonacci",
  assemblerInterpreter(program_fibonacci),
  "Term 8 of Fibonacci series is: 21"
);

let program_mod = `
mov   a, 11           ; value1
mov   b, 3            ; value2
call  mod_func
msg   'mod(', a, ', ', b, ') = ', d        ; output
end

; Mod function
mod_func:
    mov   c, a        ; temp1
    div   c, b
    mul   c, b
    mov   d, a        ; temp2
    sub   d, c
    ret`;

test.Assert("Mod", assemblerInterpreter(program_mod), "mod(11, 3) = 2");

var program_power = `mov   a, 2            ; value1
mov   b, 10           ; value2
mov   c, a            ; temp1
mov   d, b            ; temp2
call  proc_func
call  print
end

proc_func:
    cmp   d, 1
    je    continue
    mul   c, a
    dec   d
    call  proc_func

continue:
    ret

print:
    msg a, '^', b, ' = ', c
    ret`;

test.Assert("2^10 = 1024", assemblerInterpreter(program_power), "2^10 = 1024");

var program_fail = `call  func1
call  print
end

func1:
    call  func2
    ret

func2:
    ret

print:
    msg 'This program should return -1'`;

test.Assert("-1", assemblerInterpreter(program_fail), -1);
