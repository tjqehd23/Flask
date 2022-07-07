from flask import Flask, redirect
from flask import request

app = Flask(__name__)

nextId = 4
topics = [
    {'id': 1, 'title': 'html', 'body': 'html is ...'},
    {'id': 2, 'title': 'css', 'body': 'css is ...'},
    {'id': 3, 'title': 'javascript', 'body': 'javascript is ...'}
]

def template(contents,content, id=None):
    contextUI = ''
    if id != None:
        # id 값이 있다면 contextUI값이 만들어짐
        contextUI = f'''
            <li><a href="/create/">create</a></li>
            <li><a href="/update/{id}/">update</a></li>
            <li><form action="/delete/{id}/" method="POST"><input type="submit" value='delete'></form></li>
        '''
    return f'''<!doctype html>
    <html>
        <body>
            <h1><a href="/">WEB</a></h1>
            <ol>
                {contents}
            </ol>
            {content}
            <ul>
            
                {contextUI}
            </ul> 
        </body>
    </html>
    '''

def getContents():
    liTags = ''
    for topic in topics: 
        liTags += f'<li><a href="/read/{topic["id"]}">{topic["title"]}</a></li>'
    return liTags

# =========================================================================================

@app.route("/")
def index():
    return template(getContents(), '<h2>Welcome</h2>Hello, WeB')
        
# =========================================================================================

@app.route('/read/<int:id>/')
# id가 문자열로 들어오기 떄문에 int로 지정
def read(id):
    title = ''
    body = ''
    for topic in topics:
        if id == topic['id']:
            title = topic['title']
            body = topic['body']
            break  
    return template(getContents() , f'<h2>{title}</h2>{body}', id) 

# =========================================================================================

@app.route('/create/', methods=['GET', 'POST'])
def create():
    # print('request.method', request.method)
    if request.method == 'GET':
        content = '''   
        <form action="/create/" method="POST">
            <p><input type="text" name="title" placeholder="title"></p>
            <p><textarea name="body" placeholder="body"></textarea></p>
            <p><input type="submit" value="create"></p>
        </form> 
    '''
    # 어떤 주소를 누가 담당할 것인가
    # 어떤 요청을 어떤 함수가 응답할 것인가 연결해주는 작업을 라우팅
    # 그런 작업을 기술하는 어떠한 것들을 라우터
    
    # 사용자가 입력한 정보를 서버로 전송하는 역할 = form태그 
    # 서버에 어떤 경로로 전송할 것인가 = action속성
    # 각각의 값을 어떠한 이름으로 전송할 것인가 = name속성
    
    # url를 통해 서버로 데이터를 전송하는 방식 = GET방식(동적으로 동작하는 
    # 웹서비스에서 특정한 페이지를 식별하는 고유한 주소로써 사용되는 것)
    # 특정페이지를 읽어올 때 
    
    # 값을 변경할 때는 = POST방식
    # 데이터가 url을 통해 전송되지 않음(데이터가 URL에 포함되지 않음)
    # 큰 데이터도 안전하게 보낼 수 있음 
    # 값을 바꿀 때 
    # 라우트가 허용하게 하기위해 라우트가 허용하는 methods를 지정해야함
    # 데이터를 추가하는 로직을 보면 request.method가 POST인지 확인하라고 나와있는데 그럴려면
    # request(웹브라우저가 웹서버한테 전송한 여러가지 정보,상태) 
    # request라고하는 모듈을 import해야 함 - from flask import request
    # 이를 통해  request.method를 통해서 flask는 요청한 것이 GET인지 POST인지 구별 하는 것을 알 수 있음
    # request.form 을 이용해서 POST방식으로 전송한 데이터('title'과 'body)를 가져올 수 있다.
    
        return template(getContents(), content)
    elif request.method == 'POST':
        global nextId 
        title = request.form['title']
        body = request.form['body']
        newTopic = {'id':nextId, 'title':title, 'body':body}
        topics.append(newTopic)
        url = '/read/'+ str(nextId) + '/'
        nextId = nextId + 1
        # 전역 영역에 있는 전역 변수 = nextId
        # 전역 변수를 바꿀 때는 그 전역 변수가 사용되기 이 전 코드에서 global nextId(nextId는 전역변수다 라고 지정) 
        # 덕분에 nextId = nextId + 1 가 가능함 
        # /read/생성 된 아이디로 이동해야 되는데
        # 어디로 이동할 때 명령하기 위해선 - from flask import redirect추가 
        # url주소로 사용자의 브라우저를 보내버림 - redirect(url)
        return redirect(url)

# =========================================================================================
    
@app.route('/update/<int:id>/', methods=['GET', 'POST'])
def update(id):
    # print('request.method', request.method)
    if request.method == 'GET':
        title = ''
        body = ''
        for topic in topics:
            if id == topic['id']:
                title = topic['title']
                body = topic['body']
                break  
        content = f'''   
        <form action="/update/{id}/" method="POST">
            <p><input type="text" name="title" placeholder="title" value="{title}"></p>
            <p><textarea name="body" placeholder="body">{body}</textarea></p>
            <p><input type="submit" value="update"></p>
        </form> 
    '''
    # update는 title과 body가 자동으로 들어가 있어야 편함
    
    
        return template(getContents(), content)
    elif request.method == 'POST':
        global nextId 
        title = request.form['title']
        body = request.form['body']
        for topic in topics:
            if id == topic['id']:
                topic['title'] = title
                topic['body'] = body

        url = '/read/'+ str(nextId) + '/'
      
        return redirect(url)
    
# =========================================================================================
    
@app.route('/delete/<int:id>/', methods=['POST'])
def delete(id):
    for topic in topics:
        if id == topic['id']:
            topics.remove(topic)
            break
    return redirect('/')
# index로 가면 됨 , 글을 삭제하면 상세보기 페이지로 갈 수 없기 때문에
    
# delete버튼을 눌렀을 때 링크로 이동되게 하면 사용자가 클릭하지 않았는데도 삭제가 일어나는 불상사가 일어날 수 있음
# 때문에 update같이 POST 방식으로 
    
app.run(debug=True)



