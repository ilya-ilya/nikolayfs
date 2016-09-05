#include<stdlib.h>
#include<stdio.h>
#include<sys/types.h>
#include<sys/stat.h>
#include<unistd.h>
#include<json-c/json_tokener.h>
#include"auth.h"

auth_creds *
auth_creds_init(const char *native_name, const int first)
{
	auth_creds *creds;
	creds = calloc(1, sizeof(auth_creds));
	if (creds == NULL) {
		return creds;
	}
	FILE *native;
	native = fopen(native_name, "r");
	struct stat native_st;
	if (stat(native_name, &native_st) != 0) {
		free(creds);
		return NULL;
	}
	char *native_json = calloc(native_st.st_size, sizeof(char));
	size_t read = fread(native_json, sizeof(char), native_st.st_size - 1, native);
	if (ferror(native)) {
		free(creds);
		fclose(native);
		return NULL;
	}
	fclose(native);
	json_object *cred_data_dict = json_tokener_parse(native_json);
	free(native_json);
	json_object *cred_data;
	if (json_object_object_get_ex(cred_data_dict, "installed", &cred_data)) {
		printf("%d\n", json_object_object_length(cred_data));
	}
	json_object_put(cred_data_dict);
	return creds;
}

void
auth_creds_refresh(auth_creds *creds)
{
	return ;
}
