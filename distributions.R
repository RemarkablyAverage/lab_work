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
		start <- as.integer(sample(0:i, 1) + 1)
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
			#print(length_loop)
		} else {
			length_loop <- length
		}
		if (length_loop > end_sample) {
			length_loop <- end_sample
		}
		rand <- as.integer(sample((1:end_sample), size=length_loop, replace=FALSE))
		for (i in rand) {
			individual_transcript <- paste(individual_transcript, (chop_df[i,]), sep = "|")
		}
		individual_transcript <- paste(individual_transcript, "|", sep="")
		transcripts <- c(transcripts, individual_transcript)
	}
	ret_df <- data.frame(transcripts = transcripts, stringsAsFactors = FALSE)
	ret_df
}

#plot transcripts as a function of y = e^-x and 
#use | as delminator
#use nchar as count
#assumptions 
#truncated @ q3, make length fit at q3 to make a discernable difference

plot_transcripts <- function(
	dataf = NULL,
	trunca = NULL, 
	lambda = NULL) {

	tol <- 1e-10

	if (is.null(lambda)) {
		lambda <- 1
	}

	#this is to find the truncation point for non fitted distribution
	if (is.null(trunca)) {
		maxl <- 0
		for (it in 1:nrow(dataf)){
			find_trunc <- as.character(dataf[it,][[1]])
			if (maxl < nchar(find_trunc)) {
				maxl <- nchar(find_trunc)
			}
		}
		trunca <- maxl
	}
	lambda <- find_lambda(x=trunca, tolerance=tol)

	for (t in 1:nrow(dataf)) {
		#iterate through all transcripts
		current_length <- nchar(as.character(dataf[t,][[1]]))
		transcript <- strsplit(as.character(dataf[t,][[1]]),"")
		reads <- c()
		read_str <- NULL
		#parse string
		for (base in transcript[[1]]) {
			if (base != "|") {
				read_str <- paste(read_str, base, sep="")
			} else {
				reads <- c(reads, read_str)
				read_str <- NULL
			}
		}
		plots(transcript=reads, distribution_type=distribution_type, lambda=lambda)
		plots(transcript=reads, distribution_type=distribution_type, lambda=find_lambda(x=current_length, tolerance=tol))
	}
}

plots <- function(
	transcript = NULL,
	distribution_type = NULL,
	lambda = NULL) {

	p <- NULL
	#construct indexes given frames | lmaomlmao remember freaking R indexes at 1
	index_vector <- c(0)
	curr <- 1
	for (i in 1:(length(transcript))) {
		read <- transcript[i]
		curr <- curr + nchar(read)
		index_vector <- c(index_vector, curr)
	}
	#generate x axis
	x_vector <- c()
	for (x in 1:(length(index_vector) - 1)) {
		x_vector <- c(x_vector, (index_vector[x + 1] - index_vector[x]))
	}
	#generate y axis
	y_vector <- c()
	for (y in 1:(length(index_vector) - 1)) {
		input <- (index_vector[y + 1] + index_vector[y])/2
		output <- exponential_dist(x=input, lambda=lambda)
		y_vector <- c(y_vector, output)
	}
	p <- barplot(y_vector, x_vector, space = 0)
}

exponential_dist <- function(
	x = NULL,
	lambda = NULL) {

	ret <- lambda * exp(1)^(-lambda*x)
	ret
}

find_lambda <- function(
	x = NULL, 
	tolerance = NULL) {

	lambda <- 0.00001
	while ((lambda * exp(1)^(-lambda*x)) > tolerance) {
		lambda <- lambda + 0.000001
	}
	lambda
}

opstr <- generate_string(1000)
chopped_up <- create_cuts(operating_str=opstr, filterby=100, cuts=15)
transcripts <- create_transcripts(chop_df=chopped_up, transcript_number=4, length=10, variation=TRUE)






