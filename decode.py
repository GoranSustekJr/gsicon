import math

# This code does not check if number of rows in message.txt can be represented by sum of incremented numbers starting with 1
def decode(message_file):
    with open(message_file, 'r') as f:
        lines = f.readlines()
    n = len(lines)
    numOfRows = numOfRowsInPiramid(n)
    if numOfRows is not None:
        decoded_message = list()
        mess = dict()
        row = 0
        for line in lines:
            mess[int(line.split(' ')[0])] = line.split(" ")[1]
        for i in range(1, numOfRows + 1):        
            row += i
            decoded_message.append(mess[row].replace("\n", ""))
        return " ".join(decoded_message)
    else:
        return ValueError("Invalid number of lines: cannot form a valid pyramid structure")

        
        

def numOfRowsInPiramid(n):
    c = -2 * n
    discriminant = 1 - 4 * 1 * c
    if discriminant >= 0:
        n1 = (-1 + math.sqrt(discriminant)) / 2 # Negative is not important
        return int(n1)
    else:
        return None

print(decode("coding_qual_input.txt"))