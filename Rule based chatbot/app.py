from flask import Flask, request, render_template,jsonify

app = Flask(__name__)
import random
import re

class Chatbot:
    negative_responses = ("no", "nope", "sorry")
    exit_commands = ("quit", "exit", "close", "bye")
    random_questions = ("any other queries?\n",
                        
                        "feel free to ask other questions\n",
                        "i am here to help\n"
                        )

    def __init__(self):
        self.name = None
        self.asked_for_name = False
        
        self.biblo = {'describe_provided_services': r'.*\bservices\b.*',
                  'answer_prices': r'.*\bprices\b.*',
                  'area_loc': r'.*\blocation\b.*'
                  }

    def greet(self):
        if not self.asked_for_name:
            self.asked_for_name = True
            print("Hi! I am here to help you.")
        else:
            self.name = input("What is your name? ").capitalize()

        will_help = input(f"Hello, {self.name}! Do you want to know about our services, prices, or location?\n").lower()

        if will_help in self.negative_responses:
            print("Okay, feel free to ask if you have any questions. Have a great day!")
            return
        self.chat()

    def ext(self, reply):
        for command in self.exit_commands:
            if reply == command:
                print("Goodbye, {}. Have a great day!".format(self.name))
                return True

    def chat(self):
        print("Feel free to ask questions about our services, pricing, or location.")
        while True:
            reply = input(random.choice(Chatbot.random_questions)).lower()

            if self.ext(reply):
                break
            response = self.match_reply(reply)
            print(response)

    def match_reply(self, reply):
        for key, value in self.biblo.items():
            intent = key
            regex_pattern = value
            found_match = re.match(regex_pattern, reply)
            if found_match and intent == 'describe_provided_services':
                return self.describe()
            elif found_match and intent == 'answer_prices':
                return self.price()
            elif found_match and intent == 'area_loc':
                return self.area()
        if not found_match:
            return self.no_match_intent()

    def describe(self):
        return "We provide a variety of services to cater to your needs."

    def price(self):
        return "For detailed pricing information, please contact us at info@example.com."

    def area(self):
        return "We are located at xyz."

    def no_match_intent(self):
        return "I'm sorry, I don't understand that. Can you please rephrase your question?"

chatbot_instance = Chatbot()
@app.route('/')
def index():
    
    return render_template('index.html')

@app.route('/process_chat', methods=['POST'])
def process_chat():
    global chatbot_instance
    
    if chatbot_instance.name is None:
        user_input = request.form['user_input'].capitalize()
        chatbot_instance.name = user_input
        response = {
            "message": f"Hi {user_input}! How can I assist you today?",
            "is_name_prompt": False,  # Set is_name_prompt to False after getting the user's name
            "is_initial_prompt": False  # Set is_initial_prompt to False as the initial prompt is over
        }
    else:
        user_input = request.form['user_input']
        if any(exit_command in user_input.lower() for exit_command in Chatbot.exit_commands):
            response = {
                "message": f"Goodbye, {chatbot_instance.name}! Have a great day!",
                "is_name_prompt": False,  # Set is_name_prompt to False if the user is exiting the chat
                "is_initial_prompt": False
            }
            chatbot_instance.name = None  # Reset the name for the next conversation
        else:
            response = {
                "message": chatbot_instance.match_reply(user_input),
                "is_name_prompt": False,  # Set is_name_prompt to False if the user has already provided their name
                "is_initial_prompt": False
            }

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)

