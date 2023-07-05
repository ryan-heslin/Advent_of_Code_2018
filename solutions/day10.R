simulate <- function(positions, velocities) {
    last_area <- Inf
    i <- 0

    repeat ({
        positions <- positions + velocities
        # Area method recommended by subreddit
        area <- as.numeric(max(positions[, 1]) - min(positions[, 1])) *
            (max(positions[, 2]) - min(positions[, 2]))
        if (area > last_area) {
            display(last_positions)
            return(i)
        }
        last_area <- area
        last_positions <- positions
        i <- i + 1
    })
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

    cat(string, "\n")
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
