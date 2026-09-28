def generate_range(min_value,max_value):
    number_of_points = 5

    step = (max_value - min_value) / (number_of_points - 1)

    values = []

    for i in range(number_of_points):
        value  = min_value + i * step
        values.append(value)
    return values





min_payload = float(input('Enter minimum payload: '))
max_payload = float(input('Enter maximum payload: '))

payloads = generate_range(min_payload,max_payload)



print('Payload values: ')
print(payloads)