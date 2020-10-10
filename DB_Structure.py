from peewee import *
import datetime

db = MySQLDatabase('Courses', user='root',password='',host='localhost',port=3306)

class Courses(Model):
	subject   	= CharField()
	price     	= DecimalField()
	code	  	= CharField()  ####
	teacher   	= CharField()
	grade     	= CharField()
	Day1      	= CharField()
	Day2	 	= CharField(null=True)
	Day3     	= CharField(null=True)
	Day4	  	= CharField(null=True)
	Day5 	  	= CharField(null=True)
	Day6      	= CharField(null=True)
	Day7      	= CharField(null=True)
	description = TextField(null=True)
	class Meta:
		database = db

class Students(Model):
	name           = CharField()  
	grade          = CharField()
	code		   = CharField() ####
	Email 		   = CharField(null=True , unique=True)
	phone          = CharField(null=True , unique=True)
	parent_phone1  = CharField()
	parent_phone2  = CharField()
	parent_email   = CharField()
	national_id	   = BigIntegerField(null=True , unique=True)
	join_date	   = DateTimeField()
	class Meta:
		database = db

class Employees(Model):
	name        = CharField()
	age         = IntegerField()
	Email       = CharField(null=True , unique=True)
	phone       = CharField(unique=True)
	salary      = IntegerField(null=False)
	date        = DateTimeField(default=datetime.datetime.now)
	national_id = BigIntegerField(unique=True)
	password    = CharField()
	permission  = CharField()
	class Meta:
		database = db

CourseEvents = (

	(1,'pay'),
	(2,'Full pay'),
	(3,'book'),	

	)

class Daily_Events(Model):
	Course      = CharField()
	Client		= CharField()
	event_type  = CharField(choices=CourseEvents)
	datetime    = DateTimeField(default=datetime.datetime.now)
	employee    = ForeignKeyField(Employees, backref='employee')
	class Meta:
		database = db

actions = (

	(1,'Login'),
	(2,'Update'),
	(3,'Create'),	
	(4,'Delete'),
	(5,'Add'),
	)

tables = (

	(1,'Courses'),
	(2,'Students'),
	(3,'Employees'),	
	(4,'Subjects'),
	(5,'Teachers'),
	(6,'grades'),
	(5,'Daily_Events'),
	)


class History(Model):
	employee = ForeignKeyField(Employees, backref='employee')
	action   = CharField(choices=actions)
	table	 = CharField(choices=tables)
	date     = DateTimeField(default=datetime.datetime.now)
	class Meta:
		database = db

class Teachers(Model):
	name         = CharField()
	email        = CharField(null=True)
	phone        = CharField(unique=True) 
	join_date    = DateTimeField(null=True , default=datetime.datetime.now)
	national_id  = BigIntegerField(null=True , unique=True)
	subject      = CharField()
	code         = CharField()
	class Meta:
		database = db

class subjects(Model):
	subject_name = CharField(unique=True)
	class Meta:
		database = db

class grades(Model):
	grade_name = CharField(unique=True)
	class Meta:
		database = db


db.connect()
db.create_tables([Courses,Students,Employees,Daily_Events,History,Teachers,subjects,grades])
