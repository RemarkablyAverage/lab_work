#proof of concept


#generate random matrix in R with columns summing to 1 and have a
#bijection
# install.packages("ggplot2")
# install.packages("gplots")
# install.packages("Matrix")
# library("Matrix")
# library("ggplot2")
# library("gplots")

vector_create <- function(
	start = NULL,
	end = NULL,
	length = NULL) 
{

	ret_vector <- rep(0, length)
	for (x in (start:end)) {
		ret_vector[x] = 1
	}
	ret_vector
}

#generate transcripts + equiv class matrix
transcripts_classes <- function(
	equiv_classes = NULL, #integer
	transcripts = NULL, #integer
	start_vector = NULL, 
	end_vector = NULL
	) 
{

	for (i in (1:transcripts)) {
		if (i == 1) { #first row exception
			app <- vector_create(start = start_vector[i], end = end_vector[i], length = equiv_classes)
			ret_matrix <- matrix(app)
			ret_matrix <- t(ret_matrix)
		} else {
			app <- vector_create(start = start_vector[i], end = end_vector[i], length = equiv_classes)
			ret_matrix <- rbind(ret_matrix, app)
		}
	}
	ret_matrix
}


generate_distribution <- function(size = NULL) 
{
	#create some distribution??
}

probability_matrix <- function(transcript_class_matrix = NULL, uniform = TRUE) 
{
	if (uniform) {
		for (i in 1:nrow(transcript_class_matrix)) {
			if (i == 1) {
				norm_factor <- sum(transcript_class_matrix[i,])
				#can include sample distribution
				p <- 1/norm_factor * transcript_class_matrix[i,]
				ret_matrix <- matrix(p)
			} else {
				norm_factor <- sum(transcript_class_matrix[i,])
				#can include sample distribution
				p <- 1/norm_factor * transcript_class_matrix[i,]
				ret_matrix <- cbind(ret_matrix, p)
			}
		}
	} else {
		for (i in 1:nrow(transcript_class_matrix)) {
			if (i == 1) {
				#norm_factor <- sum(transcript_class_matrix[i,])
				#can include sample distribution
				#p <- #1/norm_factor * transcript_class_matrix[i,]
				#ret_matrix <- matrix(p)
			} else {
				#norm_factor <- sum(transcript_class_matrix[i,])
				#can include sample distribution
				#p <- #1/norm_factor * transcript_class_matrix[i,]
				#ret_matrix <- cbind(ret_matrix, p)
			}
		}
	}
	ret_matrix
}



reverse_pr_matrix <- function(probability_matrix = NULL, probability = FALSE) 
{
	#generate transcript vectors
	probability_matrix <- t(probability_matrix)
	if (!probability) {
		probability_matrix[which(probability_matrix != 0)] <- 1
	}
	#probability_matrix
	transcriptnames <- c()
	equivalencenames <- c()
	#set labels (transcripts_)
	for (i in 1:nrow(probability_matrix)) {
		temp <- paste0("t", i)
		transcriptnames <- append(transcriptnames, temp)
	}
	for (i in 1:ncol(probability_matrix)) {
		temp1 <- paste0("eqc", i)
		equivalencenames <- append(equivalencenames, temp1)
	}
	#tempdf <- data.frame(probability_matrix)
	rownames(probability_matrix) <- transcriptnames
	colnames(probability_matrix) <- equivalencenames
	#tempdf
	probability_matrix
}

plot_transcripts <- function(matrix = NULL, rowb = TRUE, colb = FALSE)
{
	if (sum(matrix[1,]) == 1) {
		heatmap.2(matrix, Rowv=FALSE, symm=TRUE,  trace="none", density.info="none", 
            dendrogram="none", xlab="X", ylab="Y",col=grey(seq(1,0,-0.01)), 
            tracecol="red", hline = NA, vline = NA)
	} else if (rowb && colb) {
		heatmap.2(matrix, Rowv=FALSE, symm=TRUE,  trace="both", density.info="none", 
	        dendrogram="none", xlab="X", ylab="Y",col=grey(seq(1,0,-0.01)), 
	        tracecol="red", hline = NA, vline = NA)
	} else if (rowb) {
		heatmap.2(matrix, Rowv=FALSE, symm=TRUE,  trace="row", density.info="none", 
            dendrogram="none", xlab="X", ylab="Y",col=grey(seq(1,0,-0.01)), 
            tracecol="red", hline = NA, vline = NA)
	} 
}

example_execution <- function() 
{

	equiv_classes <- 7
	transcripts <- 4
	start_vector <- c(1,2,4,5)
	end_vector <- c(4,6,5,7)

	tc <- transcripts_classes(equiv_classes = equiv_classes, transcripts = transcripts, 
		start_vector = start_vector, end_vector = end_vector)
	print(tc)
	pm <- probability_matrix(transcript_class_matrix = tc)
	print(pm)

	rm <- reverse_pr_matrix(pm)
	print(rm)
	plot_transcripts(rm)

}

example_execution2 <- function()
{
	equiv_classes <- 7
	transcripts <- 4
	start_vector <- c(1,2,4,5)
	end_vector <- c(4,6,5,7)

	tc <- transcripts_classes(equiv_classes = equiv_classes, transcripts = transcripts, 
		start_vector = start_vector, end_vector = end_vector)
	print(tc)
	pm <- probability_matrix(transcript_class_matrix = tc)
	print(pm)

	rm <- reverse_pr_matrix(pm, TRUE)
	print(rm)
	plot_transcripts(rm)
}

example_execution()


