import pytest
import greenhouse 
from datetime import date, timedelta
from pydantic import ValidationError
import importlib

importlib.reload(greenhouse)

@pytest.fixture
def default_fertilizer():
    return greenhouse.Fertilizer()

@pytest.fixture
def full_fertilizer():
    return greenhouse.Fertilizer(name = 'abc', 
                                 type = 'liquid',
                                 NPK_ratio=greenhouse.NPKRatio(n=1,p=1,k=1),
                                 application_method='Water Solution',
                                 application_frequency=greenhouse.Schedule.MONTHLY)

# happy test cases

def test_name_none(default_fertilizer):
    assert default_fertilizer.name is None
    
def test_name_str(full_fertilizer):
    assert isinstance(full_fertilizer.name, str)
    
def test_name_str_2(full_fertilizer):
    assert full_fertilizer.name == 'abc'
    
def test_type_none(default_fertilizer):
    assert default_fertilizer.type is None
    
def test_type_str(full_fertilizer):
    assert isinstance(full_fertilizer.type, str)
    
def test_type_str_2(full_fertilizer):
    assert full_fertilizer.type == 'liquid'

def test_application_method_none(default_fertilizer):
    assert default_fertilizer.application_method is None
    
def test_application_method_str(full_fertilizer):
    assert isinstance(full_fertilizer.application_method, str)
    
def test_application_method_str_2(full_fertilizer):
    assert full_fertilizer.application_method == 'Water Solution'

    



    

