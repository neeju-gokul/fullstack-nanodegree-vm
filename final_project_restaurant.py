from flask import Flask,render_template,request,redirect,url_for,jsonify,flash
from database_setup import Base,Restaurant,MenuItem,MenuCourses
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine=create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind=engine


app=Flask(__name__)

@app.route('/')
@app.route('/restaurants/')
def showRestaurants():
	DBsession=sessionmaker(bind=engine)
	session=DBsession()
	all_restaurants=session.query(Restaurant).all()
	return render_template('showRestaurants.html',restaurants=all_restaurants)

@app.route('/restaurant/new/',methods=['GET','POST'])
def newRestaurant():
	DBsession=sessionmaker(bind=engine)
	session=DBsession()
	if(request.method == 'GET'):
		return render_template('createNewRestaurant.html')
	elif(request.method == 'POST'):
		form_value_name = request.form['restaurant_name']
		add_restaurant = Restaurant(name=form_value_name)
		session.add(add_restaurant)
		session.commit()
		flash("New Restaurant created")
		#all_restaurants=session.query(Restaurant).all()
		return redirect(url_for('showRestaurants'))


@app.route('/restaurant/<int:restaurant_id>/edit/',methods=['GET','POST'])
def editRestaurant(restaurant_id):
	DBsession=sessionmaker(bind=engine)
	session=DBsession()
	db_name_value = session.query(Restaurant).filter_by(id=restaurant_id).one()
	#print(db_name_value.name)
	if(request.method == 'GET'):
		return render_template('editRestaurant.html',rest_id=restaurant_id,rest_name=db_name_value.name)
	elif(request.method == 'POST'):
		form_value_name = request.form['restaurant_name']
		db_name_value.name = form_value_name		
		session.add(db_name_value)
		session.commit()
		flash("Restaurant successfully edited")
		#all_restaurants=session.query(Restaurant).all()
		return redirect(url_for('showRestaurants'))

@app.route('/restaurant/<int:restaurant_id>/delete/',methods=['GET','POST'])
def deleteRestaurant(restaurant_id):
	DBsession=sessionmaker(bind=engine)
	session=DBsession()
	db_name_value = session.query(Restaurant).filter_by(id=restaurant_id).one()
	#print(db_name_value.name)
	if(request.method == 'GET'):
		return render_template('deleteRestaurant.html',rest_id=restaurant_id,rest_name=db_name_value.name)
	elif(request.method == 'POST'):		
		session.delete(db_name_value)
		session.commit()
		flash("Restaurant successfully deleted")
		#all_restaurants=session.query(Restaurant).all()
		return redirect(url_for('showRestaurants'))

@app.route('/restaurant/<int:restaurant_id>/')
@app.route('/restaurant/<int:restaurant_id>/menu')
def showMenu(restaurant_id):
	DBsession=sessionmaker(bind=engine)
	session=DBsession()
	rest_name = session.query(Restaurant).filter_by(id=restaurant_id).one()
	all_menus = session.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()
	return render_template('showMenus.html',rest_name=rest_name.name,rest_id=restaurant_id,menus=all_menus)

@app.route('/restaurant/<int:restaurant_id>/menu/new',methods=['GET','POST'])
def newMenuItem(restaurant_id):
	DBsession=sessionmaker(bind=engine)
	session=DBsession()
	rest_data = session.query(Restaurant).filter_by(id=restaurant_id).one()
	all_menu_courses=session.query(MenuCourses).all()
	if(request.method == 'GET'):
		return render_template('createNewMenuItem.html',rest_name=rest_data.name,restaurant_id=restaurant_id,all_courses=all_menu_courses)
	elif(request.method=='POST'):
		menu_name=request.form['menu_name']
		menu_price=request.form['menu_price']
		menu_course=request.form['menu_course']
		menu_description =request.form['menu_description']
		all_menus=MenuItem(name=menu_name,description=menu_description,price=menu_price,course=menu_course,restaurant_id=restaurant_id)
		session.add(all_menus)
		session.commit()
		flash("New Menu Item created")
		return redirect(url_for('showMenu',restaurant_id=restaurant_id))


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit/',methods=['GET','POST'])
def editMenuItem(restaurant_id,menu_id):
	DBsession=sessionmaker(bind=engine)
	session=DBsession()
	all_menus=session.query(MenuItem).filter_by(id=menu_id).one()
	all_rest=session.query(Restaurant).filter_by(id=restaurant_id).one()
	all_menu_courses=session.query(MenuCourses).all()
	if(request.method=='GET'):
		return render_template('editMenuItems.html',all_menus=all_menus,restaurant_id=restaurant_id,menu_id=menu_id,rest_name=all_rest.name,all_courses=all_menu_courses)
	elif(request.method=='POST'):
		all_menus.name=request.form['menu_name']
		all_menus.price=request.form['menu_price']
		all_menus.description=request.form['menu_description']
		all_menus.course=request.form['menu_course']
		session.add(all_menus)
		session.commit()
		flash("Menu Item succesfully edited")
		return redirect(url_for('showMenu',restaurant_id=restaurant_id))


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete/',methods=['GET','POST'])
def deleteMenuItem(restaurant_id,menu_id):
	DBsession=sessionmaker(bind=engine)
	session=DBsession()
	all_rest=session.query(Restaurant).filter_by(id=restaurant_id).one()
	menu_values=session.query(MenuItem).filter_by(id=menu_id).one()
	if(request.method=='GET'):
		return render_template('deleteMenuItems.html',restaurant_id=restaurant_id,menu_id=menu_id,menu_name=menu_values.name,rest_name=all_rest.name)
	elif(request.method=='POST'):
		session.delete(menu_values)
		session.commit()
		flash("Menu Item {} succesfully deleted".format(menu_values.name))
		return redirect(url_for('showMenu',restaurant_id=restaurant_id))

#API ENDPOINTS - JSON
@app.route('/restaurants/JSON/')
def showRestaurantsJSON():
	DBsession=sessionmaker(bind=engine)
	session=DBsession()
	all_rest=session.query(Restaurant).all()
	return jsonify(Restaurants=[i.serialize for i in all_rest])

@app.route('/restaurant/<int:restaurant_id>/menu/JSON/')
def showRestaurantMenuJSON(restaurant_id):
	DBsession=sessionmaker(bind=engine)
	session=DBsession()
	all_rest_menu=session.query(MenuItem).filter_by(restaurant_id=restaurant_id)
	return jsonify(RestaurantMenu=[i.serialize for i in all_rest_menu])

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/JSON/')
def showMenuJSON(restaurant_id,menu_id):
	DBsession=sessionmaker(bind=engine)
	session=DBsession()
	all_rest_menu=session.query(MenuItem).filter_by(id=menu_id).all()
	return jsonify(Menu=[i.serialize for i in all_rest_menu])





if(__name__=='__main__'):
	app.debug=True
	app.secret_key='Final_PROJECT'
	app.run('0.0.0.0',port=5000)
