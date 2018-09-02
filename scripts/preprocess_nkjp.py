#!/usr/bin/env python3

"""
Processes NKJP into train and dev sets obeying our
internal standard.
"""

import glob
import re
from lxml import etree
from collections import defaultdict
import os
import fire

class Preprocessor(object):
	def __init__(self):
		self.DEV = ('TrybunaLudu_Trybuna', '030-2-000000005', '120-2-900140',
					'720-3-010000250', '711-3-010000065', '010-2-000000001',
					'TomaszewskaJasnosc', '130-5-000000062', '120-4-900002',
					'120-2-910000011', '120-4-900000001')

	def allptrs(self, ptrs, named2ptrs):
		newptrs = list()
		for ptr in ptrs:
			if 'named_' not in ptr:
				newptrs.append(ptr)
			else:
				# Recursive call
				newptrs += self.allptrs(named2ptrs[ptr][1], named2ptrs)
		return newptrs

	def prepare_fnl(self, tree, nss):
		named2ptrs = defaultdict(list)
		for seg in tree.findall('.//seg', namespaces=nss):
			named = seg.xpath('./@xml:id')[0]
			for f in seg.findall('fs/f', namespaces=nss):
				if f.get('name') == 'type':
					entity = f.getchildren()[0].get('value')
				elif f.get('name') == 'subtype':
					entity += '_' + f.getchildren()[0].get('value')
			ptrs = [f.get('target').split('_')[-1] if 'named_' not in f.get('target') else f.get('target') for f in seg.findall('ptr', namespaces=nss)]
			named2ptrs[named] = (entity, ptrs)
		fnl = list()
		for named in named2ptrs:
			entity, ptrs = named2ptrs[named]
			ptrs = self.allptrs(ptrs, named2ptrs)
			fnl.append((entity, ptrs))
		return fnl

	def preprocess(self, devset_path, trainset_path, morphosyntax_paths):
		with open(devset_path, 'w') as dev, open(trainset_path, 'w') as train:
			for file in glob.glob(morphosyntax_paths):
				namedfile = file.replace('morphosyntax', 'named')
				if not os.path.exists(namedfile):
					continue

				tree, nss = self.prepare_tree(namedfile)
				fnl = self.prepare_fnl(tree, nss)

				tree, nss = self.prepare_tree(file)
				for s in tree.findall('.//s', namespaces=nss):
					text = []
					ids = []
					for seg in s:
						ids.append(seg.get('corresp').split('_')[-1])
						text += [f.getchildren()[0].text for f in seg.findall('fs/f', namespaces=nss) if f.get('name') == 'orth']
					labels = list()
					for entity, targets in fnl:
						if len(targets) and targets[0] in ids:
							labels.append(entity + ':' + ','.join([str(ids.index(target) + 1) for target in targets]))
					directory = file.split('/')[2]
					if directory in self.DEV:
						dev.write(' '.join(labels) + '\t' + ' '.join(text) + '\n')
					else:
						train.write(' '.join(labels) + '\t' + ' '.join(text) + '\n')

	@staticmethod
	def prepare_tree(filename):
		tree = etree.parse(filename)
		nss = tree.getroot().nsmap
		return tree, nss


if __name__ == "__main__":
	# Usage is simply ./preprocess_nkjp.py
    fire.Fire(Preprocessor, command="preprocess data/dev.tsv data/train.tsv data/NKJP/*/ann_morphosyntax.xml")
