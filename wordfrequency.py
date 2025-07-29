import sys
with open("file.txt", "r") as file:
    txt = file.read()
txt = txt.lower()
txt = txt.split()
frequencydict = {}
for word in txt:
    if word in frequencydict:
        frequencydict[word] += 1
    else:
        frequencydict[word] = 1
sortedwords = sorted(frequencydict.items(), key = lambda x: x[1], reverse=True)
n = int(sys.argv[1])
word = sortedwords[n-1]
print(word)
