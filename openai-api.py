import openai

# Set up your OpenAI API credentials
openai.api_key = "OPEN_AI_KEY"

# Set up the OpenAI completion API parameters
model_engine = "text-davinci-003"
temperature = 0.8
max_tokens = 2000


# Start the conversation loop
def main_chat_method():
    prompt = generate_prompt("Jennifer")
    customer_ai_conversation = ""
    while True:
        # Get user input
        user_input = input("> ")

        # Concatenate the user input and the prompt
        prompt += "\nCustomer: " + user_input
        customer_ai_conversation += "\nCustomer: " + user_input

        # Send the prompt to the OpenAI API for completion
        response = openai.Completion.create(
            engine=model_engine,
            prompt=prompt,
            temperature=temperature,
            max_tokens=max_tokens,
            n=1,
            stop=[" Customer:", " AI:"],
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0.6
        )

        # Extract the chatbot's response from the API response
        chatbot_response = response.choices[0].text.strip()

        # Print the chatbot's response
        print(chatbot_response)

        # Concatenate the chatbot's response to the prompt for the next iteration
        prompt += "\n" + chatbot_response
        customer_ai_conversation += "\n" + chatbot_response

        # if customer's intention is to finish the sentence, the loop then breaks
        if stop_the_conversation(user_input):
            break
    # classy the customer
    customer_classification(customer_ai_conversation)


def stop_the_conversation(sentence):
    prompt = """Given a customer's sentence, classify the sentiment as either wanting to end the conversation or wanting 
    to continue it. If the sentiment is to end the conversation, respond with "Yes". If the sentiment is to continue the 
    conversation, respond with "No".

Customer: "I think I have enough information for now. Thank you for your help."
Answer: Yes
Customer: {}
Answer:""".format(sentence)
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        temperature=0.1,
        max_tokens=60,
        n=1,
        stop=None,
        frequency_penalty=0,
        presence_penalty=0
    )
    api_response = response.choices[0].text.strip()
    # print("Sentence: " + sentence)
    # print("Finish: " + api_response.lower())
    if api_response.lower() == "yes":
        return True
    else:
        return False


def customer_classification(conversation):
    prompt = """Decide the lead's intention to buy the product based on the Customer's response. Choose the category of 
    the customer's intention, whether they are hot lead, warm lead, or cold lead. 

{}
 
The Customer is: """.format(conversation)
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        temperature=0,
        max_tokens=60,
        n=1,
        stop=None,
        frequency_penalty=0,
        presence_penalty=0
    )
    print("\n")
    print(response.choices[0].text.strip())


def generate_prompt(person_name):
    return """AI that can talk to the customers with the whose name is {} in a polite way.

Example:
AI: Hello {}, how can I help you today?
Customer: Hello, I would like to know a bit about your company?
AI: Sure, our company has a large offices among the globe. We have almost 3000 employees working everyday to meet the expectations of our customers.
Customer: Great. I would love to see the price list you would provide me with one.
AI: Sure, .......
Customer: ........
AI: ........ 
""".format(person_name.capitalize(), person_name.capitalize())


if __name__ == '__main__':
    print(generate_prompt("Jeni"))
    print("---------------------------------------")
    main_chat_method()

