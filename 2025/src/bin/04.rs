advent_of_code::solution!(4);

#[repr(u8)]
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Tile {
    PaperTowel = b'@',
    Nothing = b'.',
}

impl From<u8> for Tile {
    fn from(byte: u8) -> Self {
        match byte {
            b'@' => Tile::PaperTowel,
            _ => Tile::Nothing, // Treat anything else as Nothing
        }
    }
}

pub fn part_one(input: &str) -> Option<u64> {
    let grid: Vec<Vec<Tile>> = input
        .lines()
        .map(|line| line.bytes().map(Tile::from).collect())
        .collect();

    let rows = grid.len();
    let cols = grid[0].len();
    let mut total = 0;

    for (r, row) in grid.iter().enumerate() {
        for (c, &tile) in row.iter().enumerate() {
            if tile == Tile::Nothing {
                continue;
            }

            let mut count = 0;

            'neighbors: for dr in -1..=1 {
                for dc in -1..=1 {
                    if dr == 0 && dc == 0 {
                        continue;
                    }

                    // This handles bounds checking efficiently.
                    let nr = r.wrapping_add_signed(dr);
                    let nc = c.wrapping_add_signed(dc);

                    if nr < rows && nc < cols && grid[nr][nc] == Tile::PaperTowel {
                        count += 1;
                        if count >= 4 {
                            break 'neighbors;
                        }
                    }
                }
            }

            if count < 4 {
                total += 1;
            }
        }
    }

    Some(total)
}

pub fn part_two(input: &str) -> Option<u64> {
    let mut grid: Vec<Vec<Tile>> = input
        .lines()
        .map(|line| line.bytes().map(Tile::from).collect())
        .collect();

    if grid.is_empty() {
        return Some(0);
    }

    let rows = grid.len();
    let cols = grid[0].len();

    let mut to_remove = Vec::with_capacity(rows * cols / 4);
    let mut total = 0;

    loop {
        to_remove.clear();

        for (r, row) in grid.iter().enumerate() {
            for (c, &tile) in row.iter().enumerate() {
                if tile == Tile::Nothing {
                    continue;
                }

                let mut count = 0;

                'neighbors: for dr in -1..=1 {
                    for dc in -1..=1 {
                        if dr == 0 && dc == 0 {
                            continue;
                        }

                        // This handles bounds checking efficiently.
                        let nr = r.wrapping_add_signed(dr);
                        let nc = c.wrapping_add_signed(dc);

                        if nr < rows && nc < cols && grid[nr][nc] == Tile::PaperTowel {
                            count += 1;
                            if count >= 4 {
                                break 'neighbors;
                            }
                        }
                    }
                }

                if count < 4 {
                    to_remove.push((r, c));
                }
            }
        }

        if to_remove.is_empty() {
            break;
        }

        for &(r, c) in &to_remove {
            grid[r][c] = Tile::Nothing;
            total += 1;
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
        assert_eq!(result, Some(13));
    }

    #[test]
    fn test_part_two() {
        let result = part_two(&advent_of_code::template::read_file("examples", DAY));
        assert_eq!(result, Some(43));
    }
}
