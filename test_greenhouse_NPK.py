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

def test_nitro_value(default_NPK):
    assert default_NPK.n==10
    
def test_phos_value(default_NPK):
    assert default_NPK.p is None
    
def test_potas_value(default_NPK):
    assert default_NPK.k==1
    
def test_k_type(default_NPK):
    assert isinstance(default_NPK.k, float)
    
def test_p_type(default_NPK):
    assert isinstance(default_NPK.p,type(None))


### Sad test cases

def test_nitro_negative():
    with pytest.raises(ValueError):
        greenhouse.NPKRatio(
            n=-100
        )
        
def test_potas_negative():
    with pytest.raises(ValueError):
        greenhouse.NPKRatio(
            k=-100
        )

def test_phos_negative():
    with pytest.raises(ValueError):
        greenhouse.NPKRatio(
            p=-100
        )

def test_nitro_type():
    with pytest.raises(ValidationError):
        greenhouse.NPKRatio(
            n='Some'
        )
        
def test_potas_type():
    with pytest.raises(ValidationError):
        greenhouse.NPKRatio(
            k='Some'
        )

def test_phos_type():
    with pytest.raises(ValidationError):
        greenhouse.NPKRatio(
            p='Some'
        )

def test_date_type():
    with pytest.raises(ValidationError):
        greenhouse.NPKRatio(
            p=date.today()
        )

def test_nitro_type_dict():
    with pytest.raises(TypeError):
        greenhouse.NPKRatio(
            {'n':1, 'p':1, 'k':1}
        )
        

# try:
#     greenhouse.NPKRatio(
#             {'n':1, 'p':1, 'k':1})
# except Exception as e:
#     print(type(e))

