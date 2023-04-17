from t2.rand import randlist, rand_generator
from t2.prime import is_prime
from timeit import repeat
from time import process_time

# fig, ax = plt.subplots()

wanted_sizes = [40, 56, 80, 128, 168, 224, 256, 512, 1024, 2048, 4096]
# wanted_sizes = [32]

batches = 5
jobs = 10

print("Generating random numbers \n \n \n")

for size in wanted_sizes:
    print(f"Starting benchmarks for {size} bit numbers with {batches} batches of {jobs} executions")
    
    lcg_generated = []
    xor_generated = []
    
    lcg_generator = rand_generator(method="lcg")
    xor_generator = rand_generator(method="xor")

    lcg_benchmark = repeat(lambda: lcg_generated.append(next(lcg_generator)), number=jobs)
    xor_benchmark = repeat(lambda: xor_generated.append(next(xor_generator)), number=jobs)
    
    lcg_average = (sum(lcg_benchmark) / len(lcg_benchmark))
    xor_average = (sum(xor_benchmark) / len(xor_benchmark))

    print(f"On average, for {size} bit numbers, LCG performed {jobs} generations on {(lcg_average * 1000):.2f} ms")
    print(f"On average, for {size} bit numbers, XOR performed {jobs} generations on {(xor_average * 1000):.2f} ms")

    with open('generated.numbers', 'a') as fp:
        fp.write(f"SIZE={size}\n\n")
        fp.write(f"ALGO=LCG\n")
        
        for n in lcg_generated:
            fp.write(str(n) + "\n")

        fp.write(f"ALGO=XOR")
        for n in xor_generated:
            fp.write(str(n) + "\n")
        

print("\n \n \n Generating prime numbers \n \n \n")

for size in wanted_sizes:
    start = process_time()

    print(f"Starting benchmarks for {size} bit numbers with {batches} batches of {jobs} executions")

    tries = 1

    generator = rand_generator(method="lcg", min_size=size)
    
    n = next(generator)

    while not is_prime(n):
        tries += 1
        n = next(generator)

    end = process_time()

    print(f"After {tries}, number {n} found as prime on {(end - start):.4} s")
