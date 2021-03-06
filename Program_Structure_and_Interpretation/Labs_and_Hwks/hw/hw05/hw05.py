# Tree definition

def tree(label, branches=[]):
    """Construct a tree with the given label value and a list of branches."""
    for branch in branches:
        assert is_tree(branch), 'branches must be trees'
    return [label] + list(branches)

def label(tree):
    """Return the label value of a tree."""
    return tree[0]

def branches(tree):
    """Return the list of branches of the given tree."""
    return tree[1:]

def is_tree(tree):
    """Returns True if the given tree is a tree, and False otherwise."""
    if type(tree) != list or len(tree) < 1:
        return False
    for branch in branches(tree):
        if not is_tree(branch):
            return False
    return True

def is_leaf(tree):
    """Returns True if the given tree's list of branches is empty, and False
    otherwise.
    """
    return not branches(tree)

def print_tree(t, indent=0):
    """Print a representation of this tree in which each node is
    indented by two spaces times its depth from the root.

    >>> print_tree(tree(1))
    1
    >>> print_tree(tree(1, [tree(2)]))
    1
      2
    >>> numbers = tree(1, [tree(2), tree(3, [tree(4), tree(5)]), tree(6, [tree(7)])])
    >>> print_tree(numbers)
    1
      2
      3
        4
        5
      6
        7
    """
    print('  ' * indent + str(label(t)))
    for b in branches(t):
        print_tree(b, indent + 1)

def copy_tree(t):
    """Returns a copy of t. Only for testing purposes.

    >>> t = tree(5)
    >>> copy = copy_tree(t)
    >>> t = tree(6)
    >>> print_tree(copy)
    5
    """
    return tree(label(t), [copy_tree(b) for b in branches(t)])

def replace_leaf(t, old, new):
    """Returns a new tree where every leaf value equal to old has
    been replaced with new.

    >>> yggdrasil = tree('odin',
    ...                  [tree('balder',
    ...                        [tree('thor'),
    ...                         tree('loki')]),
    ...                   tree('frigg',
    ...                        [tree('thor')]),
    ...                   tree('thor',
    ...                        [tree('sif'),
    ...                         tree('thor')]),
    ...                   tree('thor')])
    >>> laerad = copy_tree(yggdrasil) # copy yggdrasil for testing purposes
    >>> print_tree(replace_leaf(yggdrasil, 'thor', 'freya'))
    odin
      balder
        freya
        loki
      frigg
        freya
      thor
        sif
        freya
      freya
    >>> laerad == yggdrasil # Make sure original tree is unmodified
    True
    """
    node_lable = new if is_leaf(t) and old == label(t) else label(t)
    return tree(node_lable, [replace_leaf(b, old, new) for b in branches(t)])

def print_move(origin, destination):
    """Print instructions to move a disk."""
    print("Move the top disk from rod", origin, "to rod", destination)

def move_stack(n, start, end):
    """Print the moves required to move n disks on the start pole to the end
    pole without violating the rules of Towers of Hanoi.

    n -- number of disks
    start -- a pole position, either 1, 2, or 3
    end -- a pole position, either 1, 2, or 3

    There are exactly three poles, and start and end must be different. Assume
    that the start pole has at least n disks of increasing size, and the end
    pole is either empty or has a top disk larger than the top n start disks.

    >>> move_stack(1, 1, 3)
    Move the top disk from rod 1 to rod 3
    >>> move_stack(2, 1, 3)
    Move the top disk from rod 1 to rod 2
    Move the top disk from rod 1 to rod 3
    Move the top disk from rod 2 to rod 3
    >>> move_stack(3, 1, 3)
    Move the top disk from rod 1 to rod 3
    Move the top disk from rod 1 to rod 2
    Move the top disk from rod 3 to rod 2
    Move the top disk from rod 1 to rod 3
    Move the top disk from rod 2 to rod 1
    Move the top disk from rod 2 to rod 3
    Move the top disk from rod 1 to rod 3
    """
    assert 1 <= start <= 3 and 1 <= end <= 3 and start != end, "Bad start/end"
    def move(height, curr = 1, dest = 3, via = 2):
        if height < 1:
            return
        move(height-1, curr, via, dest)
        print_move(curr, dest)
        move(height-1, via, dest, curr)
    # Determine the aux rod. (rod used to move things over without violating any of the rule)
    # used an XOR here for fun instead of creating if / else for all combos of start and end.
    # though there aren't many combos to go through in the first place
    aux_rod = list( set([start, end]) ^ set([1,2,3]) )[0]
    move(n, start, end, aux_rod)


def interval(a, b):
    """Construct an interval from a to b."""
    return [a, b]

def lower_bound(x):
    """Return the lower bound of interval x."""
    return x[0]

def upper_bound(x):
    """Return the upper bound of interval x."""
    return x[1]

def str_interval(x):
    """Return a string representation of interval x."""
    return '{0} to {1}'.format(lower_bound(x), upper_bound(x))

def add_interval(x, y):
    """Return an interval that contains the sum of any value in interval x and
    any value in interval y."""
    lower = lower_bound(x) + lower_bound(y)
    upper = upper_bound(x) + upper_bound(y)
    return interval(lower, upper)

def mul_interval(x, y):
    """Return the interval that contains the product of any value in x and any
    value in y."""
    p1 = lower_bound(x) * lower_bound(y)
    p2 = lower_bound(x) * upper_bound(y)
    p3 = upper_bound(x) * lower_bound(y)
    p4 = upper_bound(x) * upper_bound(y)
    return interval( min(p1, p2, p3, p4), max(p1, p2, p3, p4) )

def sub_interval(x, y):
    """Return the interval that contains the difference between any value in x
    and any value in y."""
    p1 = lower_bound(x) - lower_bound(y)
    p2 = lower_bound(x) - upper_bound(y)
    p3 = upper_bound(x) - lower_bound(y)
    p4 = upper_bound(x) - upper_bound(y)
    return interval( min(p1, p2, p3, p4), max(p1, p2, p3, p4) )
    

def div_interval(x, y):
    """Return the interval that contains the quotient of any value in x divided by
    any value in y. Division is implemented as the multiplication of x by the
    reciprocal of y."""
    assert lower_bound(y) > 0 and upper_bound(y) > 0 or lower_bound(y) < 0 and upper_bound(y) < 0
    reciprocal_y = interval(1/upper_bound(y), 1/lower_bound(y))
    return mul_interval(x, reciprocal_y)

def par1(r1, r2):
    return div_interval(mul_interval(r1, r2), add_interval(r1, r2))

def par2(r1, r2):
    one = interval(1, 1)
    rep_r1 = div_interval(one, r1)
    rep_r2 = div_interval(one, r2)
    return div_interval(one, add_interval(rep_r1, rep_r2))

def check_par():
    """Return two intervals that give different results for parallel resistors.

    >>> r1, r2 = check_par()
    >>> x = par1(r1, r2)
    >>> y = par2(r1, r2)
    >>> lower_bound(x) != lower_bound(y) or upper_bound(x) != upper_bound(y)
    True
    """
    r1 = interval(3, 5) 
    r2 = interval(1, 3) 
    return r1, r2

def multiple_references_explanation():
    return """I believe that she is correct in that par2 is a better implementation.
    If it is a multiple reference problems, then par2 has more 'hard' definitions of intervals
    at each step, ensuring that the each part of the formula is exactly what is needed. Conversely,
    par1 attempts to do it in one go. Which may have unwanted characteristics or intervals. 
    Also, par1 repeats r1 and r2  (variable that represents an uncertain number) in the 
    arguments of div_interval. Which goes agains the note in the question.
    """

def quadratic(x, a, b, c):
    """Return the interval that is the range of the quadratic defined by
    coefficients a, b, and c, for domain interval x.

    >>> str_interval(quadratic(interval(0, 2), -2, 3, -1))
    '-3 to 0.125'
    >>> str_interval(quadratic(interval(1, 3), 2, -3, 1))
    '0 to 10'
    """
    f = lambda x : a*x**2 + b*x + c
    lower, upper, inflection = lower_bound(x), upper_bound(x), -b/(2*a)
    crit_points = [f(lower), f(upper)]
    extreme = f(inflection)
    if inflection > lower and inflection < upper:
        crit_points += [extreme]
    return interval(min(crit_points), max(crit_points))

def polynomial(x, c):
    """Return the interval that is the range of the polynomial defined by
    coefficients c, for domain interval x.

    >>> str_interval(polynomial(interval(0, 2), [-1, 3, -2]))
    '-3 to 0.125'
    >>> str_interval(polynomial(interval(1, 3), [1, -3, 2]))
    '0 to 10'
    >>> str_interval(polynomial(interval(0.5, 2.25), [10, 24, -6, -8, 3]))
    '18.0 to 23.0'
    """
    ##Uses a brute force method to find the inflection points##
    ##Brute force method relies on rounding decimal places##

    # Function computation
    def f(x, constants):
        ans, pwr = constants[0], 1
        constants = constants[1:]
        for i in constants:
            ans += i*pow(x,pwr)
            pwr += 1
        return ans

    # Derivative of function computation
    def d_f(x, constants):
        ans, pwr = constants[1], 1
        constants = constants[2:]
        for i in constants:
            ans += (pwr+1)*i*pow(x,pwr)
            pwr += 1
        return ans
    
    # Finding inflection points that matter
    def find_local_inflection_points(start, end):
        """BRUTE FORCE"""
        _start = start
        inflection_points = []
        while start <= end:
            y = round(d_f(start, c), 4)
            if y == 0 and y > _start and y < end:
                inflection_points += [start]
            start = round(start + 0.0001, 4)
        return inflection_points


    crit_points = [f(lower_bound(x),c), f(upper_bound(x),c)] + \
                    find_local_inflection_points(lower_bound(x), upper_bound(x))
    
    return interval(min(crit_points), max(crit_points))
