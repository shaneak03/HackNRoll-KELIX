from src.utils.supabase_client import supabase

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