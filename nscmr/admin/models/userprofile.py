from nscmr import db

# should i create manager classes or even classes representing the documents
# instead of this approach?
collection = db.users

def get_profile_by_email(user_email):
    profile = collection.find_one({ 'email': user_email })
    return profile
