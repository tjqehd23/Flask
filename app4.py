from flask import Flask, redirect, url_for, request
app = Flask(__name__)

Platforms = [
    {'myName': 'KIM' },
    {'myName': 'RIN'},
    {'myName': 'AHN'}
]
def explan():
    liTags =''
    for Platform in Platforms:
        liTags += f'<li>{Platform["myName"]}</a></li>'
    return liTags

def templete(context,name):
      return f'''<html>
   <body>
      {context}
      <form action = "/login" method = "post">
         <p>Enter Name: {name}</p>
         <p><input type = "text" name = "myName" /></p>
         <p><input type = "submit" value = "submit" /></p>
      </form>
      
   </body>
</html>'''

@app.route('/')
def index():
   return templete(explan(),None) 


@app.route('/success/<name>')
def success(name):
   return templete(explan(),name)

@app.route('/login', methods = ['POST', 'GET'])
def login():
   if request.method == 'POST':
      user = request.form['myName']
      newPlatform = {'myName':user}
      Platforms.append(newPlatform)
      print(Platforms)
      return redirect(url_for('success', name = user))
   elif request.method == 'GET':
      user = request.args.get('myName')
      return redirect(url_for('success', name = user))
if __name__ == '__main__':
   app.run(debug = True)