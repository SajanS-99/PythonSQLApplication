    import re
import string
import random
import hashlib
import pyodbc
 
def main():



    username = input("Please enter your username: ")
    password = input("Please enter your password: ")

    try:
        conn = pyodbc.connect('driver={ODBC Driver 18 for SQL Server};server=#DNS_OF_SERVER;uid='+username+';pwd='+password+';Encrypt=yes;TrustServerCertificate=yes')
    except pyodbc.Error as ex:
        raise ex
    


    uInput = ""
    while uInput != 'E' and uInput != 'e':
        print("[1] Search Business")
        print("[2] Search Users")
        print("[3] Make Friend")
        print("[4] Write Review")
        print("[E] Exit Program")
        uInput = input("Press the corresponding number or letter for the functions above to access it: ")

        if uInput == '1':
            print("Now starting search business function")
            cityFilter = ""
            nameFilter = ""
            minFilter = ""
            maxFilter = ""
            
            filterInput = input("If you wish to filter by city, press [Y], else if you don't wish to filter by city, press any other key: ")

            if filterInput == 'Y' or filterInput == 'y':
                cityFilter = input("Please input requested city name: ")
                filterInput = ""
            
            filterInput = input("If you wish to filter by name, press [Y], else if you don't wish to filter by name, press any other key: ")

            if filterInput == 'Y' or filterInput == 'y':
                nameFilter = input("Please input requested business name: ")
                filterInput = ""        
                
            filterInput = input("If you wish to filter by maximum number of stars, press [Y], else if you don't wish to filter by maximum number of stars, press any other key: ")

            if filterInput == 'Y' or filterInput == 'y':
                while (True):
                    convertedMax = -1
                    maxFilter = input("Please input requested maximum number of stars: ")
                    try:
                        convertedMax = int(maxFilter)
                    except:
                        print("You did not input a number, please try again")
                    if convertedMax < 1 or convertedMax > 5:
                        print("Inputted maximum stars was out the range for stars. The allowed range is between 1 and 5 inclusive")
                    elif convertedMax >= 1 and convertedMax <= 5:
                        break
                filterInput = ""

            filterInput = input("If you wish to filter by minimum number of stars, press [Y], else if you don't wish to filter by minimum number of stars, press any other key: ")

            if filterInput == 'Y' or filterInput == 'y':
                while (True):
                    convertedMin = -1
                    minFilter = input("Please input requested minimum number of stars: ")
                    try:
                        convertedMin = int(minFilter)
                    except:
                        print("You did not input a number, please try again")
                    if convertedMin < 1 or convertedMin > 5:
                        print("Inputted maximum stars was out the range for stars. The allowed range is between 1 and 5 inclusive")
                    elif  convertedMin >= convertedMax:
                        print("Inputted minimum stars was larger or equal than maximum stars. Please choose a lower number of stars for your minimum")
                    elif convertedMin >= 1 and convertedMin <= 5 and convertedMin < convertedMax:
                        break
                filterInput = ""


            cityQuery = ""
            nameQuery = ""
            minQuery = ""
            maxQuery = ""
            
            if (cityFilter + nameFilter + minFilter + maxFilter) != "":
                if cityFilter != "":
                    cityQuery = " AND city = " + cityFilter
                if nameFilter != "":
                    nameQuery = " AND name LIKE %" + nameFilter + '%'
                if minFilter != "":
                    minQuery = " AND stars > " + minFilter
                if maxFilter != "":
                    maxQuery = " AND stars < " + maxFilter
                query = "SELECT business_id, name, address, city, stars FROM business WHERE" + cityQuery + nameQuery + maxQuery + minQuery
                query = re.sub('AND ', '',query,1)
            else:
                query = "SELECT business_id, name, address, city, stars FROM business"

            # printing all rows gotten for search business
            cur = conn.cursor()
            cur.execute(query)

            all = cur.fetchall()

            if len(all) == 0:
                print("No results found for query")
            else:
                for row in cur.fetchall():
                    print(row)

                
            print(query)
            uInput = ""

        elif uInput == '2':
            print("Now starting search users function")
            nameFilter = ""
            usefulFilter = ""
            funnyFilter = ""
            coolFilter = ""

            filterInput = input("If you wish to filter by name, press [Y], else if you don't wish to filter by name, press any other key: ")

            if filterInput == 'Y' or filterInput == 'y':
                nameFilter = input("Please input requested user name: ")
                filterInput = ""

            usefulFilter = input("If you wish to filter by whether a user is considered useful, press [Y], else if you don't wish to, press any other key: ") 
            funnyFilter = input("If you wish to filter by whether a user is considered funny, press [Y], else if you don't wish to, press any other key: ") 
            coolFilter = input("If you wish to filter by whether a user is considered cool, press [Y], else if you don't wish to, press any other key: ")

            nameQuery = ""
            coolQuery = ""
            funnyQuery = ""
            usefulQuery = ""
            if nameFilter != "" or (usefulFilter == 'Y' or usefulFilter == 'y') or (coolFilter == 'Y' or coolFilter == 'y') or (funnyFilter == 'Y' or funnyFilter == 'y'):
                if nameFilter != "":
                    nameQuery = " AND name LIKE %" + nameFilter + '%'
                if usefulFilter == 'Y' or usefulFilter == 'y':
                    usefulQuery = " AND useful > 0"
                if coolFilter == 'Y' or coolFilter == 'y':
                    coolQuery = " AND cool > 0"
                if funnyFilter == 'Y' or funnyFilter == 'y':
                    funnyQuery = " AND funny > 0"
                query = "SELECT user_id, name, useful, funny, cool FROM user_yelp WHERE" + nameQuery + usefulQuery + coolQuery + funnyQuery
                query = re.sub('AND ', '',query,1)
            else:
                query = "SELECT user_id, name, useful, funny, cool FROM user_yelp"

            print(query)
            cur = conn.cursor()
            cur.execute(query)

            all = cur.fetchall()

            # printing all rows gotten for search user
            if len(all) == 0:
                print("No results found for query")
            else:
                for row in cur.fetchall():
                    print(row)

            if len(all) != 0:
                friendFilter = input("If you wish to friend any user from the above list, press [Y], else if not press any other key: ")

                if friendFilter == 'Y' or friendFilter == 'y':
                    while True:

                        friendInput = input ("Please input a user id who you wish to make a friend: ")

                        if len(friendInput) == 22:
                            break
                        else:
                            print("You inputted an invalid user id. Please try again.")

                    userKey = hashlib.sha1(username.encode('utf-8')).hexdigest()
                    userKey = userKey[:22]

                    query = "INSERT INTO friendship VALUES (" + userKey + ',' + friendInput + ')'
                    print(query)

                    sqlState = ""
                    cur = conn.cursor()
                    # attempting to insert friendship
                    try:
                        cur.execute(query)
                        conn.commit()
                    except pyodbc.Error as ex:
                        sqlState = ex.args[0]

                    if sqlState == '23000':
                        print("Integrity constraint violation. Relationship already exists")
                    else:
                        print("Inserted your chosen friendship")

                    friendFilter = ""
                    
                while True:
                    friendFilter = input("Press [Y] if you wish to add another friend. Else press anything else to stop adding friends and return to the menu.")
                    if friendFilter == 'Y' or friendFilter == 'y':
                        while True:

                            friendInput = input ("Please input a user id who you wish to make a friend: ")

                            if len(friendInput) == 22:
                                break
                            else:
                                print("You inputted an invalid user id. Please try again.")

                        userKey = hashlib.sha1(username.encode('utf-8')).hexdigest()
                        userKey = userKey[:22]

                        query = "INSERT INTO friendship VALUES (" + userKey + ',' + friendInput + ')'
                        print(query)

                        sqlState = ""
                        cur = conn.cursor()
                        # attempting to insert friendship
                        try:
                            cur.execute(query)
                            conn.commit()
                        except pyodbc.Error as ex:
                            sqlState = ex.args[0]

                        if sqlState == '23000':
                            print("Integrity constraint violation. Relationship already exists")
                        else:
                            print("Inserted your chosen friendship")
                            
                        friendFilter = ""
                    else:
                        break

            
            uInput = ""

        elif uInput == '3':
            print("Now starting make friend function")

            while True:

                friendInput = input ("Please input another user id who you wish to make a friend: ")

                if len(friendInput) == 22:
                    break
                else:
                    print("You inputted an invalid user id. Please try again.")

            userKey = hashlib.sha1(username.encode('utf-8')).hexdigest()
            userKey = userKey[:22]

            query = "INSERT INTO friendship VALUES (" + userKey + ',' + friendInput + ')'

            print(query)
            sqlState = ""
            cur = conn.cursor()
            # attempting to insert friendship
            try:
               cur.execute(query)
               conn.commit()
            except pyodbc.Error as ex:
              sqlState = ex.args[0]
            if sqlState == '23000':
                print("Integrity constraint violation. Relationship already exists")
            else:
                print("Inserted your chosen friendship")

            uInput = ""

        elif uInput == '4':
            print("Now starting write review function")

            def randKey(size):  
                chars  = string.ascii_uppercase+string.ascii_lowercase+string.digits
                return ''.join(random.choice(chars) for i in range(size))
            reviewKey = randKey(22)

            userKey = hashlib.sha1(username.encode('utf-8')).hexdigest()
            userKey = userKey[:22]

            while True:
                busId = input("Please input the business id for the business you wish to write a review for: ")

                if (len(busId) == 22):
                    break
                elif (len(busId) != 22):
                    print("You inputted a business id that is too small or too large. Please input a new business id: ")

            while True:
                starInput = input("Please input a number of stars for your review, between the range of 1 and 5 inclusive: ")

                starNum = int(starInput)

                if (starNum >= 1 and starNum <= 5):
                    break
                else:
                    print("You inputted a number outside the range of numbers between 1 and 5. Please try again.")

            query = "insert into review (review_id, user_id, business_id, stars) values (" + reviewKey + ',' + userKey + ',' + busId + ',' + starInput + ')'
            print(query)

            sqlState = ""
            cur = conn.cursor()
            # attempting to insert into review
            try:
               cur.execute(query)
               conn.commit()
            except pyodbc.Error as ex:
                sqlState = ex.args[0]
            
            if len(sqlState) == 0:
                print("Inserted your chosen friendship")

            uInput = "" 

        elif uInput != 'e' and uInput != 'E':
            print("Not a valid input. Please try a new input")
            uInput = ""


    print("Exiting program. Goodbye")

main()

    