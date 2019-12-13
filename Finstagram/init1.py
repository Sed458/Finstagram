from flask import Flask, render_template, request, session, redirect, url_for, send_file
import os
import uuid
import hashlib
import pymysql.cursors
from functools import wraps
import time

app = Flask(__name__)
app.secret_key = "super secret key"
IMAGES_DIR = os.path.join(os.getcwd(), "images")

connection = pymysql.connect(host="localhost",
                             user="root",
                             password="root",
                             db="Finstagram",
                             charset="utf8mb4",
                             port=8890,
                             cursorclass=pymysql.cursors.DictCursor,
                             autocommit=True)

def login_required(f):
    @wraps(f)
    def dec(*args, **kwargs):
        if not "username" in session:
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return dec

@app.route("/")
def index():
    if "username" in session:
        return redirect(url_for("home"))
    return render_template("index.html")

#Finstagram Home
@app.route("/home")
@login_required
def home():
    username = session['username']
    cursor = connection.cursor();

    ownedGroupsQuery = 'SELECT DISTINCT groupName, groupOwner FROM Friendgroup WHERE groupOwner = %s'
    cursor.execute(ownedGroupsQuery, (username))
    ownedGroupsData = cursor.fetchall()

    groupMembersQuery = 'SELECT * FROM BelongTo NATURAL JOIN Friendgroup WHERE groupOwner = %s and groupOwner = owner_username'
    cursor.execute(groupMembersQuery, (username))
    groupMembersData = cursor.fetchall()

    groupsJoinedQuery = 'SELECT DISTINCT groupName, groupOwner FROM Friendgroup NATURAL JOIN BelongTo WHERE member_username = %s and groupOwner = owner_username'
    cursor.execute(groupsJoinedQuery, (username))
    groupsJoinedData = cursor.fetchall()

    groupsJoinedMembersQuery = 'SELECT * FROM BelongTo NATURAL JOIN Friendgroup WHERE (groupName, owner_username) IN (SELECT groupName, owner_username FROM BelongTo WHERE member_username = %s) and groupOwner = owner_username'
    cursor.execute(groupsJoinedMembersQuery, (username))
    groupsJoinedMembersData = cursor.fetchall()

    # postsQuery = 'SELECT * FROM Photo WHERE photoPoster = %s OR photoID IN (SELECT photoID FROM Photo NATURAL JOIN SharedWith NATURAL JOIN BelongTo WHERE member_username = %s) OR photoPoster = (SELECT username_followed FROM Follow WHERE username_follower = %s) ORDER BY postingdate DESC'
    postsQuery = 'SELECT * FROM Photo NATURAL JOIN Person WHERE allFollowers = 1 AND photoPoster = username AND (photoPoster = %s OR photoID IN (SELECT photoID FROM Photo NATURAL JOIN SharedWith NATURAL JOIN BelongTo WHERE member_username = %s AND allFollowers = 1 AND photoPoster IN (SELECT username_followed FROM Follow WHERE username_follower = %s and followstatus = 1)) OR photoPoster IN (SELECT username_followed FROM Follow WHERE username_follower = %s and followstatus = 1)) ORDER BY postingdate DESC'
    cursor.execute(postsQuery, (username, username, username, username))
    posts = cursor.fetchall()

    tagQuery = 'SELECT * FROM Tagged Natural Join Person WHERE tagstatus = 1'
    cursor.execute(tagQuery)
    tagData = cursor.fetchall()

    likeQuery = 'SELECT * FROM Likes Natural Join Person'
    cursor.execute(likeQuery)
    likeData = cursor.fetchall()

    cursor.close()
    return render_template("home.html", username=username, ownedGroupsData=ownedGroupsData, groupMembersData=groupMembersData, groupsJoinedData=groupsJoinedData, groupsJoinedMembersData=groupsJoinedMembersData, posts=posts, tagData=tagData, likeData=likeData)

#Upload Image
@app.route("/upload", methods=["GET"])
@login_required
def upload():
    username = session["username"]
    cursor = connection.cursor();
    groupsJoinedQuery = 'SELECT DISTINCT groupName, groupOwner FROM Friendgroup NATURAL JOIN BelongTo WHERE member_username = %s and groupOwner = owner_username'
    cursor.execute(groupsJoinedQuery, (username))
    groupsJoinedData = cursor.fetchall()
    cursor.close()

    return render_template("upload.html", groupsJoinedData=groupsJoinedData)

#Search for posts by username
@app.route('/show_posts', methods=["GET", "POST"])
def show_posts():
    poster = request.form['poster']
    username = session["username"]

    cursor = connection.cursor();
    tagQuery = 'SELECT * FROM Tagged Natural Join Person WHERE tagstatus = 1'
    cursor.execute(tagQuery)
    tagData = cursor.fetchall()

    likeQuery = 'SELECT * FROM Likes Natural Join Person'
    cursor.execute(likeQuery)
    likeData = cursor.fetchall()

    try:
        if(poster == username):
            query = 'SELECT * FROM Photo NATURAL JOIN Person WHERE photoPoster = username AND photoPoster = %s'
            cursor.execute(query, (username))
            data = cursor.fetchall()
        else:
            # cursor = connection.cursor();
            query = 'SELECT * FROM Photo NATURAL JOIN Person WHERE photoPoster = username AND photoPoster = %s AND (allFollowers = 1 AND photoPoster IN (SELECT username_followed AS photoPoster FROM Follow WHERE username_followed = %s AND username_follower = %s AND followstatus = 1) OR photoID IN (SELECT photoID FROM Photo NATURAL JOIN SharedWith NATURAL JOIN BelongTo WHERE member_username = %s) AND photoPoster IN (SELECT username_followed FROM Follow WHERE username_follower = %s and followstatus = 1)) ORDER BY postingdate DESC'
            cursor.execute(query, (poster, poster, username, username, username))
            data = cursor.fetchall()
        cursor.close()
        return render_template('show_posts.html', poster_name=poster, posts=data, tagData=tagData, likeData=likeData)
    except:
        print("ERROR. USER NOT FOUND!")
        return redirect(url_for('home'))

#Show your own posts
@app.route("/images", methods=["GET"])
@login_required
def images():
    username = session["username"]
    query = "SELECT * FROM Photo WHERE photoPoster = %s"
    with connection.cursor() as cursor:
        try:
            cursor.execute(query, (username))

        except:
            error = "YOU DON'T HAVE ANY PHOTOS"
            return redirect(url_for('home'))
        data = cursor.fetchall()

        tagQuery = 'SELECT * FROM Tagged Natural Join Person WHERE tagstatus = 1'
        cursor.execute(tagQuery)
        tagData = cursor.fetchall()

        likeQuery = 'SELECT * FROM Likes Natural Join Person'
        cursor.execute(likeQuery)
        likeData = cursor.fetchall()

    return render_template("images.html", posts=data, tagData=tagData, likeData=likeData)

@app.route("/image/<image_name>", methods=["GET"])
def image(image_name):
    image_location = os.path.join(IMAGES_DIR, image_name)
    if os.path.isfile(image_location):
        return send_file(image_location, mimetype="image/jpg")

@app.route("/login", methods=["GET"])
def login():
    return render_template("login.html")

@app.route("/register", methods=["GET"])
def register():
    return render_template("register.html")

@app.route("/loginAuth", methods=["POST"])
def loginAuth():
    if request.form:
        requestData = request.form
        username = requestData["username"]
        plaintextPasword = requestData["password"]
        hashedPassword = hashlib.sha256(plaintextPasword.encode("utf-8")).hexdigest()

        with connection.cursor() as cursor:
            query = "SELECT * FROM person WHERE username = %s AND password = %s"
            cursor.execute(query, (username, hashedPassword))
        data = cursor.fetchone()
        if data:
            session["username"] = username
            return redirect(url_for("home"))

        error = "Incorrect username or password."
        return render_template("login.html", error=error)

    error = "An unknown error has occurred. Please try again."
    return render_template("login.html", error=error)

@app.route("/registerAuth", methods=["POST"])
def registerAuth():
    if request.form:
        requestData = request.form
        username = requestData["username"]
        plaintextPasword = requestData["password"]
        hashedPassword = hashlib.sha256(plaintextPasword.encode("utf-8")).hexdigest()
        firstName = requestData["firstName"]
        lastName = requestData["lastName"]

        try:
            with connection.cursor() as cursor:
                query = "INSERT INTO person (username, password, firstName, lastName) VALUES (%s, %s, %s, %s)"
                cursor.execute(query, (username, hashedPassword, firstName, lastName))
        except pymysql.err.IntegrityError:
            error = "%s is already taken." % (username)
            return render_template('register.html', error=error)

        return redirect(url_for("login"))

    error = "An error has occurred. Please try again."
    return render_template("register.html", error=error)

@app.route("/logout", methods=["GET"])
def logout():
    session.pop("username")
    return redirect("/")

@app.route("/uploadImage", methods=["POST"])
@login_required
def upload_image():
    username = session["username"]
    caption = request.form["caption"]
    groupName = request.form["groupName"]
    groupOwner = request.form["groupOwner"]

    cursor = connection.cursor();
    ownedGroupsQuery = 'SELECT DISTINCT groupName, groupOwner FROM Friendgroup WHERE groupName IN (SELECT groupName FROM BelongTo WHERE member_username = %s)'
    cursor.execute(ownedGroupsQuery, (username))
    ownedGroupsData = cursor.fetchall()
    cursor.close()

    if request.files:
        image_file = request.files.get("imageToUpload", "")
        image_name = image_file.filename
        filepath = os.path.join(IMAGES_DIR, image_name)
        image_file.save(filepath)
        query = 'INSERT INTO Photo (caption, filepath, photoPoster, postingdate, allFollowers) VALUES (%s, %s, %s, %s, %s)'
        with connection.cursor() as cursor:
            if (groupName == "allFollowers"):
                cursor.execute(query, (caption, image_name, username, time.strftime('%Y-%m-%d %H:%M:%S'), '1'))
            else:
                cursor.execute(query, (caption, image_name, username, time.strftime('%Y-%m-%d %H:%M:%S'), '0'))

                photoIDQuery = 'SELECT max(photoID) FROM Photo'
                cursor.execute(photoIDQuery)
                maxPhotoID = cursor.fetchall()
                maxPhotoID = maxPhotoID[0].get('max(photoID)')

                shareQuery = 'INSERT INTO SharedWith (groupName, groupOwner, photoID) VALUES(%s, %s, %s)'
                cursor.execute(shareQuery, (groupName, groupOwner, maxPhotoID))

        message = "Image has been successfully uploaded."
        return render_template("upload.html", ownedGroupsData=ownedGroupsData, message=message)
    else:
        message = "Failed to upload image."
        return render_template("upload.html", ownedGroupsData=ownedGroupsData, message=message)

#Manage Followers and Tags
@app.route('/manage')
@login_required
def manage():
    username = session['username']
    cursor = connection.cursor();
    query = 'SELECT * FROM Tagged NATURAL JOIN Photo WHERE tagstatus = 0 AND username = %s'
    cursor.execute(query, (username))
    data = cursor.fetchall()

    query2 = 'SELECT * FROM Follow WHERE followstatus = 0 AND username_followed = %s'
    cursor.execute(query2, (username))
    requestData = cursor.fetchall()

    cursor.close()
    return render_template('manage.html', tagData=data, requestData = requestData)

@app.route("/follow", methods=["GET", "POST"])
def follow():
    username = session['username']
    poster = request.args['poster']

    cursor = connection.cursor();
    if (username != poster):
        try:
            query = 'INSERT INTO Follow (username_follower, username_followed, followstatus) VALUES(%s, %s, %s)'
            cursor.execute(query, (username, poster, 0))
        except pymysql.err.IntegrityError:
            error = "COULDN'T FIND USER!"
            connection.commit()
            cursor.close()
            return redirect(url_for('home'))
    else:
        error = "YOU CAN'T FOLLOW YOURSELF!"
        connection.commit()
        cursor.close()
        return redirect(url_for('home'))

    connection.commit()
    cursor.close()
    return redirect(url_for('home'))

@app.route('/followStatus', methods = ["GET", "POST"])
@login_required
def followStatus():
    username = session['username']
    followerUsername = request.form['followerName']
    if (request.form["followButton"] == "accept"):
        print ("ACCEPTED")
        updateFollowQuery = 'UPDATE Follow SET followstatus = 1 WHERE username_followed = %s AND username_follower = %s'
        cursor = connection.cursor();
        cursor.execute(updateFollowQuery, (username, followerUsername))

    elif (request.form["followButton"] == "decline"):
        print ("DECLINED")
        updateFollowQuery = 'DELETE FROM Follow WHERE username_followed = %s AND username_follower = %s'
        cursor = connection.cursor();
        cursor.execute(updateFollowQuery, (username, followerUsername))
    else:
        print ("DIDN'T WORK")

    data = cursor.fetchall()

    query2 = 'SELECT * FROM Follow WHERE followstatus = 0 AND username_followed = %s'
    cursor.execute(query2, (username))
    requestData = cursor.fetchall()

    cursor.close()
    return render_template('manage.html', tagData=data, requestData = requestData)

@app.route('/createGroup', methods = ["GET", "POST"])
@login_required
def createGroup():
    username = session["username"]
    groupName = request.form['groupName']
    cursor = connection.cursor();
    try:
        query = 'INSERT INTO Friendgroup (groupOwner, groupName) VALUES(%s, %s)'
        cursor.execute(query, (username, groupName))

        belongQuery = 'INSERT INTO BelongTo (member_username, owner_username, groupName) VALUES(%s, %s, %s)'
        cursor.execute(belongQuery, (username, username, groupName))
    except:
        print("Error, you already own a group of that name!")
    connection.commit()
    cursor.close()
    return redirect(url_for('home'))

@app.route('/addMember', methods = ["GET", "POST"])
@login_required
def addMember():
    username = session["username"]
    groupName = request.form["groupName"]
    newMember = request.form["newMember"]
    cursor = connection.cursor();

    try:
        query = 'INSERT INTO BelongTo (member_username, owner_username, groupName) VALUES(%s, %s, %s)'
        cursor.execute(query, (newMember, username, groupName))
    except:
        print("Error, username either does not exist or already in the group!")

    connection.commit()
    cursor.close()
    return redirect(url_for('home'))

@app.route('/tag', methods = ["GET", "POST"])
@login_required
def tag():
    username = session['username']
    tagged_user = request.form['tagged_user']
    photoID = request.form['photoID']
    cursor = connection.cursor();

    followQuery = 'SELECT count(username_follower) as followed FROM Follow WHERE username_follower = %s AND username_followed = %s AND followstatus = 1'
    cursor.execute(followQuery, (tagged_user, username))
    data = cursor.fetchall()
    print(data[0])

    if(data[0]["followed"] == 1):
        print("Tagging")
        tagQuery = 'INSERT INTO Tagged (username, photoID, tagstatus) VALUES (%s, %s, %s)'
        if tagged_user == username:
            cursor.execute(tagQuery, (username, photoID, 1))
        else:
            try:
                cursor.execute(tagQuery, (tagged_user, photoID, 0))
            except pymysql.err.IntegrityError:
                print("Error, multiple instances of tagged tried")
    else:
        print(tagged_user, "is not following you so you can't tag them")

    connection.commit()
    cursor.close()
    return redirect(url_for('home'))

@app.route('/tagStatus', methods = ["GET", "POST"])
@login_required
def tagStatus():
    username = session["username"]
    photoID = request.form["photoID"]

    if(request.form["tagButton"] == "accept"):
        updateQuery = 'UPDATE Tagged SET tagstatus = 1 WHERE username = %s AND photoID = %s'
    elif (request.form["tagButton"] == "decline"):
        updateQuery = 'DELETE FROM Tagged WHERE username = %s AND photoID = %s'
    else:
        print("DIDN'T WORK")

    cursor = connection.cursor();
    cursor.execute(updateQuery, (username, photoID))
    data = cursor.fetchall()

    return redirect(url_for('manage'))

if __name__ == "__main__":
    if not os.path.isdir("images"):
        os.mkdir(IMAGES_DIR)
    app.run()
