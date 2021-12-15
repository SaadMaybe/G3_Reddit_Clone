import random
import mysql
from mysql.connector import Error
import hashlib

#Subreddit information
with open("D:/CS/LUMS/CS 340/Project/Data/Dataset_Subreddit_Name.txt", "r") as f:
    subreddit_names = f.read().splitlines()
    
with open("D:/CS/LUMS/CS 340/Project/Data/Dataset_Subreddit_Description.txt", "r") as f:
    subreddit_descriptions = f.read().splitlines()

#User information    
with open("D:/CS/LUMS/CS 340/Project/Data/Dataset_Usernames.txt", "r") as f:
    usernames = f.read().splitlines()

with open("D:/CS/LUMS/CS 340/Project/Data/Dataset_Password.txt", "r") as f:
    passwords = f.read().splitlines()

#Flair information
with open("D:/CS/LUMS/CS 340/Project/Data/Dataset_Flairs.txt", "r") as f:
    flair_names = f.read().splitlines()

#Award information
with open("D:/CS/LUMS/CS 340/Project/Data/awards.txt", "r") as f:
    award_names = f.read().splitlines()

with open("D:/CS/LUMS/CS 340/Project/Data/awards_description.txt", "r") as f:
    award_descriptions = f.read().splitlines()
    
with open("D:/CS/LUMS/CS 340/Project/Data/awards_price.txt", "r") as f:
    award_prices = f.read().splitlines()
    
#Badges information
with open("D:/CS/LUMS/CS 340/Project/Data/Dataset_Badges.txt", "r") as f:
    badge_names = f.read().splitlines()
    
with open("D:/CS/LUMS/CS 340/Project/Data/Dataset_Badges_Description.txt", "r") as f:
    badge_descriptions = f.read().splitlines()

#Post information
with open("D:/CS/LUMS/CS 340/Project/Data/Dataset_Post_Title.txt", "r") as f:
    post_titles = f.read().splitlines()

with open("D:/CS/LUMS/CS 340/Project/Data/Dataset_Post_ID.txt", "r") as f:
    post_IDs = f.read().splitlines()
    
with open("D:/CS/LUMS/CS 340/Project/Data/Dataset_Post_Username.txt", "r") as f:
    post_usernames = f.read().splitlines()

with open("D:/CS/LUMS/CS 340/Project/Data/Dataset_Post_Downvotes.txt", "r") as f:
    post_downvotes = f.read().splitlines()
    
with open("D:/CS/LUMS/CS 340/Project/Data/Dataset_Post_Upvotes.txt", "r") as f:
    post_upvotes = f.read().splitlines()
    
        
#Comment information
with open("D:/CS/LUMS/CS 340/Project/Data/Dataset_Comment_ID.txt", "r") as f:
    comment_IDs = f.read().splitlines()
with open("D:/CS/LUMS/CS 340/Project/Data/Dataset_Comment_Username.txt", "r") as f:
    comment_usernames = f.read().splitlines()
with open("D:/CS/LUMS/CS 340/Project/Data/Dataset_Comment_Downvotes.txt", "r") as f:
    comment_downvotes = f.read().splitlines()
with open("D:/CS/LUMS/CS 340/Project/Data/Dataset_Comment_Upvotes.txt", "r") as f:
    comment_upvotes = f.read().splitlines()
with open("D:/CS/LUMS/CS 340/Project/Data/Dataset_Comment_parentID.txt", "r") as f:
    comment_parentIDs = f.read().splitlines()
    
    
try :
    
    connection = mysql.connector.connect(host='localhost',
                                            database='reddit2',
                                            user='root',
                                            password='<]^7f[R2<n')
    if connection.is_connected():
        db_Info = connection.get_server_info()
        print("Connected to MySQL Server version ", db_Info)
        
        cursor = connection.cursor()
        cursor.execute("select database();")
        record = cursor.fetchone()
        print("You're connected to database: ", record)
        
        '''
        print("Inserting into subreddit table")
        for a, b in zip(subreddit_names, subreddit_descriptions):
            cursor.execute("INSERT INTO reddit2.subreddits (name, description) VALUES (%s, %s)", (a, b))
        connection.commit()
        print("Inserted into subreddit table")
        
        print("Inserting into user table")
        for a, b in zip(usernames, passwords):
            cursor.execute("INSERT INTO reddit2.users (username, karma, password) VALUES (%s, %s,  %s)", (a, 0, b))
        connection.commit()
        print("Inserted into user table")
    
    #Convention: for every subreddit, we're making 5 flairs
        print("Inserting into flair table")
        for b in subreddit_names:
            for a in flair_names:
                cursor.execute("INSERT INTO reddit2.flairs (name, subreddit) VALUES (%s, %s)", (a, b))
                connection.commit()
            
        #Convention: for every subreddit, we're making 3 badges
        print("inserting into badge table")
        for c in subreddit_names:
            for a, b in zip(badge_names, badge_descriptions):
                cursor.execute("INSERT INTO reddit2.badges (name, subreddit, description) VALUES (%s, %s, %s)", (a, c, b))
                connection.commit()
        
        #Assuming that the default value for an image is NULL. Might need to check
        print("Inserting into post table")
        for a, b, c, d, e in zip(post_IDs, post_usernames, post_titles, post_upvotes, post_downvotes):
            cursor.execute("INSERT INTO reddit2.posts (postID, username, title, text, image, upvotes, downvotes) VALUES (%s, %s, %s, %s, %s, %s, %s)", (a, b, "lorem ipsum", "NULL", c, d, e))
            connection.commit()
            
        #Every user in every subreddit is given a random badge
        print("Inserting into badge_given table")
        for b in subreddit_names:
            cursor.execute("INSERT INTO reddit2.badge_given (username, badge_name, subreddit) VALUES (%s, %s, %s)", (random.choice(usernames), random.choice(badge_names), b))
            connection.commit()
        
        #Every post is assigned a random subreddit where it is inserted
        print("Inserting into posted_in table")
        for a in post_IDs:
            cursor.execute("INSERT INTO reddit2.posted_in (postid, subreddit) VALUES (%s, %s)", (a, random.choice(subreddit_names)))
            connection.commit()
        
        #Every post is assigned a random post-er
        print("Inserting into posted_by table")
        for a in post_IDs:
            cursor.execute("INSERT INTO reddit2.posted_by (username, postid) VALUES (%s, %s)", (random.choice(usernames), a))
            connection.commit()  
        
        
        print("Inserting into comment table")
        for a, b, c, d in zip(comment_IDs, comment_upvotes, comment_downvotes, comment_usernames):
            cursor.execute("INSERT INTO reddit2.comments (commentid, text, parentid, upvotes, downvotes, username) VALUES (%s, %s, %s, %s, %s, %s)", (a, "lol your opinion doesn't matter on the internet", None, b, c, d))
            connection.commit() 
        

        print("Inserting into award table")
        for a, b, c in zip(award_names, award_descriptions, award_prices):
            cursor.execute("INSERT INTO reddit2.awards (name, description, price) VALUES (%s, %s, %s)", (a, b, c))
            connection.commit()

        print('Inserting into awarded_to')
        list_post_ids = []
        for a in range (0,100):
            b = random.choice(post_IDs[0:1000])
            c = random.choice(award_names)
            x = (b,c)
            if x not in list_post_ids:
                cursor.execute("INSERT INTO reddit2.awarded_to (postid , name) VALUES (%s, %s)", (b, c))
                connection.commit()
                list_post_ids.append(x)
           
        print('Inserting into commented')
        list_commented = []
        for a in comment_IDs[0:1000]:
            b = random.choice(usernames)
            c = random.choice(post_IDs[0:1000])
            d = random.choice(subreddit_names)

            x = (b,c,d)

            if x not in list_commented:
                cursor.execute("INSERT INTO reddit2.commented (username , commentid , postid , subreddit ) VALUES (%s, %s , %s, %s)", (b, a, c, d))
                connection.commit()
                list_commented.append(x)

        
        print('inserting into joined')
        t = []
        for a in range (0,5000):
            b = random.choice(usernames)
            c = random.choice(subreddit_names)
            x = (b,c)
            if x not in t:
                print(x)
                cursor.execute("INSERT INTO reddit2.joined (username  , subreddit ,  roles ) VALUES (%s, %s , %s)", (b, c, "user" ))
                connection.commit()
                t.append(x)
          

        print('Inserting Awarded_to_comment')
        list_comment_ids = []
        for a in range(0,100):
            b = random.choice(comment_IDs[0:1000])
            c = random.choice(award_names)
            x = (b,c)
            if x not in list_comment_ids:
                print(x)
                cursor.execute("INSERT INTO reddit2.awarded_to_comment (commentid, name) VALUES (%s, %s)", (b, c))
                connection.commit()
                list_comment_ids.append(x)
        '''  
        print('Inserting into flair_added')
        list_post_ids = []
        list_x = []
        for a in range(0,100):
            b = random.choice(flair_names)
            c = random.choice(subreddit_names)
            d = random.choice(post_IDs[0:1000])
            x = (b,c)
            if d not in list_post_ids:
                if x not in list_x:
                    cursor.execute("INSERT INTO reddit2.flair_added (name, subreddit, postid) VALUES (%s, %s, %s)", (b, c, d))
                    connection.commit()   
                    list_x.append(x)
                list_post_ids.append(d)

    
#add the remaining items in list 
except Error as e:
    print("Error while connecting to MYSQL" , e)
finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("MYSQL connection is closed")