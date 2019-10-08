import random
from gtts import gTTS
from mpyg321.mpyg321 import MPyg321Player


class MyAudioPlayer(MPyg321Player):
    def __init__(self):
        super(MyAudioPlayer, self).__init__()
        self.free = True

    def onAnyStop(self):
        self.free = True


class MyTTS(gTTS):
    def __init__(self, txt, lng, sspeed):
        super(MyTTS, self).__init__(text=txt, lang=lng, slow=sspeed)
        self.GOOGLE_TTS_MAX_CHARS = 150


class Madlib:
    get_user_starters = ["I need a", "Give me a", "How about a", "Tell me a", "Now, think of a", "Now i need a"]
    get_user_enders = ["Awesome!", "Sweet!", "Amazing!", "I like where this is going!", "Great!", "Yippie!",
                       "Good one!", "Nice one!", "Your good at this!", "Your doing great!"]
    next_id = 1
    tts_obj = None
    tts_slow = False
    text_audio_player = None
    play_audio = False
    use_user_enders = True
    first_round = True
    ask_once = True
    current_madlib = None
    filenames = None

    def __init__(self, text_in):
        self.title = text_in[0]
        self.this_text = text_in[1]
        self.final_text = "poop"
        self.id = Madlib.get_an_id()

    @classmethod
    def get_an_id(cls):
        r = cls.next_id
        cls.next_id += 1
        return r

    def get_user_words(self):
        print("using madlib id:", self.id)
        self.final_text = self.this_text
        done = False
        index = 0
        vowels = ["a", "e", "i", "o", "u"]
        while not done:
            a_cursor = self.final_text.find("_", index)
            if a_cursor != -1:
                b_cursor = self.final_text.find("_", a_cursor+1)
            else:
                done = True
                continue
            if a_cursor != -1 and b_cursor != -1 and not done:
                this_word = self.final_text[a_cursor:b_cursor+1]
                stripped_word = this_word.strip("_")
                s_starter = random.choice(self.get_user_starters)
                s_starter += "n " if stripped_word[0] in vowels else " "
                r_prompt = s_starter + stripped_word + ": "
                r_input = ""
                if Madlib.play_audio is True:
                    Madlib.get_tts_audio(r_prompt)
                    Madlib.output_audio()
                    Madlib.wait_for_audio_to_finish()
                while r_input == "":
                    r_input = input(r_prompt)
                if r_input[0] in vowels and self.final_text[a_cursor-3:a_cursor] == " a ":
                    self.final_text = self.final_text[:a_cursor-1] + "n " + self.final_text[a_cursor:]
                self.final_text = self.final_text.replace(this_word, r_input, 1)
                index = a_cursor
                if Madlib.use_user_enders is True:
                    s_ender = random.choice(Madlib.get_user_enders)
                    if Madlib.play_audio is True:
                        Madlib.get_tts_audio(s_ender)
                        Madlib.output_audio()
                        Madlib.wait_for_audio_to_finish()
                    print(s_ender)

        if Madlib.play_audio is True:
            Madlib.get_tts_audio("Ok all done!")
            Madlib.output_audio()
            Madlib.wait_for_audio_to_finish()
        print("Ok all done!")

    @classmethod
    def output_audio(cls, filename="tts_output.mp3"):
        cls.wait_for_audio_to_finish()
        cls.text_audio_player.free = False
        cls.text_audio_player.play_song(filename)

    @classmethod
    def get_tts_audio(cls, text_to_say=None, lang="en", filename="tts_output.mp3"):
        if text_to_say is None:
            print("no text was given to get_tts_audio")
            return
        cls.tts_obj = MyTTS(text_to_say, lang, cls.tts_slow)
        cls.tts_obj.save(filename)

    @classmethod
    def wait_for_audio_to_finish(cls):
        if Madlib.play_audio is False:
            return
        while cls.text_audio_player.free is False:
            pass

    def print_final_text(self, get_fresh_audio=True):
        story_lines = self.final_text.splitlines()
        intro_text = "This madlib is called, " + self.title
        if Madlib.play_audio is True:
            Madlib.get_tts_audio(intro_text)
            Madlib.output_audio()
        print(intro_text)
        Madlib.wait_for_audio_to_finish()

        if get_fresh_audio is True:
            Madlib.filenames = []
        for i, sline in enumerate(story_lines):
            if self.play_audio is True:
                if i > 0:
                    Madlib.output_audio(Madlib.filenames[i - 1])
                current_name = "line{}.mp3".format(str(i).zfill(3))
                if get_fresh_audio is True:
                    Madlib.get_tts_audio(sline, filename=current_name)
                    Madlib.filenames.append(current_name)
                Madlib.wait_for_audio_to_finish()
            print(sline)
        if self.play_audio is True:
            Madlib.output_audio(Madlib.filenames[-1])
            Madlib.wait_for_audio_to_finish()
        if Madlib.first_round is True:
            Madlib.first_round = False


madlibtexts = [["A Typical Morning",
                "This morning I got up and washed my _noun_. Then my _noun_ and I went to _place_ for breakfast.\n"
               "It was a _adjective_ breakfast, although my eggs were a little too _adjective_."],
               ["A Vacation",
                "A vacation is when you take a trip to some _adjective_ place with your _adjective_ family.\n"
                "Usually you go to some place that is near a _noun_ or up on a _noun_.\n"
                "A good vacation place is one where you can ride _plural noun_ "
                "or play _game_ or go hunting for _plural noun_.\n"
                "I like to spend my time _verb ending in *i n g*_ or _verb ending in *i n g*_.\n"
                "When parents go on a vacation, they spend their time eating "
                "three _plural noun_ a day, and fathers play golf, and mothers sit around _verb ending in *i n g*_.\n"
                "Last summer, my little brother fell in a _noun_ "
                "and got poison _plant_ all over his _part of the body_.\n"
                "My family is going to go to _place_, and I will practice _verb ending in *i n g*_.\n"
                "Parents need vacations more than kids because parents are always very _adjective_.\n"
                "They have to work _number_ hours every day all year long to make enough _plural noun_ to pay "
                "for the vacation."],
               ["Personal Ad",
                "I enjoy long, _adjective_ walks on the beach, getting _verb ending in *e d*_ in the rain and "
                "serendipitous encounters with _plural noun_.\n"
                "I really like pina coladas mixed with _type of liquid_, and romantic, candle-lit _plural noun_.\n"
                "I travel frequently, especially to _place_, when I am not busy with work, I am a _occupation_.\n"
                "I am looking for _plural noun_ and beauty in the form of a _nationality_ goddess.\n"
                "She should have the physique of _name of a famous person_ and the _noun_ of _female person_.\n"
                "I would prefer if she knew how to cook, clean, and _verb_.\n"
                "I know I'm not very _adjective_ in my picture, but it was taken _number_ years ago, "
                "and I have since become more _adjective_. Call me!"],
               ["A sick note",
                "Dear School Nurse:\n"
                "_silly word_ _last name_ will not be attending school today.\n"
                "He/she has come down with a case of _type of illness_ and has horrible _plural noun_ "
                "and a _adjective_ fever.\n"
                "We have made an appointment with the _adjective_ Dr. _silly word_, who studied for many years "
                "in _place_ and has _number_ degrees in pediatrics.\n"
                "He will send you all the information you need. Thank you!\n"
                "Sincerely, Mrs. _silly word_."]]


allmadlibs = []
for text in madlibtexts:
    allmadlibs.append(Madlib(text))
print(len(allmadlibs), "madlibs loaded")
current_madlib = None
chosen_id = None
while True:
    if Madlib.first_round is True:
        prompt = "Ready to Play?: "
    else:
        prompt = "That was fun! Do you want to play again?"
        if Madlib.play_audio is True and Madlib.text_audio_player is not None:
            Madlib.get_tts_audio(prompt)
            Madlib.output_audio()
            Madlib.wait_for_audio_to_finish()
    user = input(prompt+": ").lower()
    if user == "y" or user == "yes":
        if Madlib.first_round is True:
            current_madlib = random.choice(allmadlibs)
        else:
            while chosen_id == current_madlib.id:
                current_madlib = random.choice(allmadlibs)
        chosen_id = current_madlib.id
        if Madlib.first_round is True:
            user = input("Play audio?: ").lower()
            if user == "y" or user == "yes":
                Madlib.text_audio_player = MyAudioPlayer()
                Madlib.play_audio = True
        current_madlib.get_user_words()
        current_madlib.print_final_text()
        print()
    elif user == "read again":
        if Madlib.first_round is True:
            funny_text = "i can not read a madlib if you have not made one yet. you dummy!"
            print(funny_text)
        else:
            current_madlib.print_final_text(False)
    else:
        if Madlib.play_audio is True:
            Madlib.get_tts_audio("Ok. Thanks for playing!")
            Madlib.output_audio()
            Madlib.wait_for_audio_to_finish()
        print("Ok. Thanks for playing!")
        exit()
