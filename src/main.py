# Libraries and packages
from tkinter import *
from src.settings.settings_layout import settings_layout as sl  # colors and font in a dictionary
from src.translation.translation_deepl import *
from src.deep_learning_chatbot.chat import *
from src.content_and_answers.functionalities import *
from src.deep_learning_chatbot.nltk_utils import *
from src.content_and_answers.functionalities import launch_sudoku

# VARIABLES
############################################################################################################
chat_bot_name = "Fabrice"

# State variables to store, if needed, the topic of the previous question
is_meteo = False
is_horoscope = False
is_definition = False
is_sudoku = False
language_defined = False
language = None


############################################################################################################


# SEND FUNCTION
############################################################################################################
# We need to define here the "send" function as it refers to displayed Tkinter Objects.
# As we can only link one function to a button of our keyboard, everyhting needs to be in the send function.
# We can't break it in smaller piece. This is why there are some state variable, that are set to True if needed.

def send(event=None):  # event = None so that we can use the Enter button to send a message
    global is_meteo
    global is_horoscope
    global is_definition
    global is_sudoku
    global chat_bot_name
    global language_defined
    global language

    # We store the message from the user
    input = msg_entry.get()
    msg_to_send = "You : " + "\n" + input + "\n"
    chat_text_zone.insert(END, "\n" + msg_to_send)

    # Case of languages
    if input == 'fr' and language_defined == False:
        output = 'Parfait ! Que puis-je faire pour vous ?' + '\n' + "(Psss : essayez 'quelles sont tes fonctionnalités?')"
        msg_to_display = f"{chat_bot_name} : " + output
        chat_text_zone.insert(END, "\n" + msg_to_display)
        chat_text_zone.insert(END, "\n")
        language = input
        language_defined = True

    elif input == 'en' and language_defined == False:
        output = "Perfect ! Let's stay in english then." + '\n' + "To know what I am capable of, write 'What are your functionalities?'"
        msg_to_display = f"{chat_bot_name} : " + output
        chat_text_zone.insert(END, "\n" + msg_to_display)
        chat_text_zone.insert(END, "\n")
        language = input
        language_defined = True

    elif language_defined == False:
        output = "Fantastic ! I am always glad to talk another language. How can I help you ? "
        language = input
        translated_output = translate_to_user_language(output, language)
        msg_to_display = f"{chat_bot_name} : " + translated_output
        chat_text_zone.insert(END, "\n" + msg_to_display)
        chat_text_zone.insert(END, "\n")

        language_defined = True


    elif is_meteo == True and language_defined == True:
        # We don't translate into french the name of the city
        output = get_meteo(input)  # the input here is the city given by the user
        translated_output = translate_to_user_language(output, language)
        chat_text_zone.insert(END, "\n" + f"{chat_bot_name} : " + "\n" + translated_output + "\n")
        chat_text_zone.insert(END, "\n" + f"{chat_bot_name} : " + "\n" + translate_to_user_language(
            "Avez-vous besoin d autre chose ?", language) + "\n")
        is_meteo = False

    elif is_horoscope == True and language_defined == True:
        # We need to translate the input into French
        translated_intput = translate_to_french(input)
        output = get_horoscope(translated_intput)
        translated_output = translate_to_user_language(output, language)
        chat_text_zone.insert(END, "\n" + f"{chat_bot_name} : " + "\n" + translated_output + "\n")
        chat_text_zone.insert(END, "\n" + f"{chat_bot_name} : " + "\n" + translate_to_user_language(
            "Avez-vous besoin d autre chose ?", language) + "\n")
        is_horoscope = False

    elif is_sudoku == True and language_defined == True:
        game = launch_sudoku(input)
        game.start()
        SudokuUI(new_window, game)
        new_window.geometry("%dx%d" % (WIDTH, HEIGHT + 40))
        # We need to translate the input into French

        chat_text_zone.insert(END, "\n" + f"{chat_bot_name} : " + "\n" + translate_to_user_language(
            "Avez-vous besoin d autre chose ?", language) + "\n")
        is_sudoku = False

    elif is_definition == True and language_defined == True:
        # We need to translate the input into French
        translated_intput = translate_to_french(input)
        output = get_definition(translated_intput)
        translated_output = translate_to_user_language(output, language)
        chat_text_zone.insert(END, "\n" + f"{chat_bot_name} : " + "\n" + translated_output + "\n")
        chat_text_zone.insert(END, "\n" + f"{chat_bot_name} : " + "\n" + translate_to_user_language(
            "Avez-vous besoin d autre chose ?", language) + "\n")
        is_definition = False

    else:
        # To get the intent, we need to translate the message of the user in French
        translated_intput = translate_to_french(input)
        input_without_accent = delete_accent(translated_intput)

        tag = get_intent(input_without_accent, language)  # on récupère le tag prédominant
        print(tag)

        if tag == "meteo":  # The website is in French, so we need to translate
            is_meteo = True
            output = "De quelle ville souhaitez-vous connaître la météo ? "
            translated_output = translate_to_user_language(output, language)

        elif tag == "horoscope":  # The website is in French, so we need to translate
            is_horoscope = True
            output = "Pouvez-vous me rappeler votre signe astrologique svp (ex : cancer)? "
            translated_output = translate_to_user_language(output, language)

        elif tag == "dictionary":  # The website is in French, so we need to translate
            is_definition = True
            output = "Pouvez-vous m'indiquer le mot dont vous souhaiteriez connaitre la définition svp ? (ex : diplodocus) "
            translated_output = translate_to_user_language(output, language)

        elif tag == "sudoku":  # The website is in French, so we need to translate
            is_sudoku = True
            output = "Choisissez le niveau de votre grille de Sudoku (n00b ou l33t): "
            translated_output = translate_to_user_language(output, language)

        elif tag == 'joke':  # The website is in French, so we need to translate
            output = get_joke()
            translated_output = translate_to_user_language(output, language)

        elif tag == "error":
            output = "Désolé, je ne comprends pas... Pouvez-vous réessayer ?  "
            translated_output = translate_to_user_language(output, language)

        else:  # We only need to translate if the language isn't French nor English
            output = get_deep_bot_answer(tag, language)
            translated_output = translate_to_user_language(output, language)

        msg_to_display = f"{chat_bot_name} : " + "\n" + translated_output + "\n"
        chat_text_zone.insert(END, "\n" + msg_to_display)
        chat_text_zone.insert(END, "\n")

    msg_entry.delete(0, END)  # the text inside the message entry box is deleted every time we send it


# DISPLAYING TKINTER OBJECTS
############################################################################################################

# Set the window
window = Tk()  # Top level widget
window.title(f"{chat_bot_name} for your service !")
window.resizable(width=False, height=False)  # Don't resize the main window of the chatbot
window.configure(width=400, height=600, bg=sl["gray_color"])  # Size of the widget and background color

# Set the header
header = Label(window, bg=sl["red_color"], fg=sl["text_color"],  # Color background and title color
               text="Welcome on the interface of the Chatbot !", font=sl["font_bold"],
               pady=7)  # Title, font and position of the title on the y-axis
header.place(relwidth=1)

# Set the divider between header and chat_text
divider = Label(window, width=200, bg=sl["medium_gray_color"])  # Width and color of the divider
divider.place(relwidth=1, rely=0.06,
              relheight=0.005)  # Place of the line : alignment (middle), position on y axis and height

# Set the frame
frame = Frame(window)
frame.place(relwidth=1, relheight=1, rely=0.065)  # Relative place of the chat_text

# Set the scrollbar
scrollbar = Scrollbar(frame)
scrollbar.pack(side="right", fill="y")

# Set the chat_text_zone
chat_text_zone = Text(frame, padx=3, pady=3, width=200, height=37, yscrollcommand=scrollbar.set)  # Font and position
# Displays the text
chat_text_zone.pack()

# Association of the scrollbar to the text
scrollbar.config(command=chat_text_zone.yview)

# Set the top bottom
top_bottom = Label(window, height=65)
top_bottom.place(relwidth=1, rely=0.89)

# Set the bottom bottom
bottom_bottom = Label(window, height=65)
bottom_bottom.place(relwidth=1, rely=0.945)

# Set the message entry box
msg_entry = Entry(top_bottom, fg=sl["text_color"], font=sl["font"])
msg_entry.place(relwidth=1, relheight=0.030, rely=0.0005, relx=0)

# END OF DISPLAYING
##############################################################################################################

# SENDING THE RIGHT ANSWER
##############################################################################################################

# We need to store the language used by the user
chat_text_zone.insert(END, f"{chat_bot_name} : " + "\n" + "Hi there ! I'm glad to help you. " + "\n")
chat_text_zone.insert(END,
                      "\n" + "Before going further, can you tell me which language you would like to talk with me ?" + "\n")
chat_text_zone.insert(END, "\n" + "(Simply write the international code please (ex : fr, en, de, ru,it, es...)")

# Sends the message thanks to the send function if "Return" is pressed
msg_entry.bind("<Return>", send)

# Displays the button "Send"
Button(bottom_bottom, text="Send", command=send).pack(side=RIGHT)

#########Sudoku second frame

# root = Tk()
new_window = Toplevel(window)

window.mainloop()
