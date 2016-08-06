#This is an implementation of heap/ priority queue
#For the detailed logic of this structure, please refer to:
#https://en.wikipedia.org/wiki/Heap_(data_structure)

#The time complexity of insert, pop is log(n)
PriorityQueue <- setRefClass("PriorityQueue", 
                             
                             #Values: Stores the nodes in a vector structure
                             #Size: Number of elements in the queue
                             #Capacity: Number of slots available in Values
                             #Type: Class type of nodes
                             #Comparator: A function which compares two nodes
                             fields = list(values = "vector", size = "numeric", capacity = "numeric", type = "character", comparator = "function"),
                             methods = list(
                               
                               #initialize the queue, the default capacity is 50
                               initialize = function(nodeType, customCapacity = 50, customComparator = NULL){
                                 type <<- nodeType
                                 capacity <<- customCapacity
                                 values <<- vector("list", capacity)
                                 size <<- 0
                                 if(is.null(customComparator)){
                                   comparator <<- function(a, b)a<b
                                 }else{
                                   comparator <<- customComparator
                                 }
                               },
                               
                               #this function checks whether the type of input value mathches the pre-specified type
                               check.type = function(val){
                                 if(length(val) > 1){
                                   stop("Priority queue cannot handle vector or list type.")
                                 }
                                 if(class(val) != type){
                                   if(is.numeric(val) && (type == "numeric" || type == "integer"))return(TRUE)
                                   return(FALSE)
                                 }
                                 return(TRUE)
                               },
                               
                               #this function doubles the length "values" vector 
                               double.Size = function(){
                                 capacity <<- capacity *2
                                 values <<- c(values, vector("list", capacity))
                               },
                               
                               #this function allows user to insert new node to the queue
                               insert = function(x){
                                 
                                 #check the input type
                                 if(!check.type(x)){
                                   stop(paste("Class of value x (", class(x),") does not match pre-specified type (", type, "),", sep = ""))
                                 }
                                 
                                 #if there is no available slot, double the length of the vector
                                 if(size == capacity)double.Size();
                                 
                                 # --- Everything is ready ---
                                 
                                 #Increase the size by 1, assign input value to the end of the queue
                                 size <<- size +1
                                 tmpList <- list(x)
                                 values[size] <<- tmpList
                                 index <- size
                                 
                                 #Compare the current node with its parent, if the they are in the wrong order, swap them
                                 #Repeat this process untill there is no wrong pair
                                 while(index > 1 && comparator(values[[index]], values[[index%/%2]])){
                                   tmp = values[index%/%2]
                                   values[index%/%2] <<- values[index]
                                   values[index] <<- tmp
                                   index = index%/%2
                                 }
                               },
                               
                               #This function returns the front element(the smallest)
                               front = function(){
                                 if(size)
                                  return(values[[1]])
                                 else return(NULL)
                               },
                               
                               #This function removes the front element
                                pop = function(){
                                  if(size == 0)return()
                                  
                                  #Keep the value in another variable
                                  result <- values[[1]]
                                  
                                  #Remove the front element and correct the order
                                  values[1] <<- values[size]
                                  size <<- size - 1
                                  index = 1
                                  tmpResult = 0
                                  tmpIndex = 0
                                  while(index*2<=size){
                                    if(index*2+1<=size && comparator(values[[index*2+1]], values[[index*2]])){
                                      tmpIndex = index*2+1 #Will compare current node with right child
                                    }else {
                                      tmpIndex = index*2 #Will compare current node with left child
                                    }
                                    if(comparator(values[[tmpIndex]], values[[index]])){
                                      tmp = values[tmpIndex]
                                      values[tmpIndex] <<- values[index]
                                      values[index] <<- tmp
                                      index = tmpIndex
                                    }else break
                                  }
                                  return(result)
                                },
                               
                               toList = function(){
                                 if(size == 0)return()
                                 result <- vector("list", size)
                                 count <- 1
                                 while(size){
                                   result[count] <- list(front())
                                   pop()
                                   count <- count+1
                                 }
                                 return(result)
                               }
                             )
                             )