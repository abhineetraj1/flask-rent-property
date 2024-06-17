from flask import *
import pymongo, os, datetime,shutil
from PIL import Image

DB = pymongo.MongoClient("mongodb://localhost:27017/")
RP = DB["rentproperty"]
Users = RP["users"]
Properties = RP["properties"]

app = Flask(__name__, static_folder="static",  template_folder="templates")

def rndm():
	return str(datetime.datetime.now()).replace(":","").replace(" ","").replace(".","").replace("-","")

@app.route("/", methods=["GET","POST"])
def index():
	if request.method == "GET":
		return render_template("index.html", msg=False)
	else:
		return render_template("search.html", properties=[i for i in Properties.find({"city":request.form["city"]})])

@app.route("/signup", methods=["GET","POST"])
def signup():
	if request.method == "GET":
		return render_template("signup.html", msg=False)
	else:
		for i in request.form:
			if request.form[i] == "":
				return render_template("signup.html", msg="Fill all appropiate details")
		if Users.find_one({"username":request.form["username"]}) == None:
			Users.insert_one({"name":request.form["name"],"username":request.form["username"],"password":request.form["password"],"email":request.form["email"],"phone":request.form["phone"],})
			return render_template("dashboard.html", msg=False, properties=[i for i in Properties.find({"username":request.form["username"]})], username=request.form["username"], password=request.form["password"], name=request.form["name"], phone=request.form["phone"])
		else:
			return render_template("signup.html", msg="Username already exists")

@app.route("/signin", methods=["GET","POST"])
def signin():
	if request.method == "GET":
		return render_template("signin.html", msg=False)
	else:
		try:
			if Users.find_one({"username":request.form["username"]})["password"] == request.form["password"]:
				name = Users.find_one({"username":request.form["username"]})["name"]
				phone = Users.find_one({"username":request.form["username"]})["phone"]
				return render_template("dashboard.html", msg=False, username=request.form["username"], password=request.form["password"], name=name, phone=phone,properties=[i for i in Properties.find({"username":request.form["username"]})])
			else:
				return render_template("signin.html", msg="Incorrect credentials")
		except:
			return render_template("signin.html", msg="Incorrect credentials")

@app.route("/post", methods=["POST"])
def post():
	for i in request.form:
		if request.form[i] == "":
			open("b","a").write(i)
			return render_template("dashboard.html", properties=[i for i in Properties.find({"username":request.form["username"]})], msg="Fill all appropiate details",username=request.form["username"],name=request.form["name"],phone=request.form["phone"])
	w= request.files["file"]
	w.save(w.filename)
	im = Image.open(w.filename)
	url = rndm()+".png"
	im.save(url)
	os.remove(w.filename)
	shutil.move(url,"static/properties/"+url)
	Properties.insert_one({"username":request.form["username"],"name":request.form["name"],"price":request.form["price"],"address":request.form["address"],"city":request.form["city"],"area":request.form["area"],"bedroom":request.form["bedroom"],"bathroom":request.form["bathroom"],"info":request.form["info"],"phone":request.form["phone"],"image":url})
	return render_template("dashboard.html", msg=False,username=request.form["username"],name=request.form["name"],phone=request.form["phone"], properties=[i for i in Properties.find({"username":request.form["username"]})])

@app.route("/delete", methods=["POST"])
def delete():
	try:
		for i in Properties.find():
			if str(i["_id"]) == request.form["_id"]:
				os.remove("static/properties/"+i["image"])
				Properties.delete_one(i)
	except Exception as a:
		open("delete_properties","a").write("\n",a)
		pass
	return render_template("dashboard.html", msg=False,username=request.form["username"],name=request.form["name"],phone=request.form["phone"], properties=[i for i in Properties.find({"username":request.form["username"]})])

@app.route("/profile/<user>")
def profile(user):
	for i in Users.find():
		if i["username"] == user:
			details= Users.find_one({"username":user})
			return render_template("profile.html",properties=[i for i in Properties.find({"username":user})], name=details["name"], phone=details["phone"], email=details["email"])
	return render_template("404.html")

@app.errorhandler(404)
def page_not_found(n):
	return render_template("404.html")

if __name__ == '__main__':
	app.run(debug=True)