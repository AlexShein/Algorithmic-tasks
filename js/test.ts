export function Assert(description: string, got: any, expected: any): Boolean {
  if (typeof got === "object" && typeof expected === "object") {
    const keysGot = Object.keys(got);
    const keysExpected = Object.keys(expected);
    if (keysGot.length !== keysExpected.length) {
      throw `Error running ${description}. Expected key length ${keysExpected.length}. Got ${keysGot.length}`;
    }
    keysGot.map((key) => {
      if (got[key] !== expected[key]) {
        throw `Error running ${description}. Expected key ${key} to be ${expected[key]}. Got ${got[key]}`;
      }
    });
  } else if (got !== expected) {
    throw `Error running ${description}. Expected ${expected}. Got ${got}`;
  }
  console.log(`Passed: ${description}\n`);
  return true;
}
