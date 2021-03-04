import os
print(os.path.abspath(__file__))
test_dir = os.path.dirname(os.path.abspath(__file__))
print(os.path.dirname(test_dir))