from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime
from rhythmrevive import app
from sqlconnect import conn,cursor
import os
import json
import checkBan

@app.route('/editProfile', methods=['GET', 'POST'])
def editProfile():
    if 'loginUsername' in session:
        userDbData = getUserData(session['loginUsername'])
        fetchId = userDbData[0]
        fetchPfp = userDbData[7]
        fetchUsername = userDbData[1]
        fetchDisplayName = userDbData[3]
        fetchBio = userDbData[6]
        fetchDOB = userDbData[5]
        fetchEmail = userDbData[4]
        fetchCreation = userDbData[10]
        banStatus = checkBan.checkBan(fetchUsername)
        if banStatus:
            return redirect(url_for('banned'))
        userBadgesNames = json.loads(userDbData[8])[0]
        equipBadge = getEquippedBadge(userBadgesNames)
        print(equipBadge[1])
        print(userBadgesNames)
        userBadges = getUserBadges(userBadgesNames)
        
        
        # print(userBadges)
        creationInWords = convertUserCreationToWords(fetchCreation)
        fetchBioPlaceholder = ''
        # print(fetchBio)
        fetchCreation = str(fetchCreation).split(' ')[0]
        if fetchBio == None:
            fetchBio = ''
            fetchBioPlaceholder = 'Please take a moment to introduce yourself by setting up your bio. This helps others get to know you better.'
        if fetchDOB == None:
            fetchDOB = '00-00-0000'


        if request.method == 'POST':
            editPfp = request.files.get('editPfp')
            editUsername = request.form['editUsername']
            editDisplayName = request.form['editDisplayName']
            editBio = request.form['editDisplayBio']
            editDOB = request.form['editDOB']
            dbPfpPath = fetchPfp
            editBadge = request.form['editBadge']

            # Username Error
            if editUsername != fetchUsername:
                if doUsernameExist(editUsername):
                    formError = 'Username Already Exists'
                    return render_template('editProfile.html',fetchPfp=fetchPfp,fetchUsername=fetchUsername,fetchDisplayName=fetchDisplayName,fetchBio=fetchBio,fetchBioPlaceholder=fetchBioPlaceholder,fetchDOB=fetchDOB,fetchEmail=fetchEmail,fetchCreation=fetchCreation,creationInWords=creationInWords,formError=formError,userBadges=userBadges,equipBadge=equipBadge)

            # PFP Updation
            if editPfp:
                allowed_extensions = set(['.jpg', '.jpeg', '.png'])
                filename = editPfp.filename
                if not (filename.lower().endswith(extension) for extension in allowed_extensions):
                    formError = 'Only the following file extensions are allowed: ' + ', '.join(allowed_extensions)
                    return render_template('editProfile.html',fetchPfp=fetchPfp,fetchUsername=fetchUsername,fetchDisplayName=fetchDisplayName,fetchBio=fetchBio,fetchBioPlaceholder=fetchBioPlaceholder,fetchDOB=fetchDOB,fetchEmail=fetchEmail,fetchCreation=fetchCreation,creationInWords=creationInWords,formError=formError,userBadges=userBadges,equipBadge=equipBadge)
                unique_filename = str(fetchId) + '_' + editUsername+ '.' + filename.split('.')[-1]


                storage_folder = './static/storage/pfps'
                media_path = os.path.join(storage_folder, unique_filename)
                dbPfpPath = '.' + media_path
                try:
                    editPfp.save(media_path)

                except Exception as e:
                    print('Error saving file: ' + str(e))
                    formError = 'File Upload Failed! Try Again.'
                    return render_template('editProfile.html',fetchPfp=fetchPfp,fetchUsername=fetchUsername,fetchDisplayName=fetchDisplayName,fetchBio=fetchBio,fetchBioPlaceholder=fetchBioPlaceholder,fetchDOB=fetchDOB,fetchEmail=fetchEmail,fetchCreation=fetchCreation,creationInWords=creationInWords,formError=formError,userBadges=userBadges,equipBadge=equipBadge)
                
            # Badges Update
            userBadgesNames[equipBadge[1]] = 'notequipped'
            userBadgesNames[editBadge] = 'equipped'
            print(str(userBadgesNames)+'asd')


            # Update Result
            tempBadgeList = list()
            tempBadgeList.append(userBadgesNames)
            updateResult = updateUserProfile(editUsername,editDisplayName,editDOB,editBio,dbPfpPath,fetchId,tempBadgeList)
            if updateResult:
                formError = 'Profile Updated Successfully!!'
            else:
                formError = 'Profile Update Error! Please Try Again.'
            session['loginUsername'] = editUsername
            # print(session['loginUsername'])
            userDbData = getUserData(session['loginUsername'])
            fetchId = userDbData[0]
            fetchPfp = userDbData[7]
            fetchUsername = userDbData[1]
            fetchDisplayName = userDbData[3]
            fetchBio = userDbData[6]
            fetchDOB = userDbData[5]
            fetchEmail = userDbData[4]
            fetchCreation = userDbData[10]
            userBadgesNames = json.loads(userDbData[8])[0]
            equipBadge = getEquippedBadge(userBadgesNames)
            if fetchBio == None:
                fetchBio = ''
            creationInWords = convertUserCreationToWords(fetchCreation)
            return render_template('editProfile.html',fetchPfp=fetchPfp,fetchUsername=fetchUsername,fetchDisplayName=fetchDisplayName,fetchBio=fetchBio,fetchBioPlaceholder=fetchBioPlaceholder,fetchDOB=fetchDOB,fetchEmail=fetchEmail,fetchCreation=fetchCreation,creationInWords=creationInWords,formError=formError,userBadges=userBadges,equipBadge=equipBadge)
            
    else:
        return redirect(url_for('login'))
    
    return render_template('editProfile.html',fetchPfp=fetchPfp,fetchUsername=fetchUsername,fetchDisplayName=fetchDisplayName,fetchBio=fetchBio,fetchBioPlaceholder=fetchBioPlaceholder,fetchDOB=fetchDOB,fetchEmail=fetchEmail,fetchCreation=fetchCreation,creationInWords=creationInWords,userBadges=userBadges,equipBadge=equipBadge)



def getUserData(username):
    cursor.execute("SELECT * FROM users WHERE user_name = %s", (username,))
    result = cursor.fetchone()
    # print(result)
    return result

def convertUserCreationToWords(userCreation):
    current_time = datetime.now()
    time_difference = current_time - userCreation
    days_difference = time_difference.days
    if days_difference == 0:
        formatted_time = 'today'
    elif days_difference == 1:
        formatted_time = '1 day ago'
    else:
        formatted_time = f'{days_difference} days ago'
    return formatted_time

def doUsernameExist(username):
    cursor.execute("SELECT * FROM users WHERE user_name = %s", (username,))
    result = cursor.fetchone()    
    if result:
        return True
    else:
        return False
    
def updateUserProfile(editUsername,editDisplayName,editDOB,editBio,dbPfpPath,fetchId,userBadgesNames):    
    try:
            cursor.execute("UPDATE users SET user_name=%s, display_name=%s, user_dob=%s, user_bio=%s, user_pfp=%s,user_badges=%s WHERE user_id=%s",
                        (editUsername, editDisplayName, editDOB, editBio or None, dbPfpPath,json.dumps(userBadgesNames),fetchId,))
            conn.commit()
            return True
    except Exception as e:
            print("Error updating user profile:", e)
            return False
    
def getUserBadges(dictionary):
    userBadges = []
    for key, value in dictionary.items():
        cursor.execute("SELECT * FROM badges WHERE badge_name = %s", (key,))
        badge_data = cursor.fetchone()
        if badge_data:
            badge_dict = {
                "badge_id": badge_data[0],
                "badge_name": badge_data[1],
                "badge_url": badge_data[2],
                "badge_description": badge_data[3]
            }
            userBadges.append(badge_dict)
    return userBadges

def getEquippedBadge(dictionary):
    search_value = 'equipped'
    for key, value in dictionary.items():
        if value == search_value:
            equipped = key
    cursor.execute("SELECT * FROM badges WHERE badge_name = %s", (equipped,))
    result = cursor.fetchone()
    return result