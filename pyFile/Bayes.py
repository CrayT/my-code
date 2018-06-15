def loadDataset(filename,split,trainingSet=[],testSet = []):    
    with open(filename,"rb") as csvfile:    
        lines = csv.reader(csvfile)    
        dataset = list(lines)  
        #dataset=mm.fit_transform(dataset)  
        for x in range(len(dataset)-1):    
            for y in range(4):    
                dataset[x][y] = float(dataset[x][y])    
            if random.random()<split:    
                trainingSet.append(dataset[x])    
            else:    
                testSet.append(dataset[x]) 