advent_of_code::solution!(17);

use std::collections::HashMap;
use z3::ast::{Ast, BV};
use z3::{Config, Context, Optimize};

fn parse(input: &str) -> (HashMap<char, u32>, Vec<u8>) {
    let mut registers = HashMap::new();
    let mut program = Vec::new();

    for line in input.lines().map(|l| l.trim()).filter(|l| !l.is_empty()) {
        if line.starts_with("Register") {
            let (reg, value) = line.split_once(": ").unwrap();
            let reg = reg.replace("Register ", "").chars().collect::<Vec<char>>()[0];
            let value = value.parse().expect("Invalid number");
            registers.insert(reg, value);
        } else {
            let (_, values) = line.split_once(": ").unwrap();

            program = values
                .split(",")
                .map(|s| s.parse().expect("Invalid number"))
                .collect::<Vec<u8>>()
        }
    }

    (registers, program)
}

fn run(registers: &mut HashMap<char, u32>, program: &[u8]) -> String {
    let instructions: Vec<(u8, u8)> = program.chunks_exact(2).map(|w| (w[0], w[1])).collect();
    let mut output: Vec<String> = Vec::new();
    let mut ptr = 0;

    fn combo(registers: &HashMap<char, u32>, operand: u8) -> u32 {
        match operand {
            0 => 0,
            1 => 1,
            2 => 2,
            3 => 3,
            4 => *registers.get(&'A').unwrap(),
            5 => *registers.get(&'B').unwrap(),
            6 => *registers.get(&'C').unwrap(),
            _ => 0,
        }
    }

    while let Some(&(opcode, operand)) = instructions.get(ptr) {
        match opcode {
            0 => {
                let a = registers.get(&'A').unwrap();
                let b = combo(registers, operand);
                registers.insert('A', a >> b);
            }
            1 => {
                let a = registers.get(&'B').unwrap();
                registers.insert('B', a ^ operand as u32);
            }
            2 => {
                let b = combo(registers, operand);
                registers.insert('B', b % 8);
            }
            3 => {
                let a = *registers.get(&'A').unwrap();
                let b = combo(registers, operand) as usize;
                if a != 0 {
                    ptr = b;
                    continue;
                }
            }
            4 => {
                let a = registers.get(&'B').unwrap();
                let b = registers.get(&'C').unwrap();
                registers.insert('B', a ^ b);
            }
            5 => {
                let a = combo(registers, operand);
                output.push((a % 8).to_string());
            }
            6 => {
                let a = registers.get(&'A').unwrap();
                let b = combo(registers, operand);
                registers.insert('B', a >> b);
            }
            7 => {
                let a = registers.get(&'A').unwrap();
                let b = combo(registers, operand);
                registers.insert('C', a >> b);
            }
            _ => (),
        }

        ptr += 1;
    }

    output.join(",")
}

pub fn part_one(input: &str) -> Option<String> {
    let (mut registers, program) = parse(input);
    Some(run(&mut registers, &program))
}

pub fn part_two(input: &str) -> Option<u64> {
    let (registers, program) = parse(input);
    let instructions: Vec<(u8, u8)> = program.chunks_exact(2).map(|w| (w[0], w[1])).collect();
    let n = program.len();

    let cfg = Config::new();
    let ctx = Context::new(&cfg);

    let consts = [
        BV::from_u64(&ctx, 0, 64),
        BV::from_u64(&ctx, 1, 64),
        BV::from_u64(&ctx, 2, 64),
        BV::from_u64(&ctx, 3, 64),
        BV::new_const(&ctx, "a", 64),
        BV::new_const(&ctx, "b", 64),
        BV::new_const(&ctx, "c", 64),
    ];

    fn unravel(program: &[(u8, u8)], ptr: usize, n: u8) -> Vec<Vec<(u8, u8)>> {
        let mut path: Vec<(u8, u8)> = vec![];
        let mut ptr = ptr;
        let mut n = n;

        while ptr < program.len() {
            match program[ptr].0 {
                3 => break,
                5 => n -= 1,
                _ => (),
            }

            path.push(program[ptr]);
            ptr += 1;
        }

        if n > 0 && program[ptr].0 == 3 {
            let mut paths = vec![];

            let left = vec![(3, 0)];
            let right = vec![(3, 1)];

            for p in unravel(program, program[ptr].1 as usize / 2, n) {
                paths.push([path.clone(), right.clone(), p.clone()].concat());
                paths.push([path.clone(), left.clone(), p.clone()].concat());
            }

            return paths;
        }

        vec![path]
    }

    fn get_operand_value<'a>(
        operand: u8,
        reg_a: &BV<'a>,
        reg_b: &BV<'a>,
        reg_c: &BV<'a>,
        consts: &[BV<'a>],
    ) -> BV<'a> {
        match operand {
            0 => consts[0].clone(),
            1 => consts[1].clone(),
            2 => consts[2].clone(),
            3 => consts[3].clone(),
            4 => reg_a.clone(),
            5 => reg_b.clone(),
            6 => reg_c.clone(),
            _ => consts[0].clone(),
        }
    }

    let target_values: Vec<BV> = program
        .iter()
        .map(|&x| BV::from_u64(&ctx, x as u64, 64))
        .collect();

    for path in unravel(&instructions, 0, n as u8) {
        let solver = Optimize::new(&ctx);

        let mut reg_a = consts[4].clone();
        let mut reg_b = BV::from_u64(&ctx, *registers.get(&'B').unwrap() as u64, 64);
        let mut reg_c = BV::from_u64(&ctx, *registers.get(&'C').unwrap() as u64, 64);

        let mut outputs: Vec<BV> = Vec::new();

        for (opcode, operand) in path {
            let op_val = get_operand_value(operand, &reg_a, &reg_b, &reg_c, &consts);

            match opcode {
                0 => {
                    reg_a = reg_a.bvlshr(&op_val);
                }
                1 => {
                    reg_b = reg_b.bvxor(&BV::from_u64(&ctx, operand as u64, 64));
                }
                2 => {
                    reg_b = op_val.bvurem(&BV::from_u64(&ctx, 8, 64));
                }
                3 => match operand {
                    0 => solver.assert(&reg_a.clone()._eq(&consts[0].clone())),
                    1 => solver.assert(&reg_a.clone()._eq(&consts[0].clone()).not()),
                    _ => {}
                },
                4 => {
                    reg_b = reg_b.bvxor(&reg_c);
                }
                5 => {
                    outputs.push(op_val.bvurem(&BV::from_u64(&ctx, 8, 64)));
                }
                6 => {
                    reg_b = reg_a.bvlshr(&op_val);
                }
                7 => {
                    reg_c = reg_a.bvlshr(&op_val);
                }
                _ => (),
            }
        }

        for (out, target) in outputs.iter().zip(target_values.iter()) {
            solver.assert(&out._eq(target));
        }

        solver.minimize(&reg_a);

        match solver.check(&[]) {
            z3::SatResult::Sat => {
                if let Some(model) = solver.get_model() {
                    let a = model.eval(&consts[4], true).unwrap().as_u64().unwrap();
                    return Some(a);
                }
            }
            _ => continue,
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
        assert_eq!(result, Some(String::from("5,7,3,0")));
    }

    #[test]
    fn test_part_two() {
        let result = part_two(&advent_of_code::template::read_file("examples", DAY));
        assert_eq!(result, Some(117440));
    }
}
