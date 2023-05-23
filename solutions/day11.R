hundreds <- function(x) (x %/% 100) %% 10

to_string <- function(x) paste(x, collapse = ",")

find_greatest <- function(grid, size, to_beat = -Inf) {
    if (size >= nrow(grid)) {
        return(list(sum(grid), c(1, 1)))
    }
    best <- -Inf
    best_coord <- NULL
    extent <- seq(1, size)
    mask <- expand.grid(row = extent, col = extent) |>
        as.matrix()
    start_cols <- mask[, 2]
    iterations <- seq(1, nrow(grid) - size)

    for (row in iterations) {
        for (col in iterations) {
            this_sum <- sum(grid[mask])
            if (this_sum > best) {
                best <- this_sum
                # Top left
                best_coord <- mask[1, ]
            }
            mask[, 2] <- mask[, 2] + 1
        }
        mask[, 2] <- start_cols
        mask[, 1] <- mask[, 1] + 1
    }
    list(best, best_coord)
}

find_maximum <- function(grid) {
    extent <- nrow(grid)
    sizes <- seq(1, extent)
    best <- -Inf

    for (size in sizes) {
        this_result <- find_greatest(grid, size, best)
        value <- this_result[[1]]
        # Reddit-suggested optimization
        if (value < 0) break
        if (value > best) {
            best <- value
            best_result <- c(this_result[[2]], size)
        }
    }
    best_result
}


grid_serial <- 4151
grid <- matrix(0, nrow = 300, ncol = 300)
rack_id <- col(grid) + 10
grid <- hundreds((rack_id * row(grid) + grid_serial) * rack_id) - 5
part1 <- find_greatest(grid, 3)[[2]]
rev(part1) |>
    to_string() |>
    cat("\n")

result <- find_maximum(grid)
result[1:2] <- result[2:1]
names(result) <- NULL
to_string(result) |>
    cat("\n")
