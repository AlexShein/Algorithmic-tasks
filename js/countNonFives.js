test = require("./test");

function countFivesOrder10(orderOf10) {
  let res = 1;
  for (let i = 1; i < orderOf10; i++) {
    res = res * 9 + 10 ** i;
  }
  return res;
}

function countFivesOrder10R(value, fivesCount, orderOf10, fivesPerOrderOf10) {
  const current10Power = 10 ** orderOf10;
  const nextFivesPerOrderOf10 = fivesPerOrderOf10 * 9 + current10Power;
  let numberOfFolds = Math.floor(value / current10Power);

  console.log(
    "Enter countFivesOrder10R f, value: ",
    value,
    "fivesCount: ",
    fivesCount,
    "orderOf10: ",
    orderOf10,
    "fivesPerOrderOf10: ",
    fivesPerOrderOf10,
    "current10Power: ",
    current10Power,
    "numberOfFolds: ",
    numberOfFolds,
    "nextFivesPerOrderOf10: ",
    nextFivesPerOrderOf10
  );
  if (numberOfFolds > 9) {
    [value, fivesCount] = countFivesOrder10R(
      value,
      fivesCount,
      orderOf10 + 1,
      nextFivesPerOrderOf10
    );
    numberOfFolds = Math.floor(value / current10Power);
    console.log(
      "Updated values after recursive call, ",
      "value: ",
      value,
      "fivesCount: ",
      fivesCount,
      "numberOfFolds: ",
      numberOfFolds
    );
  } else if (numberOfFolds == 5) {
    return [
      0,
      fivesCount + 5 * fivesPerOrderOf10 + value - 5 * current10Power + 1,
    ];
  }

  if (value > 0) {
    console.log(
      "If clause starts, ",
      "New value: ",
      value - numberOfFolds * current10Power,
      "New fivesCount: ",
      fivesCount +
        numberOfFolds * fivesPerOrderOf10 +
        (numberOfFolds > 5 ? current10Power - 1 : 0)
    );
    return [
      value - numberOfFolds * current10Power,
      fivesCount +
        numberOfFolds * fivesPerOrderOf10 +
        (numberOfFolds > 5 ? current10Power - 1 : 0),
    ];
  }
  console.log("Default return", value, fivesCount);
  return [0, fivesCount];
}

// Returns count of integers that don't include digit 5 in a given range
function GiveMeFive(start, end) {
  console.log("### got numbers: ", start, end);
  if (start < 0 && end < 0) {
    [start, end] = [-end, -start];
  } else if (start < 0) {
    return GiveMeFive(0, -start) + GiveMeFive(0, end);
  }
  if (start != 0) {
    return GiveMeFive(0, end) - GiveMeFive(0, start - 1);
  }
  if (end > 10) {
    [value, fivesCount] = countFivesOrder10R(end, 0, 1, 1);
    if (value >= 5) {
      fivesCount += 1;
    }
  } else {
    return end >= 5 ? 1 : 0;
  }

  return fivesCount;
}

function dontGiveMeFive(start, end) {
  return Math.abs(end - start) - GiveMeFive(start, end) + 1;
}

function bfSolution(start, end) {
  let counter = 0;
  for (let i = start; i <= end; i++) {
    if (String(i).includes("5")) counter += 1;
  }
  return counter;
}

console.log("900", bfSolution(0, 900));
console.log("10", countFivesOrder10(1), bfSolution(0, 10));
console.log("100", countFivesOrder10(2), bfSolution(0, 100));
console.log("1000", countFivesOrder10(3), bfSolution(0, 1000));
console.log("10000", countFivesOrder10(4), bfSolution(0, 10000));
// console.log('2000', dontGiveMeFive(1, 2000))
// console.log('3000', dontGiveMeFive(1, 3000))
// console.log('4000', dontGiveMeFive(1, 4000))
// console.log('5000', dontGiveMeFive(1, 5000))
// console.log('10000', dontGiveMeFive(1, 10000))

// console.log('-50 50', dontGiveMeFive(-50, 50))
// console.log('-55 53', dontGiveMeFive(-55, 53))
// console.log('-500 500', dontGiveMeFive(-500, 500))
// console.log('Count orders 967', 967 >> 1, 967 >> 2, 967 >> 3)

// console.log("5s in order (2) 100", countFivesOrder10(2));
// console.log("5s in order (3) 1000", countFivesOrder10(3));
// console.log('5s in order (4) 10000', countFivesOrder10(4))

// Tests

test.Assert("Toy example fives 545", GiveMeFive(0, 545), bfSolution(0, 545));
test.Assert("Toy example fives 7", GiveMeFive(0, 7), 1);
test.Assert("Toy example fives 16", GiveMeFive(0, 16), 2);
test.Assert("Toy example fives 15", GiveMeFive(0, 15), bfSolution(0, 15));
test.Assert("Toy example fives 57", GiveMeFive(0, 57), bfSolution(0, 57));
test.Assert(
  "Toy example fives 7 - 118",
  GiveMeFive(7, 118),
  bfSolution(7, 118)
);
test.Assert("small numbers only fives", GiveMeFive(-17, 9), 3);
// test.Assert("Larger example fives 98 - 435", GiveMeFive(98, 435), bfSolution(98, 435));
test.Assert(
  "Larger example fives 0 - 4304",
  GiveMeFive(0, 4304),
  bfSolution(0, 4304)
);
test.Assert(
  "Larger example fives 0 - 984",
  GiveMeFive(0, 984),
  bfSolution(0, 984)
);
test.Assert(
  "Larger example fives 984 - 4304",
  GiveMeFive(984, 4304),
  bfSolution(984, 4304)
);

test.Assert("small numbers", dontGiveMeFive(-17, 9), 24);
test.Assert("small numbers", dontGiveMeFive(1, 9), 8);
test.Assert("small numbers", dontGiveMeFive(4, 17), 12);
test.Assert("small numbers", dontGiveMeFive(-17, -4), 12);

test.Assert("larger numbers", dontGiveMeFive(984, 4304), 2449);
test.Assert("larger numbers", dontGiveMeFive(2313, 2317), 4);
test.Assert("larger numbers", dontGiveMeFive(-4045, 2575), 4819);
test.Assert("larger numbers", dontGiveMeFive(-4436, -1429), 2194);

// test.Assert(
//   "huge numbers",
//   dontGiveMeFive(40076, 215151422963990),
//   49707598394353
// );
// test.Assert(
//   "huge numbers",
//   dontGiveMeFive(-206981731, 223575697903165),
//   51841599744277
// );
// test.Assert(
//   "huge numbers",
//   dontGiveMeFive(-249022878360451, -249022878219653),
//   79380
// );
// test.Assert(
//   "huge numbers",
//   dontGiveMeFive(-90000000000000, 900000000000000),
//   203349266266321
// );

test.Assert("edge cases", dontGiveMeFive(0, 1), 2);
test.Assert("edge cases", dontGiveMeFive(5, 15), 9);
test.Assert("edge cases", dontGiveMeFive(-5, 4), 9);
test.Assert("edge cases", dontGiveMeFive(51, 60), 1);
