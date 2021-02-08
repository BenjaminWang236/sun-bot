function partSum(upTo, multi) {
    return (upTo / 2) * (multi * (upTo + 1));
}

function numberWithCommas(x) {
    return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

function upgradeCostTotal(target) {
    let mul = [3000, 4000, 5000];
    let thresh = [5000, 10000];

    let cost = 0;
    if (target < thresh[0]) {
        cost += partSum(target, mul[0]);
    } else if (target < thresh[1]) {
        cost += partSum(thresh[0] - 1, mul[0]);
        cost += partSum(target, mul[1]);
        cost -= partSum(thresh[0] - 1, mul[1]);
    } else {
        cost += partSum(thresh[0] - 1, mul[0]);
        cost += partSum(thresh[1] - 1, mul[1]);
        cost -= partSum(thresh[0] - 1, mul[1]);
        cost += partSum(target, mul[2]);
        cost -= partSum(thresh[1] - 1, mul[2]);
    }
    console.log("Total cost of " + target+ " is " + cost)

    return cost;
}

function upgradeCostDiff(start, target) {
    return upgradeCostTotal(target) - upgradeCostTotal(start);
}

let start = Number(31) - 1;
let target = Number(32) - 1;

if (start < 1 || target <= start) {
    console.log("Invalid Perimeters!");
    // return;
}
else {
    cost = upgradeCostDiff(start, target);
    cost = numberWithCommas(cost);
    console.log(
        "Upgrade cost (" + (start + 1) + " -> " + (target + 1) + "): " + cost + " gold"
    );
    // write(cost);
    // $("#header").html(cost);
}
    