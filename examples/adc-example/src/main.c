/**
 * @file main.c
 * ADC Example
 * @author Ajay Bhargav
 *
 */

#include <stdio.h>
#include <unistd.h>

#include <lib.h>
#include <ril.h>
#include <os_api.h>
#include <hw/adc.h>

#define MVOLTPERDIV 	2.737f
#define ADC2MVOLT(val)	((float)val * MVOLTPERDIV)

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
		debug(DBG_OFF, "Incoming voice call from: %s\n", ((struct callinfo_t *)param2)->phoneNumber);
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

/**
 * Sample Task
 * @param arg	Task Argument
 */
static void adc_task(void *arg)
{
	unsigned int adc_val;

	/*
	 * Configure ADC Channels
	 */
	adc_config(ADC_CH0);
	adc_config(ADC_CH1);
	adc_config(ADC_CH2);

	while (1) {
		/*
		* Read ADC Channels
		*/
		adc_val = adc_read(ADC_CH0);
		printf("ADC Channel 0: %d, %.2fmV\n", adc_val, ADC2MVOLT(adc_val));
		adc_val = adc_read(ADC_CH1);
		printf("ADC Channel 1: %d, %.2fmV\n", adc_val, ADC2MVOLT(adc_val));
		adc_val = adc_read(ADC_CH2);
		printf("ADC Channel 2: %d, %.2fmV\n", adc_val, ADC2MVOLT(adc_val));
		sleep(1);
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
	logicrom_init("/dev/ttyS0", urc_callback);

	printf("System Ready\n");

	/* Create ADC task */
	os_create_task(adc_task, NULL, FALSE);

	printf("System Initialization finished\n");

	while (1) {
		/* main task loop */
		sleep(1);
	}
}
