# coding: utf-8

from flask import Flask, render_template
from school_data import SCHOOL_DATA
import csv
from flask_googlemaps import GoogleMaps 
from flask_googlemaps import Map
from flask.ext.bootstrap import Bootstrap
from school_data import SCHOOL_DATA


app = Flask(__name__)
GoogleMaps(app)
bootstrap = Bootstrap(app)

        

def map_markers(): 
    latlongs = []
    with open ('f_grades.csv', 'rU') as csvfile:
        mapthing = csv.reader(csvfile)
        for row in mapthing:
			latitude = float(row[11])
			longitude = float(row[12]) 
			t = (latitude,longitude)
			latlongs.append(t)
    return latlongs

list_of_markers = map_markers()

def map_infobox():
    info = []
    with open ('f_grades.csv', 'rU') as csvfile:
        names = csv.reader(csvfile)
        for row in names:
            school_name = row[1]
            info.append(school_name)
    return info

list_of_names = map_infobox()

def get_schools(source):
    schools = []
    for row in source:
        school_name = row["School Name"]
        schools.append(school_name)
    return schools

def get_profile(source, school):
    for row in source:
        if school == row['School Name']:
            district_name = row['District Name'].decode('utf-8')
            total_points_earned = row["Total Points Earned"]
            percent_total = row["Percent of Total Possible Points"]
            percent_tested = row["Percent Tested"]
            charter = row["Charter School"]
            title = row["Title I"]
            alt = row["Alternative/ESE Center School"]
            minority = row["Percent of Minority Students"]
            disadvan = row["Percent of Economically Disadvantaged Students"]
            address = row["Full Address"]
    return district_name, total_points_earned, percent_total, percent_tested, charter, title, alt, minority, disadvan, address

@app.route('/')
def mapview():
    mymap = Map(
        identifier="view-side",
        lat=27.995985,
        lng=-82.7344139,
        style="height:400px;width:500px",
        maptype="TERRAIN",
        zoom="6",
        infobox= list_of_names,
        markers={'http://maps.google.com/mapfiles/ms/icons/green-dot.png': list_of_markers}
		
				)
    schools = get_schools(SCHOOL_DATA)
    return render_template('index.html', mymap=mymap, SCHOOL_DATA=SCHOOL_DATA,     schools=schools)
    
	

@app.route('/profile/<school>')
def profile(school):
    schools = get_schools(SCHOOL_DATA)
    district_name, total_points_earned, percent_total, percent_tested, charter, title, alt, minority, disadvan, address = get_profile(SCHOOL_DATA, school)
    get_profile(SCHOOL_DATA, school)
  
		
    return render_template('profile_.html', school=school, district_name=district_name, total_points_earned=total_points_earned, percent_total=percent_total, percent_tested=percent_tested, charter=charter, title=title, alt=alt, minority=minority, disadvan=disadvan, address=address)       

#if __name__ == '__main__':
    #app.run(debug=True)