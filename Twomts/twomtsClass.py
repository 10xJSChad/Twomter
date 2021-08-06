class twomt():
    def __init__(self, id, poster, content, date, replyTo, posterUsername):
        self.id = id
        self.poster = poster
        self.replyTo = replyTo
        self.content = content
        self.date = date
        self.posterUsername = posterUsername
        self.replies = []