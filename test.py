from datetime import timedelta, datetime
from faker import Faker
import random
from transliterate import translit
# print(translit('Привет455', reversed=True))
from werkzeug.security import generate_password_hash, check_password_hash
fake = Faker('ru_Ru')


# date = fake.year(start_date='-')
# date = fake.date_time_between(start_date="-3d").replace(second=0)
# date2 = fake.date_time_between(start_date=date, end_date=date+timedelta(hours=2))
# print(date)
# print(date)
# print(date2)
# for _ in range(10):
#     a = random.randint(0 ,2)
#     print(f"a= {a}")

# a = {"n": True, 'm': False}
# print(a['n'])
# a= {"1":[4,5,6],
#     "2":[7,7,8],
#     "3":[11,34,56]
#     }
# b= a["1"]

# for i in b:
#     print(i)
# print("-"*50)
# for item in a:
#     print(f"item = {item}")
#     for number in a[item]:
#         print(number)
# a = random.randint(10, 5000)
# b = random.randint(int(a/10), int(a/2)) *100
# a = a*100
# print(f"price = {a}, step = {b}")

# a = generate_password_hash("1q2w3e4r5t6y7u8i")
# b = generate_password_hash("1q2w3e4r5t6y7u8i")
# check = check_password_hash(a, b)
# print(check)
print(int(1.1))