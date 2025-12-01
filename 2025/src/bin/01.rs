advent_of_code::solution!(1);

pub fn part_one(input: &str) -> Option<u64> {
    let instructions: Vec<i64> = input
        .lines()
        .filter_map(|line| {
            let line = line.trim();
            if line.is_empty() {
                return None;
            }

            if line.len() < 2 {
                return None;
            }

            let (dir, num_str) = line.split_at(1);
            let num: i64 = num_str.parse().ok()?;

            match dir {
                "R" => Some(num),
                "L" => Some(-num),
                _ => None,
            }
        })
        .collect();

    let mut sum: i64 = 50; // Start position
    let mut count: u64 = 0;

    for instruction in instructions {
        sum += instruction;
        sum = sum.rem_euclid(100);

        if sum == 0 {
            count += 1;
        }
    }

    Some(count)
}

pub fn part_two(input: &str) -> Option<u64> {
    let instructions: Vec<i64> = input
        .lines()
        .filter_map(|line| {
            let line = line.trim();
            if line.is_empty() {
                return None;
            }

            if line.len() < 2 {
                return None;
            }

            let (dir, num_str) = line.split_at(1);
            let num: i64 = num_str.parse().ok()?;

            match dir {
                "R" => Some(num),
                "L" => Some(-num),
                _ => None,
            }
        })
        .collect();

    let mut sum: i64 = 50; // Start position
    let mut count: u64 = 0;

    for instruction in instructions {
        let dist = instruction.abs();
        let dir = instruction.signum();

        count += (dist / 100) as u64;

        let rem = dist % 100;

        for _ in 0..rem {
            sum += dir;
            sum = sum.rem_euclid(100);

            if sum == 0 {
                count += 1;
            }
        }
    }

    Some(count)
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
        assert_eq!(result, Some(6));
    }
}
