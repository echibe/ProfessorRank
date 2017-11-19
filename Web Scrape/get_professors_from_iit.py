from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from twilio.rest import TwilioRestClient
import time
import sys, traceback
import signal
from collections import defaultdict
import csv

# Define Web driver and path location
driver = webdriver.Chrome(executable_path='/usr/local/lib/chromedriver')
driver.set_window_size(1400,1000)

# Navigate to myIIT
driver.get('https://my.iit.edu/cp/home/displaylogin')
WebDriverWait(driver,20).until(EC.presence_of_element_located((By.NAME, 'user')))

# Login with username/pass
username = driver.find_element_by_name('user')
username.send_keys('echibe')

password = driver.find_element_by_name('pass')
password.send_keys("PASS" + Keys.RETURN)

# Bug in IIT's system. Need to do this with the URL
driver.get('http://retention.iit.edu/student_mainmenu.php?')
instructors = []


def get_instructors():
    driver.get('http://retention.iit.edu/course_eval_summary_query.php')

    # Find and list all instructors
    WebDriverWait(driver,20).until(EC.presence_of_element_located((By.NAME, 'instructor[]')))

    select_box = driver.find_element_by_name('instructor[]')

    instructors_objects = [x for x in select_box.find_elements_by_tag_name('option')]
    return instructors_objects


def navigate_to_instructor_page(i):
    i.click()
    submit_button = driver.find_element_by_tag_name('input')
    submit_button.click()
    return

def parse_instructor_data(temp_instructor_dict):
    # Parse data on instructor's page
    rows = driver.find_elements_by_tag_name('tr')

    instructor_name = rows[1].find_elements_by_tag_name('td')[2].text
    temp_instructor_dict['first'] = instructor_name.split(',')[1][1:]
    temp_instructor_dict['last'] = instructor_name.split(',')[0]
    return rows

def parse_ratings_data(rows, temp_instructor_dict):
    # Lists of tuples (rating, weight)
    instructor_ratings = []
    course_ratings = []

    weight = 1
    # How quickly should the score's weight incriment
    incriment_multiplier = 1.05
    confidence = 0
    for idx, r in enumerate(rows):
        if idx is 0:
            continue
        cells = r.find_elements_by_tag_name('td')

        # Populate courses
        try:
            course = cells[1].text.split('-')[0]
            if course not in temp_instructor_dict['courses']:
                temp_instructor_dict['courses'].append(course)
        except:
            print('error 1')
        try:
            instructor_ratings.append((float(cells[3].text)*weight, weight))
            course_ratings.append((float(cells[4].text)*weight, weight))
            weight *= incriment_multiplier
            confidence += 1
        except ValueError:
            continue
    try:
        temp_instructor_dict['instructor_avg'] = round(sum([x for (x, y) in instructor_ratings])/sum([y for (x,y) in instructor_ratings]), 2)

        temp_instructor_dict['course_avg'] = round(sum([x for (x, y) in course_ratings])/sum([y for (x,y) in course_ratings]), 2)

        temp_instructor_dict['overall_avg'] = (temp_instructor_dict['instructor_avg'] + temp_instructor_dict['course_avg']) / 2

        temp_instructor_dict['confidence'] = confidence

    except ZeroDivisionError:
        print('Insufficient data')
    return

def write_to_csv(temp_instructor_dict, writer):
    writer.writerow(temp_instructor_dict)

with open('from_iit.csv', 'w') as csvfile:
    fieldnames = ['last', 'first', 'instructor_avg', 'course_avg', 'overall_avg', 'courses', 'confidence']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for idx in range(2, len(get_instructors())):
        temp_instructor_dict = defaultdict(list)
        instructors_objects = get_instructors()
        instructors_objects[0].click()

        navigate_to_instructor_page(instructors_objects[idx])
        rows = parse_instructor_data(temp_instructor_dict)
        parse_ratings_data(rows, temp_instructor_dict)
        instructors.append(temp_instructor_dict)
        write_to_csv(temp_instructor_dict, writer)

        driver.back()
        WebDriverWait(driver,20).until(EC.presence_of_element_located((By.NAME, 'instructor[]')))
