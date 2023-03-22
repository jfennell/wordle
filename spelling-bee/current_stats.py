import pprint
import sys

"""
>>> f=open('tmp', 'r')
>>> x = [x.strip() for x in f.readlines()]
>>> x
['Hail', 'Hailed', 'Halal', 'Hale', 'Hall', 'Head', 'Headed', 'Heal', 'Healed', 'Heap', 'Heaped', 'Heed', 'Heeded', 'Heel', 'Heeled', 'Held', 'Helipad', 'Hell', 'Help', 'Helped', 'Hide', 'Hill', 'Hilled', 'Hippie']
>>> prefix = {}
>>> length = {}
>>> for w in x:
...   p = w[:2]
...   prefix[p] = prefix.get(p, 0) + 1
...   l = len(w)
...   length[l] = length.get(l, 0) + 1
...
>>> prefix
{'Ha': 5, 'Hi': 4, 'He': 15}
>>> length
{4: 13, 5: 1, 6: 9, 7: 1}
>>>
"""

def analyze_spelling_bee_answers(found_words):
	prefixes = {}
	lengths = {}

	for w in found_words:
		p = w[:2]
		prefixes[p] = prefixes.get(p, 0) + 1

		l = len(w)
		lengths[l] = lengths.get(l, 0) + 1

	print("Prefixes found:", file=sys.stderr)
	pprint.pprint(prefixes, stream=sys.stderr)
	print("Lengths found:", file=sys.stderr)
	pprint.pprint(lengths, stream=sys.stderr)

def main(args=None):
	args = args or sys.argv[1:]

	if len(args) < 1:
		raise ValueError('No command line args... provide the words you found')

	path = args[0]

	print("Analyzing '{path}'", file=sys.stderr)
	with open(path, 'r') as f:
		words = [w.strip() for w in f.readlines()]
		analyze_spelling_bee_answers(words)


if __name__ == '__main__':
	main()
