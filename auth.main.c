#include<stdlib.h>
#include<stdio.h>
#include<errno.h>
#include"auth.h"

int
main(int argc, char **argv)
{
	auth_creds *client;
	char nfile[] = "native.json";
	client = auth_creds_init(nfile, 1);
	if (client == NULL) {
		perror(argv[0]);
		exit(errno);
	}
	printf("client @ %p\n", client);
	//system("xdg-open http://google.com");
	auth_creds_refresh(client);
	free(client);
	return 0;
}
