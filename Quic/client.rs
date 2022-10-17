// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: Apache-2.0

use s2n_quic::{client::Connect, Client};
use std::{error::Error, net::SocketAddr};
use std::{thread, time};
use tokio::net::UdpSocket;
use bytes::Bytes;

use bytes::{BytesMut, BufMut};

use std::time::Duration;
use std::time::{SystemTime, UNIX_EPOCH};


/// NOTE: this certificate is to be used for demonstration purposes only!
pub static CERT_PEM: &str = include_str!(concat!(
    env!("CARGO_MANIFEST_DIR"),
    "/../../quic/s2n-quic-core/certs/cert.pem"
));

#[tokio::main]
async fn main() -> Result<(), Box<dyn Error>> {
    let client = Client::builder()
        .with_tls(CERT_PEM)?
        .with_io("0.0.0.0:0")?
        .start()?;

    let addr: SocketAddr = "127.0.0.1:4433".parse()?;
    let connect = Connect::new(addr).with_server_name("localhost");
    let mut connection = client.connect(connect).await?;

    // ensure the connection doesn't time out with inactivity
    connection.keep_alive(true)?;

    // open a new stream and split the receiving and sending sides
    let stream = connection.open_bidirectional_stream().await?;
    let (mut receive_stream, mut send_stream) = stream.split();

    // spawn a task that copies responses from the server to stdout
    tokio::spawn(async move {
        let mut stdout = tokio::io::stdout();
        let _ = tokio::io::copy(&mut receive_stream, &mut stdout).await;
    });

    //let sock = UdpSocket::bind("0.0.0.0:8080").await.unwrap();
    let t = thread::spawn(move || {
                //let mut buf = [0; 1024];
    let mut counter = 1;
    loop{
    let ten_millis = time::Duration::from_millis(30);
        thread::sleep(ten_millis);
        let start = SystemTime::now();
        let since_the_epoch = start.duration_since(UNIX_EPOCH).expect("Time went backwards");
        let mut dataStr = since_the_epoch.as_millis().to_string();
        dataStr += "_" ;
        dataStr += "data";
        dataStr += &counter.to_string();
        counter += 1;
        let b = Bytes::from(dataStr);
        send_stream.send_data(b);
    }});
    //Ok(());
    t.join().unwrap();
    Ok(())
    // copy data from stdin and send it to the server
    //let mut stdin = tokio::io::stdin();
    //tokio::io::copy(&mut stdin, &mut send_stream).await?;

    //Ok(())
}