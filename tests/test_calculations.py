import pytest
from app.calculation import add, subtract 



################################### Testing function example ##############################

# the test functions must start with "test_... or testing_..." to be recognized by pytest
# to run the tets type in terminal: "pytest" or "pytest -v" with extra info or "pytest -v -s" with showing the prints in test 
def test_add():
    print("testing add function")
    assert add(5, 3) == 8
    
# we can test our functions with mutiple parmaters using patest parametrize
@pytest.mark.parametrize("num1, num2, expected", 
                         [
                             (5, 2, 3),
                             (20, 8, 12),
                             (15, 5, 10)
                         ])
def test_subtract(num1, num2, expected):
    assert subtract(num1, num2) == expected
    
    
    
    
################################### Testing classes example ##############################    