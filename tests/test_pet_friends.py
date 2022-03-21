from api import PetFriends
from settings import valid_email, valid_password
import os

pf = PetFriends()

def test_get_api_key_for_valid_user(email = valid_email, password = valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result

def test_get_all_pets_with_valid_key(filter=''):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0

def test_add_new_pet_with_valid_data(name='Пёс', animal_type='Немецкая овчарка',
                                         age='4', pet_photo= r'images\b91731ed3e87ecaaf1fa09df1c509743.jpg'):
    "Проверяем запрос на добавление питомца"

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 200
    assert result['name'] == name

def test_successful_delete_self_pet():
    "Проверяем запрос на удаление питомца"

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Nicky", "Кот", "3", r'images\675d28c04794e3c683f4419536c4c15f_L.jpg')
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    assert status == 200
    assert pet_id not in my_pets.values()


def test_successful_update_self_pet_info(name='Spirit', animal_type='Собака', age=4):
    "Проверяем запрос на обновление питомца"

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        assert status == 200
        assert result['name'] == name
    else:
        raise Exception("There is no my pets")

def test_add_new_pet_1(name='Gray', animal_type='Dog', age='5'):
    "Проверяем запрос на добавление питомца бех фото"

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    assert status == 200
    assert result['name'] == name

def test_add_new_pet_1_1(pet_photo = r'images\76.jpg'):
    "Проверяем запрос на добавление фото питомца"

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    pet_id = my_pets['pets'][0]['id']
    status = pf.update_pet_photo(auth_key, pet_id, pet_photo)

    assert status == 200

def test_add_new_pet_mistake(name='Micky', animal_type='Терьер',
                                         age='-5', pet_photo= r'images\18.jpg'):
    "Проверяем ошибку при указании отрицательного возраста"

    if age < "0":
        raise Exception("Age < 0. It's a mistake")

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 200
    assert result['name'] == name

def test_add_new_pet_mistake_2(name='', animal_type='Терьер',
                                         age='9', pet_photo= r'images\18.jpg'):
    "Проверяем ошибку при неправильном указании имени"

    if name == '':
        raise Exception("There's no name. It's a mistake")

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 200
    assert result['name'] == name

def test_add_new_pet_mistake_3(name='Dakky', animal_type='Терьер',
                                         age='', pet_photo= r'images\18.jpg'):
    "Проверяем ошибку при неправильном указании возраста"

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    if age == '':
        raise Exception("There's no age. It's a mistake")
    else:
        assert status == 200
        assert result['name'] == name

def test_add_new_pet_mistake_4(name='Dakky', animal_type='',
                                         age='7', pet_photo= r'images\18.jpg'):
    "Проверяем ошибку при неправильном указании типа животного"

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    if animal_type == '':
        raise Exception("There's no animal_type. It's a mistake")
    else:
        assert status == 200
        assert result['name'] == name

def test_add_new_pet_mistake_5(name='Kery', animal_type='Turtle',
                                         age='7', pet_photo= ''):
    "Проверяем ошибку при отсутствии фото при добовлении питомца"

    if pet_photo == '':
        raise Exception("There's no pet_photo. It's a mistake")

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 200
    assert result['name'] == name

def test_add_new_pet_mistake_6(name='Kery', animal_type='Turtle',
                                         age='7', pet_photo= r'image\57'):
    "Проверяем ошибку при неправильном указании фото"

    if FileNotFoundError:
        raise Exception("There's mistake in pet_photo")

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 200
    assert result['name'] == name

def test_successful_delete_self_pet_pet_id_3():
    "Проверяем удаление питомца не первого по счёту"

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Nicky", "Кот", "3", r'images\675d28c04794e3c683f4419536c4c15f_L.jpg')
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    pet_id = my_pets['pets'][4]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    assert status == 200
    assert pet_id not in my_pets.values()

def test_successful_update_self_pet_info_2(name='Lucky', animal_type='Собака', age=5):
    "Проверяем обновление питомца не первого по счёту"

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][4]['id'], name, animal_type, age)

        assert status == 200
        assert result['name'] == name
    else:
        raise Exception("There is no my pets")
