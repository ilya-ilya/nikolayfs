#ifndef __AUTH_H
#define __AUTH_H 1

#ifndef REDIRECTION_TYPE
#define REDIRECTION_TYPE 0
#endif // not REDIRECTION_TYPE

#ifndef APP_NAME
#define APP_NAME "nikolayfs"
#endif // not APP_NAME

typedef struct auth_creds_struct 
{
	int expires;
	char *cid;
	char *rtoken;
	char *secret;
	char *token;
	char *tokentype;
	char *token_uri;
}
auth_creds;

extern auth_creds *auth_creds_init(const char *native_name, const int first);
extern void auth_creds_refresh(auth_creds *creds);
#endif // not __AUTH_H
