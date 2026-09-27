import py_compile, sys
try:
    py_compile.compile(sys.argv[1], doraise=True)
    print("Syntax OK")
except py_compile.PyCompileError as e:
    print(f"Syntax ERROR: {e}")
    sys.exit(1)