#include"auth.h"

int
main(void)
{
	auth_creds *client;
	char nfile[] = "native.json";
	client = auth_creds_init(nfile);
	auth_creds_refresh(client);
	return 0;
}
