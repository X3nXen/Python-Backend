class EventAnalyzer():
    def get_joiners_multiple_meetings_method(events):
        multiple_joiners = []
        for event in events:
            for joiner in event.joiners:
                ctr = 0
                for search_event in events:
                    if joiner in search_event.joiners and joiner not in multiple_joiners:
                        ctr += 1
                if ctr >= 2:
                    multiple_joiners.append(joiner)
        return multiple_joiners

