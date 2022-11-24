def sorting(rating_list, count_of_elements):
    max = rating_list[0][1]
    count = 0; k1 = 0; k2 = 0
    for k in range(count_of_elements - 1):
        if count:
            k1 = k
            k2 = k
            max = rating_list[k][1]
            
        for k1 in range(k1, count_of_elements):
            if rating_list[k1][1] > max:
                k2 = k1
                max = rating_list[k1][1]
            
        promejyt = rating_list[k]
        rating_list[k] = rating_list[k2]
        rating_list[k2] = promejyt
        count = count + 1	
        k1 = 0
    return rating_list
                
        
		