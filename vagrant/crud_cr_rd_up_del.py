from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base,Restaurant,MenuItem,MenuCourses

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

#mycourse=MenuCourses(name='Appetizer')
#session.add(mycourse)
#session.commit()

#mycourse=MenuCourses(name='Entree')
#session.add(mycourse)
#session.commit()

mycourse=MenuCourses(name='Dessert')
session.add(mycourse)
session.commit()

#mycourse=MenuCourses(name='Main Course')
#session.add(mycourse)
#session.commit()


#myFirstRestaurant = Restaurant(name='Pizza Palace')
#session.add(myFirstRestaurant)
#session.commit()

#first = session.query(Restaurant).first()
#print(first.name)

#cheesepizza = MenuItem(name='Cheese Pizza',description='Made with cheese',course='Entree',price='$15',restaurant=myFirstRestaurant)
#session.add(cheesepizza)
#session.commit()

#To crud read

#menu_list = session.query(MenuItem).all()
#for menu in menu_list:
#	print menu.name


#To crud update

menu_lists = session.query(MenuCourses).filter_by(name='Beverages').one()

#print menu_lists.id

menu_lists.name = 'Beverage'
session.add(menu_lists)
session.commit()

#print menu_lists.price

#for list in menu_lists: IF WE DID NOT USE ONE() IN THE ABOVE STATEMENT
#	print(list.id)
#	print(list.name)
#	print(list.restaurant.name)


# CRUD DELETE

#del_lists = session.query(MenuItem).filter_by(name='Pho').one()
#print del_lists.name

#del_lists = session.query(Restaurant).filter_by(name='test5')

#session.delete(del_lists)
#session.commit()



