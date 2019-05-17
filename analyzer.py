import nltk

class Analyzer():
    """Implements sentiment analysis."""

    def __init__(self, positives, negatives):
        """Initialize Analyzer."""
        self.positives=[]
        self.negatives=[]
        
        with open(positives) as positive:
            for str in positive:
                if not str.startswith(";"):
                    self.positives.append(str.strip("\n"))
        
        with open(negatives) as negative:
                for str in negative:
                    if not str.startswith(";"):
                        self.negatives.append(str.strip("\n"))
        
        

    def analyze(self, text):
        """Analyze text for sentiment, returning its score."""
        tokenizer=nltk.tokenize.TweetTokenizer()
        tokens = tokenizer.tokenize(text)
        score = 0
        
        for token in tokens:
            if token in self.positives:
                score+=1
            elif token in self.negatives:
                score-=1
        
        return score
