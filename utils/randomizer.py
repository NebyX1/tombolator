import random

def random_numbers(input_number):
    if input_number < 3 or input_number > 7:
        raise ValueError("El valor de 'input_number' debe estar entre 3 y 7.")

    generated_numbers = random.sample(range(0, 100), input_number)
    result = " - ".join(str(number) for number in generated_numbers)
    return result

input_number = 4  # Cambia este valor según la cantidad de números que deseas generar

print(random_numbers(input_number))