Theses scripts implement the control and data plane to support real-time multi-media communications between multiple devices. 

The system under consideration is assumed to consist of two types of entities: hubs and spokes.  
Spokes are the sources and sinks of multi-media data, such as cameras, audio microphones, renderers or virtual reality goggles. Spokes are the entities closest to the end-users. Hubs are the entities that interconnect spokes and contain the intelligence to generate custom scenes for each spoke.  

The control plane is implemented using TCP, while the data plane is implemented using raw UDP and Quic.
