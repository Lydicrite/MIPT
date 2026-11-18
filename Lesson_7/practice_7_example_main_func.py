import random
import numpy as np
import copy
from functools import partial

def gen_norm_hist(count):
    hist = [random.random() for i in range(count)]
    hist = np.array(hist)
    hist /= hist.sum()
    return hist

def recursion_gen_norm_hist(count):
    if count >= 2:
        res = np.array([random.random()])
        return np.append(res,recursion_gen_norm_hist(count - 1))
    else:
        return random.random()


def cumulative_hist(hist, count):
    if(count < len(hist) - 1):
        hist[count+1] += hist[count]
        return cumulative_hist(hist, count+1)
    else:
        return hist

# weightted_vec: x*y
def weighted(y):
    def prod(x):
        return sum([x[i] * y[i] for i in range(len(x))])
    return prod

def func_x(x):
    def func_y(y):
        def func_z(z):
            return x+y+z
        return func_z
    return func_y

# Ax+ by+cz
def get_intence(x,y,z,a,b,c):
    return a*x + b*y + c*z


class  Hist:
    def __iter__(self):
        return self

    def __init__(self, count):
        self.count = count
        self.counter = 0

    def __next__(self):
        if self.counter < self.count:
            self.counter += 1
            return random.random()
        else:
            raise StopIteration

def hist_generator(count):
   while count > 0:
       count -= 1
       yield random.random()


def filter_05(num):
    if num > 0.5:
        return True
    else:
        return False

if __name__ == '__main__':
    '''
    # First order object
    my_func = gen_norm_hist
    print(my_func(10))

    #recursion
    rec_hist = recursion_gen_norm_hist(10)
    rec_hist /= rec_hist.sum()
    print(rec_hist)

    #high order func
    print(list(map(gen_norm_hist, [i for i in range(10)])))

    # lambda

    hist_norm = lambda x: x / x.sum()
    res = recursion_gen_norm_hist(10)
    print(res)
    print(hist_norm(res))

    complex_lambda = lambda x: (
             x ** 2 if x > 0
             else 0 if x == 0
             else abs(x)
               )
    
    print(complex_lambda(-3))
    print(complex_lambda(0))
    print(complex_lambda(3))

    l_func = lambda x, y: x ** 2 + y ** 3
    print(l_func(3,4))

    #компактная генерация данныех (с  lambda-функцией)
    doubled_lambda = list(map(lambda x: x * 2, [i for i in range(10)]))
    print(doubled_lambda)
    '''
    # отбор элементов по условию
    numbers = [i for i in range(10)]
    even_lambda = list(filter(lambda x: x % 2 == 0, numbers))
    print(even_lambda)

    # сортировка с пользовательским ключом
    numbers = [5, -3, 2, -8, 1, 0, -2]
    sorted_numbers = sorted(numbers, key=lambda x: abs(x)%2)
    print(sorted_numbers)

    hist_10 = lambda x1: x1(10)
    print(hist_10(gen_norm_hist))


    hist_10 = lambda x1: x1(10)
    print(cumulative_hist(hist_10(gen_norm_hist),0))

    # замыкание
    print(weighted(gen_norm_hist(3))(recursion_gen_norm_hist(3)))

    # каррирование
    print(func_x(5)(4)(3))
    func = lambda x: lambda y: lambda z: x+y+z
    print(func(5)(4)(3))

    #частичное применение
    av_I = partial(get_intence, a=0.3, b = 0.3, c = 0.4)
    print(av_I(0.1,0.2,0.3))

    #итератор
    h = Hist(3)
    for i in h:
        print(i)

    #generator
    h = hist_generator(3)
    print(next(h))
    print(next(h))
    print(next(h))
    #print(next(h))

    #
    m_hist = map(gen_norm_hist, [i for i in range(10)])
    print(next(m_hist))
    print(next(m_hist))
    print(next(m_hist))

    # фильтрация
    hist = gen_norm_hist(2) + 0.2
    result_filter = filter(filter_05, hist)
    print(next(result_filter))
    print(hist)
    print(list(result_filter))

    # объединение двух или более псисков в 1
    res = zip([1,2], ['no', 'no', 'yes'])
    print(list(res))















