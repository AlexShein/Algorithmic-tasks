export function Assert(description: string, got:any, expected: any): Boolean {

    if (got !== expected) {
        throw `Error running ${description}. Expected ${expected}. Got ${got}`
    }
    console.log(`Passed: ${description}`)
    return true
}
