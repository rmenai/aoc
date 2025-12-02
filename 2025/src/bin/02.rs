advent_of_code::solution!(2);

pub fn part_one(input: &str) -> Option<u64> {
    let mut sum = 0;

    for range_str in input.trim().split(',') {
        if let Some((start_str, end_str)) = range_str.trim().split_once('-') {
            let start: u64 = start_str.parse().expect("Failed to parse start");
            let end: u64 = end_str.parse().expect("Failed to parse end");

            for num in start..=end {
                if let Some(log) = num.checked_ilog10() {
                    let digits = log + 1;

                    if digits % 2 == 0 {
                        let divisor = 10_u64.pow(digits / 2);

                        let first_half = num / divisor;
                        let second_half = num % divisor;

                        if first_half == second_half {
                            sum += num;
                        }
                    }
                }
            }
        }
    }

    Some(sum)
}

pub fn part_two(input: &str) -> Option<u64> {
    let mut sum = 0;

    for range_str in input.trim().split(',') {
        if let Some((start_str, end_str)) = range_str.trim().split_once('-') {
            let start: u64 = start_str.parse().expect("Failed to parse start");
            let end: u64 = end_str.parse().expect("Failed to parse end");

            for num in start..=end {
                if is_invalid_id(num) {
                    sum += num;
                }
            }
        }
    }

    Some(sum)
}

fn is_invalid_id(num: u64) -> bool {
    let s = num.to_string();
    let n = s.len();

    // We stop at n/2 because the pattern must appear at least twice
    for p in 1..=(n / 2) {
        if n.is_multiple_of(p) && s[..n - p] == s[p..] {
            return true;
        }
    }

    false
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part_one() {
        let result = part_one(&advent_of_code::template::read_file("examples", DAY));
        assert_eq!(result, Some(1227775554));
    }

    #[test]
    fn test_part_two() {
        let result = part_two(&advent_of_code::template::read_file("examples", DAY));
        assert_eq!(result, Some(4174379265));
    }
}
