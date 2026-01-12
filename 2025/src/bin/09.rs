advent_of_code::solution!(9);

fn parse(input: &str) -> Vec<(usize, usize)> {
    input
        .lines()
        .filter_map(|line| {
            let (l, r) = line.split_once(',')?;

            let l = l.trim().parse::<usize>().ok()?;
            let r = r.trim().parse::<usize>().ok()?;

            Some((l, r))
        })
        .collect()
}

pub fn part_one(input: &str) -> Option<u64> {
    let points: Vec<(usize, usize)> = parse(input);
    let mut corners: Vec<u64> = Vec::new();

    for i in 0..points.len() {
        for j in (i + 1)..points.len() {
            let width = points[i].0.abs_diff(points[j].0) + 1;
            let height = points[i].1.abs_diff(points[j].1) + 1;
            let area = width * height;

            corners.push(area as u64);
        }
    }

    corners.sort_unstable_by(|a, b| b.cmp(a));
    corners.first().copied()
}

pub fn part_two(input: &str) -> Option<u64> {
    None
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part_one() {
        let result = part_one(&advent_of_code::template::read_file("examples", DAY));
        assert_eq!(result, Some(50));
    }

    #[test]
    fn test_part_two() {
        let result = part_two(&advent_of_code::template::read_file("examples", DAY));
        assert_eq!(result, None);
    }
}
