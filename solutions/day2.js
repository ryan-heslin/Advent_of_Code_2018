const fs = require('fs');

function get_checksums(lines) {
    let twos = threes = 0;
    two_pattern = /([a-z])\1/
    for (line of lines) {
        // One-liner from https://stackoverflow.com/questions/19480916/count-number-of-occurrences-for-each-char-in-a-string
        let result = [...line].reduce((a, e) => { a[e] = a[e] ? a[e] + 1 : 1; return a }, {});
        let two_found = three_found = false;
        for (v of Object.values(result)) {
            if (two_found && three_found) break;
            if (v == 2) {
                two_found = true;
            } else if (v == 3) {
                three_found = true;
            }
        }
        twos += two_found;
        threes += three_found;
    }
    return twos * threes;
}

function one_off(a, b) {
    found = false;
    for (let i = 0; i < a.length; i++) {
        if (a[i] != b[i]) {
            if (found) return false;
            found = true;
        }
    }
    return found;
}

function find_identical(combos) {
    for (combo of combos) {
        if (one_off(combo[0], combo[1])) return combo;
    }
}

function find_common(a, b) {
    for (let i = 0; i < a.length; i++) {
        if (!(a[i] == b[i])) {
            return a.slice(0, i).concat(a.slice(i + 1)).join("");
        }
    }
}

const raw_input = fs.readFileSync('inputs/day2.txt', 'utf-8').replace(/\n$/, "").split("\n");

const part1 = get_checksums(raw_input);
console.log(part1);

const arrs = raw_input.map((x) => [...x])
const combos = arrs.flatMap(
    (v, i) => arrs.slice(i + 1).map(w => [v, w])
);

const common = find_identical(combos)
part2 = find_common(common[0], common[1]);
console.log(part2)
