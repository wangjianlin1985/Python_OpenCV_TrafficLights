import datetime

from flask import Flask, render_template, request, jsonify
import sql
import json
import os
import video

# pip install flask
# pip install opencv_python
# pip install sqlite3

'''
1、6-7个路口显示（前台）
2、路口红绿灯显示（前台）
3、路口摄像头设置是否开启（前台）
4、路口红绿灯控制时间（前台）
5、路口红路灯直接控制（前台）
6、点击路口 显示当前摄像头内容（前台）
7、摄像头开启后录像保存，支持回放（后台）
8、当前人流统计（后台，假数据）
9、手动操作记录（后台）
10、车流人流信息变化
'''

app = Flask(__name__, static_folder="static", template_folder="./")
app.debug = True
app.send_file_max_age_default = datetime.timedelta(seconds=1)

ws = sql.WebSql()
Video = video.Video()

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/page', methods=['POST','GET'])
def page():
    json_data = request.get_data()
    json_data = json.loads(json_data)
    ord = ['纵向', '横向']
    #data = {'data':[1,sw,val]};
    # 结构，page，方向，颜色
    record = ' 手动操作路口{}{}红绿灯为{}'.format(json_data['data'][0], ord[json_data['data'][1]-1], json_data['data'][2])
    record = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + record
    ws.insert_record(json_data['data'][0],record)
    ws.save_web()
    print(record)
    return ''

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/admin/get')
def admin_get():
    print(ws.select('RECORD'))
    return {'data':ws.select('RECORD')}

@app.route('/admin/video')
def admin_video():
    dirs = os.listdir('static/movies')
    data = []
    for dir in dirs:
        if os.path.isfile(os.path.join('static/movies', dir))\
                and dir.endswith('.mp4'):
            data.append(os.path.join('static/movies', dir))
    print(data)
    return {'data':data}

@app.route('/admin/video/post', methods=['POST','GET'])
def admin_video_post():
    json_data = request.get_data()
    json_data = json.loads(json_data)
    print(json_data)
    if json_data['switch']:
        Video.start_video('static/movies/{}_road{}.mp4'.format(datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S"),json_data['id']))
    else:
        Video.stop_video()
    return ''


@app.route('/page1.html')
def page1():
    return render_template('page1.html')


@app.route('/page2.html')
def page2():
    return render_template('page2.html')


@app.route('/page3.html')
def page3():
    return render_template('page3.html')


app.run()
