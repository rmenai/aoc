advent_of_code::solution!(8);

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct Vec3 {
    pub x: usize,
    pub y: usize,
    pub z: usize,
}

#[derive(Debug, Eq, PartialEq, PartialOrd, Ord)]
struct Edge {
    distance_sq: u64,
    from_index: usize,
    to_index: usize,
}

impl Vec3 {
    fn dist_sq(&self, other: &Vec3) -> u64 {
        let dx = self.x.abs_diff(other.x) as u64;
        let dy = self.y.abs_diff(other.y) as u64;
        let dz = self.z.abs_diff(other.z) as u64;

        (dx * dx) + (dy * dy) + (dz * dz)
    }
}

struct UnionFind {
    parent: Vec<usize>,
    size: Vec<usize>,
}

impl UnionFind {
    fn new(n: usize) -> Self {
        let parent = (0..n).collect();
        let size = vec![1; n];

        UnionFind { parent, size }
    }

    fn find(&mut self, i: usize) -> usize {
        if self.parent[i] != i {
            self.parent[i] = self.find(self.parent[i]);
        }

        self.parent[i]
    }

    fn union(&mut self, i: usize, j: usize) {
        let root_i = self.find(i);
        let root_j = self.find(j);

        if root_i != root_j {
            self.parent[root_i] = root_j;
            self.size[root_j] += self.size[root_i];
        }
    }
}

fn parse(input: &str) -> Vec<Vec3> {
    input
        .lines()
        .map(|line| {
            let mut parts = line
                .split(',')
                .map(|s| s.trim().parse::<usize>().expect("Invalid number"));

            Vec3 {
                x: parts.next().expect("Missing X"),
                y: parts.next().expect("Missing Y"),
                z: parts.next().expect("Missing Z"),
            }
        })
        .collect()
}

pub fn part_one(input: &str) -> Option<u64> {
    let points = parse(input);
    let mut edges = Vec::new();

    for i in 0..points.len() {
        for j in (i + 1)..points.len() {
            let dist = points[i].dist_sq(&points[j]);

            edges.push(Edge {
                distance_sq: dist,
                from_index: i,
                to_index: j,
            });
        }
    }

    edges.sort_unstable();

    let mut dsu = UnionFind::new(points.len());

    for edge in edges.iter().take(points.len()) {
        dsu.union(edge.from_index, edge.to_index);
    }

    let mut circuit_sizes: Vec<u64> = dsu
        .parent
        .iter()
        .enumerate()
        .filter(|&(i, p)| i == *p)
        .map(|(i, _)| dsu.size[i] as u64)
        .collect();

    circuit_sizes.sort_unstable_by(|a, b| b.cmp(a));

    let result = circuit_sizes[0] * circuit_sizes[1] * circuit_sizes[2];
    Some(result)
}

pub fn part_two(input: &str) -> Option<u64> {
    let points = parse(input);
    let mut edges = Vec::new();

    for i in 0..points.len() {
        for j in (i + 1)..points.len() {
            let dist = points[i].dist_sq(&points[j]);

            edges.push(Edge {
                distance_sq: dist,
                from_index: i,
                to_index: j,
            });
        }
    }

    edges.sort_unstable();

    let mut dsu = UnionFind::new(points.len());
    let mut groups_count = points.len();

    for edge in edges {
        let root_a = dsu.find(edge.from_index);
        let root_b = dsu.find(edge.to_index);

        if root_a != root_b {
            dsu.union(edge.from_index, edge.to_index);
            groups_count -= 1;

            if groups_count == 1 {
                let x1 = points[edge.from_index].x as u64;
                let x2 = points[edge.to_index].x as u64;
                return Some(x1 * x2);
            }
        }
    }

    None
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part_one() {
        let result = part_one(&advent_of_code::template::read_file("examples", DAY));
        assert_eq!(result, Some(45));
    }

    #[test]
    fn test_part_two() {
        let result = part_two(&advent_of_code::template::read_file("examples", DAY));
        assert_eq!(result, Some(25272));
    }
}
