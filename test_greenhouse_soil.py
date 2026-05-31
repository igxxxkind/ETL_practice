import pytest
import greenhouse 
from datetime import date, timedelta
from pydantic import ValidationError


@pytest.fixture
def default_soil():
    return greenhouse.Soil(ph_level=6.5)
### Happy test cases


def test_soil_ph(default_soil):
    assert default_soil.ph_level == 6.5
    
def test_soil_fertilizers(default_soil):
    assert default_soil.applied_fertilizers is None
    
def test_default_soil_type(default_soil):
    assert default_soil.soil_type == greenhouse.SoilType.NORMAL

def test_default_drainage_type(default_soil):
    assert default_soil.drainage_type== greenhouse.DrainageType.KERAMZYT
    
def test_default_moisture_level(default_soil):
    assert default_soil.moisture_level == greenhouse.MoistureLevel.MODERATE


### Sad test cases

def test_soil_ph_negative():
    with pytest.raises(ValidationError):
        greenhouse.Soil(
            ph_level=-1
        )
        
def test_soil_ph_too_large():
    with pytest.raises(ValidationError):
        greenhouse.Soil(
            ph_level=15
        )

def test_soil_ph_type():
    with pytest.raises(TypeError):
        greenhouse.Soil(
            ph_level="Acidic"
        )

# the idea is to ensure the default behavior of the relevant classes.      
# try:
#     greenhouse.Soil(drainage_type='None')
# except Exception as e:
#     print(type(e))
  
def test_invalid_soil_value():
    with pytest.raises(ValidationError):
        greenhouse.Soil(soil_type='Sand')

def test_invalid_soil_type():
    with pytest.raises(ValidationError):
        greenhouse.Soil(soil_type=123)

def test_invaluid_drainage_value_none():
    with pytest.raises(ValidationError):
        greenhouse.Soil(drainage_type=None)
        
def test_invaluid_drainage_value():
    with pytest.raises(ValidationError):
        greenhouse.Soil(drainage_type='None')
 
def test_invalid_drainage_type():
    with pytest.raises(ValidationError):
        greenhouse.Soil(drainage_type=123)

def test_invalid_applied_fertilizers():
    with pytest.raises(ValidationError):
        greenhouse.Soil(applied_fertilizers='None')

def test_invalid_applied_fertilizers_type():
    with pytest.raises(ValidationError):
        greenhouse.Soil(applied_fertilizers=500)
