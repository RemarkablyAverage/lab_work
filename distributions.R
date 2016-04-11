# install.packages("ggplot2")
# install.packages("gplots")
# install.packages("Matrix")
# library("Matrix")



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
#ADD OVERLAP
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
	while (i <= cuts) {
		start <- as.integer(sample(0:i, 1) + 1)
		#small
		end <- as.integer(sample((10:20), 1))
		cut <- substr(operating_str, start, end)
		if (filter) {
			if (nchar(cut) < filterby && nchar(cut) > 0) {
				cuts_vector <- c(cuts_vector, cut)
				i <- i + 1
			} else {
				i <- i + 1
			}
		} else {
			cuts_vector <- c(cuts_vector, cut)
			i <- i + 1
		}
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
		rand <- as.integer(sample((1:end_sample), size=length_loop, replace=TRUE))
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
	t = NULL) {

	p <- NULL
	final_df <- NULL
	transcript <- strsplit(as.character(dataf[t,][[1]]),"")
	read_str <- NULL
	#parse string
	for (base in transcript[[1]]) {
		if (base != "|") {
			read_str <- paste(read_str, base, sep="")
		}
	}
	trunc <- create_df(transcript=read_str, type="trunc", limit=20)
	fit <- create_df(transcript=read_str, type="fit", fit=TRUE)
	final_df <- rbind(trunc, fit)
	p <- ggplot(final_df, aes(x, y)) + geom_line(aes(colour = type, group = type), linetype = "dotted")
	p <- p + geom_point(aes(colour = factor(type)))
	p
}

create_df <- function(
	transcript = NULL,
	type = NULL,
	fit = NULL,
	limit=NULL) {

	if (!is.null(fit)) {
		sigma <- 4
	} else {
		sigma <- 6
	} 

	#generate x 
	if (!is.null(limit)) {
		x_vector <- c(1:20)
	} else {
		x_vector <- c(1:nchar(transcript))
	}
	#generate y 
	y_vector <- c()
	for (y in 1:length(x_vector)) {
		output <- exponential_dist(x=y, sigma=sigma)
		y_vector <- c(y_vector, output)
	}
	y_vector <- y_vector / sum(y_vector)
	print("probabilities + sum")
	print(y_vector)
	print(sum(y_vector))
	data.frame(x = x_vector, y = y_vector, type=as.character(type))
}

exponential_dist <- function(
	x = NULL,
	sigma = NULL) {

	ret <- (x / (sigma^2) * exp(1)^(-x^2/(2*sigma^2)))
	ret
}

find_sigma <- function(
	x = NULL) {

	tolerance <- 1e-10
	sigma <- 0.00001
	while (x / (sigma^2) * exp(1)^(-x^2/(2*sigma^2)) > tolerance) {
		sigma <- sigma + 0.000001
	}
	sigma
}

opstr <- generate_string(100)
chopped_up <- create_cuts(operating_str=opstr, filter=TRUE, filterby=10, cuts=40)
transcripts <- create_transcripts(chop_df=chopped_up, transcript_number=4, length=5, variation=TRUE)
plot_transcripts(dataf=transcripts, t=1)





