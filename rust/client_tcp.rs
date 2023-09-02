use std::env::args;
use std::fs::File;
use std::io::{Read, Write};
use std::net::TcpStream;
use std::thread;

fn main() -> std::io::Result<()> {
    let mut handles = Vec::new();
    let arguments = args().collect::<Vec<String>>();

    let output_path = arguments[1].clone();
    let addresses = arguments[2..].to_vec();

    for addr in addresses {
        let ip = addr.split(":").collect::<Vec<&str>>()[0];
        let file_path = format!("{output_path}{ip}.bin");

        handles.push(thread::spawn(|| {
            handle_connection(addr, file_path).unwrap_or_else(|err| println!("{err}"));
        }));
    }

    for handle in handles {
        handle.join().unwrap_or_else(|err| println!("{err:?}"));
    }

    Ok(())
}

fn handle_connection(addr: String, file_path: String) -> std::io::Result<()> {
    let mut client = TcpStream::connect(addr)?;

    let mut file = File::create(file_path)?;
    let mut buf = [0; 65536];

    loop {
        let num_bytes = client.read(&mut buf)?;

        if num_bytes == 0 {
            break;
        }

        file.write_all(&buf[..num_bytes])?;
        file.sync_data()?;
    }

    Ok(())
}
