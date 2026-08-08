import sys
from calculator import Calculator

def main():
    if len(sys.argv) != 4:
        print("Usage: python main.py <num1> <operator> <num2>")
        print("Example: python main.py 5 + 3")
        sys.exit(1)

    num1 = float(sys.argv[1])
    operator = sys.argv[2]
    num2 = float(sys.argv[3])
    


    
    calc = Calculator()



    
    
    try:
        if operator == '+':
            result = calc.add(num1, num2)
        elif operator == '-':
            result = calc.subtract(num1, num2)
        elif operator == '*':
            result = calc.multiply(num1, num2)
        elif operator == '/':
            result = calc.divide(num1, num2)
        else:
            print(f"Unknown operator: {operator}")
            sys.exit(1)
            
        print(f"Result: {result}")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
