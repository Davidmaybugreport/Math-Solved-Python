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
    print("Commands:")
    print("  - Type 'TOF' to toggle True/False mode ON/OFF")
    print("  - Type 'exit', 'quit', or 'q' to stop.")
    print("----------------------------------------\n")
    
    tof_mode = False  # Track whether True/False mode is active
    
    while True:
        # Show current status in the prompt
        status_tag = " [TOF: ON]" if tof_mode else ""
        user_input = input(f"Enter expression{status_tag}: ").strip()
        
        # Check if user wants to quit
        if user_input.lower() in ["exit", "quit", "q"]:
            print("Exiting solver. Goodbye!")
            break
            
        # Check if user wants to toggle TOF mode
        if user_input.upper() == "TOF":
            tof_mode = not tof_mode
            state = "ON (True/False mode active)" if tof_mode else "OFF"
            print(f"--> [TOF Mode is now {state}]\n")
            continue
            
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
                
                left_expr = parse_expr(left_str, transformations=transformations)
                right_expr = parse_expr(right_str, transformations=transformations)
                
                if tof_mode:
                    # In TOF mode, check if the equation evaluates to True or False
                    # or solve it and see if the equality holds
                    try:
                        is_true = bool(left_expr == right_expr)
                        # If there are variables, try substituting or solving
                        eq = Eq(left_expr, right_expr)
                        variables = list(eq.free_symbols)
                        if variables:
                            solutions = solve(eq, variables[0])
                            print(f"-> TOF Result: Solutions exist for {variables[0]} -> {solutions}\n")
                        else:
                            print(f"-> TOF Result: {is_true}\n")
                    except Exception:
                        print(f"-> TOF Result: False\n")
                else:
                    eq = Eq(left_expr, right_expr)
                    variables = list(eq.free_symbols)
                    
                    if not variables:
                        print(f"-> Result: {left_expr == right_expr}\n")
                    else:
                        var = variables[0]
                        solutions = solve(eq, var)
                        print(f"-> Solutions for {var}: {solutions}\n")
            
            else:
                # Regular arithmetic expression or inequality check
                cleaned = clean_input(user_input)
                expr = parse_expr(cleaned, transformations=transformations)
                
                if tof_mode:
                    # If TOF mode is on, evaluate whether the expression evaluates to True/Non-zero
                    try:
                        val = expr.evalf() if expr.is_number else expr
                        is_true = bool(val) and val != 0
                        print(f"-> TOF Result: {is_true} (Value: {val})\n")
                    except Exception:
                        print(f"-> TOF Result: False\n")
                else:
                    result = expr.evalf() if expr.is_number else expr
                    print(f"-> Result: {result}\n")
                
        except Exception as e:
            print(f"-> Error solving expression: {e}\n")

if __name__ == "__main__":
    solve_math_problem()
    
