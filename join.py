import csv
from collections import defaultdict
from difflib import SequenceMatcher


from_iit = []
with open('from_iit.csv') as csvfile1:
    reader = csv.DictReader(csvfile1)

    for row in reader:
        temp_dict1 = defaultdict(lambda x: 0)
        temp_dict1['last'] = row['last']
        temp_dict1['first'] = row['first']
        temp_dict1['IIT_rating'] = row['instructor_avg']
        temp_dict1['courses'] = row['courses']
        temp_dict1['confidence'] = row['confidence']
        from_iit.append(temp_dict1)

from_rmp = []
with open('rmp.csv') as csvfile2:
    reader = csv.DictReader(csvfile2)

    for row in reader:
        temp_dict2 = defaultdict(lambda x: 0)
        temp_dict2['last'] = row['last']
        temp_dict2['first'] = row['first']
        temp_dict2['rmp_rating'] = row['rmp_rating']
        temp_dict2['confidence'] = row['confidence']
        from_rmp.append(temp_dict2)

id = 1
with open('final.csv', 'w') as csvfile3:
    fieldnames = ['id', 'last', 'first', 'rmp_rating', 'confidence', 'IIT_rating', 'courses', 'overall']
    writer = csv.DictWriter(csvfile3, fieldnames=fieldnames)
    writer.writeheader()
    temp_dict3 = defaultdict(lambda x: 0)
    results=[]

    for professor1 in from_iit:
        found = False
        for professor2 in from_rmp:
            matched = False
            compare_string_prof1 = professor1['first']+', '+professor1['last']
            compare_string_prof2 = professor2['first']+', '+professor2['last']
            match_percentage = SequenceMatcher(a=compare_string_prof1,b=compare_string_prof2).ratio()
            if(match_percentage>.95):
                matched = True
            elif(match_percentage>.75):
                print(compare_string_prof1, " & ", compare_string_prof2)
                input_matched = input('Matched? y/n: ')
                if(input_matched=='y'):
                    matched = True
                    print('Matched!')
            if(matched):
                # Exists in both RMP and IIT
                temp_dict3['id'] = id
                id += 1
                temp_dict3['last'] = professor1['last']
                temp_dict3['first'] = professor1['first']
                if(professor2['rmp_rating']):
                    temp_dict3['rmp_rating'] = float(professor2['rmp_rating'])
                else:
                    temp_dict3['rmp_rating'] = None
                temp_dict3['confidence'] = int(professor2['confidence'])

                if(professor1['IIT_rating']):
                    temp_dict3['IIT_rating'] = float(professor1['IIT_rating'])
                else:
                    temp_dict3['IIT_rating'] = None

                temp_dict3['courses'] = professor1['courses']

                if not professor1['confidence']:
                    confidence1 = 0
                else:
                    confidence1 = int(professor1['confidence'])
                if not professor2['confidence']:
                    confidence2 = 0
                else:
                    confidence2 = int(professor2['confidence'])
                temp_dict3['confidence'] = confidence1 + confidence2

                # Find overall score
                if(temp_dict3['rmp_rating'] and temp_dict3['IIT_rating']):
                    temp_dict3['overall'] = ((temp_dict3['rmp_rating']*confidence2) + (temp_dict3['IIT_rating']*confidence1)) / (confidence1+confidence2)
                elif(temp_dict3['rmp_rating']):
                    temp_dict3['overall'] = temp_dict3['rmp_rating']
                elif(temp_dict3['IIT_rating']):
                    temp_dict3['overall'] = temp_dict3['IIT_rating']
                else:
                    temp_dict3['overall'] = None

                from_rmp.remove(professor2)
                found = True
                writer.writerow(temp_dict3)
                break
        if(not found):
            # Exists in IIT but not RMP
            temp_dict3['id'] = id
            id += 1
            temp_dict3['last'] = professor1['last']
            temp_dict3['first'] = professor1['first']
            temp_dict3['rmp_rating'] = None
            temp_dict3['confidence'] = 0
            if(professor1['IIT_rating']):
                temp_dict3['IIT_rating'] = float(professor1['IIT_rating'])
            else:
                temp_dict3['IIT_rating'] = None
            temp_dict3['courses'] = professor1['courses']
            temp_dict3['overall'] = temp_dict3['IIT_rating']
            temp_dict3['confidence'] = professor1['confidence']
            writer.writerow(temp_dict3)


    # in RMP but not IIT
    for professor3 in from_rmp:
        temp_dict3['id'] = id
        id += 1
        temp_dict3['last'] = professor3['last']
        temp_dict3['first'] = professor3['first']
        if(professor3['rmp_rating']):
            temp_dict3['rmp_rating'] = float(professor3['rmp_rating'])
        else:
            temp_dict3['rmp_rating'] = None

        temp_dict3['confidence'] = int(professor3['confidence'])
        temp_dict3['IIT_rating'] = None
        temp_dict3['courses'] = None
        temp_dict3['overall'] = temp_dict3['rmp_rating']
        writer.writerow(temp_dict3)
