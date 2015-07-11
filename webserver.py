from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Restaurant, Base, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

class webServerHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            if self.path.endswith("/restaurants"):

                restaurants = session.query(Restaurant).all()

                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"

                output += '<a href="restaurants/new">Add New Restaurant</a>'
                output += '</br></br></br>'

                for restaurant in restaurants:
                    output += restaurant.name
                    output += "</br>"
                    output += '''
                            <a href="/edit">Edit</a></br>
                            <a href="/delete">Delete</a></br></br></br></br>
                    '''
                output += "</body></html>"
                self.wfile.write(output)
                return

            if self.path.endswith("restaurants/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>Make a New Restaurant</h1>"
                output += '''
                    <form method='POST' enctype='multipart/form-data' action='/restaurants/new'>
                        <input name="restaurantName" type="text"><input type="submit" value="Create">
                    </form>
                    '''
                output += "</body></html>"
                self.wfile.write(output)
                return

            if self.path.endswith("restaurants/edit"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"

                output += "<h1></h1>"
                output += '''
                    <form method='POST' enctype='multipart/form-data' action='/restaurants'>
                        <input name="message" type="text" ><input type="submit" value="Edit">
                    </form>
                    '''

                output += "</body></html>"
                self.wfile.write(output)
                return

            if self.path.endswith("restaurants/delete"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"

                output += "<h1></h1>" 
                output += '''
                    <form method='POST' enctype='multipart/form-data' action='/restaurants'>
                        <input name="message" type="text" ><input type="submit" value="Delete">
                    </form>
                    '''

                output += "</body></html>"
                self.wfile.write(output)
                return

            # elif self.path.endswith("/hello"):
                
            #     self.send_response(200)
            #     self.send_header('Content-type', 'text/html')
            #     self.end_headers()
            #     output = ""
            #     output += "<html><body>"
            #     output += "<h1>Hello!</h1>"
            #     output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
            #     output += "</body></html>"
            #     self.wfile.write(output)
            #     print output
            #     return

            # elif self.path.endswith("/hola"):
            #     self.send_response(200)
            #     self.send_header('Content-type', 'text/html')
            #     self.end_headers()
            #     output = ""
            #     output += "<html><body>"
            #     output += "<h1>&#161 Hola !</h1>"
            #     output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
            #     output += "</body></html>"
            #     self.wfile.write(output)
            #     print output
            #     return

        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)

    def do_POST(self):
        try:
            if self.path.endswith("/restaurants/new"):
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                messagecontent = fields.get('restaurantName')

                #output = ""
                #output += "<html><body>"

                #output += " <h2> Okay, how about this: </h2>"
                #output += "<h1> %s </h1>" % messagecontent[0]

                newRestaurant = Restaurant(name = messagecontent[0])
                session.add(newRestaurant)
                session.commit()

                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                #Redirect back to restaurants
                self.send_header('Location', '/restaurants')
                self.end_headers()

                #output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
                
                #output += "</body></html>"
                #self.wfile.write(output)
                #print output
        except:
            pass


def main():
    try:
        port = 8080
        server = HTTPServer(('', port), webServerHandler)
        print "Web Server running on port %s" % port
        server.serve_forever()
    except KeyboardInterrupt:
        print " ^C entered, stopping web server...."
        server.socket.close()

if __name__ == '__main__':
    main()