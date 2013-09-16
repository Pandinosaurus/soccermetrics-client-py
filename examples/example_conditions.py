#!/usr/bin/env python
#
# Retrieve match dates, kickoff times, and kickoff temps of all
# of Everton's matches.
#

from soccermetrics.rest import SoccermetricsRestClient

# A closure that we've written to page through the resource
# representation.  We'll add the functionality in a future
# release of the client so that you won't have to write this,
# but we want to make sure you can run this example now.
def iter(resp):
    while True:
        yield (resp.data)
        if not resp.meta.next:
            raise StopIteration
        else:
            resp = client.link.get(resp.meta.next)

if __name__ == "__main__":

    # Create a SoccermetricsRestClient object.  This call assumes that
    # SOCCERMETRICS_APP_ID and SOCCERMETRICS_APP_KEY are in your environment
    # variables, which we recommend.
    client = SoccermetricsRestClient()

    # Get match info data from all matches.  We do this by first querying
    # for all of Everton's home matches, then by querying their away matches.
    #
    # The result is a list, so we can join them together by concatenation.
    # (Order doesn't matter, we're going to sort the result in a sec.)
    matches = []
    for key in ['home_team_name','away_team_name']:
        param = {key: 'Everton'}
        for page in iter(client.match.information.get(**param)):
            matches.extend(page)

    # Results from the API are unsorted, so sort the results by match date.
    # You can also sort by matchday but not all matches are played in order.
    sorted_matches = sorted(matches, key=lambda k: k.match_date)

    # Now we can iterate over the sorted match list (and make sure you are
    # sorting over the sorted match list!)  For every match record, retrieve
    # its match condition record, which contains weather conditions.
    #
    # Match date and kickoff time are in the match information record, but
    # temperatures are in the match condition record.
    print "Match Date,Kickoff Time,Kickoff Temp"
    for match in sorted_matches:
        condition = client.link.get(match.link.conditions).data
        print "%s,%s,%2.1f" % (match.match_date, match.kickoff_time, condition.kickoff_temp)