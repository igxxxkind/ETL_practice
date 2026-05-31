import pytest
import greenhouse 
from datetime import date, timedelta
from pydantic import ValidationError
import importlib

importlib.reload(greenhouse)

@pytest.fixture
def default_NPK():
    return greenhouse.NPKRatio(n=10, k=1)

### Happy test cases

def nitro_test_value(default_NPK):
    assert default_NPK.n==10
    
def phos_test_value(default_NPK):
    assert default_NPK.k==1
    
def potas_test_value(default_NPK):
    assert default_NPK.k is None
    


### Sad test cases

def nitro_value():
    with pytest.raises(ValueError):
        greenhouse.NPKRatio(
            n=-100
        )
        
def potas_value():
    with pytest.raises(ValueError):
        greenhouse.NPKRatio(
            k=-100
        )

def phos_value():
    with pytest.raises(ValueError):
        greenhouse.NPKRatio(
            p=-100
        )

def nitro_type():
    with pytest.raises(ValidationError):
        greenhouse.NPKRatio(
            n='Some'
        )
        
def potas_type():
    with pytest.raises(ValidationError):
        greenhouse.NPKRatio(
            k='Some'
        )

def phos_type():
    with pytest.raises(ValidationError):
        greenhouse.NPKRatio(
            p='Some'
        )

def nitro_type_dict():
    with pytest.raises(TypeError):
        greenhouse.NPKRatio(
            {'n':1, 'p':1, 'k':1}
        )
        

# try:
#     greenhouse.NPKRatio(
#             {'n':1, 'p':1, 'k':1})
# except Exception as e:
#     print(type(e))

