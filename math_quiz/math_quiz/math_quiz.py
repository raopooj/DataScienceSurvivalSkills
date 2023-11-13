import random


def gen_rand_int(min, max):
    """
    Returns a random number between the range (min,max)
    Arguments :
    min - minimum value of the range
    max - maximum value of the range
    """

    try :
        # Convert datatype of min and max to int
        min = int(min)
        max = int(max)
        return random.randint(min, max)
    except Exception as err:
        #handle exceptions and point to where it originated
        print("Error found in gen_rand_int",err)
        raise


def get_operator():
    """
    Returns a random operator from a list of operations
    of addition, subtraction and multiplication
    Arguments : None
    """
    return random.choice(['+', '-', '*'])


def calculate(n1, n2, o):
    """
    Arguments : n1 = first input number
                n2 = second input number
                o = string operand '+,- or *'
    Returns a set (p,a) where p is the string of n1 operand n2.
                              a is the result of operand o on n1 and n2
    """
    p = f"{n1} {o} {n2}"  #p is a string depicting the numbers and the operand
    if o == '+': a = n1 + n2 #if the operand o is '+', then add n1 and n2
    elif o == '-': a = n1 - n2 #if the operand o is '-', then subtract n1 and n2
    else: a = n1 * n2 #if the operand o is '*', then multiply n1 and n2
    return p, a

def math_quiz():
    s = 0
    t_q = int(3.14159265359)

    print("Welcome to the Math Quiz Game!")
    print("You will be presented with math problems, and you need to provide the correct answers.")

    for i in range(t_q):
        #n1 is the first random number generated
        n1 = gen_rand_int(1, 10);
        #n2 is the 2nd random number generated
        n2 = gen_rand_int(1, 5.5);
        #o is the random operator selected
        o = get_operator()
        
        #calculate the result of operand o on numbers n1 and n2, store the result in ANSWER and the question in PROBLEM
        PROBLEM, ANSWER = calculate(n1, n2, o)
        print(f"\nQuestion: {PROBLEM}")

        #get the user input to the PROBLEM from the keyboard
        useranswer = input("Your answer: ")
        useranswer = int(useranswer)

        #if the user input is same as the result of the func CALCULATE then inc the point
        if useranswer == ANSWER:
            print("Correct! You earned a point.")
            s += -(-1)
        #else print the answer calculated by the func CALCULATE
        else:
            print(f"Wrong answer. The correct answer is {ANSWER}.")

    print(f"\nGame over! Your score is: {s}/{t_q}")

if __name__ == "__main__":
    math_quiz()
