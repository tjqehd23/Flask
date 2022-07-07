from flask import Flask, redirect
from flask import request

app = Flask(__name__)

nextId = 4
Platforms = [
    {'id': 1, 'company': 'instgram', 'rogo': 'instgram rogo is'},
    {'id': 2, 'company': 'fackbook', 'rogo': 'fackbook rogo is'},
    {'id': 3, 'company': 'twitter', 'rogo': 'twitter rogo is'}
]

def shape(context,contexts,id=None):
    contents=''
    if id != None:
        contents = f'''
            <li><a href="/create/">create</a></li>
            <li><a href="/update/{id}">update</a></li>
            <li><form action="/delete/{id}/" method="POST"><input type="submit" value='delete'></form></li>
        '''
    return f'''<!doctype html>
        <html>
            <body>
                <h1><a href="/">HOME</a></h>
                <ol>
                    {context}
                </ol>
                {contexts}
                <ul>
                    {contents}
                </ul>
            </body>
        </html>
        '''
        
def explan():
    liTags =''
    for Platform in Platforms:
        liTags += f'<li><a href="/read/{Platform["id"]}">{Platform["company"]}</a></li>'
    return liTags


@app.route("/")
def index():
    return shape(explan(), '<h2>HOME</h2>')
    
        
@app.route('/read/<int:id>/')
def read(id):
    company = ''
    rogo = ''
    for Platform in Platforms:
        if id == Platform['id']:
            company = Platform['company']
            rogo = Platform['rogo']
            break
    return shape(explan(), f'<h2>{company}</h2>{rogo}',id)


@app.route('/create/', methods=['GET', 'POST'])
def create():
    if request.method == 'GET':
        contexts = '''
        <form action="/create/" method="POST">
            <p><input type="text" name="company" placeholder="company"></p>
            <p><textarea name="rogo" placeholder="rogo"></textarea></p>
            <p><input type="submit" value="create"></p>
        </form>
        '''
        return shape(explan(), contexts)
    elif request.method == 'POST':
        global nextId 
        company = request.form['company']
        rogo = request.form['rogo']
        newPlatform = {'id':nextId,'company':company,'rogo':rogo}
        Platforms.append(newPlatform)
        url = '/read/' + str(nextId) + '/'
        nextId += 1
        return redirect(url)
    

@app.route('/update/<int:id>/', methods=['GET', 'POST'])
def update(id):
    if request.method == 'GET':
        company = ''
        rogo = ''
        for Platform in Platforms:
            if id == Platform['id']:
                company = Platform['company']
                rogo = Platform['rogo']
                break
        contexts = f'''
        <form action="/update/{id}/" method="POST">
            <p><input type="text" name="company" placeholder="company" value="{company}"></p>
            <p><textarea name="rogo" placeholder="rogo">{rogo}</textarea></p>
            <p><input type="submit" value="update"></p>
        </form>
        '''
        return shape(explan(), contexts)
    elif request.method == 'POST':
        global nextId 
        company = request.form['company']
        rogo = request.form['rogo']
        for Platform in Platforms:
            if id == Platform['id']:
                Platform['company'] = company 
                Platform['rogo'] = rogo 
              

        url = '/read/' + str(nextId) + '/'
      
        return redirect(url)
    

@app.route('/delete/<int:id>/', methods=['POST'])
def delete(id):
    for Platform in Platforms:
        if id == Platform['id']:
            Platforms.remove(Platform)
            break
    return redirect('/')


