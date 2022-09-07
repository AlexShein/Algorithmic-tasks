test = require("./test");

function countFivesOrder10(power) {
  let res = 1;
  for (let i = 1; i < power; i++) {
    res = res * 9 + 10 ** i;
  }
  return res;
}

// Returns count of integers that include digit 5 in a range [0 .. value]
function countFives(value, fivesCount, power, fivesPerPowerOf10) {
  const currentPowerOf10 = 10 ** power;
  const nextFivesPerPowerOf10 = fivesPerPowerOf10 * 9 + currentPowerOf10;
  let numberOfFolds = Math.floor(value / currentPowerOf10);

  if (numberOfFolds > 9) {
    [value, fivesCount] = countFives(
      value,
      fivesCount,
      power + 1,
      nextFivesPerPowerOf10
    );
    numberOfFolds = Math.floor(value / currentPowerOf10);
  }
  if (numberOfFolds == 5) {
    return [
      0,
      fivesCount + 5 * fivesPerPowerOf10 + value - 5 * currentPowerOf10 + 1,
    ];
  } else if (numberOfFolds > 5) {
    return [
      value - numberOfFolds * currentPowerOf10,
      fivesCount + (numberOfFolds - 1) * fivesPerPowerOf10 + currentPowerOf10,
    ];
  }
  return [
    value - numberOfFolds * currentPowerOf10,
    fivesCount + numberOfFolds * fivesPerPowerOf10,
  ];
}

// Returns count of integers that don't include digit 5 in a given range
function giveMeFive(start, end) {
    console.log("Entering giveMeFive with values: ", start, end);
    if (start < 0 && end < 0) {
    [start, end] = [-end, -start];
} else if (start < 0) {
    return giveMeFive(0, -start) + giveMeFive(0, end);
}
if (start != 0) {
    return giveMeFive(0, end) - giveMeFive(0, start - 1);
  }
  if (end > 10) {
      [value, fivesCount] = countFives(end, 0, 1, 1); // start with 10th and there's one five per each 10 except for 50
      if (value >= 5) {
          fivesCount += 1;
        }
    } else {
        return end >= 5 ? 1 : 0;
    }
    
    return fivesCount;
}

// Returns count of integers that don't include digit 5 in a given range
function dontGiveMeFive(start, end) {
  return Math.abs(end - start) - giveMeFive(start, end) + 1;
}

function bfSolution(start, end) {
  let counter = 0;
  for (let i = start; i <= end; i++) {
    if (String(i).includes("5")) counter += 1;
  }
  return counter;
}

console.log("57", bfSolution(0, 57));
console.log("800", bfSolution(0, 800));
console.log("10", countFivesOrder10(1), bfSolution(0, 10));
console.log("100", countFivesOrder10(2), bfSolution(0, 100));
console.log("1000", countFivesOrder10(3), bfSolution(0, 1000));
console.log("10000", countFivesOrder10(4), bfSolution(0, 10000));

// Tests

test.Assert("Toy example fives 545", giveMeFive(0, 545), bfSolution(0, 545));
test.Assert("Toy example fives 7", giveMeFive(0, 7), 1);
test.Assert("Toy example fives 16", giveMeFive(0, 16), 2);
test.Assert("Toy example fives 15", giveMeFive(0, 15), bfSolution(0, 15));
test.Assert("Toy example fives 57", giveMeFive(0, 57), bfSolution(0, 57));
test.Assert(
  "Toy example fives 7 - 118",
  giveMeFive(7, 118),
  bfSolution(7, 118)
);
test.Assert("small numbers only fives", giveMeFive(-17, 9), 3);
test.Assert(
  "Larger example fives 0 - 4304",
  giveMeFive(0, 4304),
  bfSolution(0, 4304)
);
test.Assert(
  "Larger example fives 0 - 400",
  giveMeFive(0, 400),
  bfSolution(0, 400)
);
test.Assert(
  "Larger example fives 0 - 500",
  giveMeFive(0, 500),
  bfSolution(0, 500)
);
test.Assert(
  "Larger example fives 0 - 600",
  giveMeFive(0, 600),
  bfSolution(0, 600)
);
test.Assert(
  "Larger example fives 0 - 984",
  giveMeFive(0, 984),
  bfSolution(0, 984)
);
test.Assert(
  "Larger example fives 984 - 4304",
  giveMeFive(984, 4304),
  bfSolution(984, 4304)
);
test.Assert(
  "Larger example fives 0 - 257",
  giveMeFive(0, 257),
  bfSolution(0, 257)
);
test.Assert(
  "Larger example fives -4045 - 2575",
  giveMeFive(-4045, 2575),
  bfSolution(-4045, 2575)
);

test.Assert("small numbers", dontGiveMeFive(-17, 9), 24);
test.Assert("small numbers", dontGiveMeFive(1, 9), 8);
test.Assert("small numbers", dontGiveMeFive(4, 17), 12);
test.Assert("small numbers", dontGiveMeFive(-17, -4), 12);

test.Assert("larger numbers", dontGiveMeFive(984, 4304), 2449);
test.Assert("larger numbers", dontGiveMeFive(2313, 2317), 4);
test.Assert("larger numbers", dontGiveMeFive(-4045, 2575), 4819);
test.Assert("larger numbers", dontGiveMeFive(-4436, -1429), 2194);

test.Assert(
  "huge numbers",
  dontGiveMeFive(40076, 215151422963990),
  49707598394353
);
test.Assert(
  "huge numbers",
  dontGiveMeFive(-206981731, 223575697903165),
  51841599744277
);
test.Assert(
  "huge numbers",
  dontGiveMeFive(-249022878360451, -249022878219653),
  79380
);
test.Assert(
  "huge numbers",
  dontGiveMeFive(-90000000000000, 900000000000000),
  203349266266321
);

test.Assert("edge cases", dontGiveMeFive(0, 1), 2);
test.Assert("edge cases", dontGiveMeFive(5, 15), 9);
test.Assert("edge cases", dontGiveMeFive(-5, 4), 9);
test.Assert("edge cases", dontGiveMeFive(51, 60), 1);
