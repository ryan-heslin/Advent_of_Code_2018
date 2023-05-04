find_guard <- function(record) {
    guards <- data.frame(minute = seq(0, 59, 1))
    minutes <- rep(0, length.out = 60)
    for (row in asplit(record, MARGIN = 1)) {
        if (row[["event"]] == "falls asleep") {
            sleep_start <- row[["timestamp"]]
            # Most recent wakes up
        } else if (row[["event"]] == "wakes up") {
            sleep_end <- row[["timestamp"]]
            sleep_minutes <- seq(minutes(sleep_start), minutes(sleep_end) - 1) + 1
            guards[[current_guard]][sleep_minutes] <- guards[[current_guard]][sleep_minutes] + 1

            # New guard
        } else {
            guard <- row[["event"]]
            if (is.null(guards[[guard]])) {
                guards[[guard]] <- minutes
            }
            current_guard <- guard
        }
    }
    guards
}

minutes <- function(ts) as.integer(strftime(ts, format = "%M"))

sleepiest_guard <- function(guards) {
    sleepiest <- colSums(guards) |>
        which.max()
    minute <- which.max(guards[[sleepiest]]) - 1
    minute * as.numeric(colnames(guards)[[sleepiest]])
}


sleepiest_minute <- function(guards) {
    guards <- as.matrix(guards)
    sleepiest <- which(guards == max(guards), arr.ind = TRUE)
    id <- strtoi(colnames(guards)[[sleepiest[[2]]]])
    id * (sleepiest[[1]] - 1)
}

raw <- readLines("inputs/day4.txt") |>
    sort()

timestamps <- gsub("[][]", "", raw) |>
    gsub(pattern = "Guard #(\\d+) begins shift", replacement = "\\1") |>
    strsplit(split = "(?<=:\\d{2})\\s", perl = TRUE) |>
    do.call(what = rbind) |>
    as.data.frame() |>
    `colnames<-`(c("timestamp", "event"))

timestamps[["timestamp"]] <- as.POSIXct(timestamps[["timestamp"]])
sleep <- find_guard(timestamps)
part1 <- sleepiest_guard(sleep[, -1])
print(part1)

part2 <- sleepiest_minute(sleep[, -1])
print(part2)
