from single_point import parse
import pandas as pd


# getting the means and frequents that will be used for replacing missing data
def getMeansAndMostFrequent(data):
    res = list()
    for i in data:
        # if the data column is of type string, calculate the most frequents, strip for white spaces
        if (isinstance(data[i][0], str)):

            # append to the result vector
            res.append(data[i].value_counts().idxmax().strip())
            pass
        else:
            # if the data column is of type int, calculate the most mean, round the number
            res.append(int(data[i].mean(axis=0).round()))

    # return the result vector
    return res


# replacing the missing (?) data entries with the means and most frequents to be fed into the parser function
def addMissingValues(missingMatrix, meansAndMostFrequents):
    res = list()

    for row in missingMatrix:

        # if there's a row with missing data
        if '?' in row:
            for n, i in enumerate(row):
                if i == '?':
                    # replace the missing entry with the corresponding value in the means and most frequents vector
                    row[n] = meansAndMostFrequents[n]

            res.append(row)
        else:
            res.append(row)

    # return the matrix with no missing values
    return res

# parsing the data, using the full file path provided by the user
def parse_data(data_file_full_path):
    """ This method parses the data into the final matrix [M x N] - called X matrix.
        and Nx1 vector of classifier results - Y vector.
    """

    f = open(data_file_full_path)
    final_x_matrix = list()
    final_y_vector = list()
    missingMatrix = list()

    columns = ["age", "workclass", "fnlwgt", "education", "education-num", "martial-status", "occupation",
               "relationship", "race", "sex", "capital-gain", "capital-loss", "hours-per-week", "native-country",
               "salary"]

    # splitting the data for each row, splitting for every entry using (", ")
    file_input = f.read().split('\n')
    for row in file_input:
        missingMatrix.append(row.split(', '))

    # read the data as csv with the column names, to be fed into get means and most frequents
    data = pd.read_csv(data_file_full_path, names=columns)
    means_and_most_frequents = getMeansAndMostFrequent(data)

    # replacing the missing values with the data in means and most frequents vector
    filledMatrix = addMissingValues(missingMatrix, means_and_most_frequents)

    # popping the last empty row
    filledMatrix.pop()

    # parse each row to be replaced with numbers from the parse function
    for row in filledMatrix:
        newrow = parse(row)
        final_x_matrix.append(newrow[0])
        final_y_vector.append(newrow[1])

    # return X matrix, y vector, and means and most frequents vector - to be used in parse test data function
    return final_x_matrix, final_y_vector, means_and_most_frequents


# parsing the test data of type .test , using the means and most frequents
def parse_test_data(test_file_full_path, means_and_frequents):
    f = open(test_file_full_path)
    missingMatrix = list()
    final_x_matrix = list()
    final_y_vector = list()

    # splitting the data for the rows
    file_input = f.read().split('\n')

    for row in file_input:
        missingMatrix.append(row.split(', '))

    # removing the first and last entry to avoid list index out of range error
    missingMatrix.remove(missingMatrix[0])
    missingMatrix.pop()

    # replace the missing values with the means and most frequents
    filledMatrix = addMissingValues(missingMatrix, means_and_frequents)

    for row in filledMatrix:
        newRow = parse(row)
        final_x_matrix.append(newRow[0])
        final_y_vector.append(newRow[1])

    return final_x_matrix, final_y_vector

