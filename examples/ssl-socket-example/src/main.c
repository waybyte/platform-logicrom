/**
 * @file main.c
 * SSL Socket Example
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
#include <siwi/sockets.h>

/**
 * Server IP
 */
#define SERVER_IP "tcpbin.com"
/**
 * Server Port
 */
#define SERVER_PORT 4243

int socket_id;

/**
 * URC Handler
 * @param param1	URC Code
 * @param param2	URC Parameter
 */
static void urc_callback(unsigned int param1, unsigned int param2)
{
	switch (param1) {
	case URC_SYS_INIT_STATE_IND:
		if (param2 == SYS_STATE_SMSOK) {
			/* Ready for SMS */
		}
		break;
	case URC_SIM_CARD_STATE_IND:
		switch (param2) {
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
		debug(DBG_OFF, "Incoming voice call from: %s\n", ((ST_ComingCall*)param2)->phoneNumber);
		/* Take action here, Answer/Hang-up */
		break;
	case URC_CALL_STATE_IND:
		switch (param2) {
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

	socket_id = ssl_socket_request(SSL_VER_DEFAULT, NULL);

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
		if (network_getstatus(0) != NET_STATE_GPRS) {
			sleep(1);
			continue;
		}

		/* Check if socket not connected */
		if (ssl_socket_getstatus(socket_id) != SOCK_STA_CONNECTED) {
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
int main(int argc, char *argv[])
{
	/*
	 * Initialize library and Setup STDIO
	 */
	siwilib_init("/dev/ttyS0", urc_callback);
	/* Start GPRS service */
	network_gprsenable(TRUE);

	printf("System Ready\n");

	/* Create Application tasks */
	os_create_task(socket_task, NULL, FALSE);

	printf("System Initialization finished\n");

	while (1) {
		/* Main task loop */
		sleep(1);
	}
}
