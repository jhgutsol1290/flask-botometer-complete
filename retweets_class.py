class Retweeters():
    def get_array_screen_names(self, retweets):
        self.array_screen_names = []
        array_tweets = [status for status in retweets]
        for element in array_tweets:
            new_element = '@' + element.user.screen_name
            self.array_screen_names.append(new_element)
        return self.array_screen_names