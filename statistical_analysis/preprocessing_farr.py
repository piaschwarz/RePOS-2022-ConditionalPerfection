import csv


def get_colum_names(filename):
    """
    function to open and read the input file
    :param filename:
    :return: colum_names - a list of column names
    """
    f = open(filename)
    # with open(filename) as f:
    file = csv.DictReader(f, delimiter=',')  # use DictReader to skip header with column names

    # access and store column names
    # first make dict
    dict_file = dict(list(file)[0])

    # then list from keys
    column_names = list(dict_file.keys())
    f.close()
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
    ex = []
    logic, prag, ger, filler = 0, 0, 0, 0
    submission_id = 0
    with open(filename) as f:
        file = csv.reader(f)

        filler_count, time_count = 0, 0
        for num, row in enumerate(file):

            if row[0] != 'submission_id':
                # assign new submission id
                submission_id = int(row[0])

                # we want to eliminate participants according to the following conditions:
                #   1. they know logic or pragmatics or are no German native speaker -> exclude complete participant
                #   2. they answered at least 3 fillers incorrectly -> exclude complete participant
                #   3. they responded too fast (< 10s) -> exclude only the item, not the participant

                # 1. check whether answer to either 'knows_logic' or 'knows_pragmatics' is 'Ja'
                # also check whether participant is German native
                if (row[column_names.index('knows_logic')] or row[column_names.index('knows_pragmatics')]) == 'Ja' or \
                        row[column_names.index('german_native')] == 'Nein':
                    if row[column_names.index('knows_logic')] == 'Ja':
                        logic += 1
                    if row[column_names.index('knows_pragmatics')] == 'Ja':
                        prag += 1
                    if row[column_names.index('german_native')] == 'Nein':
                        ger += 1
                    # excludes_long.add(str(submission_id)+" log_prag_ger")
                    excludes_short.add(submission_id)

                # 2. check number of correctly answered fillers
                # count if type is 'FALSE' AND response is 'Ja' OR type is 'TRUE' AND response is 'Nein'
                elif (row[column_names.index('item_answer_type')] == 'FALSE' and
                    row[column_names.index('response')] == 'Ja') or \
                    (row[column_names.index('item_answer_type')] == 'TRUE' and
                     row[column_names.index('response')] == 'Nein'):
                    filler_count += 1
                    # if 3 is reached, add participant with note and reset filler_count
                    if filler_count == 3:
                        # excludes_long.add(str(submission_id)+" fillers")
                        excludes_short.add(submission_id)
                        filler += 1
                        filler_count = 0

                # 3. check response time < 10000 (10s) - get sum as absolute number
                elif int(row[column_names.index('response_time')]) + int(row[column_names.index('stopwatch_ms')]) < 10000:
                    excludes_long.add(str(num+1)+" timing")
                    # add line number +1 since header is still part of the file
                    line_number.add(num+1)

    print(len(excludes_short), "complete participant(s) was/were excluded\n\t",
          logic/12, "participant(s) was/were excluded due to knowing logic\n\t",
          prag/12, "participant(s) was/were excluded due to knowing pragmatics\n\t",
          ger/12, "participant(s) was/were no German native speaker(s)\n",
          filler/12, "participant(s) did not answer more than 3 fillers correctly\n",
          len(line_number), "items were excludes")
    return sorted(excludes_short), sorted(line_number)


def write_output(new_file, original_file, exclude_file, excludes):
    """
    create a new file with the participants remaining after the exclude
    :param new_file: new csv file to write output to
    :param original_file: original data containing all participants
    :param exclude_file: the file to store the excluded participants/rows for further checks
    :param excludes: the output of exclude_participants()
    """
    # open both files
    original = open(original_file, 'r')
    exclude_rows = open(exclude_file, 'w')
    with open(new_file, 'w') as copied:
        writer = csv.writer(copied, delimiter=",")
        excluded = csv.writer(exclude_rows, delimiter=",")
        excluded.writerow(get_colum_names(original_file))  # add header
        reader = csv.reader(original, delimiter=",")
        # iterate over rows and get line number for record
        for num, row in enumerate(reader):
            # only write the content of the row if the line number is not part of the excludes
            # and the id is not in excludes
            if num not in excludes[1] and not any(id in excludes[0] for id in row):
                writer.writerow(row)
            else:
                excluded.writerow(row)
    original.close()


if __name__ == '__main__':
    """print(write_output('new_file.csv', 'test.csv', 'excludes.csv',
                       exclude_participants('test.csv', get_colum_names('test.csv'))))"""

    print(exclude_participants('test.csv', get_colum_names('test.csv')))

