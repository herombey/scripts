use std::env;
use std::fs::File;
use std::io::{self, BufRead, BufReader, Write};
use std::collections::HashSet;
use std::sync::Mutex;
use rayon::prelude::*;

fn process_chunk(chunk: String) -> HashSet<String> {
    chunk.lines().map(String::from).collect()
}

fn process_file(file: &str) -> io::Result<HashSet<String>> {
    let file = File::open(file)?;
    let reader = BufReader::new(file);
    let mut set = HashSet::new();

    for chunk in reader.lines().map(|line| line.unwrap()) {
        set.extend(process_chunk(chunk));
    }

    Ok(set)
}

fn combine_text_files(files: Vec<String>) -> io::Result<()> {
    let master_list = Mutex::new(HashSet::new());

    files.par_iter().map(|file| {
        process_file(file).map(|file_set| {
            let mut master = master_list.lock().unwrap();
            master.extend(file_set);
        })
    }).collect::<Result<Vec<_>, _>>()?;

    let mut master_file = File::create("master.txt")?;
    let master = master_list.lock().unwrap();

    for entry in master.iter() {
        writeln!(master_file, "{}", entry)?;
    }

    println!("Combining and deduplicating completed. Master list saved to master.txt.");
    Ok(())
}

fn main() {
    let args: Vec<String> = env::args().skip(1).collect();
    if args.is_empty() {
        eprintln!("Usage: program <file1> <file2> ...");
        std::process::exit(1);
    }

    if let Err(e) = combine_text_files(args) {
        eprintln!("Error: {}", e);
        std::process::exit(1);
    }
}
