advent_of_code::solution!(16);

use std::cmp::Reverse;
use std::collections::{BinaryHeap, HashMap, HashSet, VecDeque};

pub fn part_one(input: &str) -> Option<u64> {
    let maze: Vec<Vec<char>> = input.lines().map(|line| line.chars().collect()).collect();
    let (n, m) = (maze.len(), maze.first()?.len());
    let dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)];

    const INF: u64 = u64::MAX;
    const TURN_PENALTY: u64 = 1000;
    const MOVE_COST: u64 = 1;

    let mut heap = BinaryHeap::new();
    let mut dist = vec![vec![INF; m]; n];

    dist[n - 2][1] = 0;
    heap.push(Reverse((0, n - 2, 1, 0, 1)));

    while let Some(Reverse((d, i, j, ri, rj))) = heap.pop() {
        if d != dist[i][j] {
            continue;
        }

        if maze[i][j] == 'E' {
            return Some(d);
        }

        for (di, dj) in dirs {
            let (ni, nj) = (i as i32 + di, j as i32 + dj);
            if 0 <= ni && 0 <= nj && ni < n as i32 && nj < m as i32 {
                let (ni, nj) = (ni as usize, nj as usize);
                if maze[ni][nj] != '#' {
                    let mut nd = d + MOVE_COST;
                    if ri * di + rj * dj == 0 {
                        nd += TURN_PENALTY;
                    }

                    if dist[ni][nj] >= nd {
                        dist[ni][nj] = nd;
                        heap.push(Reverse((nd, ni, nj, di, dj)));
                    }
                }
            }
        }
    }

    None
}

pub fn part_two(input: &str) -> Option<u64> {
    let maze: Vec<Vec<char>> = input.lines().map(|line| line.chars().collect()).collect();
    let (n, m) = (maze.len(), maze.first()?.len());
    let dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)];

    const INF: u64 = u64::MAX;
    const TURN_PENALTY: u64 = 1000;
    const MOVE_COST: u64 = 1;

    let mut heap = BinaryHeap::new();
    let mut pred: HashMap<_, HashSet<_>> = HashMap::new();
    let mut cost = vec![vec![[INF; 4]; m]; n];

    cost[n - 2][1][0] = 0;
    heap.push(Reverse((0, n - 2, 1, 0)));
    pred.insert((n - 2, 1, 0), HashSet::new());

    while let Some(Reverse((c, i, j, d))) = heap.pop() {
        if c != cost[i][j][d] {
            continue;
        }

        for (nd, (di, dj)) in dirs.iter().enumerate() {
            let (ni, nj) = (i as i32 + di, j as i32 + dj);

            if 0 <= ni && 0 <= nj && ni < n as i32 && nj < m as i32 {
                let (ni, nj) = (ni as usize, nj as usize);
                if maze[ni][nj] != '#' {
                    let mut nc = c + MOVE_COST;

                    if nd != d {
                        nc += TURN_PENALTY;
                    }

                    if nc < cost[ni][nj][nd] {
                        cost[ni][nj][nd] = nc;
                        heap.push(Reverse((nc, ni, nj, nd)));
                        pred.insert((ni, nj, nd), HashSet::from([(i, j, d)]));
                    } else if nc == cost[ni][nj][nd] {
                        pred.entry((ni, nj, nd)).and_modify(|entry| {
                            entry.insert((i, j, d));
                        });
                    }
                }
            }
        }
    }

    let min_cost = (0..4)
        .filter(|&d| cost[1][m - 2][d] != INF)
        .map(|d| cost[1][m - 2][d])
        .min()
        .unwrap_or(INF);

    if min_cost == INF {
        return Some(0);
    }

    let mut queue = VecDeque::new();
    let mut visited_states = HashSet::new();
    let mut unique_cells = HashSet::new();

    // Start BFS only from endpoint states with minimal cost
    for d in 0..4 {
        if cost[1][m - 2][d] == min_cost {
            queue.push_back((1, m - 2, d));
            visited_states.insert((1, m - 2, d));
            unique_cells.insert((1, m - 2));
        }
    }

    while let Some((i, j, d)) = queue.pop_front() {
        if let Some(preds) = pred.get(&(i, j, d)) {
            for &(pi, pj, pd) in preds {
                if visited_states.insert((pi, pj, pd)) {
                    queue.push_back((pi, pj, pd));
                    unique_cells.insert((pi, pj));
                }
            }
        }
    }

    Some(unique_cells.len() as u64)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part_one() {
        let result = part_one(&advent_of_code::template::read_file("examples", DAY));
        assert_eq!(result, Some(11048));
    }

    #[test]
    fn test_part_two() {
        let result = part_two(&advent_of_code::template::read_file("examples", DAY));
        assert_eq!(result, Some(64));
    }
}
