from flask import Flask
from flask import request
from flask import render_template, jsonify, redirect
import json
import requests

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
@app.route("/<int:strava_id>", methods=['GET'])
def index(strava_id=None):

	if request.method == 'GET':
		if strava_id:
			strava_data = None
			strava_data = get_kom(strava_id)
			return render_template('rider.html', strava_data=strava_data)
		else:
			return render_template('index.html')


	elif request.method == 'POST':
		if request.form['strava_id']:
 			strava_id = request.form['strava_id']
 			redirect_url ='/'+ strava_id
 			return redirect(redirect_url)
	else:
		return render_template('page_not_found.html'), 404

#@app.route('/get_strava_data')
def get_kom(strava_id):
	
	rides = {}
	#Initial API call with no offset
	offset = 0
	payload = {'athleteId': strava_id, 'offset': offset}
	returned_api_data = requests.get("http://app.strava.com/api/v1/rides?", params=payload)

	#While you are still getting JSON data, continue to call API
	while (True):
		#print returned_api_data.json[u'rides']
		# There's got to be a more pythonic way to check whether you are still getting results?
		if len(returned_api_data.json[u'rides']) > 0:
			for ride in returned_api_data.json[u'rides']:

				#Gets the segment efforts on a specific ride
				efforts_index = requests.get("http://app.strava.com/api/v2/rides/" + str(ride[u'id']) + "/efforts")
				#print efforts_index.json[u'id']

				#For all of the efforts, check to get their 
				for effort in efforts_index.json[u'efforts']:
				 	print effort[u'effort']
					# effort_show = requests.get("http://app.strava.com/api/v2/rides/" + str(ride[u'id']) + "/efforts/" + str(effort[u'effort'][u'id']))
					# try:
					# 	leaderboard_rank = effort_show.json
					# 	print leaderboard_rank
					# except KeyError, e:
					# 	print "failed to find leaderboard_rank"

				# 		#Gives you KOM owner info
				# 	#

		# 		# 		#Gives you Category climb info
		# 		# 	#print effort_show.json['segment']['climb_category']

		# 		# 		#Gives you your best rank
		# 		# 	#print effort_show.json['leaderboard']['best']['rank']

		# 		# 		#Gives you your best info
		# 		# 		#Throws key error if this is your first time
		# 		# 	print effort_show.json['leaderboard']['best']['effort']

						
					
		# 			#print "Segment {segment} rank: {leaderboard_rank}".format(segment=effort['segment']['id'], leaderboard_rank=effort_show.json['leaderboard']['rank'])  
		# 		#ride['id'] 
		# 		#print ride
		# 		#print ""
		

		print "		Printed all rides in offset %d" % offset
		offset += 50
		print "		New offset: %d" % offset

		
		

		payload = {'athleteId': strava_id, 'offset': offset}
		returned_api_data = requests.get("http://app.strava.com/api/v1/rides?", params=payload)

		
	return "Test"

if __name__ == '__main__':
	app.debug = True
	app.run()