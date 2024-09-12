
from decimal import Decimal
import time
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import auth
from .models import CustomUser,Category,Libraryuser,Books,Rentalhistory,Cart,Purchasehistory
from django.core.mail import send_mail
from django.conf import settings
import datetime
from django.contrib.auth import update_session_auth_hash



# Create your views here.

def home(request):
    return render(request, 'home.html')

def admin_panel(request):
    notifi=CustomUser.objects.filter(status='0').count()
    pending=notifi-1
    return render(request, 'admin_panel.html',{'pen':pending})
def user_login(request):
    if request.method != 'POST':
        messages.get_messages(request)
    return render(request, 'login.html')

def login1(request):
    messages.get_messages(request)
    if request.method == 'POST':
        user_name = request.POST.get('username')
        password1= request.POST.get('password')
        user=authenticate(username=user_name, password=password1)

        if user is not None:
            if user.user_type == '1':
                auth_login(request, user) 
                return redirect('admin_panel')
            elif user.user_type == '2':
                auth.login(request, user)
                return redirect('user_panel')                  
        else:
            messages.info(request, 'Invalid credentials')
            return redirect('login')
        
def add_category(request):
    return render(request, 'add_category.html')
def add_categorydb(request):
    if request.method == 'POST':
        category_name = request.POST.get('category_name')
        

        course = Category(category_name=category_name)
        course.save()

        messages.success(request, 'Category added successfully')
        return redirect('add_category')
    
def user_register(request):
    return render(request, 'user_register.html')


from django.core.validators import validate_email
from django.core.exceptions import ValidationError

def user_registerdb(request):
    if request.method == 'POST':
        # Validate the mobile number
        number = request.POST.get('contact_number')
        if len(number) != 10:
            messages.error(request, 'Phone number should be 10 digits')
            return render(request, 'user_register.html')
        
        # Validate the email
        email = request.POST.get('email')
        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, 'Invalid email format')
            return render(request, 'user_register.html')

        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        age = request.POST['age']
        contact_number = request.POST['contact_number']
        user_type = request.POST['text']

        # Check for existing username or email
        if CustomUser.objects.filter(username=username).exists() or CustomUser.objects.filter(email=email ).exists():
            messages.error(request, 'Username or email already exists')
            return render(request, 'user_register.html')
        
        else:
            user = CustomUser.objects.create_user(username=username, email=email, first_name=first_name, last_name=last_name, user_type=user_type)
            user.save()

            luser = Libraryuser(age=age, number=contact_number, user=user)
            luser.save()
            subject = 'Registration Confirmation'
            message = 'Registration is successful, Please wait for admin approval'
            send_mail(subject, "Hello " + username + ' ' + message, settings.EMAIL_HOST_USER, [email])
            messages.success(request, 'Registration is successful, Please wait for admin approval')
            return redirect('user_register')
    
    return render(request, 'user_register.html')

from django.db.models import Q


#view for render apd page
def apd(request):
    user =  CustomUser.objects.filter(~Q(user_type=1))
    lib_user = Libraryuser.objects.filter(user__in=user)
    return render(request, 'apd.html' , {"user" : user, "lib_user" : lib_user})


import random



def approve(request, k):
    print("hello", k)
    usr = CustomUser.objects.get(id=k)
    pas = str(random.randint(100000, 999999))

    if usr.user_type == "2":
        usr.status = 1
        usr.set_password(pas)
        usr.save()
        lusr = Libraryuser.objects.get(user=k)
        subject = 'Admin approved'
        message = f'username: {usr.username}\npassword: {pas}\nemail: {lusr.user.email}'
        send_mail(subject, message, settings.EMAIL_HOST_USER, [lusr.user.email])

    messages.success(request, 'User approved successfully.')
    return redirect('apd')




def disapprove(request, k):
    usr = CustomUser.objects.get(id=k)
    if usr.user_type == "2":
        usr.status = 2
        usr.save()
        lusr = Libraryuser.objects.get(user=k)
        lusr.delete()
        email = usr.email
        subject = 'Admin Disapproved'
        message = f'Dear {usr.first_name},\n\nYour account has been disapproved by the admin.'
        send_mail(subject, message, settings.EMAIL_HOST_USER, [email])
        passw = CustomUser.objects.get(id=k)
        # passw.delete()
        messages.info(request, 'User Disapproved')
        return redirect('apd')
    
def user_panel(request):
    books=Books.objects.all()
    return render(request, 'user_panel.html',{'books':books}) 


def add_books(request):
    categorys=Category.objects.all()
    return render(request,'add_books.html',{'category':categorys})

def add_booksdb(request):
    if request.method=='POST':
        books_name=request.POST['book_name']       
        auther_name=request.POST['auther_name']
        bpid=request.POST['bpid']
        stocks=request.POST['stocks']
        price=request.POST['price']
        img = request.FILES.get('img')
        sel=request.POST['sel']
        category1=Category.objects.get(id=sel)
        book=Books(book_name=books_name,auther_name=auther_name,bpid=bpid,stocks=stocks,price=price,img=img,category=category1)
        book.save()
        messages.success(request, 'Book added successfully')
        return redirect('add_books')
    
def book_details(request):
    book=Books.objects.all()
    return render(request,'book_details.html',{'books':book})

def delete_book(request,pk):
    bk=Books.objects.get(id=pk)
    bk.delete()
    return redirect('book_details')

def edit_book(request, pk):
    book = Books.objects.get(id=pk)
    categories = Category.objects.all()

    if request.method == 'POST':
        book.book_name = request.POST['book_name']
        book.auther_name = request.POST['auther_name']
        book.bpid = request.POST['bpid']
        book.stocks = request.POST['stocks']
        book.price = request.POST['price']
        book.img = request.FILES.get('img') if request.FILES.get('img') else book.img
        selected_category = request.POST['sel']
        book.category = Category.objects.get(id=selected_category)

        book.save()
        messages.success(request, 'Book updated successfully!')
        return redirect('book_details')

    return render(request, 'edit_book.html', {'book': book, 'categories': categories})

def user_details(request):
    teach=Libraryuser.objects.all()
    ute=CustomUser.objects.all()
    return render(request, 'user_details.html', {'tea':teach,'ut':ute})

def delete_user(request, k):
    luser = Libraryuser.objects.get(user=k)
    user = CustomUser.objects.get(id=k)  # Get the associated CustomUser
    luser.delete() 
     # Delete the Teacher instance
    user.delete()  # Delete the associated CustomUser instance
    return redirect('user_details')

def search(request):
    if request.method == 'GET':
        query = request.GET.get('q')
        print(query)
        if query:
            books = Books.objects.filter(Q(book_name__icontains=query) |
                                        Q(auther_name__icontains=query))
            print(books)
            return render(request, 'user_panel.html', {'books': books})
        else:
            return redirect('book_details')
    return render(request, 'user_panel.html')

def rent(request,pk):
    books = Books.objects.get(id=pk)
    return render(request, 'rent.html', {'books': books})

# views.py

from django.shortcuts import render, get_object_or_404, redirect
from .models import Books, Rentalhistory
from django.utils import timezone





def rent_book(request, book_id):
    book = get_object_or_404(Books, id=book_id)
    if request.method == 'POST':
        return_date = request.POST.get('return_date')
        rental_date = request.POST.get('rental_date')
        
        if return_date:

            # Check if the user has already taken the book
            if Rentalhistory.objects.filter(user=request.user, book=book, return_status='Pending').exists():
                messages.error(request, 'You have already taken this book. Please return it first.')
            else:
                # Reduce the stock count
                book.stocks -= 1
                book.save()

                # Calculate fine if rental date is higher than return date
                rental_date = timezone.datetime.strptime(rental_date, '%Y-%m-%d').date()
                return_date = timezone.datetime.strptime(return_date, '%Y-%m-%d').date()
                fine_amount = 0
                if rental_date < return_date:
                    # fine_amount = 0
                    if return_date < timezone.datetime.now().date(): 
                        fine_amount = book.price * 0.05


                # Create a new rental history entry
                Rentalhistory.objects.create(
                    user=request.user,  # Assuming user is logged in
                    book=book,
                    rent_date=timezone.now().date(),
                    due_date=return_date,
                    return_status='Pending',
                    payment_status='Not Applicable',
                    fine_amount=fine_amount
                    
                )
                if rental_date > return_date:
                    send_mail(
                'Overdue Book Alert',
                f'Your rental for "{book.book_name}" is overdue. Please return the book. Current fine: ₹{fine_amount:.2f}',
                settings.EMAIL_HOST_USER,
                [request.user.email],
                fail_silently=False,
            )
                    send_mail(
    'Overdue Book Alert - Admin Notification',
    f'User {request.user.username} has an overdue rental for the book "{book.book_name}". '
    f'The rental was due on {return_date}. Current fine amount: ₹{fine_amount:.2f}. '
    'Please take the necessary actions.',
    settings.EMAIL_HOST_USER,
    [settings.EMAIL_HOST_USER],  # Admin's email address
    fail_silently=False,
)
                messages.success(request, 'Rental request successful.')
                return redirect('user_panel')
    return render(request, 'rent_book.html', {'book': book})



def user_rentals(request):
    rentals = Rentalhistory.objects.filter(user=request.user)
    books_already_rented = [r.book for r in rentals]
    return render(request, 'user_rentals.html', {'rentals': rentals})




from django.shortcuts import render, get_object_or_404, redirect
from .models import Rentalhistory, Books
from django.utils import timezone



def pay_fine(request, book_id):
    rental = get_object_or_404(Rentalhistory, book_id=book_id, user=request.user, return_status='Pending')
    if request.method == 'POST':
        # Process payment
        rental.fine_payed=rental.fine_amount
        rental.fine_amount = 0
        rental.payment_status = 'Paid'
        if  rental.issue_reported:
            rental.fine_payed =  rental.book.price + rental.book.price  * Decimal('0.10')
            rental.return_status = 'Returned'
        rental.save()
        return redirect('user_rental_history')  # Redirect to the rental history page
    return render(request, 'user_rentalhistory.html', {'rental': rental})
def user_rental_history(request):
    rentals = Rentalhistory.objects.filter(user=request.user)
    return render(request, 'user_rentalhistory.html', {'rentals': rentals})

def admin_rentalhistory(request):
    rentals = Rentalhistory.objects.select_related('user', 'book').all()
    print(rentals)
    return render(request, 'admin_rental_history.html', {'rentals': rentals})


def return_book(request, book_id):
    rentals = Rentalhistory.objects.filter(book_id=book_id, user=request.user, return_status='Pending')
    if rentals.exists():
        rental = rentals.first()

        if request.method == 'POST':
            # Update rental record with return date
            rental.return_status = 'Returned'
            rental.returned_date = datetime.datetime.now()
            rental.save()
            book = rental.book
            book.stocks += 1
            book.save()
            return redirect('user_rental_history')  # Redirect to the rental history page
        return render(request, 'user_rentalhistory.html', {'rental': rental})
    else:
        messages.error(request, 'No pending rental for this book')
        return redirect('user_rental_history')  # Redirect to the rental history page
    



def booklist(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    books = Books.objects.filter(category=category)
    return render(request, 'book_list.html', {'category': category, 'books': books})

def book_list(request):
    books = Books.objects.all()
    return render(request, 'book_list.html', {'books': books})

def add_to_cart(request, book_id):
    book = get_object_or_404(Books, id=book_id)
    cart_item, created = Cart.objects.get_or_create(user=request.user, book=book)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('view_cart')

def view_cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_price = sum(item.total_price() for item in cart_items)
    item_count = cart_items.count()
    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price, 'item_count': item_count})


def increase_quantity(request, book_id):
    cart_item = get_object_or_404(Cart, book_id=book_id, user=request.user)
    if cart_item.book.stocks < cart_item.quantity + 1:
        return redirect('view_cart')
    else:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('view_cart')


def decrease_quantity(request, book_id):
    cart_item = get_object_or_404(Cart, book_id=book_id, user=request.user)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    return redirect('view_cart')

def remove_item(request, book_id):
    cart_item = Cart.objects.filter(book_id=book_id, user=request.user)
    if cart_item.exists():
        cart_item.delete()
    return redirect('view_cart')




def checkout(request):
    user = request.user
    cart_items = Cart.objects.filter(user=user)
    
    total_price = sum(item.total_price() for item in cart_items)  # Make sure total_price() is defined

    if request.method == 'POST':
        return redirect('checkout_db')  # Redirect to checkout_db to handle form submission
    
    return render(request, 'checkout.html', {
        'cart_items': cart_items,
        'total_price': total_price,
    })

def checkout_db(request):
    user = request.user  # Get the currently logged-in user
    
    if request.method == 'POST':
        # Extract form data
        email = request.POST.get('email')
        your_name = request.POST.get('your_name')
        delivery_address = request.POST.get('delivery_address')
        mobile_number = request.POST.get('mobile_number')
        payment_method = request.POST.get('payment_method')
        
        # Handle cart items
        cart_items = Cart.objects.filter(user=user)
        if cart_items.exists():
            # Save purchase history for each item in the cart
            for item in cart_items:
                Purchasehistory.objects.create(
                    user=user,
                    book=item.book,
                    quantity=item.quantity,
                    total_price=item.total_price(),  # Assuming Cart model has a method for total_price
                )
                
                # Decrease the quantity of books in the book table
                item.book.stocks -= item.quantity
                item.book.save()
            
            
            # Clear the cart after checkout
            cart_items.delete()
            
            # Send confirmation email
            subject = 'Order Confirmation'
            current_date = datetime.datetime.now()
            delivery_date = current_date + datetime.timedelta(days=7)

            message = f"Hello {your_name},\n\nYour order has been placed successfully.\n\nDetails:\nDelivery Address: {delivery_address}\nMobile Number: {mobile_number}\nPayment Method: {payment_method}\nDelivery Date: {delivery_date.strftime('%d-%m-%Y')}\n\nThank you for shopping with us."
            send_mail(subject, message, settings.EMAIL_HOST_USER, [email])
            
            # Set success message and redirect
            # messages.success(request, 'Your order has been placed successfully. Please check your email for confirmation.')
            return redirect('view_cart')
        else:
            messages.error(request, "Your cart is empty.")
    
    return render(request, 'checkout.html')


def user_purchase_history(request):
    purchase = Purchasehistory.objects.filter(user=request.user)
    return render(request, 'user_purchasehistory.html', {'purchase': purchase})

def admin_purchase_history(request):
    purchase = Purchasehistory.objects.select_related('user', 'book').all()
    print(purchase)
    return render(request, 'admin_purchasehistory.html', {'purchase': purchase})



def report_issue(request, book_id):
    user = request.user
    if request.method == 'POST':
        try:
            rental = Rentalhistory.objects.get(book_id=book_id, return_status="Pending", issue_reported=False, user_id=user.id)
            print(rental)
            # Handle the issue reporting logic here (e.g., create an issue record, send a notification, etc.)
            fine_amount = rental.book.price + rental.book.price * Decimal('0.10')
            rental.fine_amount = fine_amount if rental.fine_amount is None else rental.fine_amount + fine_amount
            rental.issue_reported = True
            rental.reported_at = datetime.datetime.now()
            rental.payment_status = "Not Paid"
            rental.save()
            
            # ReportBookIssue.objects.create(
            #     user=request.user,
            #     book_price=rental.book.price,
            #     fine_amount=fine_amount,
            #     book_id=rental.book_id
            # )
            
            messages.success(request, 'Issue reported successfully.')
        except Rentalhistory.DoesNotExist:
            messages.error(request, 'Rental record not found.')
        
        return redirect('user_rental_history')  # Redirect to the rental history page or wherever appropriate

    # Handle GET requests if necessary
    return redirect('user_rentalhistory')



# def admin_damage_report(request):
#     damaged_books = ReportBookIssue.objects.select_related('user', 'book').all()
#     print (damaged_books)
#     return render(request, 'admin_damage_report.html', {'damaged_books': damaged_books})


def admin_damage_report(request):
    damaged_books = Rentalhistory.objects.select_related('user', 'book').filter(issue_reported=True)
    print (damaged_books)
    return render(request, 'admin_damage_report.html', {'damaged_books': damaged_books})


def reset_password(request):
    if request.method == 'POST':
        pas = request.POST['np']
        cpas = request.POST['cp']
        if pas == cpas:
            if len(pas) < 6 or not any(char.isupper() for char in pas) \
                    or not any(char.isdigit() for char in pas) \
                    or not any(char in '!@#$%^&*()_+-=[]{}|;:,.<>?/~' for char in pas):
                messages.error(request, 'Password must be at least 6 characters long and contain at least one uppercase letter, one lowercase letter, one digit, and one special character.')
                return redirect('re_pas')
            else:
                usr = request.user.id
                tsr = CustomUser.objects.get(id=usr)
                tsr.set_password(pas)  
                tsr.save()
                update_session_auth_hash(request, tsr)  
                messages.success(request, 'Your password was successfully updated!')
                return redirect('re_pas')
        else:
            messages.error(request, 'Passwords do not match.')
            return redirect('re_pas')
    else:
        return redirect('re_pas')  

            
def re_pas(request):
    return render(request, 'reset_password.html')




def edit_profile(request):
    user = request.user
    libraryuser = Libraryuser.objects.get(user=user)

    if request.method == 'POST':
        # Validate the mobile number
        number = request.POST.get('contact_number')
        if len(number) != 10:
            messages.error(request, 'Phone number should be 10 digits')
            return render(request, 'edit_profile.html', {'user': user, 'libraryuser': libraryuser})

        # Validate the email
        email = request.POST.get('email')
        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, 'Invalid email format')
            return render(request, 'edit_profile.html', {'user': user, 'libraryuser': libraryuser})

        # Check for existing username or email
        username = request.POST.get('username')
        if CustomUser.objects.filter(username=username).exclude(id=user.id).exists() or CustomUser.objects.filter(email=email).exclude(id=user.id).exists():
            messages.error(request, 'Username or email already exists')
            return render(request, 'edit_profile.html', {'user': user, 'libraryuser': libraryuser})

        # Update user and libraryuser details
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.username = username
        user.email = email
        user.save()

        libraryuser.age = request.POST['age']
        libraryuser.number = request.POST['contact_number']
        libraryuser.save()

        messages.success(request, 'Profile updated successfully')
        return redirect('view_profile')  # Redirect to the view_profile page after updating

    return render(request, 'edit_profile.html', {'user': user, 'libraryuser': libraryuser})

def view_profile(request):
    user = request.user
    libraryuser = Libraryuser.objects.get(user=user)
    return render(request, 'view_profile.html', {'user': user, 'libraryuser': libraryuser})






    
