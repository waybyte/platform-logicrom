/**
 * @file main.c
 * SSL Socket Example with client authentication
 * @author Ajay Bhargav
 *
 */

#include <stdio.h>
#include <unistd.h>
#include <string.h>

#include <lib.h>
#include <ril.h>
#include <os_api.h>

#include <network.h>
#include <net/sockets.h>

/**
 * Server IP
 */
#define SERVER_IP "tcpbin.com"
/**
 * Server Port
 */
#define SERVER_PORT 4244

int socket_id;

/**
 * SSL Client certificate
 */
const char client_cert[] = "-----BEGIN CERTIFICATE-----\n\
MIIDZTCCAk2gAwIBAgIBKjANBgkqhkiG9w0BAQsFADCBizELMAkGA1UEBhMCVVMx\n\
CzAJBgNVBAgMAkNBMRYwFAYDVQQHDA1TYW4gRnJhbmNpc2NvMQ8wDQYDVQQKDAZ0\n\
Y3BiaW4xDDAKBgNVBAsMA29wczETMBEGA1UEAwwKdGNwYmluLmNvbTEjMCEGCSqG\n\
SIb3DQEJARYUaGFycnliYWdkaUBnbWFpbC5jb20wHhcNMjAwNjA2MTIwMjMwWhcN\n\
MjAwNjA3MTIwMjMwWjAcMRowGAYDVQQDDBF0Y3BiaW4uY29tLWNsaWVudDCCASIw\n\
DQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEBAL6jI3SzOhkCh28/MLNgZH+lQ9+E\n\
/dkS/vnau5rWoVo3IJNsZ81FRLwPJzubiF/ZeKk0C5XYM/fuaIl5qHb4z7ImuTKi\n\
6DRrF+lhBXHi7MF+aHyUiPhr4ey8DQ/2QbcMLcm0nxDABVvx3MK18j3u9snDKWxI\n\
wX+pa7sVAoeo5lvBlTBD6R/lq9iDlGM5l+Gg/AX/2ze11pbDCZNO42A++VkjCsqb\n\
vZ0ezN7X3aFBRXqoty6ngMYpjUNxoQ4OElNOoPozk9VDZvcTRF568zZ0FcP3AtCx\n\
iOZLSQk6W48SfCbH8wUPgIWsSKyjtFJL0qTkXeFLFtQMQaXm39c/qJackgMCAwEA\n\
AaNCMEAwHQYDVR0OBBYEFJifGeElqlMLAhmnMBBzy5xDzlkRMB8GA1UdIwQYMBaA\n\
FOLuMowBSAZfV5v82LmlaIIOvU/DMA0GCSqGSIb3DQEBCwUAA4IBAQBIG4EbqwPu\n\
EQVoTZdGUB7MqLEuwMEIQw/vxc3zPH+qNoaZBxXIr/+90UyYPYsDbGgYngLUeuW7\n\
YPfrun603+mAjgLCzCc/qRYPd0o5sfTXYSla/Ho4chF8OF812gxVTGs0+VLfWuig\n\
Y8H30A4VXl8vPi6OCmV9vVmnh2K4uhmxp9h7zqHy7HjRnOymipvu7+TxG9BmAJPR\n\
AafFth2mSiuNZRGBqzY1MfjCUt18YQtBYUduhRzWe3+niwkhMZP6sbq/Q2cRwoSh\n\
yKi9KDo/SL6b2cmG5ECu2FLcqhOIZOoAB4P0UVlyZqefefMnXbl8mP7siI+uVHWT\n\
WwOvwPEtnDbF\n\
-----END CERTIFICATE-----";

/**
 * SSL Client private key
 */
const char client_key[] = "-----BEGIN PRIVATE KEY-----\n\
MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC+oyN0szoZAodv\n\
PzCzYGR/pUPfhP3ZEv752rua1qFaNyCTbGfNRUS8Dyc7m4hf2XipNAuV2DP37miJ\n\
eah2+M+yJrkyoug0axfpYQVx4uzBfmh8lIj4a+HsvA0P9kG3DC3JtJ8QwAVb8dzC\n\
tfI97vbJwylsSMF/qWu7FQKHqOZbwZUwQ+kf5avYg5RjOZfhoPwF/9s3tdaWwwmT\n\
TuNgPvlZIwrKm72dHsze192hQUV6qLcup4DGKY1DcaEODhJTTqD6M5PVQ2b3E0Re\n\
evM2dBXD9wLQsYjmS0kJOluPEnwmx/MFD4CFrEiso7RSS9Kk5F3hSxbUDEGl5t/X\n\
P6iWnJIDAgMBAAECggEAKx+qQJbeeJPa4S5xLNKMSVewL9rctYMXjJuPPqp4m3jG\n\
9LJcFNIrh0MCQ/id89i088mjKUVcFCSpHxgXJLqJ+SnLUQoK7vie0xswaR/FIMwg\n\
hLXw+gkldTDg35B8MxUdMniaVuapD7B5mM4huyLYTrHIKAeZRfCkPxC0ns11NqIB\n\
9Gpx1yJuHFu7WkEtrbqhKfaYeymPbm2G53/BUJNJgMYwxxYG3NJVhb4Q8SMjZ09g\n\
fGP24svwVFBGLykvL/yQSTEuK5/rE8wF+TU/G4hA9bQci+fs1XHFXDnob9wg1Iiv\n\
0dfD40JW4gb1kCp1VtyV4EFQgeo36KiQTlKJi+qSqQKBgQD8IAXE45n9SExumBpk\n\
ZOAAjWxSSJMCwxO+31DSCXhwetI8WGVbxbkuALnupnINYTFpe1ubwniCm/ihExmy\n\
rEkLESjQ18oGRMJWVT9yxk8m0Hv/wPo1xm+dIPpGEY8DKDSDnkCOHxvKeXlGjlbR\n\
YOG+Vmh+PEmzuvH2BBOAVRFu7QKBgQDBkTG4qZBNGw3LowQgN7pRk7EBAOvnkIea\n\
mi63G3dkuaS4UiYd0ymxuR5RoQfz7zb3S3ArjxDO+J9YBeECkwMp0OkQt6PqDVoa\n\
aUG2eU6yTmDzNX2aEqM1RnXqHePizVXnGFlj3nzW4fTaU/kN4hWAdm+3HnBYBq5f\n\
qiD8rkL2rwKBgQCpN4znsqLd3jJ+X9QG4bV+aWz0ZQVWazvLdfK2peiSBb0pB2Mw\n\
DyrUd2RTip8t37fcRhEcH4/miWx8H2e2BfAYX3H3iX1sa6XLb/ffvr3NHUy8QPcu\n\
NHshCMsxUAOeaNOmKwbE3Jg4cwM0mcAnU1DwAOqtHyWQXb6cEexMy8uhmQKBgCOL\n\
B7hC2o5uA1B7NIy97uZ/2ia3BppUvbGz0hQpZPkH5ak63Gjpl2Rc+6Y9jXpLWKp8\n\
HbLB6HI40PmWysRwPkp1Y/Z/4gdeQEdNQJXDHKI9JixCjDe4aGOl9ozwxCGnVrjC\n\
jdd6yS2j/BQDC15zP0OBe+4CFtrzDx3d3YTIct9dAoGAS5UgYs13MODq/xNIJcLD\n\
qiyEJBC0SZ9g+K+W1pUR7dYZI2UcLSwEFd/QE4iBgqdjQ5poczsnZ4jIVH3f4Ji8\n\
kr9pQivTnQWOmTqtWqdNSvt2xlkxlf5LOZUnfT4hDldAnLzOXiUI3k3BTQygt91f\n\
GUgZ3N0O3bwWSyhuAATc+1U=\n\
-----END PRIVATE KEY-----";

/**
 * SSl Client certificate and privatekey
 */
const struct ssl_certs_t certs = {
	.cert_type = SSL_TYPE_BUFFER,
	.cert = client_cert,
	.cert_len = sizeof(client_cert) - 1,
	.pkey_type = SSL_TYPE_BUFFER,
	.privatekey = client_key,
	.privatekey_len = sizeof(client_key) - 1,
};

/**
 * URC Handler
 * @param param1	URC Code
 * @param param2	URC Parameter
 */
static void urc_callback(unsigned int param1, unsigned int param2)
{
	switch (param1)
	{
	case URC_SYS_INIT_STATE_IND:
		if (param2 == SYS_STATE_SMSOK)
		{
			/* Ready for SMS */
		}
		break;
	case URC_SIM_CARD_STATE_IND:
		switch (param2)
		{
		case SIM_STAT_NOT_INSERTED:
			debug(DBG_OFF, "SYSTEM: SIM card not inserted!\n");
			break;
		case SIM_STAT_READY:
			debug(DBG_INFO, "SYSTEM: SIM card Ready!\n");
			break;
		case SIM_STAT_PIN_REQ:
			debug(DBG_OFF, "SYSTEM: SIM PIN required!\n");
			break;
		case SIM_STAT_PUK_REQ:
			debug(DBG_OFF, "SYSTEM: SIM PUK required!\n");
			break;
		case SIM_STAT_NOT_READY:
			debug(DBG_OFF, "SYSTEM: SIM card not recognized!\n");
			break;
		default:
			debug(DBG_OFF, "SYSTEM: SIM ERROR: %d\n", param2);
		}
		break;
	case URC_GSM_NW_STATE_IND:
		debug(DBG_OFF, "SYSTEM: GSM NW State: %d\n", param2);
		break;
	case URC_GPRS_NW_STATE_IND:
		break;
	case URC_CFUN_STATE_IND:
		break;
	case URC_COMING_CALL_IND:
		debug(DBG_OFF, "Incoming voice call from: %s\n", ((struct callinfo_t *)param2)->phoneNumber);
		/* Take action here, Answer/Hang-up */
		break;
	case URC_CALL_STATE_IND:
		switch (param2)
		{
		case CALL_STATE_BUSY:
			debug(DBG_OFF, "The number you dialed is busy now\n");
			break;
		case CALL_STATE_NO_ANSWER:
			debug(DBG_OFF, "The number you dialed has no answer\n");
			break;
		case CALL_STATE_NO_CARRIER:
			debug(DBG_OFF, "The number you dialed cannot reach\n");
			break;
		case CALL_STATE_NO_DIALTONE:
			debug(DBG_OFF, "No Dial tone\n");
			break;
		default:
			break;
		}
		break;
	case URC_NEW_SMS_IND:
		debug(DBG_OFF, "SMS: New SMS (%d)\n", param2);
		/* Handle New SMS */
		break;
	case URC_MODULE_VOLTAGE_IND:
		debug(DBG_INFO, "VBatt Voltage: %d\n", param2);
		break;
	case URC_ALARM_RING_IND:
		break;
	case URC_FILE_DOWNLOAD_STATUS:
		break;
	case URC_FOTA_STARTED:
		break;
	case URC_FOTA_FINISHED:
		break;
	case URC_FOTA_FAILED:
		break;
	case URC_STKPCI_RSP_IND:
		break;
	default:
		break;
	}
}

static int status_callback(int id, int event)
{
	switch (event)
	{
	case SOCK_EV_CONNECTED:
		printf("Socket connected\n");
		break;
	case SOCK_EV_DISCONNECTED:
		printf("Socket disconnected\n");
		break;
	default:
		printf("Socket Event: %d\n", event);
		break;
	}
	return 0;
}

static void socket_init(void)
{
	struct ssl_sockopt_t sockopt;

	socket_id = ssl_socket_request(SSL_VER_DEFAULT, (struct ssl_certs_t *)&certs);

	strcpy(sockopt.server_ip, SERVER_IP);
	sockopt.port = SERVER_PORT;
	sockopt.arg = NULL;
	sockopt.status_callback = status_callback;
	ssl_socket_setopt(socket_id, &sockopt);
}

/**
 * SSL Socket Task
 * @param arg	Task Argument
 */
static void socket_task(void *arg)
{
	int ret;
	unsigned char buffer[] = "Hello World\n";
	unsigned char recv_buffer[128];

	/* Setup and initialize socket */
	socket_init();

	while (1)
	{
		/* Wait for GPRS */
		if (network_getstatus(0) != NET_STATE_GPRS)
		{
			sleep(1);
			continue;
		}

		/* Check if socket not connected */
		if (ssl_socket_getstatus(socket_id) != SOCK_STA_CONNECTED)
		{
			/* Initiate SSL socket connection */
			ret = ssl_socket_open(socket_id);
			if (ret < 0)
			{
				printf("SSL socket open fail: %s\n", strerror(-ret));
				/* retry after 10s */
				sleep(10);
				continue;
			}
		}

		ret = ssl_socket_send(socket_id, buffer, strlen((char *)buffer), 0);
		printf("Socket send status: %d\n", ret);

		memset(recv_buffer, 0, sizeof(recv_buffer));
		ret = ssl_socket_read(socket_id, recv_buffer, sizeof(recv_buffer), 10000);
		if (ret < 0)
			printf("SSL socket read error: %s\n", strerror(-ret));
		else
			printf("SSL socket read (%d bytes):\n%s\n", ret, recv_buffer);
	}
}

/**
 * Application main entry point
 */
int main(void)
{
	/*
	 * Initialize library and Setup STDIO
	 */
	logicrom_init("/dev/ttyS0", urc_callback);
	/* Start GPRS service */
	network_gprsenable(TRUE);

	printf("System Initialized\n");

	/* Create Application tasks */
	os_create_task(socket_task, NULL, FALSE);

	while (1) {
		/* Main task loop */
		sleep(1);
	}
}
