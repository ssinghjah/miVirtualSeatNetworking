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
use rand::{thread_rng, Rng};
use rand::distributions::Alphanumeric;
use std::str::from_utf8;

/// NOTE: this certificate is to be used for demonstration purposes only!
pub static CERT_PEM: &str = include_str!(concat!(
    env!("CARGO_MANIFEST_DIR"),
    "/../../quic/s2n-quic-core/certs/cert.pem"
));

fn appendToCSV(path: &str, data: [&str; 3]){
        let mut file = std::fs::OpenOptions::new().write(true).append(true).open(path).unwrap();
        let mut wtr = csv::Writer::from_writer(file);
        wtr.write_record(&data).expect("unable to write to csv");
        wtr.flush().expect("unable to flush csv");
}

#[tokio::main]
async fn main() -> Result<(), Box<dyn Error>> {
    let client = Client::builder()
        .with_tls(CERT_PEM)?
        .with_io("0.0.0.0:0")?
        .start()?;

    let mut appServer = Server::builder().with_tls((CERT_PEM, KEY_PEM))?.with_io("127.0.0.1:4433")?.start()?;


    while let Some(mut connection) = appServer.accept().await {
    	  
    }


    let addr: SocketAddr = "127.0.0.1:4433".parse()?;
    let connect = Connect::new(addr).with_server_name("localhost");
    let mut connection = client.connect(connect).await?;

    // ensure the connection doesn't time out with inactivity
    connection.keep_alive(true)?;

    // open a new stream and split the receiving and sending sides
    let stream = connection.open_bidirectional_stream().await?;
    let (mut receive_stream, mut send_stream) = stream.split();

    let ()

    tokio::spawn(async move {
     while let Ok(Some(data)) = receive_stream.receive().await
     {
        let start = SystemTime::now();
        let since_the_epoch = start.duration_since(UNIX_EPOCH).expect("Time went backwards");
        println!("{:?}", since_the_epoch);
        // parse sequence number
        let mut seqEnd = 0;
        for dataIndex in 0..data.len()
        {
            if data[dataIndex] == 95
            {
                seqEnd = dataIndex;
                break;
            }
        }

        let seq = &data[..seqEnd];
        println!("Data: {:?}", data);
        appendToCSV("./acks.csv", [&since_the_epoch.as_millis().to_string(), &std::str::from_utf8(&data).unwrap().to_string(), &data.len().to_string()]);
      }});

    // spawn a task that copies responses from the server to stdout
    /*tokio::spawn(async move {
        let mut stdout = tokio::io::stdout();
        let _ = tokio::io::copy(&mut receive_stream, &mut stdout).await;
    });*/

    //let sock = UdpSocket::bind("0.0.0.0:8080").await.unwrap();
    let t = thread::spawn(move || {
    let mut counter:u16 = 1;
    loop{
    let ten_millis = time::Duration::from_millis(16);
        thread::sleep(ten_millis);
        let start = SystemTime::now();
        let since_the_epoch = start.duration_since(UNIX_EPOCH).expect("Time went backwards");
        let mut dataStr = counter.to_string();
        dataStr += "_" ;
        dataStr += &since_the_epoch.as_millis().to_string();
        dataStr += "_";
        let rand_string: String = thread_rng().sample_iter(&Alphanumeric).take(1024).map(char::from).collect();
        dataStr += &rand_string;
        counter += 1;
        let b = Bytes::from(dataStr);
        let bLen = b.len();
        send_stream.send_data(b);
        appendToCSV("./tx.csv", [&since_the_epoch.as_millis().to_string(), &counter.to_string(), &bLen.to_string()]);

    }});

    t.join().unwrap();
    Ok(())
}
