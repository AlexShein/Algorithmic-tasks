test = require('./test')

function encode(rawInput) {
  if (rawInput.length > 1) {
    shiftedStrings = [rawInput]
    for (let i = 0; i < rawInput.length - 1; i++) {
      shiftedStrings.push(shiftedStrings[i].slice(-1) + shiftedStrings[i].slice(0, rawInput.length - 1))
    }
    shiftedStrings.sort()
    return [
      shiftedStrings.map(item => item.slice(-1)).reduce((acc, curr) => acc + curr, ''),
      shiftedStrings.indexOf(rawInput),
    ]
  }
  return ['', -1]
}

function decode(rawEncoded, i) {
  if (rawEncoded !== '') {
    let length = 1,
      encoded = rawEncoded.split(''),
      shiftedStrings = [...encoded].sort()

    while (length < rawEncoded.length) {
      shiftedStrings = encoded.map((element, i) => element + shiftedStrings[i]).sort()
      length += 1
    }
    return shiftedStrings[i]
  }
  return ''
}

test.Assert('Encode empty', encode(''), ['', -1])
test.Assert('Encode 1', encode('bananabar'), ['nnbbraaaa', 4])
test.Assert('Encode 2', encode('Humble Bundle'), ['e emnllbduuHB', 2])
test.Assert('Encode 3', encode('Mellow Yellow'), ['ww MYeelllloo', 1])

test.Assert('Decode empty', decode('', -1), '')
test.Assert('Decode 1', decode('nnbbraaaa', 4), 'bananabar')
test.Assert('Decode 2', decode('e emnllbduuHB', 2), 'Humble Bundle')
test.Assert('Decode 3', decode('ww MYeelllloo', 1), 'Mellow Yellow')
