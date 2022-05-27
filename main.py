from flask import Flask, render_template, request, session, redirect, url_for, flash
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from werkzeug.utils import secure_filename
from datetime import datetime
import json
import os
import shutil
from faceRecognition import *


# opening config.json file in reading mode
with open('config.json', 'r') as c:
    params = json.load(c)["params"]



# creating flask object
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/finding_missing_people'
db = SQLAlchemy(app)

# configuration of mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = ''
app.config['MAIL_PASSWORD'] = ''
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_SUPPRESS_SEND'] = False
app.config['TESTING'] = False
mail = Mail(app)

# setting session secret key
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

app.config['Missing_ImgFolder'] = params['missing_images']
app.config['Suspect_ImgFolder'] = params['suspect_images']
app.config['Found_ImgFolder'] = params['found_images']
allowed_extension = ['png', 'jpg', 'jpeg']


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extension



# for entries in missing table in our database
class Missing(db.Model):

    complaintID = db.Column(db.String(10), primary_key=True)

    # detail of missing person
    name = db.Column(db.String(30), unique=False, nullable=False)
    gender = db.Column(db.String(1), unique=False, nullable=False)
    age = db.Column(db.Integer, unique=False, nullable=False)

    # guardians detail
    guardian_name = db.Column(db.String(30), unique=False, nullable=False)
    guardian_contact = db.Column(db.Integer, unique=False, nullable=False)
    city = db.Column(db.String(20), unique=False, nullable=False)
    pincode = db.Column(db.String(6), unique=False, nullable=False)

    image_name = db.Column(db.String(20), unique=False, nullable=False)
    missing_date = db.Column(db.String(30), unique=False, nullable=True)


# for entries in found table of database
class Found(db.Model):
    complaintID = db.Column(db.String(10), primary_key=True)

    # detail of found person
    name = db.Column(db.String(30), unique=False, nullable=False)
    gender = db.Column(db.String(1), unique=False, nullable=False)

    # guardians detail
    guardian_name = db.Column(db.String(30), unique=False, nullable=False)
    guardian_contact = db.Column(db.Integer, unique=False, nullable=False)
    address = db.Column(db.String(40), unique=False, nullable=False)

    # helpers detail
    helper_name = db.Column(db.String(30), unique=False, nullable=False)
    helper_contact = db.Column(db.Integer, unique=False, nullable=False)
    found_location = db.Column(db.String(40), unique=False, nullable=False)

    missing_date = db.Column(db.String(30), unique=False, nullable=True)
    found_date = db.Column(db.String(30), unique=False, nullable=True)

    actual_image = db.Column(db.String(30), unique=False, nullable=False)
    suspect_image = db.Column(db.String(30), unique=False, nullable=False)




# If susect's image is mached with any missing people image, then:-
#
# 1. make a entry in found table of database
# 2. moving actual image from missing to found image folder
#    ( suspect image folder will remain as it is, but its name will be changed to cID_name)
# 3. Sending mail to admin
# 4. deleting the entry from missing table in database





# WebApp Home Page
@app.route('/', methods=['GET', 'POST'])
def home():

    if request.method == 'POST' and request.form['Submit_B'] == 'matchImg':
        # sName = request.form.get('name')
        location = request.form.get('loc')
        helperName = request.form.get('hName')
        helperContact = request.form.get('hPhone')
        found_date = request.form.get('fDate')

        # fetching image and saving in folder
        i = request.files['susImg']
        filename = secure_filename(i.filename)

        # checking for allowed image types
        if not allowed_file(filename):
            flash("Image type not allowed! (Only .png, .jpg and .jpeg types are allowed)", "error")
            return render_template('index.html')


        i.save(os.path.join(app.config['Suspect_ImgFolder'], filename))


        # ********************* Matching Suspects Image *********************


        # detetcing whether the img has a face or not
        locationOfImg = app.config['Suspect_ImgFolder'] + filename

        if detectFace(locationOfImg) == 0:
            os.remove(locationOfImg)

            flash("Face not detected in uploaded Image!", "error")
            return render_template('index.html')


        # fetching all the images from missing table in database
        missingPeopleNames = []

        missingList = Missing.query.all()
        for m in missingList:
            missingImg = m.complaintID + '_' + m.image_name
            missingPeopleNames.append(missingImg)


        # missing database is empty
        if not missingList:
            match = False
            result_mssg = "Match Not Found! Thankyou"

        else:
            # calling function from faceRecognition.py
            match = match_faces(filename, missingPeopleNames)

            if not match:

                # deleting the image of suspect from folder
                path = params['suspect_images']
                if os.path.exists(path + filename):
                    os.remove(path + filename)

                result_mssg = "Match Not Found! Thankyou"

            else:

                # 1........

                # match will return the image name  ( complaintID_name.ext )
                # separating compliant ID and name from match

                # c_id, name = match.split("_")
                c_id = match[: match.find('_') ]
                name = match[  match.find('_') +1 : ]
                foundPerson = Missing.query.get(c_id)

                # id helper didn't entered found date
                if not found_date:
                    found_date = datetime.now()


                # entering the details in found database

                try:
                    entry = Found(complaintID = c_id, name = foundPerson.name, gender = foundPerson.gender, guardian_name = foundPerson.guardian_name,
                                  guardian_contact = foundPerson.guardian_contact, address = foundPerson.city,helper_name = helperName,
                                  helper_contact = helperContact, found_location = location, missing_date = foundPerson.missing_date,
                                  found_date = found_date, actual_image= name, suspect_image= filename)
                    db.session.add(entry)
                    db.session.commit()

                except IntegrityError as err:
                    errorMsg = "Some error occurred, Image can't be matched"
                    print(err.orig.args[1])

                    os.remove(locationOfImg)

                    flash(errorMsg, "error")
                    return render_template('index.html')


                # 2.......
                src_folder = params['missing_images']
                destination = params['found_images']
                file_to_move = src_folder + c_id + '_' + foundPerson.image_name

                shutil.move(file_to_move, destination)


                # renaming the suspect image
                cwd = os.getcwd()

                os.chdir(params["suspect_images"])
                os.rename( filename, c_id + '_' + filename)
                os.chdir(cwd)


                # 3.......
                mailMsg = Message("A suspect is located for missing person",
                              sender="",
                              recipients=[ params["admin_mail"] ] )

                mailMsg.body = '''Hello Admin,
                    A Suspect is being located and his/her face is matched with a missing person.
                    Immediate action is required.
                    
                    Details of missing person case is:
                    
                    Case ID: %s
                    Name of missing person: %s
                    Gender: %s
                    Guardian's Name: %s
                    Guardian's Contact: %s
                    Actual Address: %s
                    Located location: %s
                    
                    Details of person who helped:
                    
                    Name: %s
                    Contact: %s
                    ''' % (c_id, foundPerson.name, foundPerson.gender, foundPerson.guardian_name,
                           foundPerson.guardian_contact, foundPerson.city, location, helperName, helperContact)

                mail.send(mailMsg)



                # 4.......
                personName = foundPerson.name
                image_of_suspect = c_id + '_' + filename
                matched_image = foundPerson.complaintID + '_' + foundPerson.image_name

                db.session.delete(foundPerson)
                db.session.commit()


                result_mssg = f'''Match Found with {personName}. Concerned authorities had been notified via mail.
                                  Thankyou for helping! We appreciate your vigilance.'''

                return render_template('index.html', match=match, match_msg=result_mssg,
                                       image_of_suspect = image_of_suspect, matched_image = matched_image, scroll="match-result")



        return render_template('index.html', match=match, match_msg = result_mssg, scroll="match-result")

    return render_template('index.html')



# Admin Login Page
@app.route('/admin_login', methods=['GET', 'POST'])
def adminLogin():

    if 'admin' in session and session['admin'] == params['admin_uname']:
        flash("Already Logged In!", "info")
        return redirect(url_for('adminProfile'))


    elif request.method == 'POST':
        username = request.form.get('uname')
        userPswd = request.form.get('pswd')

        if username == params['admin_uname'] and userPswd == params['admin_pswd']:
            # setting session
            session['admin'] = username
            return redirect(url_for("adminProfile"))

        else:
            flash("Username and Password did not matched", "error")
            return render_template('adminLogin.html')

    return render_template('adminLogin.html')




@app.route('/admin_dashboard')
def dashboard():
    return redirect(url_for('adminProfile'))


# Dashboard of Admin (Profile section)
@app.route('/admin_dashboard/profile')
def adminProfile():

    # proceed to dashboard only if admin is logged in
    if 'admin' in session and session['admin'] == params['admin_uname']:
        username = session['admin']
        email = params['admin_mail']
        return render_template('adminProfile.html', uname = username, email = email)

    # admin need to login before going to dashboard
    else:
        flash("Login first!", "error")
        return redirect(url_for('adminLogin'))




# Registering a new missing case
@app.route('/admin_dashboard/registerMissing')
def registerMissing():
    if 'admin' in session and session['admin'] == params['admin_uname']:
        return render_template('missingForm.html')

    else:
        flash("You need to login first!", "error")  # if someone tries the above URL directly
        return redirect(url_for('adminLogin'))


@app.route('/admin_dashboard/registerMissing', methods=['GET','POST'])
def missingForm():

    if request.method == 'POST':

        # Fetching details from form and storing in fieldValues list
        formFields = ['cID', 'name', 'gender', 'age', 'gName', 'gPhone', 'city', 'pincode', 'mDate' ]
        fieldValues = []

        for field in formFields:
            temp = request.form.get(field)
            fieldValues.append(temp)


        # fetching image and saving in folder
        i = request.files['mImg']
        filename = secure_filename(i.filename)
        filename = fieldValues[0] + '_' + filename

        if not allowed_file(filename):
            flash("Image type not allowed! (Only .png, .jpg and .jpeg types are allowed)", "error")
            return render_template('missingForm.html')


        i.save(os.path.join(app.config['Missing_ImgFolder'], filename))


        # Checking whether there is a face in uploaded image or not
        locationOfImg = app.config['Missing_ImgFolder'] + filename
        if detectFace(locationOfImg) == 1:

            # Adding entry into database
            date_of_missing = fieldValues[8]
            if not date_of_missing:
                fieldValues[8] = datetime.now()


            try:
                entry = Missing(complaintID = fieldValues[0], name = fieldValues[1], gender = fieldValues[2], age = fieldValues[3],
                            guardian_name = fieldValues[4], guardian_contact = fieldValues[5], city = fieldValues[6],
                            pincode = fieldValues[7], missing_date = fieldValues[8], image_name= secure_filename(i.filename))
                db.session.add(entry)
                db.session.commit()
                flash("Missing case registered successfully!", 'info')


            # if some relational error occurs
            except IntegrityError as err:
                errorMsg = "Error (case not registered): " + err.orig.args[1]
                flash(errorMsg, "error")

                os.remove(locationOfImg)


        elif detectFace(locationOfImg) == 0:
            # removing the saved image
            os.remove(locationOfImg)

            flash('Error (case not registered):  Face not detected in Uploaded Image! Try again', "error")


        else :
            # removing the saved image
            os.remove(locationOfImg)

            flash('Error (case not registered):  Multiple face detected in Uploaded Image!', "error")


    return render_template('missingForm.html')



# displaying all missing cases
@app.route('/admin_dashboard/missingCases')
def missingCases():

    if 'admin' in session and session['admin'] == params['admin_uname']:
        missing = Missing.query.all()
        return render_template('missingCases.html', missing= missing)

    else:
        flash("You need to login first!", "error")
        return redirect(url_for('adminLogin'))



# displaying all found cases
@app.route('/admin_dashboard/foundCases')
def foundCases():

    if 'admin' in session and session['admin'] == params['admin_uname']:
        found = Found.query.all()
        return render_template('foundCases.html', found=found)

    else:
        flash("You need to login first!", "error")
        return redirect(url_for('adminLogin'))



# Admin Logout
@app.route('/admin_dashboard/logout')
def logout():
    session.pop('admin', None)
    return redirect(url_for("home"))



if __name__ == '__main__':
    app.run(debug=True)