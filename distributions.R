install.packages("ggplot2")
install.packages("gplots")
install.packages("Matrix")
library("Matrix")
library("ggplot2")
library("gplots")

generate_string <- function(
	length = NULL) {

	randomString <- c()
	for (i in 1:length) {
		appchar <- sample(c("A", "T", "C", "G"), 1, replace=FALSE)
		randomString <- paste(randomString, appchar, sep = "")
	}
	randomString
}

#randomly cut up string
#put into dataframe
#random generate index number 1-cuts
#piece back strings together
create_cuts <- function(
	operating_str = NULL,
	filterby = NULL,
	filter = FALSE,
	cuts = NULL) {

	if (is.null(cuts)) {
		cuts <- 1000
	}
	if (is.null(operating_str)) {
		operating_str <- generate_string(300000)
	}
	if (is.null(filterby)) {
		filterby <- 100
	}
	i <- 1;
	cuts_vector <- c()
	while (operating_str != "" && i <= cuts) {
		start <- as.integer(sample(0:(nchar(operating_str)/(cuts * i)), 1) + 1)
		end <- as.integer(sample((10:20) * start, 1))
		cut <- substr(operating_str, start, end)
		cuts_vector <- c(cuts_vector, cut)
		operating_str <- gsub(cut, "", operating_str)
		i <- i + 1
	}
	#filter 
	if (filter) {
		actual_cuts <- mapply(function(x) { if (nchar(x) >= filterby) return (TRUE) else return (FALSE) }, cuts_vector)
		cuts_vector <- cuts_vector[actual_cuts == TRUE]
	}
	cuts_df <- data.frame(cuts = cuts_vector, stringsAsFactors = FALSE)
	cuts_df
}

#return a dataframe of transcripts
create_transcripts <- function(
	chop_df = NULL,
	transcript_number = NULL,
	length = NULL,
	variation = NULL) {

	if (is.null(transcript_number)) {
		transcript_number <- 4
	}
	if (is.null(length)) {
		length <- 30
	}
	if (is.null(variation)) {
		variation <- TRUE
	}
	end_sample <- nrow(chop_df)
	transcripts <- c()
	for (x in 1:transcript_number) {
		individual_transcript <- c()
		if (variation) {
			start <- as.integer(length - sample(length/8:length, 1))
			end <- as.integer(length + sample(length:length*1.2, 1))
			length_loop <- sample(start:end, 1)
			print(length_loop)
		} else {
			length_loop <- length
		}
		for (i in 1:length_loop) {
			rand <- as.integer(sample((1:end_sample), 1))
			individual_transcript <- paste(individual_transcript, (chop_df[rand,]), sep = "|")
		}
		transcripts <- c(transcripts, individual_transcript)
	}
	ret_df <- data.frame(transcripts = transcripts, stringsAsFactors = FALSE)
	ret_df
}

#plot transcripts as a function of y = e^-x and 
#use | as delminator
#use nchar as count

plot_transcripts <- function(
	dataf = NULL,
	set_distribution_length = NULL,
	distribution_type = NULL) {

	#parse string
	distribution_vector <- c()

	for (t in 1:nrow(dataf)) {
		#iterate through all transcripts
		transcript <- dataf[t,]
		for (i in 1:nchar(transcript)) {

		}
		#call plot function
		plot(transcript, distribution_type)
	}
}

plot <- function(
	transcript = NULL,
	distribution_type = NULL) {

}

opstr <- generate_string(1000)
chopped_up <- create_cuts(operating_str=opstr, filterby=100, cuts=15)
transcripts <- create_transcripts(chopped_up, length=10)












