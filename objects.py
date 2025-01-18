from src.utils.supabase_client import supabase
import json

class Users:
    def __init__(self, id, name, q1, q2, q3, q4, q5, q1_ans, q2_ans, q3_ans, q4_ans, q5_ans):
        self.id = id
        self.name = name
        self.q1 = q1
        self.q2 = q2
        self.q3 = q3
        self.q4 = q4
        self.q5 = q5
        self.q1_ans = q1_ans
        self.q2_ans = q2_ans
        self.q3_ans = q3_ans
        self.q4_ans = q4_ans
        self.q5_ans = q5_ans

    def create_user_in_db(self):
        # Check if the user already exists in the database
        user_ans = supabase.table('User').select('id').eq('id', self.id).execute()
        if user_ans.data:
            print(f"User with ID {self.id} already exists.")
        else:
            supabase.table('User').insert([
                {
                    'id': self.id,
                    'name': self.name,
                    'q1': self.q1,
                    'q2': self.q2,
                    'q3': self.q3,
                    'q4': self.q4,
                    'q5': self.q5,
                    'q1_ans': self.q1_ans,
                    'q2_ans': self.q2_ans,
                    'q3_ans': self.q3_ans,
                    'q4_ans': self.q4_ans,
                    'q5_ans': self.q5_ans
                }
            ]).execute()
            print(f"User with ID {self.id} created.")

    def update_user_in_db(self):
        supabase.table('User').update([
            {
                'id': self.id,
                'name': self.name,
                'q1': self.q1,
                'q2': self.q2,
                'q3': self.q3,
                'q4': self.q4,
                'q5': self.q5,
                'q1_ans': self.q1_ans,
                'q2_ans': self.q2_ans,
                'q3_ans': self.q3_ans,
                'q4_ans': self.q4_ans,
                'q5_ans': self.q5_ans
            }
        ]).eq('id', self.id).execute()

questions = ["What ingredient do you judge a person for the most when ordered at mala?",
             "If you were a condiment, which one would you be, and why?",
             "What’s the weirdest thing you’ve eaten out of pure curiosity?",
             "How do you pick your seat in a group dinner setting?",
             "How do you feel about people who use 'lol' at the end of every sentence?",
             "If your personality were a type of weather, what would it be?",
             "What’s one movie you secretly hate but pretend to like because everyone else does?",
             "If you had to rank your friends by how they text, who’s at the top and why?",
             "If your browser tabs were a reflection of your brain, what would they reveal?",
             "What’s your most “out there” excuse for missing a deadline?",
             "What’s the one thing you always pack for trips but never actually use?",
             "If your dream home had to include one ridiculously unnecessary feature, what would it be?",
             "How do you feel about people who set 15 alarms to wake up in the morning?",
             "If animals could talk, which one would be the most annoying?",
             "What’s the first thing you’d do if you suddenly woke up as a chair?",
             "If you could delete one word from existence, what would it be and why?",
             "If someone says “We should hang out” but doesn’t plan it, are they lying?",
             "How do you feel about people who brag about getting 2 hours of sleep?",
             "If you woke up as a cat, what’s the first thing you’d do?",
             "Would you rather fight 100 duck-sized horses or one horse-sized duck?"]


class Responses:
    def __init__(self, name, question, answer):
        self.name = name
        self.question = question
        self.answer = answer

    def jsonify(self):
        return json.dumps({
            "name": self.name,
            "question": self.question,
            "answer": self.answer
        })

class Group:
    def __init__(self, grp_id):
        self.grp_id = grp_id
        self.members_id = []
        self.qns_and_ans = []

    def update_group_in_DB(self):
        # Check if the group exists in the database
        group_response = supabase.table('Groups').select('grp_id').eq('grp_id', self.grp_id).execute()
        if group_response.data:
            # Group exists, update the information
            supabase.table('Groups').update([
                {
                    'grp_id': self.grp_id,
                    'members_id': self.members_id,
                    'qns_and_ans': [response.jsonify() for response in self.qns_and_ans]
                }
            ]).eq('grp_id', self.grp_id).execute()
            print(f"Group with ID {self.grp_id} updated.")
        else:
            print(f"Group with ID {self.grp_id} does not exist, creating new grp in DB.")
            supabase.table('Groups').insert([
                {
                    'grp_id': self.grp_id,
                    'members_id': self.members_id,
                    'qns_and_ans': [response.jsonify() for response in self.qns_and_ans]
                }
            ]).execute()
            print(f"Group with ID {self.grp_id} created.")

    def pull_facts_from_db(self, user_id):
        print("Pulling usr info")
        user = supabase.table('User').select('*').eq('id', user_id).execute()
        print("user found to pull facts from")
        self.qns_and_ans.append(Responses(user.data[0]['name'], user.data[0]['q1'], user.data[0]['q1_ans']))
        self.qns_and_ans.append(Responses(user.data[0]['name'], user.data[0]['q2'], user.data[0]['q2_ans']))
        self.qns_and_ans.append(Responses(user.data[0]['name'], user.data[0]['q3'], user.data[0]['q3_ans']))
        self.qns_and_ans.append(Responses(user.data[0]['name'], user.data[0]['q4'], user.data[0]['q4_ans']))
        self.qns_and_ans.append(Responses(user.data[0]['name'], user.data[0]['q5'], user.data[0]['q5_ans']))

    def add_member(self, user_id):
        # Add to DB and pull qns and Ans
        self.members_id.append(user_id)
        self.pull_facts_from_db(user_id)
        self.update_group_in_DB()

    def pull_all_facts_for_group(self):
        self.qns_and_ans = []
        group_response = supabase.table('Groups').select('*').eq('grp_id', self.grp_id).execute()
        if group_response.data:
            group_data = group_response.data[0]
            if 'qns_and_ans' in group_data:
                self.qns_and_ans = group_data['qns_and_ans']
            else:
                print("No questions and answers found for the group.")
        else:
            print("Group not found.")

if __name__ == "__main__":
    g1 = Group("grp1")
    g1.add_member("test_id")
    g1.add_member("Test User2")
    print("g1 user created")

    g1.update_group_in_DB()
    print("g1 updated to db")

    g2 = Group("grp1")
    g2.pull_all_facts_for_group()
    print("g2 pulled from db")

    for facts in g2.qns_and_ans:
        print(facts)