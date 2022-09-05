export function Assert(description: string, got:any, expected: any): Boolean {

    if (got !== expected) {
        throw `Error running ${description}\nExpected ${expected}\nGot ${got}`
    }
    console.log(`Passed: ${description}`)
    return true
}
