

from market import app
from flask import render_template, redirect, url_for,flash,request
from market.models import Item,User,Cart,Category
from.forms import RegisterForm,LoginForm
from market import db
from flask_login import current_user,login_user,logout_user,login_required
from .forms import EditCategoryForm 


@app.route('/')
@app.route('/dashboard')
@login_required
def dashboard_page():
    if current_user.is_admin:
        return redirect(url_for('admin_categories'))
    items = Item.query.filter(Item.quantity > 0).all()
    return render_template('dashboard.html', items=items)

   

@app.route('/cart') 
@login_required
def cart_page():
    user = User.query.get(current_user.id)
    cart_items = user.cart_items

   
    total_price = sum(item.item.price * item.quantity for item in cart_items)

    return render_template('cart.html', cart_items=cart_items, total_price=total_price)


@app.route('/profile')
@login_required
def profile_page():
    return render_template('profile.html',user=User.query.get(current_user.id))


@app.route('/register',methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              email=form.email_address.data,
                              password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        return redirect(url_for('dashboard_page'))
    if form.errors != {}: 
        for err_msg in form.errors.values():
            print(f'There was an error with creating a user: {err_msg}')
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(
                attempted_password=form.password.data
        ):
            login_user(attempted_user)
            flash(f'Success! You are logged in as: {attempted_user.username}', category='success')
            return redirect(url_for('dashboard_page'))
        else:
            flash('Username and password are not match! Please try again', category='danger')
    return render_template('login.html', form=form)

@app.route('/logout')
def logout_page():
    logout_user()
    return redirect(url_for("login_page"))


@app.route('/add_to_cart/<int:item_id>', methods=['GET', 'POST'])
@login_required
def add_to_cart(item_id):
    user = User.query.get(current_user.id)
    item = Item.query.get(item_id)

    if item.quantity > 0:
        cart_item = Cart.query.filter_by(user_id=user.id, item_id=item.id).first()
        
        if cart_item:
            cart_item.quantity += 1
        else:
            cart_item = Cart(user_id=user.id, item_id=item.id, quantity=1)

        db.session.add(cart_item)
        item.quantity -= 1

        if item.quantity == 0 and item in user.items:
            db.session.delete(item)

        db.session.commit()
        flash(f'{item.name} added to cart!', 'success')
    else:
        flash(f'{item.name} is out of stock!', 'danger')

    return redirect(url_for('cart_page'))



@app.route('/remove_from_cart/<int:item_id>')
@login_required
def remove_from_cart(item_id):
    user = User.query.get(current_user.id)
    cart_item = Cart.query.filter_by(user_id=user.id, item_id=item_id).first()

    if cart_item:
        item = cart_item.item  
        item.quantity += cart_item.quantity  

        db.session.delete(cart_item)  
        db.session.commit()

        flash(f'{item.name} removed from cart and quantity restored!', 'success')
    else:
        flash('Item not found in cart!', 'danger')

    return redirect(url_for('cart_page'))



@app.route('/checkout', methods=['POST'])
@login_required
def checkout():
    user = User.query.get(current_user.id)
    cart_items = user.cart_items

    
    for cart_item in cart_items:
        db.session.delete(cart_item)

    db.session.commit()

    flash('Your items have been purchased!', 'success')
    return redirect(url_for('dashboard_page'))



@app.route('/admin/admin_categories')
@login_required
def admin_categories():
    if not current_user.is_admin:
        flash('Access denied. You are not an admin.', 'danger')
        return redirect(url_for('dashboard_page')) 
    return render_template('admin_categories.html',user=User.query.get(current_user.id),categories=Category.query.all())

with app.app_context():
    db.create_all()

    admin=User.query.filter_by(username='admin').first()
    if not admin:
        admin=User(username='admin',password='admin',is_admin=True,email='admin@gmail.com')
        db.session.add(admin)
        db.session.commit()

@app.route('/admin_items')
@login_required
def adminitems_page():
     return render_template('admin_items.html')

@app.route('/category/add', methods=['GET', 'POST'])
@login_required
def add_category():
    if request.method == 'POST':
        name = request.form.get('name')

        
        print(f"Received form data - name: {name}")
        if not name:
            flash('Category name is required', 'danger')
        else:
           
            category = Category(name=name)
            db.session.add(category)

            try:
               
                db.session.commit()
                flash(f'Category {category.name} added successfully', 'success')
            except Exception as e:
                
                db.session.rollback()  
                flash(f'Error adding category to the database: {str(e)}', 'danger')

            return redirect(url_for('admin_categories'))

    return render_template('categories/add.html')


 

@app.route('/category/<int:category_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_category(category_id):
    category = Category.query.get(category_id)
    form = EditCategoryForm()  
    if request.method == 'POST' and form.validate_on_submit():
        new_name = form.new_name.data
        if not new_name:
            flash('Category name is required', 'danger')
        else:
            category.name = new_name
            db.session.commit()
            flash(f'Category {category.name} updated successfully', 'success')
            return redirect(url_for('admin_categories'))
    
    form.new_name.data = category.name

    return render_template('categories/edit.html', form=form, category=category)


@app.route('/category/<int:category_id>/show')
@login_required
def show_category(category_id):
    category = Category.query.get(category_id)
    return render_template('categories/show.html', category=category,user=User.query.get(current_user.id),_category=category.query.get(category_id))

@app.route('/category/<int:category_id>/add-items',methods=['GET'])
@login_required
def add_items(category_id):
    category = Category.query.get(category_id)
    return render_template('items/add-items.html', category=category, user=User.query.get(current_user.id), _category=category.query.get(category_id))

@app.route('/category/<int:category_id>/add-items',methods=['POST'])
@login_required
def add_items_post(category_id):
    category = Category.query.get(category_id)
    name = request.form.get('name')
    expdate = request.form.get('expdate')
    quantity = int(request.form.get('quantity'))
    price = float(request.form.get('price'))

        
    new_item = Item(
            name=name,
            expdate=expdate,
            quantity=quantity,
            price=price,
            owner=current_user.id,  
            category_id=category_id
        )

    db.session.add(new_item)
    db.session.commit()

    return redirect(url_for('show_category', category_id=category.id))
    

@app.route('/category/<int:category_id>/edit-item/<int:item_id>', methods=['GET', 'POST'])
@login_required
def edit_item(category_id, item_id):
    category = Category.query.get(category_id)
    item = Item.query.get(item_id)  

    if request.method == 'POST':
        
        item.name = request.form.get('name')
        item.expdate = request.form.get('expdate')
        item.quantity = int(request.form.get('quantity'))
        item.price = float(request.form.get('price'))

        db.session.commit()  

        return redirect(url_for('show_category', category_id=category.id))

    return render_template('items/edit.html', category=category, user=User.query.get(current_user.id), item=item)

@app.route('/category/<int:category_id>/delete-item/<int:item_id>', methods=['GET', 'POST'])
@login_required
def delete_item(category_id, item_id):
    category = Category.query.get(category_id)
    item = Item.query.get(item_id)  

    if request.method == 'POST':
        if item.quantity == 0:
            flash(f'Item {item.name} has a quantity of 0. Please trying restocking before deleting.', 'warning')
            return redirect(url_for('show_category', category_id=category.id))

       
        db.session.delete(item)
        db.session.commit()
        
        flash(f'Item {item.name} deleted successfully', 'success')
        return redirect(url_for('show_category', category_id=category.id))

    return render_template('items/delete.html', category=category, user=User.query.get(current_user.id), item=item)








@app.route('/category/<int:category_id>/delete', methods=['GET'])
@login_required
def confirm_delete_category(category_id):
    category = Category.query.get(category_id)
    if not category:
        flash(f'Category not found!', 'danger')
        return redirect(url_for('admin_categories'))

    return render_template('categories/delete.html', category=category)


    
@app.route('/category/<int:category_id>/delete', methods=['POST'])
@login_required
def delete_category(category_id):
    category = Category.query.get(category_id)

    if not category:
        flash(f'Category not found!', 'danger')
        return redirect(url_for('admin_categories'))

   
    itemsleft = Item.query.filter_by(category_id=category.id).all()

    if itemsleft:
        
        flash(f'Cannot delete category "{category.name}" because it is not empty.', 'danger')
        return redirect(url_for('admin_categories'))

  
    db.session.delete(category)

    try:
        db.session.commit()
        flash(f'Category {category.name} deleted successfully', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting category: {str(e)}', 'danger')

    return redirect(url_for('admin_categories'))


@app.route('/search', methods=['GET'])
def search_results():
    query = request.args.get('query')
    
    items = Item.query.filter(Item.name.ilike(f"%{query}%")).all()
    categories = Category.query.filter(Category.name.ilike(f"%{query}%")).all()
    return render_template('search_results.html', items=items,categories=categories)






