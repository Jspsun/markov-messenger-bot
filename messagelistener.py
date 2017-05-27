import fbchat
import settings
import tools
import pickle
import urllib2

class Listener(fbchat.Client):

    def __init__(self, email, password, debug=True, user_agent=None):
        fbchat.Client.__init__(self, email, password, debug, user_agent)

    def on_message(self, mid, author_id, author_name, message, metadata):
        self.markAsDelivered(author_id, mid)
        self.markAsRead(author_id)

        if str(author_id) != str(self.uid):
            with open("DATA/clean_data.txt", 'wb') as f_out:
                f_out.write(message)
            
            tools.generate_corpus("DATA/clean_data.txt", "DATA/corpus.p", settings.markov_length)

            corpus = pickle.load(open("DATA/corpus.p", 'rb'))

            response = tools.generate_markov_message(corpus, sentence_type="question")

            urllib2.urlopen("https://senderbot.herokuapp.com/send~" + response + "~" + author_id)

bot = Listener("waterloogoosehonk@gmail.com", "HiIAmGoose101")
bot.listen()
