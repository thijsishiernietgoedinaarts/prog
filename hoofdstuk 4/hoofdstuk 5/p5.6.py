def divisors(n):
    'returns the list of divisors of n'
    res = []
    for i in range(1, n +1):
        if n % i == 0:
            res.append(i)
    print(res)
divisors(8)