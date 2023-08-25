use std::env::args;
use std::fs::File;
use std::io::Write;
use std::net::UdpSocket;

fn main() -> std::io::Result<()> {
    let arguments = args().collect::<Vec<String>>();
    let server_ip = arguments[1].clone();
    let file_path = arguments[2].clone();

    let socket = UdpSocket::bind(server_ip)?;

    let mut buf = [0; 8192];
    let mut file = File::create(file_path)?;

    loop {
        let (num_bytes, _) = socket.recv_from(&mut buf)?;
        let buf = &mut buf[..num_bytes];

        if num_bytes != 0 {
            file.write_all(buf)?;
            file.sync_data()?;
        }
    }
}
