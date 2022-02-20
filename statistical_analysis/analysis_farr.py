import csv


def get_colum_names(filename):
    """
    function to open and read the input file
    :param filename:
    :return: colum_names - a list of column names
    """
    with open(filename) as f:
        file = csv.DictReader(f, delimiter=',')  # use DictReader to skip header with column names

        # access and store column names
        # first make dict
        dict_file = dict(list(file)[0])

        # then list from keys
        column_names = list(dict_file.keys())
    return column_names


def exclude_participants(filename, column_names):
    """
    go through the file and find people we should exclude - the ids and information for exclude are stored and returned
    to make sure we can (if necessary) further check why exclude happened
    :param filename: the file to process
    :param column_names: a list with column names as extracted in get_colum_names()
    :return: a set of participant ids with information
    """
    excludes = set()
    submission_id = 0
    with open(filename) as f:
        print("open")
        file = csv.reader(f, delimiter=',')

        filler_count, time_count = 0, 0
        # process every line in the file (except header)
        for row in file:
            print("row")
            # if submission id does not match the first item in the row, the participant has changed
            if submission_id != row[0]:
                # assign new submission id
                submission_id = row[0]

            # we want to exclude if the submission id is the same
            else:
                # we want to eliminate participants according to the following conditions:
                #   1. they know either logic or pragmatics             PIA: or are not German native speakers -> exclude complete participant
                #   2. they answered at least 3 fillers incorrectly     PIA: exclude complete participant
                #   3. they responded too fast (< 10s)                  PIA: exclude only the item, not complete participant
                # TODO: did I forget about something?

                # 1. check whether answer to either 'knows_logic' or 'knows_pragmatics' is 'Ja'
                # also check whether participant is German native
                if (row[column_names.index('knows_logic')] or row[column_names.index('knows_pragmatics')]) == 'Ja' or \
                        row[column_names.index('german_native')] == 'Nein':
                    excludes.add(str(submission_id)+" log_prag_ger")

                # 2. check number of correctly answered fillers
                # count if type is 'FALSE' AND response is 'Ja' OR type is 'TRUE' AND response is 'Nein'
                if (row[column_names.index('item_answer_type')] == 'FALSE' and
                    row[column_names.index('response')] == 'Ja') or \
                    (row[column_names.index('item_answer_type')] == 'TRUE' and
                     row[column_names.index('response')] == 'Nein'):
                    filler_count += 1
                    # if 3 is reached, add participant with note and reset filler_count
                    if filler_count == 3:
                        excludes.add(str(submission_id)+" fillers")
                        filler_count = 0

                # 3. check response time < 10000 (10s) - get difference as absolute number
                if abs(int(row[column_names.index('response_time')]) - int(row[column_names.index('stopwatch_ms')])) < \
                        10000:
                    time_count += 1
                    # if 5 is reached, add participant with note and reset time_count
                    # TODO: NOTE: I set a limit of 5 for the test phase, this can be adjusted
                    if time_count == 5:
                        excludes.add(str(submission_id)+" too fast")
                        time_count = 0
        return sorted(excludes)


if __name__ == '__main__':
    print(exclude_participants('results_test.csv', get_colum_names('results_test.csv')))

