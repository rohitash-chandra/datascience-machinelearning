 
# Create the data frame.
emp.data <- data.frame(
   emp_id = c (1:5), 
   emp_name = c("Rick","Dan","Michelle","Ryan","Gary"),
   salary = c(623.3,515.2,611.0,729.0,843.25), 
   
   start_date = as.Date(c("2012-01-01", "2013-09-23", "2014-11-15", "2014-05-11",
      "2015-03-27")),
   stringsAsFactors = FALSE
)
# Print the data frame.			
print(emp.data)

 
str(emp.data)
  
# Print the summary.
print(summary(emp.data)) 

# Extract Specific columns.
result <- data.frame(emp.data$emp_name,emp.data$salary)
print(result)


# Extract first two rows.
result <- emp.data[1:2,]
print(result)


# Extract 3rd and 5th row with 2nd and 4th column.
result <- emp.data[c(3,5),c(2,4)]
print(result)


# Add the "dept" coulmn.
emp.data$dept <- c("IT","Operations","IT","HR","Finance")
v <- emp.data
print(v)
