#ifndef __AUTH_H
#define __AUTH_H 1
typedef struct auth_creds_struct 
{
	int field;
}
auth_creds;

extern auth_creds *auth_creds_init(char *filename);
extern void auth_creds_refresh(auth_creds *creds);
#endif // not __AUTH_H
