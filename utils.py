from telegram import InlineKeyboardButton

def splitArr(arr, size):
    arrs = []
    while len(arr) > size:
        pice = arr[:size]
        arrs.append(pice)
        arr = arr[size:]
    arrs.append(arr)
    return arrs

def fillKeyboard(dict):
    result = []
    for key, value in dict.items():
        result.append(InlineKeyboardButton(key, callback_data=value))

    return splitArr(result, 2)