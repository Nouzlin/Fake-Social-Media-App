__author__ = 'Linus'
import routes

ENCODER = 1000000

def encrypt_val(group_id, person_id):
    encoded_group = int(group_id) * int(ENCODER)
    value = int(int(encoded_group) + int(person_id))
    url = routes.su.encode_url(value)
    return url

def decrypt_val(cipher_text):
    data = routes.su.decode_url(cipher_text)
    person_id = data % ENCODER
    group_id = (data - person_id) / ENCODER
    return dict(person_id=person_id, group_id=group_id)