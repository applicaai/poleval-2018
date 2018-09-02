#!/usr/bin/env python3

"""
Tags input using all the trained models
and stores results in a single file
in our internal standard.
"""

import glob
import fire
from flair.data import Sentence
from flair.models import SequenceTagger

def pop_results(s):
	opened = ''
	openedAt = -1
	res = list()
	for i, t in enumerate(s):
		g = t.get_tag('ner')
		tp = g.split('-')[-1]
		if (tp != opened or 'B-' in g) and opened != '':
			tmp = list()
			for j in range(openedAt, i):
				tmp.append(j+1)
			res.append(opened + ':' + ','.join([str(x) for x in tmp]))
			opened = ''
			openedAt = -1
		if g not in ('', 'O') and 'B-' in g:
			opened = tp
			openedAt = i
		t.add_tag('ner', '')
	return res

def tag_file(input_name='data/test.tsv',
	         output_name='data/out.tsv',
	         models_pattern='data/models/*/best-model.pt'):
	taggers = list()
	for file in glob.glob(models_pattern):
		taggers.append(SequenceTagger.load_from_file(file))
	with open(input_name) as input, open(output_name, 'w') as output:
		for line in input:
			s = Sentence(line.rstrip())
			res = list()
			for tagger in taggers:
				tagger.predict(s)
				res += pop_results(s)
			output.write(' '.join(res) + '\n')

if __name__ == "__main__":
    fire.Fire(tag_file)
