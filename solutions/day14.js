function expand_recipes(stop) {
    let elf1 = 0;
    let elf2 = 1;
    let target = Array.from(stop, Number);
    stop = Number(stop);
    let answer_length = 10;
    let recipes = [3, 7];
    let reader = read_digits();
    let run_index = last_start = 0;
    let part2_done = false;
    let part2 = null;
    let threshold = target.length
    let endpoint = stop + answer_length

    while ((recipes.length < endpoint) || !(part2_done)) {
        let next = reader(recipes[elf1] + recipes[elf2]);
        if (!part2_done) {
            // Only ever 1 or 2 digits
            for (let i = 0; i < next.length; i++) {
                if (run_index == threshold) {
                    part2 = last_start;
                    part2_done = true;
                    break
                }
                if (next[i] == target[run_index]) {
                    run_index++;
                } else {  //Failure, digits don't match
                    run_index = 0
                    last_start = recipes.length + i + 1 //+1 for zero index
                }
            }
        }
        recipes.push(...next);
        elf1 = (elf1 + recipes[elf1] + 1) % recipes.length;
        elf2 = (elf2 + recipes[elf2] + 1) % recipes.length;
    }
    return [recipes.slice(stop, stop + answer_length + 1), part2];

}

function read_digits() {
    let cache = {};
    return function(num) {
        if (num in cache) return cache[num];
        let result = (num < 10) ? [num] : [Math.floor(num / 10), num % 10]
        cache[num] = result;
        return result;
    }

}

const n_recipes = 306281;
const result = expand_recipes(String(n_recipes));
const part1 = result[0].join("").substring(0, 10);
console.log(part1);
console.log(result[1]);
