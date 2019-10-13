"""

Created by: Nathan Starkweather
Created on: 02/25/2014
Created in: PyCharm Community Edition


"""

    def yes_or_no(votes):
        return sum(x == "YES" for x in votes)

    def vote_2_list(voters):
        voters = list(zip(*voters))  # transpose rows <=> columns
        return [yes_or_no(ballot_option) for ballot_option in voters]

    test1 = [
        ['YES', 'NO','YES','NO'],
        ['NO','YES','YES','NO']
    ]

    def make_total(voters):
        list_of_bool = vote_2_list(voters)
        return sum(list_of_bool)

    print(vote_2_list(test1))
    print(make_total(test1))
