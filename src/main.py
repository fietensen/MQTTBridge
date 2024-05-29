from proxy import Proxy
import os
import sys
import logging
import asyncio

if __name__ == '__main__':
    # set up logging
    LOG_LEVEL = os.environ.get('MQTTBRIDGE_LOG')
    logging.basicConfig(
        format='[%(asctime)s] %(levelname)s: %(message)s',
        level=LOG_LEVEL if LOG_LEVEL else 'INFO'
    )

    # load configuration from environment variables
    logging.debug("Loading configuration from environment variables")

    TARGET_MQTT_BROKER_HOST = os.environ.get('MQTTBRIDGE_TARGET_HOST')
    if not TARGET_MQTT_BROKER_HOST:
        logging.error("The environment variable MQTTBRIDGE_TARGET_HOST was not set. Aborting.")
        sys.exit(1)


    TARGET_MQTT_BROKER_PORT = os.environ.get('MQTTBRIDGE_TARGET_PORT')
    if not TARGET_MQTT_BROKER_PORT:
        logging.warning("The environment variable MQTTBRIDGE_TARGET_PORT was not set. Defaulting to 1883")
        TARGET_MQTT_BROKER_PORT = 1883
    else:
        try:
            TARGET_MQTT_BROKER_PORT = int(TARGET_MQTT_BROKER_PORT)
        except ValueError:
            logging.error("Couldn't parse MQTTBRIDGE_TARGET_PORT. Aborting.")
            sys.exit(1)
    

    SELF_MQTT_BROKER_HOST = os.environ.get('MQTTBRIDGE_PROXY_HOST')
    if not SELF_MQTT_BROKER_HOST:
        logging.warning("The environment variable MQTTBRIDGE_PROXY_HOST was not set. Defaulting to 127.0.0.1")
        SELF_MQTT_BROKER_HOST = '127.0.0.1'


    SELF_MQTT_BROKER_PORT = os.environ.get('MQTTBRIDGE_PROXY_PORT')
    if not SELF_MQTT_BROKER_PORT:
        logging.warning("The environment variable MQTTBRIDGE_PROXY_PORT was not set. Defaulting to 1883")
        SELF_MQTT_BROKER_PORT = 1883
    else:
        try:
            SELF_MQTT_BROKER_PORT = int(SELF_MQTT_BROKER_PORT)
        except ValueError:
            logging.error("Couldn't parse MQTTBRIDGE_PROXY_PORT. Aborting.")
            sys.exit(1)
    
    
    proxy = Proxy(
        TARGET_MQTT_BROKER_HOST,
        TARGET_MQTT_BROKER_PORT,
        proxy_host=SELF_MQTT_BROKER_HOST,
        proxy_port=SELF_MQTT_BROKER_PORT,
    )

    try:
        proxy.serve_forever(
            asyncio.get_event_loop()
        )
    except KeyboardInterrupt:
        logging.info("Deteced keyboard interrupt. Aborting.")
        proxy.shutdown()