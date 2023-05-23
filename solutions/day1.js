const fs = require('fs');


function first_dupe(nums) {
    let seen = new Set();
    let value = 0;
    let i = 0;
    let length = nums.length;
    while (true) {
        value += nums[i];
        if (seen.has(value)) return value;
        seen.add(value);
        i = (i + 1) % length;
    }
}

const raw_input = fs.readFileSync('inputs/day1.txt', 'utf-8').replace(/\n$/, "").split("\n");
const numbers = raw_input.map(Number);
const part1 = numbers.reduce((x, y) => x + y);
console.log(part1);

const part2 = first_dupe(numbers);
console.log(part2);
