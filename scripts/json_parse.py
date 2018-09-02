#!/usr/bin/env python3

"""
Processes input and output files generating
the final, PolEval-compatible JSON.
"""

import sys
import fire
import json

class JsonParser(object):
    """ Wrapper for json style output/input """
    def __init__(self, jsonfile):
        self.tokenized_lines = []
        self.tokenized_numbers = []

        with open(jsonfile) as f:
            self.data = json.load(f)
            for number, d in enumerate(self.data):
                for line in d['text'].split('\n\n'):
                    self.tokenized_lines.append(line)
                    self.tokenized_numbers.append(number)

        self.second_access = False
        self.first_key = None

    def __getitem__(self, key):
        self.first_key = key
        self.second_access = True
        return self

    def __setitem__(self, key, value):
        if not self.second_access:
            raise ValueError('Trying to set JsonParser...')
        else:
            self.second_access = False
            if key not in self.data[self.first_key].keys():
                self.data[self.first_key][key] = value
            else:
                self.data[self.first_key][key] += value

    def get_data(self):
        """ Return current json text """
        return self.data

    def get_original(self):
        """ Return original (init values) text numbers & lines """
        return self.tokenized_numbers, self.tokenized_lines


class OutputConverter(object):
    """ Class wraper for fire """

    def parse(self, original, tokenized, predictions, output):
        """ Parse files to output """
        with open(tokenized) as tokens, open(predictions) as preds:
            Parser = JsonParser(original)
            last_num = -1
            first = True
            for token, line_pred, num, line in zip(
                    tokens, preds,
                    *Parser.get_original()):

                if num != last_num:
                    offset = 0
                    first = True

                for pred in line_pred.split():
                    text = self._allign_magic(line, token, pred, offset)
                    if first:
                        first = False
                    else:
                        text = "\n" + text
                    Parser[num]['answers'] = text

                last_num = num
                offset += len(line) + 2  # +2 is from '\n\n' breaking in "JSON"

        with open(output, 'w') as outfile:
            json.dump(Parser.get_data(), outfile)

    def _allign_magic(self, line, tokenized, prediction, offset):
        """ Takes orignal & toknized line and outputs a prediction match between them """
        assert len(tokenized) >= len(line), "Tokenized should be longer!"

        # Get prediction start & stop in word count
        preds = prediction.split(':')
        assert len(preds) > 1, "Malformed prediction: {}".format(prediction)
        label, places = preds[0], preds[1]
        # label = label.replace(".", "_")
        preds = [int(i) for i in places.split(',')]
        min_p, max_p = self._min_and_max(preds)

        # Change word count to char count
        tokens = tokenized.split(' ')
        assert len(tokens) >= max_p, "Wrong number of tokens!"
        start = stop = 0
        for num, token in enumerate(tokens):
            if num < min_p:
                start += len(token) + 1
                stop += len(token) + 1
            elif num < max_p:
                stop += len(token) + 1
            elif num == max_p:
                stop += len(token)
            else:
                break

        # Change char count from tokenized file to original
        num = 0
        from_start = 0
        from_stop = 0
        for char in line:
            # Can be changed to if char != tokenized[num]
            while char != tokenized[num]:
                if num < start:
                    from_start += 1
                    from_stop += 1
                elif num < stop:
                    from_stop += 1
                else:
                    break
                num += 1
            num += 1
        start -= from_start
        stop -= from_stop

        # Return NLP style output, with added offset for the whole document
        return "{} {} {}\t{}".format(
            label, start + offset, stop + offset, line[start:stop])

    @staticmethod
    def _min_and_max(data):
        """ Words counted from 1, not 0, hence '-1' """
        sort = sorted(data)
        return sort[0]-1, sort[-1]-1


if __name__ == "__main__":
    fire.Fire(OutputConverter)
