import csv
    
def fill_empty():
    input_file = open('values2.csv', 'r')
    reader1 = csv.reader(input_file)
    output_file = open('interpolated_output.csv', 'w', newline='')
    csv_write1 = csv.writer(output_file, delimiter = ',')
    
    matrix1 = [] # store the values from 'input file'
    for i in reader1:
        matrix1.append([])
        j = 0
        while (j < len(i)):
            try:
                float(i[j])
                matrix1[-1].append(float(i[j]))
            except:
                matrix1[-1].append(i[j])
            j = j + 1
    
    i = 0
    while (i < 2):
        matrix1_X = []
        matrix1_Y = []
        i1 = 0
        while (i1 < len(matrix1)):
            i2 = 0
            matrix1_X.append([])
            while (i2 < len(matrix1[i1])):
                matrix1_X[i1].append(matrix1[i1][i2])
                i2 = i2 + 1    
            i1 = i1 + 1
    
        i1 = 0
        while (i1 < len(matrix1)):
            i2 = 0
            matrix1_Y.append([])
            while (i2 < len(matrix1[i1])):
                matrix1_Y[i1].append(matrix1[i1][i2])
                i2 = i2 + 1    
            i1 = i1 + 1
    
        limit1 = 0
        limit2 = 0
        i1 = 0
        div = 0
        pos = 0
        # fill on Y axis
        while (i1 < len(matrix1_Y)):
            i2 = 0
            state = []
            while (i2 < len(matrix1_Y[0])):
                state.append(1)
                i2 = i2 + 1
            i2 = 0
            while (i2 < len(matrix1_Y[i1])):
                if type(matrix1_Y[i1][i2]) == str:    
                    state[i2] = -1
                i2 = i2 + 1
        
            if state.count(1) > 1:
                    i2 = 0
                    prev_limit2 = i2 # previous limit2 
                    while (i2 < len(state) - 1):
                        if state[i2] == 1:
                            limit1 = i2
                            pos = limit1 + 1
                            while (pos < len(state)):
                                if state[pos] == 1:
                                    limit2 = pos
                                    break
                                else:
                                    pos = pos + 1
                            # complete the second part in this loop
                            if limit2 > prev_limit2:
                                div = abs(matrix1_Y[i1][limit1] - matrix1_Y[i1][limit2]) / abs(limit1 - limit2)
                                i3 = limit1 + 1
                                if matrix1_Y[i1][limit1] <= matrix1_Y[i1][limit2]:
                                    while (i3 < limit2):
                                        matrix1_Y[i1][i3] = matrix1_Y[i1][i3 - 1] + div
                                        state[i3] = 1
                                        i3 = i3 + 1
                                else:
                                    while (i3 < limit2):
                                        matrix1_Y[i1][i3] = matrix1_Y[i1][i3 - 1] - div
                                        state[i3] = 1
                                        i3 = i3 + 1
                        
                                prev_limit2 = limit2                           
                                i2 = limit2 # the new iteration of i2 will start from this position
                            else:
                                break
                        else:
                            i2 = i2 + 1
                
                    if state.__contains__(-1) == True:
                        #fill the positions having neighbours in only one side
                        # repeat the differences recorded in the neighbours to fill up these positions
                        diff_list = [] # list to store the differences between different points in series
                        i2 = 0
                        while (i2 < len(matrix1_Y[i1])):
                            if type(matrix1_Y[i1][i2]) != str:
                                while (type(matrix1_Y[i1][i2]) != str):
                                    if i2 + 1 == len(matrix1_Y[i1]) or type(matrix1_Y[i1][i2 + 1]) == str:
                                        break
                                    else:  
                                        diff_list.append(matrix1_Y[i1][i2] - matrix1_Y[i1][i2 + 1])
                                    i2 = i2 + 1
                                #break
                                i2 = i2 + 1
                            else:
                                i2 = i2 + 1

                        i2 = 0
                        pos = i2 # here 'pos' will store the first non empty position
                        while (i2 < len(matrix1_Y[i1])):
                            if type(matrix1_Y[i1][i2]) != str:
                                pos = i2
                                break
                            i2 = i2 + 1

                        direction = 0 # 0 -> top to bottom; 1 -> bottom to top
                        i2 = 0
                        while (pos > 0):
                            if direction == 0:
                                if i2 < len(diff_list) - 1:
                                    matrix1_Y[i1][pos - 1] = matrix1_Y[i1][pos] + diff_list[i2]
                                    i2 = i2 + 1
                                if i2 == len(diff_list) - 1:
                                    matrix1_Y[i1][pos - 1] = matrix1_Y[i1][pos] + diff_list[i2]
                                    direction = 1
                            else:   # direction = 1
                                if i2 > 0:
                                    matrix1_Y[i1][pos - 1] = matrix1_Y[i1][pos] + diff_list[i2]
                                    i2 = i2 - 1
                                if i2 == 0:
                                    matrix1_Y[i1][pos - 1] = matrix1_Y[i1][pos] + diff_list[i2]
                                    direction = 0
                            pos = pos - 1 
                    
                        i2 = len(matrix1_Y[i1]) - 1
                        pos = i2 # here 'pos' will store the last non empty position
                        while (i2 >= 0):
                            if type(matrix1_Y[i1][i2]) != str:
                                pos = i2
                                break
                            i2 = i2 - 1

                        pos = pos + 1
                        direction = 1 # 0 -> top to bottom; 1 -> bottom to top
                        i2 = len(diff_list) - 1
                        while (pos < len(matrix1_Y[i1])):   # need a loop for controlling the iterations of i2
                            if direction == 0:
                                if i2 < len(diff_list) - 1:
                                    matrix1_Y[i1][pos] = matrix1_Y[i1][pos - 1] - diff_list[i2]
                                    i2 = i2 + 1
                                if i2 == len(diff_list) - 1:
                                    matrix1_Y[i1][pos] = matrix1_Y[i1][pos - 1] - diff_list[i2]
                                    direction = 1
                            else:   # direction = 1
                                if i2 > 0:
                                    matrix1_Y[i1][pos] = matrix1_Y[i1][pos - 1] - diff_list[i2]
                                    i2 = i2 - 1
                                if i2 == 0:
                                    matrix1_Y[i1][pos] = matrix1_Y[i1][pos - 1] - diff_list[i2]
                                    direction = 0
                            pos = pos + 1 
                        # eg: pos_0 = pos_1 + (diff_list[0] with its assigned sign (+ or -))
                        # once diff_list iteration completes then repeat in reverse order
                        # if position == len(diff_list) - 1 then start position from len(diff_list) - 1 till 0

            i1 = i1 + 1
    

        limit1 = 0
        limit2 = 0
        i1 = 0
        div = 0
        pos = 0
        # fill on X axis
        while (i1 < len(matrix1_X[0])):
            i2 = 0
            state = []
            while (i2 < len(matrix1_X)):
                state.append(1)
                i2 = i2 + 1
            i2 = 0
            while (i2 < len(matrix1_X)):
                if type(matrix1_X[i2][i1]) == str:    
                    state[i2] = -1
                i2 = i2 + 1
        
            if state.count(1) > 1:
                    i2 = 0
                    prev_limit2 = i2 # previous limit2 
                    while (i2 < len(state) - 1):
                        if state[i2] == 1:
                            limit1 = i2
                            pos = limit1 + 1
                            while (pos < len(state)):
                                if state[pos] == 1:
                                    limit2 = pos
                                    break
                                else:
                                    pos = pos + 1
                            # complete the second part in this loop
                            if limit2 > prev_limit2:
                                div = abs(matrix1_X[limit1][i1] - matrix1_X[limit2][i1]) / abs(limit1 - limit2)
                                i3 = limit1 + 1
                                if matrix1_X[limit1][i1] <= matrix1_X[limit2][i1]:
                                    while (i3 < limit2):
                                        matrix1_X[i3][i1] = matrix1_X[i3 - 1][i1] + div
                                        state[i3] = 1
                                        i3 = i3 + 1
                                else:
                                    while (i3 < limit2):
                                        matrix1_X[i3][i1] = matrix1_X[i3 - 1][i1] - div
                                        state[i3] = 1
                                        i3 = i3 + 1
                        
                                prev_limit2 = limit2                           
                                i2 = limit2 # the new iteration of i2 will start from this position
                            else:
                                break
                        else:
                            i2 = i2 + 1
                
                    if state.__contains__(-1) == True:
                        #fill the positions having neighbours in only one side
                        # repeat the differences recorded in the neighbours to fill up these positions
                        diff_list = [] # list to store the differences between different points in series
                        i2 = 0
                        while (i2 < len(matrix1_X)):
                            if type(matrix1_X[i2][i1]) != str:
                                while (type(matrix1_X[i2][i1]) != str):
                                    if i2 + 1 == len(matrix1_X) or type(matrix1_X[i2 + 1][i1]) == str:
                                        break
                                    else:  
                                        diff_list.append(matrix1_X[i2][i1] - matrix1_X[i2 + 1][i1])
                                    i2 = i2 + 1
                                #break
                                i2 = i2 + 1
                            else:
                                i2 = i2 + 1

                        i2 = 0
                        pos = i2 # here 'pos' will store the first non empty position
                        while (i2 < len(matrix1_X)):
                            if type(matrix1_X[i2][i1]) != str:
                                pos = i2
                                break
                            i2 = i2 + 1

                        direction = 0 # 0 -> top to bottom; 1 -> bottom to top
                        i2 = 0
                        while (pos > 0):
                            if direction == 0:
                                if i2 < len(diff_list) - 1:
                                    matrix1_X[pos - 1][i1] = matrix1_X[pos][i1] + diff_list[i2]
                                    i2 = i2 + 1
                                if i2 == len(diff_list) - 1:
                                    matrix1_X[pos - 1][i1] = matrix1_X[pos][i1] + diff_list[i2]
                                    direction = 1
                            else:   # direction = 1
                                if i2 > 0:
                                    matrix1_X[pos - 1][i1] = matrix1_X[pos][i1] + diff_list[i2]
                                    i2 = i2 - 1
                                if i2 == 0:
                                    matrix1_X[pos - 1][i1] = matrix1_X[pos][i1] + diff_list[i2]
                                    direction = 0
                            pos = pos - 1 
                    
                        i2 = len(matrix1_X) - 1
                        pos = i2 # here 'pos' will store the last non empty position
                        while (i2 >= 0):
                            if type(matrix1_X[i2][i1]) != str:
                                pos = i2
                                break
                            i2 = i2 - 1

                        pos = pos + 1
                        direction = 1 # 0 -> top to bottom; 1 -> bottom to top
                        i2 = len(diff_list) - 1
                        while (pos < len(matrix1_X)):
                            if direction == 0:
                                if i2 < len(diff_list) - 1:
                                    matrix1_X[pos][i1] = matrix1_X[pos - 1][i1] - diff_list[i2]
                                    i2 = i2 + 1
                                if i2 == len(diff_list) - 1:
                                    matrix1_X[pos][i1] = matrix1_X[pos - 1][i1] - diff_list[i2]
                                    direction = 1
                            else:   # direction = 1
                                if i2 > 0:
                                    matrix1_X[pos][i1] = matrix1_X[pos - 1][i1] - diff_list[i2]
                                    i2 = i2 - 1
                                if i2 == 0:
                                    matrix1_X[pos][i1] = matrix1_X[pos - 1][i1] - diff_list[i2]
                                    direction = 0
                            pos = pos + 1 
                        # eg: pos_0 = pos_1 + (diff_list[0] with its assigned sign (+ or -))
                        # once diff_list iteration completes then repeat in reverse order
                        # if position == len(diff_list) - 1 then start position from len(diff_list) - 1 till 0

            i1 = i1 + 1
    
        # Added points
        i1 = 0
        while (i1 < len(matrix1)):
            i2 = 0
            while (i2 < len(matrix1[i1])):
                if type(matrix1[i1][i2]) == str:
                    if type(matrix1_X[i1][i2]) != str and type(matrix1_Y[i1][i2]) != str:
                        matrix1[i1][i2] = (matrix1_X[i1][i2] + matrix1_Y[i1][i2]) / 2
                    elif type(matrix1_X[i1][i2]) != str and type(matrix1_Y[i1][i2]) == str:
                        matrix1[i1][i2] = matrix1_X[i1][i2]
                    elif type(matrix1_X[i1][i2]) == str and type(matrix1_Y[i1][i2]) != str:
                        matrix1[i1][i2] = matrix1_Y[i1][i2]
                i2 = i2 + 1    
            i1 = i1 + 1

        i = i + 1
    
    # write to file:
    for i in matrix1:
        csv_write1.writerow(i)
    
fill_empty()