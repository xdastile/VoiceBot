import json
import random

#Get recent messages
def get_recent_messages():
    
    #define the file name and learn instructions
    file_name="stored_data.json"

    learn_instruction={
        "role": "system",
        "content": "You are an assistant for public transport users in Mexico CDMX. Reply with short answers that are relevant to public transport use in CDMX in Mexico.\
            You may answer questions about points of interest in CDMX, important information around transportation, the weather in CDMX, and any other interesting iformation about CDMX. \
                Your name is Rachel. The user is called Xolani. Keep your answers to under 30 words.",

    }


    #Initialize messages
    messages=[]

    #Add a random element
    x=random.uniform(0, 1)

    if x<0.5:
        learn_instruction["content"]=learn_instruction["content"] + "Your response will return some dry humour."

    else:
        learn_instruction["content"]=learn_instruction["content"] + "Your response will return some rather a challenging question."

    #Append instruction to messages
    messages.append(learn_instruction)

    #Get last messages
    try:
        with open(file_name, "r") as user_file:
            data=json.load(user_file)

            #Append the last 5 items of data
            if data:
                if len(data) < 5:
                    for item in data:
                        messages.append(item)
                else:
                    for item in data[-5:]:
                        messages.append(item)

    except Exception as e:
        print(e)
        pass


    #Return messages
    return messages

#Store messages
def store_messages(request_message, response_message):
    #define the file name
    file_name="stored_data.json"

    #Get recent messages
    messages=get_recent_messages()[1:]

    #Add messages to data
    user_message={"role": "user", "content": request_message}
    assistant_message={"role": "assistant", "content": response_message}
    messages.append(user_message)
    messages.append(assistant_message)

    #save the updated file
    with open(file_name, "w") as f:
        json.dump(messages, f)


#reset messages
def reset_messages():
    #soverwrite current file with othing
    open("stored_data.json", "w")
