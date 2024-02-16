class Event():
    def __init__(self, summary="", start_date="", end_date="", location=""):
        self.name        = summary
        self.start_date  = start_date
        self.end_date    = end_date
        self.duration    = ""
        self.location    = location

    def to_dict(self):
        return {
            self.name : {
                "start_date": self.start_date,
                "end_date": self.end_date,
                "duration": self.duration,
                "location": self.location
            }
        }