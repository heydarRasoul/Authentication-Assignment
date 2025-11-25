# def print_kwargs(**kwargs):
#     return kwargs

# print(print_kwargs(kwarg1=1, kwarg2=2, kwarg3=3))
# print(print_kwargs(kwarg5=5, kwarg6=6))

# def print_args(*args):
#     return args

# print(print_args(1, 2, 3, 4))
# print(print_args(5, 6))


# def print_args_kwargs(*args, **kwargs):
#     print(args)
#     print(kwargs)

# print_args_kwargs(1, 2, 3, 4, kwarg1=1, kwarg2=2)

# =============
import functools

# define function here and then we just call theis function by using decorator @
def print_args(func):
    @functools.wraps(func)
    def decorator_wrapper(*args, **kwargs):
        print(func.__name__)
        for idx, e in enumerate(args):
            print(f'{idx}: {e}')
        return func(*args, **kwargs)
    return decorator_wrapper

# here is calling function with decorator we just add function name and what we need to run function over tight bellove it.
@print_args
def sum_num(*args):
    # __name__ here just print the name of function.
    # print(sum_num.__name__) 
    # for idx, e in enumerate(args):
    #     print(f'{idx}: {e}')
    return sum(list(args))

@print_args
def concatenate_str(*args):
    # print(concatenate_str.__name__)
    # for idx, e in enumerate(args):
    #     print(f'{idx}: {e}')
  
    return " ".join(args)

@print_args
def sort_list(*args):
    # print(sort_list.__name__)
    # for idx, e in enumerate(args):
    #     print(f'{idx}: {e}')
    return sorted(list(args))


# print(sum_num(1,2,3))
# print(concatenate_str("hello", "world"))
# print(sort_list(32, 14, 27, 60))



# ======================

logged_in = False

def auth_logged_in(func):
    @functools.wraps(func)
    def decorator_wrapper(*args, **kwargs):
        if logged_in == False:
            return print("Please login to perform this action.")
        else:
            return func(*args, **kwargs)
    return decorator_wrapper


@auth_logged_in
def sum_num(*args):
    return sum(list(args))
#print > Please login to perform this action.

@auth_logged_in
def concatenate_str(*args):
    return " ".join(args)

@auth_logged_in
def sort_list(*args):
    return sorted(list(args))   




# print(sum_num(1,2,3))
# print(concatenate_str("hello", "world"))
# print(sort_list(32, 14, 27, 60))



# =====================


def only_strings(func):
    @functools.wraps(func)
    def decorator_wrapper(*args, **kwargs):
        new_list = args[0]

        for idx, e in enumerate(new_list):
            new_list[idx] = str(e)
        args = (new_list,)

        return func(*args, **kwargs)

    return decorator_wrapper


@only_strings
def string_joined(list_of_strings):
    new_list = list_of_strings

    return ", ".join(new_list)

lst = ["one", "two", "three", "four", "five", 3]
# print(string_joined(lst))
# print(lst)

# =====================


def only_strings(func):
    @functools.wraps(func)
    def decorator_wrapper(*args, **kwargs):
        for key in kwargs:
            kwargs[key] = kwargs[str(key)]
        
        return func(*args, **kwargs)    
    return decorator_wrapper


@only_strings
def convert_to_str(**kwargs):
    new_list = []

    for key, val in kwargs.items():
        new_list.append(str(val))

    return ', '.join(new_list)


lst = ['one', 'two', 'three', 'four', 'five', 3]
joined_str = convert_to_str(kw1=1, kw2='two', kw3=3, kw4='four')

# print(joined_str)
# print(type(joined_str))



# ===============================

def only_strings(func):
    @functools.wraps(func)
    def decorator_wrapper(*args, **kwargs):
        new_list = []
        for key, val in kwargs.items():
            new_list.append(str(val))

        joined_str = ', '.join(new_list)

        return joined_str  
    return decorator_wrapper


@only_strings
def convert_to_str(**kwargs):
    return ', '.join(kwargs.values())
   

    
   
joined_strr = convert_to_str(kw1=1, kw2='two', kw3=3, kw4='four', kw5='five')

print("join_str: ",joined_strr)
print(type(joined_strr))