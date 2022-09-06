test = require("./test");

const alphabet = "abcdefghijklmnopqrstuvwxyz";

function toLetters(number) {
  Math.floor(number / 26) % 26;
  return [
    alphabet[number % 26],
    alphabet[Math.floor(number / 26) % 26],
    alphabet[Math.floor(Math.floor(number / 26) / 26) % 26],
  ].join("");
}

function findTheNumberPlate(rawCustomerID) {
  customerID = rawCustomerID
  let numbers = String(((customerID) % 999 ) + 1).padStart(3, "0");
  let letters = toLetters(Math.floor((customerID) / 999));
  return letters + numbers;
}

test.Assert("Toy example 998", findTheNumberPlate(998), "aaa999");
test.Assert("Toy example 999", findTheNumberPlate(999), "baa001");
test.Assert("Test 3", findTheNumberPlate(3), "aaa004");
test.Assert("Test 1487", findTheNumberPlate(1487), "baa489");
test.Assert("Test 40000", findTheNumberPlate(40000), "oba041");
test.Assert("Test max", findTheNumberPlate(17558423), "zzz999");
test.Assert("Test 234567", findTheNumberPlate(234567), "aja802");
test.Assert("Test 43056", findTheNumberPlate(43056), "rba100");
