advent_of_code::solution!(6);

fn parse(input: &str) -> Vec<(Vec<u64>, char)> {
    let lines: Vec<&str> = input.lines().filter(|l| !l.is_empty()).collect();
    let (ops_str, grid_strs) = lines.split_last().expect("Input empty");

    let rows: Vec<Vec<u64>> = grid_strs
        .iter()
        .map(|line| {
            line.split_whitespace()
                .filter_map(|n| n.parse().ok())
                .collect()
        })
        .collect();

    let ops: Vec<char> = ops_str
        .split_whitespace()
        .filter_map(|s| s.chars().next())
        .collect();

    (0..ops.len())
        .map(|i| {
            let col = rows.iter().map(|row| row[i]).collect();
            (col, ops[i])
        })
        .collect()
}

fn parse2(input: &str) -> Vec<(Vec<u64>, char)> {
    let lines: Vec<&str> = input.lines().filter(|l| !l.is_empty()).collect();
    if lines.is_empty() {
        return Vec::new();
    }

    let height = lines.len();
    let width = lines.iter().map(|l| l.len()).max().unwrap_or(0);
    let grid: Vec<Vec<char>> = lines
        .iter()
        .map(|l| format!("{:<width$}", l).chars().collect())
        .collect();

    let mut exercises = Vec::new();
    let mut current_nums = Vec::new();
    let mut current_op = None;

    for x in 0..width {
        let is_separator = (0..height).all(|y| grid[y][x] == ' ');

        if is_separator {
            if let Some(op) = current_op {
                if !current_nums.is_empty() {
                    exercises.push((current_nums.clone(), op));
                }
            }
            current_nums.clear();
            current_op = None;
            continue;
        }

        let mut num_str = String::new();
        for y in 0..height - 1 {
            let c = grid[y][x];
            if c.is_ascii_digit() {
                num_str.push(c);
            }
        }
        if let Ok(n) = num_str.parse::<u64>() {
            current_nums.push(n);
        }

        // 4. Extract Operator: Check the bottom row
        let bottom_char = grid[height - 1][x];
        if bottom_char == '+' || bottom_char == '*' {
            current_op = Some(bottom_char);
        }
    }

    // Capture the final problem (if no trailing separator)
    if let Some(op) = current_op
        && !current_nums.is_empty()
    {
        exercises.push((current_nums, op));
    }

    exercises
}

pub fn part_one(input: &str) -> Option<u64> {
    let exercices: Vec<(Vec<u64>, char)> = parse(input);
    let mut total = 0;

    for (nums, op) in exercices {
        match op {
            '*' => total += nums.iter().product::<u64>(),
            '+' => total += nums.iter().sum::<u64>(),
            _ => (),
        }
    }

    Some(total)
}

pub fn part_two(input: &str) -> Option<u64> {
    let exercices: Vec<(Vec<u64>, char)> = parse2(input);
    let mut total = 0;

    for (nums, op) in exercices {
        match op {
            '*' => total += nums.iter().product::<u64>(),
            '+' => total += nums.iter().sum::<u64>(),
            _ => (),
        }
    }

    Some(total)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part_one() {
        let result = part_one(&advent_of_code::template::read_file("examples", DAY));
        assert_eq!(result, Some(4277556));
    }

    #[test]
    fn test_part_two() {
        let result = part_two(&advent_of_code::template::read_file("examples", DAY));
        assert_eq!(result, Some(3263827));
    }
}
