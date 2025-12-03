advent_of_code::solution!(3);

pub fn part_one(input: &str) -> Option<u64> {
    let mut res = 0;

    for line in input.lines() {
        let volts: Vec<u8> = line.bytes().map(|b| b - b'0').collect();

        let (idx, a) = volts[..volts.len() - 1]
            .iter()
            .enumerate()
            .rev() // We want the indice of the first max
            .max_by_key(|(_, v)| **v)
            .unwrap();

        let b = volts[(idx + 1)..].iter().max().unwrap();
        res += (*a as u64) * 10 + (*b as u64);
    }

    Some(res)
}

pub fn part_two(input: &str) -> Option<u64> {
    let mut res = 0;

    for line in input.lines() {
        let volts: Vec<u8> = line.bytes().map(|b| b - b'0').collect();

        let mut total = 0;
        let mut start = 0;
        for i in (1..=12).rev() {
            let end = volts.len() - (i - 1);

            let (idx, d) = volts[start..end]
                .iter()
                .enumerate()
                .rev()
                .max_by_key(|(_, v)| **v)
                .unwrap();

            total = total * 10 + (*d as u64);
            start += idx + 1;
        }

        res += total;
    }

    Some(res)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part_one() {
        let result = part_one(&advent_of_code::template::read_file("examples", DAY));
        assert_eq!(result, Some(357));
    }

    #[test]
    fn test_part_two() {
        let result = part_two(&advent_of_code::template::read_file("examples", DAY));
        assert_eq!(result, Some(3121910778619));
    }
}
