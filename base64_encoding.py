import base64

def encode_body(message):
    message_bytes = message.encode('ascii')
    print(message_bytes)
    base64_bytes = base64.b64encode(message_bytes)
    print(base64_bytes)
    base64_message = base64_bytes.decode('ascii')
    print(base64_message)
    return base64_message

def decode_body(message):
    base64_bytes = message.encode('ascii')
    message_bytes = base64.b64decode(base64_bytes)
    decoded_data = message_bytes.decode('ascii')
    return decoded_data

def decode_utf(message):
    decoded_data = message.decode('utf-8')
    return decoded_data

data = encode_body("{ username: 'mandar3', password: 'mandar3' }")
print('Bearer', data)

decoded_data = decode_body(data)
print('Decoded data', decoded_data)