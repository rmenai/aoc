advent_of_code::solution!(7);

use std::mem;

#[repr(u8)]
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Tile {
    Splitter = b'^',
    Ray = b'S',
    Nothing = b'.',
}

impl From<u8> for Tile {
    fn from(byte: u8) -> Self {
        match byte {
            b'S' => Tile::Ray,
            b'^' => Tile::Splitter,
            _ => Tile::Nothing, // Treat anything else as Nothing
        }
    }
}

fn parse(input: &str) -> Vec<Vec<Tile>> {
    input
        .lines()
        .map(|line| line.bytes().map(Tile::from).collect())
        .collect()
}

pub fn part_one(input: &str) -> Option<u64> {
    let mut grid: Vec<Vec<Tile>> = parse(input);
    let n = grid.len();
    let m = grid[0].len();

    let mut count = 0;

    for i in 0..(n - 1) {
        for j in 0..m {
            if grid[i][j] == Tile::Ray {
                if grid[i + 1][j] == Tile::Splitter {
                    count += 1;
                    grid[i + 1][j - 1] = Tile::Ray;

                    grid[i + 1][j + 1] = Tile::Ray;
                } else {
                    grid[i + 1][j] = Tile::Ray;
                }
            }
        }
    }

    Some(count)
}

pub fn part_two(input: &str) -> Option<u64> {
    let grid: Vec<Vec<Tile>> = parse(input);
    let m = grid[0].len();

    let mut prev = vec![0; m];
    let mut curr = vec![0; m];

    for j in 0..m {
        if grid[0][j] == Tile::Ray {
            prev[j] = 1;
        }
    }

    for row in grid.iter().skip(1) {
        curr.fill(0);

        for j in 0..m {
            if row[j] == Tile::Splitter {
                curr[j - 1] += prev[j];
                curr[j + 1] += prev[j];
            } else {
                curr[j] += prev[j];
            }
        }

        mem::swap(&mut prev, &mut curr);
    }

    Some(prev.iter().sum())
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part_one() {
        let result = part_one(&advent_of_code::template::read_file("examples", DAY));
        assert_eq!(result, Some(21));
    }

    #[test]
    fn test_part_two() {
        let result = part_two(&advent_of_code::template::read_file("examples", DAY));
        assert_eq!(result, Some(40));
    }
}
