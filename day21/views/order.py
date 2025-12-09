from flask import Blueprint, redirect, session, render_template, request
from utils import db
from utils import cache
#蓝图对象
od = Blueprint('order', __name__)

@od.route('/order/list')
def order_list():

    user_info =  session.get('user_info')
    role = user_info.get('role') # 1_客户 2_管理员
    real_name = user_info['real_name']
    if role == 2:
        # select * from order
        data_list = db.fetch_all("select * from `order` left join userinfo on `order`.user_id = userinfo.id",[])

    else:
        # select * from order where user_id = user_info['id']
        data_list = db.fetch_all("select * from `order` left join userinfo on `order`.user_id = userinfo.id where `order`.user_id = %s ",[user_info['id'], ])

    static_dict ={
        1:{"text":"待执行","cls":"primary"},
        2:{"text":"正在执行","cls":"info"},
        3:{"text":"完成","cls":"success"},
        4:{"text":"失败","cls":"danger"}
    }

    print(data_list)
    return render_template("order_list.html", data_list=data_list, static_dict=static_dict, real_name=real_name)

@od.route('/order/create' , methods=['GET', 'POST'])
def order_create():
    if request.method == 'GET':
        return render_template('order_create.html')
    url = request.form['url']
    count = request.form['count']

    # 写入数据库
    user_info = session.get('user_info')
    params = [url,count,user_info['id']]
    order_id = db.insert("insert into `order`(url,count,user_id,status) values(%s,%s,%s,1)",params)


    # 写入redis
    cache.push_queue(order_id)

    return redirect("/order/list")
@od.route('/order/delete')
def delete_list():
    return "删除功能暂未实现"
