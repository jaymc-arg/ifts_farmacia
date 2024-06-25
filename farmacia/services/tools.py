def convert_seconds(total_seconds):
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    return f"{hours:02}:{minutes:02}:{seconds:02}"

def convert_tuple_list(tuple_list):
    converted_list = []
    for item in tuple_list:
        if len(item) == 3:
            index, seconds1, seconds2 = item
            formatted_time1 = convert_seconds(seconds1)
            formatted_time2 = convert_seconds(seconds2)
            converted_list.append((index, formatted_time1, formatted_time2))
        elif len(item) == 2:
            index, seconds = item
            formatted_time = convert_seconds(seconds)
            converted_list.append((index, formatted_time))
    return converted_list