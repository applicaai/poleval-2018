nkjp: download decompress

download:
	curl 'http://clip.ipipan.waw.pl/NationalCorpusOfPolish?action=AttachFile&do=get&target=NKJP-PodkorpusMilionowy-1.2.tar.gz' --compressed -H 'Host: clip.ipipan.waw.pl' -H 'Referer: http://clip.ipipan.waw.pl/NationalCorpusOfPolish?action=AttachFile&do=view&target=NKJP-PodkorpusMilionowy-1.2.tar.gz' -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:59.0) Gecko/20100101 Firefox/59.0' -o data/NKJP-PodkorpusMilionowy-1.2.tar.gz
	curl -o data/poleval_test_ner_2018.json 'http://mozart.ipipan.waw.pl/~axw/poleval2018/poleval_test_ner_2018.json'
	curl -o data/POLEVAL-NER_GOLD.json 'http://mozart.ipipan.waw.pl/~axw/poleval2018/POLEVAL-NER_GOLD.json'
	curl -o scripts/poleval_ner_test.py 'http://mozart.ipipan.waw.pl/~axw/poleval2018/poleval_ner_test.py' && chmod +x scripts/poleval_ner_test.py

decompress:
	mkdir -p data/NKJP
	tar -xzf  data/NKJP-PodkorpusMilionowy-1.2.tar.gz -C data/NKJP/

clean:
	rm -rf NKJP-PodkorpusMilionowy-1.2.tar.gz data/NKJP

preprocess:
	./scripts/preprocess_nkjp.py

postprocess:
	./scripts/json_parse.py parse data/poleval_test_ner_2018.json data/test.tsv data/out.tsv data/out.json

evaluate:
	python3 scripts/poleval_ner_test.py -g data/POLEVAL-NER_GOLD.json -u data/out.json

packages:
	pip install -r requirements.txt

prepare: packages nkjp preprocess

models:
	mkdir -p data/models
	./scripts/train_tagger.py

tag:
	./scripts/tag.py

predict: tag postprocess
