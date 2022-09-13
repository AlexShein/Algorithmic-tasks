test = require("./test");

function assemblerInterpreter(rawProgram) {
  const program = rawProgram.split("\n");
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
        // console.log("### Msg", "\narg = ", arg);
        if (arg[0] === "'") outBuff += arg.replaceAll("'", "");
        else {
          // console.log(
          //   "#### Str",
          //   "\narg = ", arg,
          //   "\noutBuff + getVal(arg) = ",
          //   // String.raw(outBuff + getVal(arg))
          //   `"${outBuff + getVal(arg)}"`
          // );
          outBuff += getVal(arg);
        }
      });
      execStack[currInd] += 1;
    },
  };

  // Execution of program starts here

  // # TODO (Alexander Shein) Pre-process to remove labels and comments
  program.map((line, i) => {
    const labelEnd = line.search(":");
    const quoteStart = line.search("'");
    if (labelEnd != -1 && (quoteStart == -1 || labelEnd < quoteStart)) {
      labels[line.slice(0, labelEnd).trim()] = i;
      program[i] = line.slice(labelEnd + 1, line.length);
    }
  });

  console.log("Preparation ended\nlabels = ", labels);

  let counter = -1;
  while (true) {
    // Debug check
    // if (execStack[currInd] >= program.length || counter > 50) break;
    // Debug outputs
    counter += 1;
    console.log(
      "# Runner loop\ncounter = ",
      counter,
      "\nexecStack = ",
      execStack,
      "\ncurrInd = ",
      currInd,
      "\nreg = ",
      reg,
      "\noutBuff = ",
      `"${outBuff}"`
    );

    let line = program[execStack[currInd]].trim();
    // Comments processing
    const commentStart = line.search(";");

    console.log(
      "## Pre-Operation",
      "\nline = ",
      line,
      "\ncommentStart = ",
      commentStart,
      "\nprogram[execStack[currInd]] = ",
      program[execStack[currInd]]
    );

    if (commentStart == 0) {
      execStack[currInd] += 1;
      continue;
    } else if (commentStart != -1) line = line.slice(0, commentStart).trim();
    if (line === "") {
      execStack[currInd] += 1;
      continue;
    }
    // Get command and args
    const opEnd = line.search(" ") !== -1 ? line.search(" ") : line.length;
    const op = line.slice(0, opEnd);
    const [...args] = line
      .slice(opEnd, line.length)
      .split(",")
      .map((x) => x.trim())
      .filter((x) => x !== "");
    // Execute operation
    console.log(
      "## Operation\nop = ",
      op,
      "\nargs = ",
      args,
      "\nopEnd = ",
      opEnd,
      "\nline = ",
      line
    );
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
  // return outBuff || -1;
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
