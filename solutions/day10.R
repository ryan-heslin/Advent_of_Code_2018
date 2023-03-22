simulate <- function(positions, velocities) {
    last_average <- -Inf
    last_area <- Inf
    attrs <- list(
        Size = nrow(positions), Labels = dimnames(positions)[[1]], Diag = FALSE,
        Upper = FALSE, method = "euclidean", call = quote(dist(x, method = "euclidean"))
    )
    # TODO binary search for min average distance like a civilized person
    i <- 0
    while (TRUE) {
        positions <- positions + velocities
        distances <- dist(positions, method = "euclidean")
        # distances <- dist2(positions, attrs)
        # Area method recommended by subreddit
        average <- mean(distances)
        area <- as.numeric(max(positions[, 1]) - min(positions[, 1])) * (max(positions[, 2]) - min(positions[, 2]))
        if (area > last_area) {
            display(last_positions)
            return(i)
        }
        last_area <- area
        last_average <- average
        last_positions <- positions
        i <- i + 1
    }
}
display <- function(X) {
    lower <- min(X)
    X <- X - lower + 1
    extent <- max(X)
    mat <- matrix(".", nrow = extent, ncol = extent)
    mat[cbind(X[, 2], X[, 1])] <- "#"
    string <- asplit(mat, MARGIN = 2) |>
        do.call(what = paste0) |>
        paste("\n")

    cat(string[-(1:40)])
    cat("\n")
}

dist2 <- function(X, attrs) {
    .Call(C_Cdist, X, "euclidean", attrs, 2)
}


raw_input <- readLines("inputs/day10.txt")
data <- gsub("velocity=", ",", raw_input) |>
    gsub(pattern = "[^-0-9,]+", replacement = "") |>
    strsplit(",") |>
    do.call(what = rbind) |>
    `class<-`("integer")

positions <- data[, 1:2]
velocities <- data[, 3:4]
part2 <- simulate(positions, velocities)
print(part2)
