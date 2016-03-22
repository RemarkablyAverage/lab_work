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
	return randomString
}

#randomly cut up string
#put into dataframe
#random generate index number 1-cuts
#piece back strings together
create_cuts <- function(
	operating_str = NULL,
	filterby = NULL,
	cuts = NULL) {

	if (is.null(cuts)) {
		cuts <- 30
	}
	if (is.null(operating_str)) {
		operating_str <- generate_string(400)
	}
	if (is.null(filterby)) {
		filterby <- 45
	}
	i <- 1;
	cuts_vector <- c()
	while (operating_str != "" && i <= cuts) {
		start <- as.integer(sample(0:(nchar(operating_str)/(cuts * i)), 1) + 1)
		end <- as.integer((sample(10:20) * start) , 1)
		if (start + end <= filterby) {
			cut <- substr(operating_str, start, end)
			cuts_vector <- c(cuts_vector, cut)
			operating_str <- gsub(cut, "", operating_str)
			i <- i + 1
		} else {
			next
		}
	}
	cuts_df <- data.frame(cuts = cuts_vector)
	cuts_df
}

#return a vector of transcripts
create_transcripts <- function(
	chop_df = NULL
	transcript_number = NULL) {

	if (is.null(transcript_number)) {
		transcript_number <- 7
	}
	
	end_sample <- nrow(chop_df)

}



main <- function() {
	chopped_up <- cut_str(test_str)
	transcripts <- create_transcripts(chopped_up)
}











