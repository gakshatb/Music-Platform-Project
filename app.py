######################################     IMPORT LIBRARIES     ########################################
# Module Importing
from model import * 
from config import appconfig as appcfg
from config import dataconfig as database


import os
import json
import difflib
from flask import Flask, render_template, request,redirect, url_for, flash, session, jsonify, abort


# Use the Agg backend to avoid the main thread issue
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


###########################################     SETUP APP     ##########################################


curr_dir = os.path.abspath(os.path.dirname(__file__))


#Creating a Flask instance
app=Flask(__name__, template_folder="templates")
app.secret_key= appcfg.SECRET_KEY


#############################################     LOGIN-REGISTRATION-LOGOUT     ###########################################

# Landing Page
@app.route('/', methods=['GET'])
def index():
    action = request.args.get('section', None)
    user=None
    username = session.get('username', None)
    if username:
        con=sqlite3.connect(database.DATABASE)
        con.row_factory=sqlite3.Row
        cur=con.cursor()
        cur.execute("select * from user where username=?",(username,))
        user=cur.fetchone()
        con.close()
    if action=='about':
        return render_template('about.html', user=user)
    if action=='our-mission':
        return render_template('OurMission.html', user=user)
    if action=='email':
        return render_template('contact.html', user=user)
    if action=='support':
        return render_template('support.html', user=user)
    if action=='faq':
        return render_template('FAQ.html', user=user)
    return render_template('index.html', user=user)


# Login Functionality.
@app.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('username', None):
        return redirect('/')
    if request.method == 'POST':
        username = request.form['username'].strip().lower()
        password = request.form['password'].strip()
        con=sqlite3.connect(database.DATABASE)
        con.row_factory=sqlite3.Row
        cur=con.cursor()
        cur.execute("select * from user where username=? and password=?",(username, password))
        data=cur.fetchone()
        con.close()
        if data:
            session["username"] = data["username"]
            session["user_id"] = data["user_id"]
            flash('Login successful!', 'success')
            return redirect('/')
        else:
            flash('Invalid credentials. Please try again.', 'danger')
            return redirect('/login')
    if request.method == 'GET':
        return render_template('login.html')
    abort(404)


@app.route('/register',methods=['GET','POST'])
def register():
    if session.get('username', None):
        return redirect('/')
    if request.method=='POST':
        try:
            name = request.form['name'].strip()
            username = request.form['username'].strip().lower()
            email = request.form['email'].strip().lower()
            number = request.form['number'].strip().lower()
            password = request.form['password'].strip()
            con = sqlite3.connect(database.DATABASE)
            cur = con.cursor()
            cur.execute("select * from user where username=? or email=? or phone_number=?",(username,email,number))
            data=cur.fetchone()
            if data:  
                flash("Record already Exists") 
            else:  
                cur.execute("insert into user(username,name,email,phone_number,password) values(?,?,?,?,?)",(username,name,email,number,password))
                con.commit()
                con.close()
                flash("Record Added  Successfully") 
        except sqlite3.Error as e:
            flash("SQLite error: " + str(e))
        except Exception as e:
            flash("Error: " + str(e))
        finally:
            return redirect("/")            
    if request.method=='GET':
        return render_template('register.html')
    abort(404) 


# Logout Functionality.
@app.route('/logout')
def logout():
    session.clear()
    return redirect("/")


#############################################     PROFILE     ###########################################


@app.route('/user', methods=['GET'])
def user():
    action = request.args.get('action', None)
    user=None
    username = session.get('username', None)
    if username:
        con=sqlite3.connect(database.DATABASE)
        con.row_factory=sqlite3.Row
        cur=con.cursor()
        cur.execute("select * from user where username=?",(username,))
        user=cur.fetchone()
        con.close()
    if user:
        if action=='edit':
            pass
        if action=='view':
            pass
        if action=='change_avatar':
            pass
        return render_template('profile.html', user=user)
    abort(404)
    

#######################################     RUN THE APPLICATION     ####################################


# App Exection
if __name__== "__main__":
    app.run(debug=True, host='0.0.0.0')


"""
############################### Main Application ###################################
# Home Page
@app.route("/app/<nm>")
def test(nm):
    con=get_db_connection()
    cur=con.cursor()
    # genre
    cur.execute("select genre, count(*) from song group by genre")
    gen=cur.fetchall()

    # recommended songs
    cur.execute(
        '''SELECT DISTINCT s.title, genre, avg_rating.avg_rating 
        FROM song s JOIN rating r ON s.sid = r.sid
        JOIN (
            SELECT sid, AVG(rating) AS avg_rating
            FROM rating
            GROUP BY sid
            ) avg_rating ON s.sid = avg_rating.sid
        ORDER BY avg_rating.avg_rating DESC;''')
    recom_song=cur.fetchall()

    # Songs
    cur.execute("select title, genre from song")
    song_nm=cur.fetchall()

    # playlist
    cur.execute("select playlist_name from album where user=?", (nm,))
    playlist=cur.fetchall()
    con.close()

    if song_nm:  
        return render_template("apphome.html", name=nm, genre=gen, recommendation=recom_song, songs=song_nm, album=playlist) 
    else:
        flash("Something went wrong!") 



    
# Profile Page
@app.route("/app/<nm>_profile")
def profile(nm):
    con=get_db_connection()
    cur=con.cursor()
    cur.execute("select * from user where name=?", (nm,))
    data=cur.fetchone()
    cur.execute("select name from creator where name=?", (nm,))
    creator_check=cur.fetchone()
    con.close()
    if creator_check:
        return render_template("profile.html", name=nm, prof_dat=data, is_creator=True)
    else:
        return render_template("profile.html", name=nm, prof_dat=data, is_creator=False)




# Song Page
@app.route("/app/<track>", methods=["GET",'POST'])
def song(track):
    con=get_db_connection()
    cur=con.cursor()
    cur.execute("select * from song where title=?", (track,))
    data=cur.fetchone()
    
    # rating
    cur.execute("select rating from rating where user_name=? and sid=?", (session.get('name'),data[0]))
    rate = cur.fetchone()
    con.close()

    if data:  
        return render_template("applyrics.html",name=session.get('name'), play=data, rated=rate)
    else:
        flash("Something went wrong!")




# Add the rating to song
@app.route('/app/add_rating', methods=['POST'])
def add_rating():
    data = request.get_json()
    user_name = session.get('name')
    sid = data.get('sid')
    rating = data.get('rating')
    if not sid or not rating or not user_name:
        return jsonify({'error': 'Invalid data provided'}), 400   
    else:
        con = get_db_connection()
        cur = con.cursor()
        cur.execute("SELECT * FROM rating WHERE user_name=? AND sid=?", (user_name, sid))
        existing_rating = cur.fetchone()

        if existing_rating:
            # If the user has already rated, update the existing rating
            cur.execute("update rating set rating=? where user_name=? and sid=?", (rating, user_name, sid))
            con.commit()
            return jsonify({'message': 'Rating updated sucessfully for the Song.'})
        else:
            # If not, insert the new rating
            cur.execute("INSERT INTO rating (user_name, sid, rating) VALUES (?, ?, ?)", (user_name, sid, rating))
            con.commit()

        con.close()

    return jsonify({'message': 'Rating added successfully'})




# Search Feature
@app.route("/app/search", methods=["GET",'POST'])
def search():
    matches = {'Songs':[], 'Playlist':[]}
    if request.method == 'POST':
        query = request.form.get('search', default='').strip()
        con = get_db_connection()
        cur = con.cursor()

        # Fetch song names
        cur.execute("SELECT title FROM song")
        all_songs = [song[0].lower() for song in cur.fetchall()]
        # Fetch album names
        cur.execute("SELECT playlist_name FROM album")
        all_albums = [album[0].lower() for album in cur.fetchall()]
        con.close()

        # Perform close match comparison for both songs and albums
        song_matches = difflib.get_close_matches(query.lower(), all_songs, n=3)
        album_matches = difflib.get_close_matches(query.lower(), all_albums, n=3)

        # Extend the matches list with both song and album matches
        if song_matches:
            matches['Songs'].extend(song_matches)
        if album_matches:
            matches['Playlist'].extend(album_matches)
        
    return render_template('search.html', query=query, results=matches)      
    



# Create-Playlist
@app.route("/app/<nm>/createplaylist", methods=['GET', 'POST'])
def create_playlist(nm):
    con=get_db_connection()
    cur=con.cursor()
    cur.execute("select sid,title from song")
    all_songs=cur.fetchall()
    con.close()

    if request.method == 'POST':
        try:
            album_name=request.form['playlistname'].strip()
            song_id = request.form.getlist('checkbox')
            con=get_db_connection()
            cur=con.cursor()
            # album
            cur.execute("select * from album where playlist_name=?",(album_name,))
            data=cur.fetchone()
            # songs
            cur.execute("select sid,title from song")
            all_songs=cur.fetchall()
            
            if data:  
                flash("Album already Exist.") 
            else:   
                # Serialist song_id list for storage in database.  
                cur.execute("insert into album values(?,?,?)",(album_name,json.dumps(song_id),nm))
                con.commit()
                flash("Record Added  Successfully")
                return render_template("createplaylist.html", name=nm, all_songs_list=all_songs)

        except sqlite3.Error as e:
            flash("SQLite error: " + str(e))

        except Exception as e:
            flash("Error: " + str(e))
            
        finally:
            con.close()

    if all_songs:  
        return render_template("createplaylist.html", name=nm, all_songs_list=all_songs)
    else:
        flash("Something went wrong!")




# Edit-Playlist
@app.route('/app/<nm>/edit_<plist>',methods = ['POST','GET'])
def edit_playlist(nm, plist):
    con=get_db_connection()
    cur=con.cursor()
    cur.execute("select sid,title from song")
    all_songs=cur.fetchall()
    cur.execute("select sid from album where playlist_name=? and user=?",(plist,nm))
    pslist= cur.fetchone()
    con.close()

    if request.method == 'POST':
        try:
            album_name = request.form['playlistname'].strip()
            if not album_name:
                album_name=plist
            song_id = request.form.getlist('checkbox')
            con=get_db_connection()
            cur=con.cursor()
            # album
            cur.execute("select * from album where playlist_name=?",(plist,))
            data=cur.fetchone()          

            if data: 
                cur.execute("update album set playlist_name=?, sid=? where playlist_name=?",(album_name,json.dumps(song_id), plist))
                con.commit()
                flash("Record Updated Successfully")
                return redirect(url_for('edit_playlist', nm=nm,plist=album_name))

        except sqlite3.Error as e:
            # flash("SQLite error: " + str(e))
            pass
            
        except Exception as e:
            # flash("Error: " + str(e))
            pass
                 
        finally:
            con.close()

    if all_songs:  
        # Deserialize the JSON string back into a Python list
        return render_template("editplaylist.html", name=nm, plist_name=plist, all_songs_list=all_songs, plist_song=json.loads(pslist[0]))
    else:
        flash("Something went wrong!")
#######################################################################################




######################### Creator Application #########################################
# Creator Route(Dashboard or Register)
@app.route("/creator_<nm>", methods=['GET', 'POST'])
def creator_index(nm):
    con=get_db_connection()
    cur=con.cursor()
    cur.execute("select name from creator where name=?", (nm,))
    creator=cur.fetchone()
    con.close()

    if request.method=='POST':
        try:
            con=get_db_connection()
            cur=con.cursor()
            cur.execute("insert into creator(name) values(?)",(nm,))
            con.commit()
            return redirect(url_for('creator_dashboard', nm=nm))           
        finally:
            con.close()   

    if creator:
        return redirect(url_for('creator_dashboard', nm=nm))
    else:
        return render_template("creator_register.html", name=nm)




# Creator Dashboard
@app.route('/<nm>_creator_dashboard')
def creator_dashboard(nm):
    statistics=[]
    con=get_db_connection()
    cur=con.cursor()
    # Avg Rating
    cur.execute(
        '''SELECT round(avg(Distinct avg_rating.avg_rating),3) 
        FROM song s JOIN rating r ON s.sid = r.sid
        JOIN (
            SELECT sid, AVG(rating) AS avg_rating
            FROM rating
            GROUP BY sid
        ) avg_rating ON s.sid = avg_rating.sid
        where s.uploader=?
        ORDER BY avg_rating.avg_rating DESC
        ''', (nm,))
    statistics.append(cur.fetchone())
    # Total Songs
    cur.execute("select title from song where uploader=?", (nm,))
    statistics.append(cur.fetchall())
    # Total Song Count
    statistics.append(len(statistics[1]))
    # Total Albums
    cur.execute("select count(playlist_name) from album where user=?", (nm,))
    statistics.append(cur.fetchone())
    
    return render_template('creator_dashboard.html', name=nm, stats=statistics)




# Create Edit-Song
@app.route('/app/edit_<sng>',methods = ['POST','GET'])
def edit_song(sng):
    con=get_db_connection()
    cur=con.cursor()
    cur.execute("select * from song where title=?", (sng,))
    song_dat=cur.fetchone()
    con.close()
    if request.method=='POST':
        try:
            title=request.form['title'].strip()
            singer=request.form['singer'].strip()
            date=request.form['date'].strip()
            lyrics=request.form['lyrics'].strip()
            duration= request.form['duration'].strip()
            genre=request.form['genre'].strip()
            con=get_db_connection()
            cur=con.cursor()
            cur.execute("select * from song where title=?",(sng,))
            data=cur.fetchone()          

            if data: 
                cur.execute("update song set title=?, singer=?, date=?, lyrics=?, duration=?, genre=? where title=?",(title, singer, date, lyrics, duration, genre, sng))
                con.commit()
                flash("Record Updated Successfully")
                return redirect(url_for('edit_song', sng=title))

        except sqlite3.Error as e:
            # flash("SQLite error: " + str(e))
            pass
            
        except Exception as e:
            # flash("Error: " + str(e))
            pass
                 
        finally:
            con.close()

    return render_template('editsong.html', name=session.get('name'), song=song_dat)




# Creator Delete-Song
@app.route('/app/<nm>/delete_<snm>',methods=["POST"])
def delete_song(nm,snm):
    if request.method=='POST':
        con = get_db_connection()
        cur = con.cursor()
        cur.execute("DELETE FROM song WHERE title=?", (snm,))
        con.commit()
        con.close()
        return redirect(url_for('creator_dashboard', nm=nm))




# Creator Upload-Song
@app.route('/<nm>_upload_song', methods=['GET','POST'])
def upload_songs(nm):
    if request.method=='POST':
        try:
            id=request.form['id'].strip()
            title=request.form['title'].title().strip()
            singer=request.form['singer'].title().strip()
            date=request.form['date'].strip()
            lyrics=request.form['lyrics'].strip()
            duration= request.form['duration'].strip()
            genre=request.form['genre'].title().strip()
            # nm
            con= get_db_connection()
            cur=con.cursor()

            cur.execute("select * from song where sid=? or title=?",(id,title))
            data=cur.fetchone()
        
            if data:  
                flash("Record already Exists") 
            else:  
                cur.execute("insert into song values(?,?,?,?,?,?,?,?)",(id, title, singer, date, lyrics, duration, genre,nm))
                con.commit()
                flash("Record Added  Successfully")
        except:
            flash("Error in Insert Operation")        
        finally:
            con.close()
            return redirect(url_for('upload_songs', nm=nm))
    return render_template('creator_upload_songs.html', name=nm)
###########################################################################




########################## Admin Application ##############################
# Creating Dashboard-Chart
def create_chart(data):
    fig, ax = plt.subplots()
    ax.bar(range(len(data)), [d for d in data], alpha=0.7, color='skyblue', edgecolor='white')
    ax.set_xticks(range(len(data)))
    ax.set_xticklabels(['User', 'Creator', 'Songs', 'Album', 'Genre'], color='white')
    ax.set_ylabel('Count', color='white')
    ax.set_title('Admin Data Statistics',color='white')

    # Set y-axis tick labels color to white
    ax.tick_params(axis='y', colors='white')
    for spine in ax.spines.values():
        spine.set_edgecolor('white')

    # Save the chart with a transparent background
    plt.savefig('static/admin_chart.png', transparent=True)
    plt.close()


# Admin-login with dashboard
@app.route('/admin', methods=['GET','POST'])
def admin_login():
    if request.method == 'POST':
        # Hard-coded credentials for admin.
        admins = {'admin': 'pwd'}

        admin_username = request.form['admin-username']
        admin_password = request.form['admin-password']

        if admin_username in admins and admins[admin_username] == admin_password:
            session['name'] = admin_username
            con= get_db_connection()
            cur=con.cursor()
            adm_dta=[]
            # User
            cur.execute("select count(*) from user where not exists(select * from creator where creator.name = user.name);")
            adm_dta.append(cur.fetchone())
            # Creator
            cur.execute("select count(*) from creator")
            adm_dta.append(cur.fetchone())
            # Songs
            cur.execute("select count(*) from song")
            adm_dta.append(cur.fetchone())
            # Album
            cur.execute("select count(*) from album")
            adm_dta.append(cur.fetchone())
            # Genre
            cur.execute("select count(distinct genre) from song")
            adm_dta.append(cur.fetchone())
            con.close()

            # Generate and save the bar chart.
            chart_data = [item[0] for item in adm_dta]
            # Set up matplotlib to use Agg backend and ion mode to prevent matplotlib mulithreading issue.
            matplotlib.use('Agg')
            plt.ion()

            create_chart(chart_data)

            # Turn off ion mode after saving the chart.
            plt.ioff()

            return render_template('admin.html', nm=admin_username, admin_data=adm_dta)
        else:
            flash("Authentication Failed! Contact Admistrator.")          
    
    return render_template('admin_login.html')




# Admin Track
@app.route('/admin_tracks', methods=['GET'])
def admin_tracks():
    con= get_db_connection()
    cur=con.cursor()
    # genre
    cur.execute("select genre, count(*) from song group by genre")
    gen=cur.fetchall()
    # songs
    cur.execute("select title, genre from song")
    song_nm=cur.fetchall()
    con.close()

    return render_template('admin_tracks.html', genre=gen, songs=song_nm, nm=session.get('name'))




# Delete Admin-Tracks
@app.route('/delete_track?<sng>',methods=["POST"])
def delete_track(sng):
    if request.method=='POST':
        con = get_db_connection()
        cur = con.cursor()
        cur.execute("DELETE FROM song WHERE title=?", (sng,))
        con.commit()
        con.close()
        return redirect(url_for('admin_tracks'))




# Admin_albums
@app.route('/admin_albums', methods=['GET'])
def admin_albums():
    con=get_db_connection()
    cur=con.cursor()
    cur.execute("select playlist_name from album")
    abm_nm=cur.fetchall()
    con.close()
    return render_template('admin_albums.html', album_name=abm_nm, nm=session.get('name'))




# Delete Album
@app.route('/delete_album?<abm>',methods=["POST"])
def delete_album(abm):
    if request.method=='POST':
        con = get_db_connection()
        cur = con.cursor()
        cur.execute("DELETE FROM album WHERE playlist_name=?", (abm,))
        con.commit()
        con.close()
        return redirect(url_for('admin_albums'))
###########################################################################    

"""