import re
import csv
from collections import defaultdict

f = open('rmp.txt')
temp_dict = defaultdict(lambda x: 0)

with open('rmp.csv', 'w') as csvfile:
    fieldnames = ['last', 'first', 'rmp_rating', 'confidence']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for idx, line in enumerate(f):
        rating = line[0:3]
        end = line[3:]
        professor = re.search('(.*)(\s\d)', end).group(1)
        num_ratings = re.search('(\d+)', end).group(1)
        last = professor.split(',')[0]
        first = professor.split(',')[1]
        temp_dict['last'] = last
        temp_dict['first'] = first
        temp_dict['confidence'] = num_ratings
        try:
            temp_dict['rmp_rating'] = float(rating)
        except:
            temp_dict['rmp_rating'] = ''
        writer.writerow(temp_dict)
