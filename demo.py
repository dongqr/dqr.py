from flask import Flask, render_template, request, redirect, make_response
from DButils import DButil

# 实例化Flask对象    __name__参数用于确定启动程序的位置
app = Flask(__name__)
db = DButil()


@app.route('/index')
def index():
    # 通过cookies判断判断用户是否登录
    name = request.cookies.get("name")
    if name:
        res = db.queryall()
        print(res)
        return render_template("index.html", res=res)
    else:
        return redirect('/loginHtml')


@app.route('/loginHtml')
def loginhtml():
    return render_template("login.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    # 拿到数据，判断
    name = request.form.get("name")
    pswd = request.form.get("pswd")
    print(name)
    print(pswd)
    if name:
        if pswd:
            # 判断是否在数据库中
            qres = db.queryone(name)
            print(qres)
            if qres:
                # 数据库已经存在用户名，可以验证密码
                res = db.login(name, pswd)
                print(res)
                if res:
                    mkr = make_response("登陆成功，进入首页")
                    mkr.set_cookie("name", name)
                    return mkr
                else:
                    # 密码错误，登录失败
                    print("登陆失败")
                    return redirect('/loginHtml')
            else:
                return "用户名不存在数据库中，请先注册"
        else:
            return "密码不能为空"
    else:
        return "用户名不能为空"


if __name__ == '__main__':
    app.run()
