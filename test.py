from difflib import SequenceMatcher

a = 'Alon Mattox Batson'
b = 'Mattox Batson'

print(SequenceMatcher(a=a,b=b).ratio())
