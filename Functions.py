from main import *

def joinSubreddit(subreddit_name):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT username FROM reddit2.active_users")
        curr_user = cursor.fetchone()[0]
        inpUsername = curr_user
        
        #Check if the subreddit that the user wants to join exists or not
        cursor.execute("SELECT name FROM reddit2.subreddits WHERE name=%s", (subreddit_name,))
        if(cursor.rowcount == 0):
            print("Subreddit does not exist")
            return False
        
        #Check if the user is already a member of the subreddit
        cursor.execute("SELECT roles FROM reddit2.joined WHERE username=%s AND subreddit=%s", (inpUsername, subreddit_name))
        if(cursor.rowcount != 0):
            print("You are already a member of this subreddit")    
            return False
        
        try:
            cursor.execute("INSERT INTO reddit2.joined VALUES(%s, %s, %s)", (inpUsername, subreddit_name, "Member"))    
            mysql.connection.commit()
        except Exception as rip:
            return False
            
    
        return True
    except Exception as rip:
        return False

def makePost(postid, username, title, text, img, subreddit_name):
    try:
        cursor = mysql.connection.cursor()
        cursed = mysql.connection.cursor()
        n = cursor.execute("SELECT count(postid) FROM reddit2.posted_in")
        n = n+1

        # Check if the user has joined the subreddit
        cursor.execute("SELECT username FROM reddit2.joined WHERE name=%s", (username,))
        if(cursor.rowcount == 0):
            print("You are not a part of a subreddit")
            return False

        try:
            cursor.execute("INSERT INTO reddit2.posts VALUES(%i, %s, %s)", (postid, subreddit_name, "Member"))    
            mysql.connection.commit()
        except Exception as rip:
            return False
        return True
    except Exception as rip:
        return False

def createSubreddit(subreddit_name, description):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT username FROM reddit2.active_users")
        curr_user = cursor.fetchone()[0]
        
        inpUsername = curr_user
        
        cursor.execute("SELECT name FROM reddit2.subreddits WHERE name=%s", (subreddit_name,))
        if(cursor.fetchone() != None):
            print("Subreddit with this name already exists")
            return False
        
        #Insert into the subreddit table
        cursor.execute("INSERT INTO reddit2.subreddits VALUES(%s, %s)", (subreddit_name, description))
        mysql.connection.commit()

        #Insertion into the Joined table, to show that the user has created the subreddit
        cursor.execute("INSERT INTO reddit2.joined VALUES(%s, %s, %s)", (inpUsername, subreddit_name, "Subreddit Owner"))
        mysql.connection.commit()
        
        return True    
    except Exception as a:
        return False
    
def leaveSubredditCase(subreddit_name):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT username FROM reddit2.active_users")
        curr_user = cursor.fetchone()[0]
        
        username = curr_user
        print("subreddit ka naam is ", subreddit_name)
        
        cursor.execute("SELECT name FROM reddit2.subreddits WHERE name= %s", (subreddit_name,))
        if(cursor.fetchone() == None):
            print("Subreddit does not exist")
            return False
        
        #Check if the user is the owner of the subreddit
        cursor.execute("SELECT roles FROM reddit2.joined WHERE username=%s AND subreddit=%s", (username, subreddit_name))
        
        if(cursor.rowcount == 0): #The user is not a member of the subreddit
            #If thr user is not a member of the subreddit, they're made to join the subreddit
            print("you're not a member of the subreddit :p")
            return False
        if(cursor.fetchone()[0] == "Subreddit Owner"):
            print("You are the owner of this subreddit, you cannot leave :>")
            return False
        #Remove from the joined table
        print("username is ", username, "and subreddit name is", subreddit_name)
        cursor.execute("DELETE FROM reddit2.joined WHERE username=%s AND subreddit=%s", (username, subreddit_name))
        mysql.connection.commit()
        return True
    except Exception as rip:
        return False

def makePost(PostId, username, titlePart, textPart, imagePart):
    cursor = mysql.connection.cursor()
    cursed = mysql.connection.cursor()
    success = 0

    try:
        cursed = cursor.execute("SELECT COUNT(PostId) FROM posted")
        success = cursor.execute("INSERT INTO reddit2.users VALUES(%s, %s, %s)", (username, 0, passwd))
        mysql.connection.commit()
    except Exception as it_is_what_it_is:
        print("excepion caught")
        pass
    
    if success == 1: #Successfully inserted
        print("Congratulations! Your account has been made")
        return True
    else:
        print("Error, the account already exists, please choose a different username")
        return False


def signup_case(username, passwd):
    cursor = mysql.connection.cursor()
    success = 0

    try:
        success = cursor.execute("INSERT INTO reddit2.users VALUES(%s, %s, %s)", (username, 0, passwd))
        mysql.connection.commit()
    except Exception as it_is_what_it_is:
        print("excepion caught")
        pass
    
    if success == 1: #Successfully inserted
        print("Congratulations! Your account has been made")
        return True
    else:
        print("Error, the account already exists, please choose a different username")
        return False
    
def login(input_user, input_password):
    try:
        cursor = mysql.connection.cursor()
        
        cursor.execute("SELECT username, password FROM reddit2.users WHERE username=%s AND password=%s", (input_user, input_password))
        
        if cursor.rowcount == 0:
            print("Incorrect username or password")
            return False
        else:
            cursor = mysql.connection.cursor()
            cursor.execute("UPDATE reddit2.active_users SET username = %s WHERE username = %s", (input_user, "guest"))
            mysql.connection.commit()
            
            return True
    except Exception as rip:
        return False

def viewSubreddit(subreddit_name):
    try:
        cursor = mysql.connection.cursor()

        cursor.execute("SELECT name FROM reddit2.subreddits WHERE name = %s", (subreddit_name))

        if cursor.rowcount == 0:
            return False
        else:
            return True
    except Exception as ded:
        return False
