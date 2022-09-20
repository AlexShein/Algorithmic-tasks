test = require("./test");

function getDifference(firstSet, secondSet) {
  return new Set([...firstSet].filter((element) => !secondSet.has(element)));
}

function recoverSecret(triplets) {
  const letters = new Set(),
    letterPrecedence = {},
    processedLetters = new Set();
  let result = "";

  // Get all letters and get Sets of preceding letters for each one
  triplets.map((triplet) => {
    triplet.map((letter, i) => {
      letters.add(letter);

      if (i > 0) {
        letter in letterPrecedence
          ? letterPrecedence[letter].add(triplet[i - 1])
          : (letterPrecedence[letter] = new Set([triplet[i - 1]]));
      } else if (!(letter in letterPrecedence))
        letterPrecedence[letter] = new Set();
    });
  });

  while (true) {
    for (let letter of getDifference(letters, processedLetters).keys()) {
      const precedingLetters = getDifference(
        // Leaving only unprocessed letters
        letterPrecedence[letter],
        processedLetters
      );

      if (precedingLetters.size == 0) {
        result += letter;
        processedLetters.add(letter);
        break;
      }
    }

    if (processedLetters.size == letters.size) return result;
  }
}

secret1 = "whatisup";
triplets1 = [
  ["t", "u", "p"],
  ["w", "h", "i"],
  ["t", "s", "u"],
  ["a", "t", "s"],
  ["h", "a", "p"],
  ["t", "i", "s"],
  ["w", "h", "s"],
];

test.Assert("Whatisup", recoverSecret(triplets1), secret1);
