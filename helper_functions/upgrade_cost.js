function partSum(upTo, multi) {
    return (upTo / 2) * (multi * (upTo + 1));
}

function partSumAny(start, end, multi) {
    return partSum(end, multi) - partSum(start - 1, multi);
}

function numberWithCommas(x) {
    return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

// var start = prompt("Current Level");
// if (start != null) {
//     console.log(start);
//     return;
// }
// var target = prompt("Target Level");
// if (target != null) {
//     console.log(target);
//     return;
// }

let start = 1;
let target = 10000;
if (start < 1 || target <= start) {
    console.log("Invalid Perimeters!");
    return;
}

let mul = [3000, 4000, 5000];
let thresh = [5000, 10000];
let cost = partSumAny(
    start < thresh[0] ? start : thresh[0],
    target < thresh[0] ? target : thresh[0] - 1,
    mul[0]
);
// console.log("cost up to 4999: " + numberWithCommas(cost));
if (target >= thresh[0]) {
    cost += partSumAny(
        start < thresh[1] ? thresh[0] : thresh[1],
        target < thresh[1] ? target : thresh[1] - 1,
        mul[1]
    );
}
// console.log("cost up to 9999: " + numberWithCommas(cost));
if (target >= thresh[1]) {
    cost += partSumAny(thresh[1], target, mul[2]);
}

cost = numberWithCommas(cost);
console.log(
    "Upgrade cost (" + start + " -> " + target + "): " + cost + " gold"
);
// write(cost);
// $("#header").html(cost);
