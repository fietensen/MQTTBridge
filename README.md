# MQTTBridge
MQTTBridge is a simple and lightweight proxy tool designed to faciliate MQTT communication by bridging WebSocket MQTT connections to raw MQTT. This tool enables clients to connect via WebSocket MQTT and seamlessly proxies the communication to standard MQTT brokers.

## Getting Started

### On your host machine

#### Setup

1. Ensure you have a working copy of `python3` and `python3-pip`
2. Install the Project's dependencies by executing `pip install -r requirements.txt` in the project's root directory
3. Set following environment variables for configuration:
    - `MQTTBRIDGE_TARGET_HOST` - The host name / address of the target (pure) mqtt broker
    - `MQTTBRIDGE_TARGET_PORT` - The port of the target (pure) mqtt broker (defaults to `1883`)
    - `MQTTBRIDGE_PROXY_HOST` - The host name / address of the MQTTBridge proxy (defaults to `127.0.0.1` / localhost)
    - `MQTTBRIDGE_PROXY_PORT` - The port of the MQTTBridge proxy (defaults to `1883`)

#### Running

After the setup, running MQTTBridge is as simple as running the following command in the project's root directory:
`python ./src/main.py`

### Via docker

MQTTBridge comes with with a docker configuration. You can either build your own image running `docker build -t [IMAGE_NAME] .` in the project's root directory, or use the prebuilt, published image which you can find at https://hub.docker.com/repository/docker/fietensen/mqttbridge.

To run the docker image you can run following command:
```sh
docker run -e MQTTBRIDGE_TARGET_HOST=test.mosquitto.org -e MQTTBRIDGE_TARGET_PORT=1883 -e MQTTBRIDGE_PROXY_HOST=0.0.0.0 -e MQTTBRIDGE_PROXY_PORT=1883 -p 1883:1883 fietensen/mqttbridge
```

make sure to replace the environment variables and the port mappings according to your requirements. In case you have decided to build your own image, also replace the image name. MQTTBridge should now be running, happy hacking!

## Contributing

We welcome contributions! Please issue ideas for improvement and create pull requests :)

## License

This project is licensed under the MIT License.