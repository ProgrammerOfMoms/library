import pymysql.cursors
import calendar

#function of connection to database
def connect(user, password, host, db):
    cnx = pymysql.connect(
        user=user,
		password = password,
        host = host,
        db = db
    )
    return cnx

connection = connect("root", "Pasbot20!8","localhost","LIBRARY") #connect to db


#function of executing sql-requests
def executeRequest(sql):
    with connection.cursor() as cursor:
        try:
            countOfResponses = cursor.execute(sql)
        except:
            return -1
        if countOfResponses!=0:
            return list(cursor.fetchall())
        else:
            return 0

class Student:
    def __init__(self, id):
        self.id = id
        sql = "SELECT name FROM Students WHERE id = "+str(id)
        self.name = executeRequest(sql)[0][0]
    points = 0

#function of getting avg time of reading one book by month one student
def getAvgTime(books):
    time = 0
    for book in books:
        startDay = book[0][8:len(book[1])]#it's day when student took the book
        endDay = book[1][8:len(book[1])]#it's day when student returned the book
        time += int(endDay) - int(startDay)
    return time/len(books)

#it returns key for sort by points
def keyForPoints(student):
    return student.points


#function of searching student in list of students
def isExist(id, students):
    for student in students:
        if id == student.id:
            return student
    return -1

def angryReader(year):
    students = []
    winners = []
    sql = "SELECT id FROM Students"
    idOfStudents = executeRequest(sql) #getting list of id students
    for id in idOfStudents:
        student = Student(id[0]) #creating new student
        for month in range(1,12): #for each month in year
            #generating sql request for getting list of books which student read in month
            if month<10:
                startDate = str(year)+"-0"+str(month)+"-01"
                endDate = str(year)+"-0"+str(month)+"-"+str(calendar.monthrange(year,month)[1])
                sql = "SELECT issued, returned FROM St_B WHERE issued BETWEEN '"+startDate+"' AND '"+endDate+"' AND returned <= '"+endDate+"' AND id_st = "+str(id)
            else:
                startDate = str(year)+"-"+str(month)+"-01"
                endDate = str(year)+"-"+str(month)+"-"+str(calendar.monthrange(year,month)[1])
                sql = "SELECT issued, returned FROM St_B WHERE issued BETWEEN '"+startDate+"' AND '"+endDate+"' AND returned <= '"+endDate+"' AND id_st = "+str(id)
            books = executeRequest(sql) #getting books
            print(books)
            if books!=0 and books!=-1: #if student read one book in month at least
                countOfBooks = len(books)
                print("AAAAA",countOfBooks)
                student.points += countOfBooks*3 #for each read book student get 3 points
            
                #if student read more than 5 books in month he get 5 extra points
                if countOfBooks>5:
                    student.points+=5
            
                #getting avg time of reading one book in month
                avgTime = getAvgTime(books)
                #the less avg time the more points which student will get 
                student.points+=1/(avgTime/calendar.monthrange(year,month)[1])
        
        students.append(student)#adding student in list of students
    students.sort(key = keyForPoints, reverse = True)#sorting list by points

    maxPoints = students[0].points
    if maxPoints == 0:
        return []
    #defining winners
    for student in students:
        if student.points == maxPoints:
            winners.append(student)
        else:
            break #if points of student are not equal max points we can to out from loop because list of students is sorted by points
    return winners

def main():
    winners = angryReader(2017)
    if winners !=[]:
        for winner in winners:
            print(winner.id, " ", winner.name, " ", winner.points)
    else:
         print ("No winners")

if __name__=="__main__":
    main()
