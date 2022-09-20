test = require("./test");

function validateSegment(arrays) {
  let flatArr = [];
  arrays.forEach((curSet) => {
    flatArr = [...flatArr, ...curSet];
  });
  const numbersMap = new Map();
  for (let i = 1; i <= 9; i++) numbersMap.set(i, 0);
  for (item of flatArr) {
    if (numbersMap.has(item)) numbersMap.set(item, numbersMap.get(item) + 1);
    else return false;
  }
  return [...numbersMap.keys()].every((item) => numbersMap.get(item) === 1);
}

function validSolution(board) {
  for (let i = 0; i < 9; i++) {
    if (!validateSegment([board[i]])) return false; // Rows
    if (!validateSegment(board.map((arr) => arr.slice(i, i + 1)))) return false; // Columns
    if (i % 3 == 0) {
      for (let j = 0; j < 9; j += 3) {
        if (
          !validateSegment(
            board.slice(i, i + 3).map((arr) => arr.slice(j, j + 3))
          )
        )
          return false; // Segment
      }
    }
  }
  return true;
}

test.Assert(
  "S1",
  validSolution([
    [5, 3, 4, 6, 7, 8, 9, 1, 2],
    [6, 7, 2, 1, 9, 5, 3, 4, 8],
    [1, 9, 8, 3, 4, 2, 5, 6, 7],
    [8, 5, 9, 7, 6, 1, 4, 2, 3],
    [4, 2, 6, 8, 5, 3, 7, 9, 1],
    [7, 1, 3, 9, 2, 4, 8, 5, 6],
    [9, 6, 1, 5, 3, 7, 2, 8, 4],
    [2, 8, 7, 4, 1, 9, 6, 3, 5],
    [3, 4, 5, 2, 8, 6, 1, 7, 9],
  ]),
  true
);

test.Assert(
  "S1 false",
  validSolution([
    [6, 3, 4, 6, 7, 8, 9, 1, 2],
    [6, 7, 2, 1, 9, 5, 3, 4, 8],
    [1, 9, 8, 3, 4, 2, 5, 6, 7],
    [8, 5, 9, 7, 6, 1, 4, 2, 3],
    [4, 2, 6, 8, 5, 3, 7, 9, 1],
    [7, 1, 3, 9, 2, 4, 8, 5, 6],
    [9, 6, 1, 5, 3, 7, 2, 8, 4],
    [2, 8, 7, 4, 1, 9, 6, 3, 5],
    [3, 4, 5, 2, 8, 6, 1, 7, 9],
  ]),
  false
);

test.Assert(
  "S2",
  validSolution([
    [5, 3, 4, 6, 7, 8, 9, 1, 2],
    [6, 7, 2, 1, 9, 0, 3, 4, 8],
    [1, 0, 0, 3, 4, 2, 5, 6, 0],
    [8, 5, 9, 7, 6, 1, 0, 2, 0],
    [4, 2, 6, 8, 5, 3, 7, 9, 1],
    [7, 1, 3, 9, 2, 4, 8, 5, 6],
    [9, 0, 1, 5, 3, 7, 2, 1, 4],
    [2, 8, 7, 4, 1, 9, 6, 3, 5],
    [3, 0, 0, 4, 8, 1, 1, 7, 9],
  ]),
  false
);
