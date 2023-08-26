use std::env::args;
use std::fs::File;
use std::io::{Read, Write};
use std::net::{TcpListener, TcpStream};
use std::thread;

fn main() -> std::io::Result<()> {
    let arguments = args().collect::<Vec<String>>();
    let server_ip = arguments[1].clone();
    let output_dir = arguments[2].clone();
    // let server_ip = "192.168.80.118:6969";
    // let output_dir = "./pointcloud";

    let socket = TcpListener::bind(server_ip)?;

    for stream in socket.incoming() {
        let stream = stream?;
        let address = stream.local_addr()?.ip().to_string();
        let file_path = format!("{output_dir}{address}.bin");

        thread::spawn(|| {
            handle_connection(stream, file_path).unwrap_or_else(|err| println!("{err}"));
        });
    }

    Ok(())
}

fn handle_connection(mut stream: TcpStream, file_path: String) -> std::io::Result<()> {
    let mut buf = [0; 16384];
    let mut file = File::create(file_path)?;

    loop {
        let num_bytes = stream.read(&mut buf)?;
        // let buf = &mut buf[..num_bytes];

        if num_bytes != 0 {
            file.write_all(&buf[..num_bytes])?;
            file.sync_data()?;
        }
    }
}
