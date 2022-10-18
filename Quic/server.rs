use s2n_quic::Server;
use std::error::Error;
use std::time::{SystemTime, UNIX_EPOCH};
use bytes::Bytes;

/// NOTE: this certificate is to be used for demonstration purposes only.
pub static CERT_PEM: &str = include_str!(concat!(
    env!("CARGO_MANIFEST_DIR"),
    "/../../quic/s2n-quic-core/certs/cert.pem"
));

/// NOTE: this certificate is to be used for demonstration purposes only.
pub static KEY_PEM: &str = include_str!(concat!(
    env!("CARGO_MANIFEST_DIR"),
    "/../../quic/s2n-quic-core/certs/key.pem"
));


#[tokio::main]
async fn main() -> Result<(), Box<dyn Error>> {
    let mut server = Server::builder()
        .with_tls((CERT_PEM, KEY_PEM))?
        .with_io("127.0.0.1:4433")?
        .start()?;

    while let Some(mut connection) = server.accept().await {
        // spawn a new task for the connection
        tokio::spawn(async move {
            println!("Connection accepted from {:?}", connection.remote_addr());

            while let Ok(Some(mut stream)) = connection.accept_bidirectional_stream().await {
                // spawn a new task for the stream
                tokio::spawn(async move {
                    println!("Stream opened from {:?}", stream.connection().remote_addr());

                    // echo any data back to the stream
                    while let Ok(Some(data)) = stream.receive().await {
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
                        println!("Data: {:?}, sequence: {:?}, length: {:?}", seq, data, data.len());
                        stream.send_data(data.slice(..seqEnd));
                        //stream.send_data(data[..seqEnd]);
                        //let b = Bytes::from(seq_str);
                        //stream.send(b).await.expect("stream should be open");
                    }
                });
            }
        });
    }

    Ok(())
}


