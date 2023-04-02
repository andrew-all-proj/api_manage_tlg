import base64

def decode_base64(encoded_string: str) -> str:
    # Декодируем строку из формата Base64 и возвращаем декодированную строку
    decoded_bytes = base64.b64decode(encoded_string)
    return decoded_bytes.decode('utf-8')