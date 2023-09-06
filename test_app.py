# test_app.py
import pytest
import json

@pytest.fixture(scope='module')
def client():
    from app import app
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_render_with_simple_fields(client):
    data = {"wound assessment": "monthly comprehensive assessments"}
    response = client.post('/', json=data)
    assert response.status_code == 200

    html_output = response.data.decode('utf-8') 

    html_unparsed = html_output.replace(' ', '').replace('\n', '').lower().strip()

    # debug lineee
    print(html_unparsed) 

    assert "woundassessment" in html_unparsed

# Test for simple flat object
def test_render_with_flat_object(client):
    data = {"name": "John", "age": 30, "city": "New York"}
    response = client.post('/', json=data)
    assert response.status_code == 200
    html_unparsed = response.data.decode('utf-8').replace(' ', '').replace('\n', '').lower().strip()
    assert all(x.lower() in html_unparsed for x in data.keys())

# Test for nested objects
def test_render_with_nested_objects(client):
    data = {
        "person": {
            "name": "John",
            "age": 30,
            "address": {
                "city": "New York",
                "zip": "10001"
            }
        }
    }
    response = client.post('/', json=data)
    assert response.status_code == 200
    html_unparsed = response.data.decode('utf-8').replace(' ', '').replace('\n', '').lower().strip()
    keys = ['person', 'name', 'age', 'address', 'city', 'zip']
    assert all(x.lower() in html_unparsed for x in keys)

# Test for nested arrays
def test_render_with_nested_arrays(client):
    data = {
        "fruits": ["apple", "banana", "cherry"],
        "vegetables": ["carrot", "lettuce"]
    }
    response = client.post('/', json=data)
    assert response.status_code == 200
    html_unparsed = response.data.decode('utf-8').replace(' ', '').replace('\n', '').lower().strip()
    assert "fruits" in html_unparsed and "vegetables" in html_unparsed

# Test for complex nested objects and arrays
def test_render_with_complex_nesting(client):
    data = {
        "person": {
            "name": "John",
            "hobbies": ["reading", "swimming"],
            "pets": [
                {
                    "type": "dog",
                    "name": "Rex"
                },
                {
                    "type": "fish",
                    "name": "Goldie"
                }
            ]
        }
    }
    response = client.post('/', json=data)
    assert response.status_code == 200
    html_unparsed = response.data.decode('utf-8').replace(' ', '').replace('\n', '').lower().strip()
    keys = ['person', 'name', 'hobbies', 'reading', 'swimming', 'pets', 'type', 'dog', 'fish', 'name', 'rex', 'goldie']
    assert all(x.lower() in html_unparsed for x in keys)

# Test for data types (boolean, null, integer)
def test_render_with_data_types(client):
    data = {
        "isActive": True,
        "isMarried": False,
        "children": None,
        "numberOfCars": 2
    }
    response = client.post('/', json=data)
    assert response.status_code == 200
    html_unparsed = response.data.decode('utf-8').replace(' ', '').replace('\n', '').lower().strip()
    keys = ['isActive', 'isMarried', 'children', 'numberOfCars']
    assert all(x.lower() in html_unparsed for x in keys)

# Test for single string
def test_render_with_single_string(client):
    data = "wound assessment"
    response = client.post('/', json=data)
    assert response.status_code == 200
    html_unparsed = response.data.decode('utf-8').replace(' ', '').replace('\n', '').lower().strip()
    assert "woundassessment" in html_unparsed

# Test for deeply nested objects and arrays
def test_render_with_deep_nesting(client):
    data = {
        "wound assessment and treatment": {
            "wound assessment": "monthly comprehensive assessments",
            "wound and skin care treatment": {
                "procedures and therapies": {
                    "procedure record entry": [
                        {
                            "procedure": [
                                {
                                    "free text": "three times weekly",
                                    "coded value": "36777000 | Debridement (procedure) |\nDebridement\nDebridement (procedure)\nRemoval of devitalized tissue\nRemoval of devitalised tissue\n",
                                },
                                {
                                    "coded value": "36777000 | Debridement (procedure) |\nDebridement\nDebridement (procedure)\nRemoval of devitalized tissue\nRemoval of devitalised tissue\n",
                                    "free text": "Leg elevation"
                                },
                                "Physical activity",
                                "Diet"
                            ]
                        }
                    ]
                }
            }
        }
    }
    response = client.post('/', json=data)
    assert response.status_code == 200
    html_unparsed = response.data.decode('utf-8').replace(' ', '').replace('\n', '').lower().strip()
    keys = [
        'woundassessmentandtreatment', 'woundassessment', 'monthlycomprehensiveassessments', 
        'woundandskincaretreatment', 'proceduresandtherapies', 'procedurerecordentry',
        'procedure', 'freetext', 'threetimesweekly', 'codedvalue',
        'legelevation',
        'physicalactivity', 'diet'
    ]
    assert all(x.lower() in html_unparsed for x in keys)
    # need to add the other keys in to make sure that it works properly

