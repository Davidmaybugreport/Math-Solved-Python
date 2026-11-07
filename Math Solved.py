from sympy import symbols, Eq, solve, SympifyError
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application

# Enable implicit multiplication (e.g., "5x" instead of "5*x")
transformations = standard_transformations + (implicit_multiplication_application,)

def clean_input(expr_str):
    """Cleans up user input to format it nicely for SymPy."""
    return expr_str.replace("^", "**")

def solve_math_problem():
    print("========================================")
    print("      PYTHON ALGEBRA SOLVER (Pydroid)   ")
    print("========================================")
    print("Examples:")
    print("  - Linear equation: 589244 - x = 276738")
    print("  - Quadratic equation: x**2 - 5*x + 6 = 0")
    print("  - Arithmetic: 589244 + 312506")
    print("  - Type 'exit', 'quit', or 'q' to stop.")
    print("----------------------------------------\n")
    
    while True:
        user_input = input("Enter equation or expression (or 'exit'): ").strip()
        
        # Check if user wants to quit
        if user_input.lower() in ["exit", "quit", "q"]:
            print("Exiting solver. Goodbye!")
            break
            
        if not user_input:
            continue

        try:
            # Check if it's an equation containing '='
            if "=" in user_input:
                parts = user_input.split("=")
                if len(parts) != 2:
                    print("Error: Invalid equation format. Use a single '=' sign.\n")
                    continue
                
                left_str = clean_input(parts[0])
                right_str = clean_input(parts[1])
                
                # Parse strings into SymPy expressions
                left_expr = parse_expr(left_str, transformations=transformations)
                right_expr = parse_expr(right_str, transformations=transformations)
                
                eq = Eq(left_expr, right_expr)
                
                # Find all free variables in the equation (like x, y, etc.)
                variables = list(eq.free_symbols)
                
                if not variables:
                    # If no variables, just check if it's True/False
                    print(f"Result: {left_expr == right_expr}\n")
                else:
                    # Solve for the detected variables
                    var = variables[0] # Takes the first variable found (e.g., x)
                    solutions = solve(eq, var)
                    print(f"-> Solutions for {var}: {solutions}\n")
            
            else:
                # If it's just an arithmetic expression or algebra to simplify
                cleaned = clean_input(user_input)
                expr = parse_expr(cleaned, transformations=transformations)
                result = expr.evalf() if expr.is_number else expr
                print(f"-> Result: {result}\n")
                
        except Exception as e:
            print(f"-> Error solving expression: {e}\n")

if __name__ == "__main__":
    solve_math_problem()
  
