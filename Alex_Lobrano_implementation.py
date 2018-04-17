# Alex_Lobrano_implementation.py

import math
import random
import fractions
import hashlib
import string
import time
import sys

randnum = random.SystemRandom()

# Generate prime number of size n bits
def generate_prime(n, filename):
	
	for i in xrange(3*pow(n,2)):						# Try for 3*n^2 iterations to find a prime number
		p = randnum.getrandbits(n-1)					# Generate n-1 random bits
		p = format(p, 'b')								# Convert to binary string
		for i in range(n - len(p) - 1):
			p = "0" + p									# Add missing zeroes
		p = "1" + p										# Add 1 to front to ensure n bits
		p = int(p, 2)									# Convert back to int
		if(isPrimeMR(p, filename)): 					# Check using Miller-Rabin if p is prime
			return p

# Get number p, test if it's prime using Miller-Rabin
def isPrimeMR(p, filename):
	
	if(p % 2 == 0): 									# Check if p is even
		return False
	u = p - 1											# Set u = p - 1 to begin finding u*2^r
	u = u / 2											# u is now even, so divide it by 2
	r = 1												# r is now equal to 1
	while(u % 2 == 0):									# Continue dividing u by 2 and incrementing r until u is odd
		u = u / 2
		r += 1
	for j in range(10):									# Look for 10 strong witnesses
		a = randnum.randint(2, p-1)						# Choose a random number between 2 and p-1
		if(foundWitness(a,u,r,p)):						# Check if a is a strong witness for p being composite
			return False
	return True
	
# Get number p, test if it is composite by seeing if a is a strong witness with values u and r
def foundWitness(a, u, r, p):
	if((pow(a,u,p) != 1) and (pow(a,u,p) != p-1)):		# Test if a^u mod p is not equal to 1 or -1
		for i in range(1, r):							
			if(pow(a,2**i*u,p) == p-1):					# Test for all {1...r} if a^(u*2^i) is equal to -1
				return False							# If an a^(u*2^i) is equal to -1, then a is not a strong witness
		return True										# If all a^(u*2^i) were checked and none equaled -1, a is a strong witness 
	return False										# If a^u mod p is equal to 1 or -1, then a is not a strong witness

# Returns x such that a*x + b*y = g
def modinv(a, b):
    x0, x1, y0, y1 = 1, 0, 0, 1
    while a != 0:
        q, b, a = b // a, a, b % a
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1
    return y0
	#return b, y0, x0 #(g,x,y)
	
# Generates a string of size characters
def generate_string(size):
	temp = ''
	for i in range(size):
		temp += random.choice(string.ascii_letters + string.digits)
	return temp
	
class Hash_and_Sign_RSA:
	# Initialize RSA, generate e, d
	def __init__(self):
		pass

	# Use generate_prime	
	def gen(self, filename):
		
		# security parameter
		self.n = 1024
		
		# Primes p and q
		self.p = generate_prime(self.n, filename)		# Generate prime p
		self.q = generate_prime(self.n, filename)		# Generate prime q
		
		# RSA modulus N = pq
		self.rsamodulus = self.p * self.q				# Calculate RSA modulus N = p*q
		
		# Phi(N)
		self.phi = (self.p - 1)*(self.q - 1)			# Calculate phi(N) = (p-1)(q-1)
		
		# Public key e
		self.e = randnum.randint(1, self.phi - 1)		# Generate integer e between 1 and phi(N)-1
		while(fractions.gcd(self.e, self.phi) != 1):	# Check if e is relatively prime to phi(N)
			self.e = randnum.randint(1, self.phi - 1)	# If not relatively prime, generate new e and try again
		
		# Secret key d
		self.d = modinv(self.e, self.phi) + self.phi	# Calculate d as modular inverse of e
		
		return self.d, (self.rsamodulus, self.e)
	
	def sign(self, sk, m, N):
		hash = hashlib.sha256(str(m))					# Convert m to string and compute hash
		hash_int = int(hash.hexdigest(), 16)			# Convert hash to integer
		sigma = pow(hash_int, sk, N)					# Calculate sigma = hash_int^sk mod N
		return sigma
	
	def verify(self, pk, m, sigma, N):
		ver = format(pow(sigma, pk, N), 'x')			# Calculate ver = sigma^pk mod N and save as hex
		hash = hashlib.sha256(str(m))					# Convert m to string and compute hash
		if(hash.hexdigest() == ver): return 1 			# Check if H(m) equals ver
		else: return 0