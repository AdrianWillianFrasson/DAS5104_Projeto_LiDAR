use std::env::args;
use std::fs::File;
use std::io::Write;
use std::net::UdpSocket;

fn main() -> std::io::Result<()> {
    print!("{:?}", args().collect::<Vec<String>>());

    let addr = "127.0.0.1:6969";

    let socket = UdpSocket::bind(addr)?;
    let mut buf = [0; 8192];

    let mut file = File::options()
        .append(true)
        .create(true)
        .open("./data.bin")?;

    loop {
        let (num_bytes, _) = socket.recv_from(&mut buf)?;
        let buf = &mut buf[..num_bytes];

        println!("{buf:?}");
        println!("{}", String::from_utf8_lossy(buf));
        println!("--------------------------------");
        file.write_all(buf)?;
    }
}
