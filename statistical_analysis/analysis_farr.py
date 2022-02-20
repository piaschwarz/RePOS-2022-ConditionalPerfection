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
    excludes_long, excludes_short, line_number = set(), set(), set()
    submission_id = 0
    with open(filename) as f:
        file = csv.reader(f, delimiter=',')

        filler_count, time_count = 0, 0
        # process every line in the file (except header)
        for num, row in enumerate(file):
            # if submission id does not match the first item in the row, the participant has changed
            if submission_id != row[0]:
                # assign new submission id
                submission_id = row[0]

            # we want to exclude if the submission id is the same
            else:
                # we want to eliminate participants according to the following conditions:
                #   1. they know logic or pragmatics or are no German native speaker -> exclude complete participant
                # TODO: What happens if there is no value for the above information?

                #   2. they answered at least 3 fillers incorrectly -> exclude complete participant
                #   3. they responded too fast (< 10s) -> exclude only the item, not the participant

                # 1. check whether answer to either 'knows_logic' or 'knows_pragmatics' is 'Ja'
                # also check whether participant is German native
                if (row[column_names.index('knows_logic')] or row[column_names.index('knows_pragmatics')]) == 'Ja' or \
                        row[column_names.index('german_native')] == 'Nein':
                    excludes_long.add(str(submission_id)+" log_prag_ger")
                    excludes_short.add(submission_id)

                # 2. check number of correctly answered fillers
                # count if type is 'FALSE' AND response is 'Ja' OR type is 'TRUE' AND response is 'Nein'
                if (row[column_names.index('item_answer_type')] == 'FALSE' and
                    row[column_names.index('response')] == 'Ja') or \
                    (row[column_names.index('item_answer_type')] == 'TRUE' and
                     row[column_names.index('response')] == 'Nein'):
                    filler_count += 1
                    # if 3 is reached, add participant with note and reset filler_count
                    if filler_count == 3:
                        excludes_long.add(str(submission_id)+" fillers")
                        excludes_short.add(submission_id)
                        filler_count = 0

                # 3. check response time < 10000 (10s) - get sum as absolute number
                if int(row[column_names.index('response_time')]) + int(row[column_names.index('stopwatch_ms')]) < 10000:
                    excludes_long.add(str(num)+" timing")
                    # add ine number as negative number to not confuse it with the submission id
                    line_number.add(num)
        return sorted(excludes_short), sorted(line_number)


def write_output(new_file, original_file, excludes):
    """
    create a new file with the participants remaining after the exclude
    :param new_file: new csv file to write output to
    :param original_file: original data containing all participants
    :param excludes: the output of exclude_participants()
    """
    # open both files
    original = open(original_file, 'r')
    with open(new_file, 'w') as copied:
        writer = csv.writer(copied, delimiter=",")
        reader = csv.reader(original, delimiter=",")
        # iterate over rows and get line number for record
        for num, row in enumerate(reader):
            # only write the content of the row if the line number is not part of the excludes
            # and the id is not in excludes
            if num not in excludes[1] and not any(id in excludes[0] for id in row):
                writer.writerow(row)


if __name__ == '__main__':
    print(write_output('new_file.csv', 'test.csv',
                       exclude_participants('test.csv', get_colum_names('test.csv'))))