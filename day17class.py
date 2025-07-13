class User:
    def __init__(self, user_id, username):
        print("new user being Created")
        self.id = user_id
        self.username = username
        self.followers = 0
        self.following = 0

    def follow(self, user):
        self.following += 1
        user.followers += 1

user_1 = User(user_id="901",username="angela")

user_2 = User(user_id="801",username="jack")

print(user_1.follow(user_2))

print(user_1.following)
print(user_1.followers)
print(user_2.following)
print(user_2.followers)
