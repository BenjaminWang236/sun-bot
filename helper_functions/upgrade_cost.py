import sys
import sympy
from sympy import symbols


def verifyInputPerimeters(starting_level, target_level):
    """
    Return True if perimeters are valid
    Otherwise return False with explanation
    
    If this is a full-fledge project I'd use a
    lookup table for error codes, but this isn't
    """
    # return starting_level > 0 and target_level > starting_level
    if starting_level < 1:
        print(f"Current level {starting_level} must be at least 1")
        return 1
    if target_level == starting_level:
        print("No Upgrade Cost: 0")
        return 2
    if target_level < starting_level:
        print(
            f"Target level ({target_level}) not > current level ({starting_level})"
        )
        return 3
    return 0


def partialSum(upTo, sybs, expr):
    """
    n-th Partial Sum is equal to (n / 2) * (expr @ 1 + expr @ n)
    """
    expr2 = expr
    expr2 = (upTo / 2) * (expr2.subs(sybs[0], 1) + expr2.subs(sybs[0], upTo))
    return int(float(expr2.evalf()))


def partialSumFromAnywhere(start, end, sybs, expr):
    """
    n-th partial sum starting from i is equal to:
    n-th partial sum - (i-1)-th partial sum
    
    @parem: start is the 'i'
            end is the 'n'
    """
    # if end >= start:
    #     return 0
    target_total_cost = partialSum(end, sybs, expr)
    starting_total_cost = partialSum(start - 1, sybs, expr)
    print(
        f"Total costs: Target {target_total_cost:,} - Start {starting_total_cost:,}"
    )
    # return partialSum(end, sybs, expr) - partialSum(start - 1, sybs, expr)
    return target_total_cost - starting_total_cost


def upgrade_cost_total(target_level):
    """
    This problem is basically a "n-th Partial Sum" problem
    with three separate arithmetic series equations separated
    at thresholds up to 5k and 10k (exclusive):
    
    From 1 to 4,999, arithmetic series of 3000 * x
    From 5,000 to 9,999, arthmetic series of 4000 * x
    From 10,000 onward, arthmetic series of 5000 * x
    
    n-th partial sum is as follows:
    ∑cx from x = 1 up to x = n, where
    c is the constant aka the multiplier factors (ie. 3000, 4000, 5000),
    1 is the starting level,
    n is the target level
    
    Except current level might not be 1, so the problem becomes
    "n-th partial sum from i" or ∑cx from x = i up to x = n,
    where i denotes the starting level

    This can be reduced down to the difference of two "n-th Partial Sum"s:
    n-th Partial Sum - (i-1)-th Partial Sum
    = (∑cx from x = 1 up to x = n) - (∑cx from x = 1 up to x = i - 1)
    
    Lastly, the "n-th Partial Sum" has a neat formula:
    ∑cx from x = 1 up to x = n
    = ∑a from x = 1 up to x = n
    = (n / 2) * (a_1 + a_n), where
    a is the expression, 'cx' in this case
    a_1 is the expression 'cx' evaluated at x = 1
    a_n is the expression 'cx' evaluated at x = n
    """

    n = symbols("n")
    sybs = [n]
    exprs = [3000 * n, 4000 * n, 5000 * n]
    thresholds = [5000, 10000]

    cost = 0
    if target_level < thresholds[0]:
        cost += partialSum(target_level, sybs, exprs[0])
    elif target_level < thresholds[1]:
        cost += partialSum(thresholds[0] - 1, sybs, exprs[0])
        cost += partialSum(target_level, sybs, exprs[1])
        cost -= partialSum(thresholds[0] - 1, sybs, exprs[1])
    else:
        cost += partialSum(thresholds[0] - 1, sybs, exprs[0])
        cost += partialSum(thresholds[1] - 1, sybs, exprs[1])
        cost -= partialSum(thresholds[0] - 1, sybs, exprs[1])
        cost += partialSum(target_level, sybs, exprs[2])
        cost -= partialSum(thresholds[1] - 1, sybs, exprs[2])

    print(f'Total cost of {target_level:,} is {cost:,} gold')

    return cost


def upgrade_cost_diff(starting_level, target_level):
    """
    Difference between total costs of starting-level and target-level
    """
    return upgrade_cost_total(target_level) - upgrade_cost_total(
        starting_level)


def main():
    """
    Grow Castle Heros/Leaders/Towers Upgrade Cost (Gold) calculator
    
    main()
    """

    starting_level = int(float(input("Current Level:\n")))
    target_level = int(float(input("Target Level:\n")))
    cost = upgrade_cost_diff(starting_level, target_level)
    print(f"Upgrade Cost ({starting_level} -> {target_level}): {cost:,} gold")


if __name__ == "__main__":
    """
    If this is the file executed, main() will run.
    Otherwise main() will not run but the other functions are callable
    """
    main()
