advent_of_code::solution!(5);

fn parse(input: &str) -> (Vec<(u64, u64)>, Vec<u64>) {
    let (range_block, numbers_block) = input.split_once("\n\n").unwrap();

    let ranges: Vec<(u64, u64)> = range_block
        .lines()
        .map(|line| {
            let (start, end) = line.split_once('-').unwrap();
            (start.parse().unwrap(), end.parse().unwrap())
        })
        .collect();

    let numbers: Vec<u64> = numbers_block
        .lines()
        .map(|line| line.parse().unwrap())
        .collect();

    (ranges, numbers)
}

pub fn part_one(input: &str) -> Option<u64> {
    let (mut ranges, mut numbers) = parse(input);

    ranges.sort_unstable();
    numbers.sort_unstable();

    let mut nums = numbers.iter().peekable();
    let mut count = 0;

    for (start, end) in ranges {
        while let Some(&&n) = nums.peek() {
            if n < start {
                nums.next();
            } else if n <= end {
                count += 1;
                nums.next();
            } else {
                break;
            }
        }
    }

    Some(count)
}

pub fn part_two(input: &str) -> Option<u64> {
    let (mut ranges, _) = parse(input);
    ranges.sort_unstable();

    let mut range_iter = ranges.into_iter();
    let (mut cur_start, mut cur_end) = range_iter.next()?;
    let mut length = 0;

    for (next_start, next_end) in range_iter {
        if next_start > cur_end {
            length += cur_end - cur_start + 1;
            (cur_start, cur_end) = (next_start, next_end);
        } else {
            cur_end = cur_end.max(next_end);
        }
    }

    length += cur_end - cur_start + 1;
    Some(length)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part_one() {
        let result = part_one(&advent_of_code::template::read_file("examples", DAY));
        assert_eq!(result, Some(3));
    }

    #[test]
    fn test_part_two() {
        let result = part_two(&advent_of_code::template::read_file("examples", DAY));
        assert_eq!(result, Some(14));
    }
}
