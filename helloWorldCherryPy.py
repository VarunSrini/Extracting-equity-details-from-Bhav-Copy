import redis
import random
import string
import os
import cherrypy
from os.path import abspath
import json

redis_host = "localhost"
redis_port = 6379
redis_password = ""

# The decode_repsonses flag here directs the client to convert the responses from Redis into Python strings
# using the default encoding utf-8.  This is client specific.
r = redis.StrictRedis(host=redis_host, port=redis_port, password=redis_password, decode_responses=True)


class StringGenerator(object):
    @cherrypy.expose
    def index(self):
        # add this in the head : <link href="/static/styles.css" rel="stylesheet">

        li = r.zrevrange("equity", 0, 9)
        
        '''li = []
        for i in range(10):
            d = {}
            d["name"] = i
            d["open"] = 10 + i
            d["high"] = i   
            d["low"] = i    
            d["close"] = i

            json_data = json.dumps(d)

            li.append(json_data)'''
        
        lis = []

        for i in li:
            lis.append(json.loads(r.get(r.get(i))))
        
        '''for i in li:
            lis.append(json.loads(i))'''

        return"""<html>
          <head>
              
          </head>
          <body>
              <form method="get" action="search">
                  <input type="text" name="mf" />
                  <button type="submit">Give it now!</button>
            </form>
            
            <div id="table01">
              <table id ="stocks" >
                  <tr>
                      <th>Name</th>
                      <th>Open</th>
                      <th>High</th>
                      <th>Low</th>
                      <th>Close</th>
                      
                  </tr>
                  <tr>
                      <td></td>
                      <td></td>
                      <td></td>
                      <td></td>
                      <td></td>
                  </tr>
                  <tr>
                      <td></td>
                      <td></td>
                      <td></td>
                      <td></td>
                      <td></td>
                  </tr>
                  <tr>
                      <td></td>
                      <td></td>
                      <td></td>
                      <td></td>
                      <td></td>
                  </tr>
                  <tr>
                      <td></td>
                      <td></td>
                      <td></td>
                      <td></td>
                      <td></td>
                  </tr>
                  <tr>
                      <td></td>
                      <td></td>
                      <td></td>
                      <td></td>
                      <td></td>
                  </tr>
                  <tr>
                      <td></td>
                      <td></td>
                      <td></td>
                      <td></td>
                      <td></td>
                  </tr>
                  <tr>
                      <td></td>
                      <td></td>
                      <td></td>
                      <td></td>
                      <td></td>
                  </tr>
                  <tr>
                      <td></td>
                      <td></td>
                      <td></td>
                      <td></td>
                      <td></td>
                  </tr>
                  <tr>
                      <td></td>
                      <td></td>
                      <td></td>
                      <td></td>
                      <td></td>
                  </tr>
                  <tr>
                      <td></td>
                      <td></td>
                      <td></td>
                      <td></td>
                      <td></td>
                  </tr>
              </table>
              </div>
              
              <script>
                  var arr = {a};

                  for(var i = 0; i < 10; i++){{
                      console.log(arr[i]["open"]);
                      console.log(arr[i]["name"])
                  }}

                  for(var i = 1; i <= 10; i++){{
                      document.getElementById("stocks").rows[i].cells[0].innerHTML = arr[i-1]["name"];
                      document.getElementById("stocks").rows[i].cells[1].innerHTML = arr[i-1]["open"];
                      document.getElementById("stocks").rows[i].cells[2].innerHTML = arr[i-1]["high"];
                      document.getElementById("stocks").rows[i].cells[3].innerHTML = arr[i-1]["low"];
                      document.getElementById("stocks").rows[i].cells[4].innerHTML = arr[i-1]["close"];
                  }}
                  
              </script>  
         </body>
        </html>""".format(a = lis)
    
    @cherrypy.expose
    def generate(self, length=8):
        #return ''.join(random.sample(string.hexdigits, int(length)))
        a = length
        return"""<html>
          <head></head>
          <body>
              <form method="get" action="index">
                  <button type="submit">Previous page</button>
              </form>
            
              <table>
                  <tr>
                      <th>String</th>
                  </tr>
                  <tr>
                      <td>{}</td>
                  </tr>
              </table>
         </body>
        </html>""".format(a)

    @cherrypy.expose
    def search(self, mf):
        #return ''.join(random.sample(string.hexdigits, int(length)))
        a = mf.strip()

        jsonObject = json.loads(r.get(str(a)))
        return"""<html>
          <head></head>
          <body>
              <form method="get" action="index">
                  <button type="submit">Previous page</button>
              </form>
            
              <table>
                  <tr>
                      <th>Name</th>
                      <th>Open</th>
                      <th>High</th>
                      <th>Low</th>
                      <th>Close</th>
                      
                  </tr>
                  <tr>
                      <td>{}</td>
                      <td>{}</td>
                      <td>{}</td>
                      <td>{}</td>
                      <td>{}</td>
                  </tr>
              </table>
         </body>
        </html>""".format(jsonObject["name"], jsonObject["open"],jsonObject["high"], jsonObject["low"],jsonObject["close"])


if __name__ == '__main__':

    '''CP_CONF = {
        '/': {
            'tools.sessions.on': True,
            'tools.staticdir.root': os.path.abspath(os.getcwd())
        },
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': './style'
        }
        }
    cherrypy.quickstart(StringGenerator(), '/', CP_CONF)'''

    cherrypy.quickstart(StringGenerator())

    



















    
