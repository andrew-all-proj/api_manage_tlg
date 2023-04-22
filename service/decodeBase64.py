import base64


def decode_base64(encoded_string: str) -> str:
    # Декодируем строку из формата Base64 и возвращаем декодированную строку
    try:
        res = base64.b64decode(encoded_string).decode('utf-8')
    except Exception as ex:
        print(ex)
        return ""
    return res
