from django.shortcuts import redirect
from functools import wraps

def seller_required(redirect_url=None):
    def decorator(view_func):
        @wraps(view_func)
        def wrapped_view(request, *args, **kwargs):
            # Check if the user is authenticated
            if not request.user.is_authenticated:
                return redirect('login_url')  # Redirect to login page if not authenticated
            
            # Check if the user is a seller
            if request.user.user_type != 'seller':
                if redirect_url:
                    return redirect(redirect_url)  # Redirect to the specified URL
                else:
                    return redirect('not_seller_url')  # Redirect to a default page indicating the user is not a seller

            # User is authenticated and is a seller, proceed to the view
            return view_func(request, *args, **kwargs)
        
        return wrapped_view
    
    return decorator

def superuser_required(redirect_url=None):
    def decorator(view_func):
        @wraps(view_func)
        def wrapped_view(request, *args, **kwargs):
            # Check if the user is authenticated
            # if not request.user.is_authenticated:
            #     return redirect('login_url')  # Redirect to login page if not authenticated
            
            # Check if the user is a seller
            if request.user.user_type != 'admin':
                if redirect_url:
                    return redirect(redirect_url)  # Redirect to the specified URL
                else:
                    return redirect('not_seller_url')  # Redirect to a default page indicating the user is not a seller

            # User is authenticated and is a seller, proceed to the view
            return view_func(request, *args, **kwargs)
        
        return wrapped_view
    
    return decorator