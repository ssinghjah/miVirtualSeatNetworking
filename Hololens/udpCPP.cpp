#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <netinet/in.h>
#include <arpa/inet.h>

int main()
{

  int SERVER_PORT = 1234;
  const char* SERVER_IP = 'ec2-3-101-152-92.us-west-1.compute.amazonaws.com';
  int sockfd;
  int BUFF_LEN = 1024;
  struct sockaddr_in serverAddr;
  char buffer[BUFF_LEN];
  socklen_t addr_size;

  sockfd = socket(PF_INET, SOCK_DGRAM, 0);
  memset(&serverAddr, '\0', sizeof(serverAddr));

  serverAddr.sin_family = AF_INET;
  serverAddr.sin_port = htons(port);
  serverAddr.sin_addr.s_addr = inet_addr(SERVER_IP);

  strcpy(buffer, "Hello Server\n");
  sendto(sockfd, buffer, 1024, 0, (struct sockaddr*)&serverAddr, sizeof(serverAddr));
  printf("[+]Data Send: %s", buffer);

  return 0;


}
