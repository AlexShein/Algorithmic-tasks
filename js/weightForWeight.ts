import { Assert } from "./test";

function digitsSum(value: string): number {
  return value
    .split("")
    .map((val) => parseInt(val))
    .reduce((acc, val) => acc + val, 0);
}

// Order string of numbers by sum of each numbers digits
// And order them alphabetically if digit sums are equal
export function orderWeight(input: string): string {
  return input
    .split(" ")
    .filter((value) => isFinite(parseInt(value)))
    .sort((value1, value2) => {
      const digitSum1 = digitsSum(value1);
      const digitSum2 = digitsSum(value2);
      return digitSum1 == digitSum2
        ? String(value1) > String(value2)
          ? 1
          : -1
        : digitSum1 > digitSum2
        ? 1
        : -1;
    })
    .join(" ");
}

Assert("Empty", orderWeight(""), "");
Assert("Toy case", orderWeight("11 100"), "100 11");
Assert("Toy case spaces", orderWeight(" 11 100   "), "100 11");
Assert(
  "Test Kata 1",
  orderWeight("103 123 4444 99 2000"),
  "2000 103 123 4444 99"
);
Assert(
  "Test Kata 2",
  orderWeight("2000 10003 1234000 44444444 9999 11 11 22 123"),
  "11 11 2000 10003 22 123 1234000 44444444 9999"
);
