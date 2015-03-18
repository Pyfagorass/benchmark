"""
This script simply finds the number of primes below n (n=10^6)
in the most brute force manner possible to simply benchmark 
one service vs another.
"""

import time
import math
import multiprocessing as mp
import platform

print(platform.processor())

# Set Number of Cores
numCores = mp.cpu_count()

# Set Number Limit
n = 10**6

# Each test is run 5 times, and we take the average
results = []
for i in range(5):
    startTime = time.time()
    # PrimeCounting Code
    numPrimes = 0
    for testNumber in xrange(2, n):
        PrimeQ = True
        for testFactor in xrange(2, int(math.sqrt(testNumber)+1)):
            if testNumber % testFactor == 0:
                PrimeQ = False
        if PrimeQ == True:
            numPrimes += 1

    results.append(time.time()-startTime)

print("Single Process (seconds): " + str(sum(results)/5))
print("Sanity check: " + str(numPrimes))


print("")
"""
The code below is to do a multiprocess version
===============================================
"""

def primeCount(start, end, step_size, output):
    # step_size = number of processors
    numPrimes = 0
    for testNumber in xrange(start, end, step_size):
        PrimeQ = True
        for testFactor in xrange(2, int(math.sqrt(testNumber)+1)):
            if testNumber % testFactor == 0:
                PrimeQ = False
        if PrimeQ == True:
            numPrimes += 1
    
    output.put(numPrimes)    

# Each test is run 5 times, and we take the average
results = []
for i in range(5):
    startTime = time.time()
    # Define an output queue
    output = mp.Queue()
    # Setup list of processes to run
    processes = [mp.Process(target=primeCount, args=(2+m, n, numCores, output)) for m in range(numCores)]
    # Run procersses
    for p in processes:
        p.start()
    # Exit the completed processes
    for p in processes:
        p.join()
    # Get process results from the output queue
    numPrimes = sum([output.get() for p in processes])
    results.append(time.time()-startTime)

print("Multiprocess ("+str(numCores)+" cores) (seconds): " + str(sum(results)/5))
print("Sanity check: " + str(numPrimes))
