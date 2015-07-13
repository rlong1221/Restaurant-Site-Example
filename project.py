#import Flask class from flask library
from flask import Flask
#create instance of the class using
app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Restaurant, Base, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

#decorator / routes to the last decorator, /hello
@app.route('/')
@app.route('/hello')
#if the instances route from the above routes, do the following function
def HelloWorld():
	restaurant = session.query(Restaurant).first()
	items = session.query(MenuItem).filter_by(restaurant_id = restaurant.id)
	output = ''
	for item in items:
		output += item.name
		output += '</br>'
		output += item.price
		output += '</br>'
		output += item.description
		output += '</br>'
		output += '</br></br>'
	return output

if __name__ == '__main__':
	#server reloads itself whenever it notices changes
    app.debug = True
    app.run(host='0.0.0.0', port=5000)