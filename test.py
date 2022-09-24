from fastapi import status

my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1},
    {"title": "favorite foods", "content": "I like pizza!", "id": 2}]

slownik = {"data": my_posts}

print(slownik)


print(my_posts)


for p in my_posts:
    print(p["id"])


for i, p in enumerate(my_posts):
    print(i)
    print(p)


print(dir(status))