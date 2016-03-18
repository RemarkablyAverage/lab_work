install.packages("ggplot2")
install.packages("gplots")
install.packages("Matrix")
library("Matrix")
library("ggplot2")
library("gplots")


#takes in a count to how many base pairs(lol???)
#returns a data frame with the number of cuts
# cuts   |   actual string
#  1     | ATCG....G
#  2     | ATCG.....G 
#etc


generate_string <- function(
	length = NULL) {

	randomString <- c()
	for (i in 1:length) {
		appchar <- sample(c("A", "T", "C", "G"), 1, replace=FALSE)
		randomString <- paste(randomString, appchar, sep = "")
	}
	randomString
}

cut_string <- function(
	) {

}

string_table_create <- function( 
	length = NULL,
	cuts = NULL,
	
	) {

}