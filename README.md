# Water your plant with ESP32
This is a project for watering a plant with the help of an ESP32. It was created for the course "Industrial Internet of Things und Industrie 4.0" at HSBI in Spring '24.

The project consists of two subparts:
- **[esp32-bewaesserungs-projekt](https://github.com/newjonny/esp32-bewasserungs-projekt)**: This part contains the code for the ESP32 node, written in C++, which includes the logic for watering a plant.
- **[esp32-bewaesserungs-projekt-cloud](https://github.com/newjonny/esp32-bewaesserungs-projekt-cloud) (YOU ARE HERE)**: This part contains the worker script that subscribes to relevant topics on the MQTT-broker.

## Structure of this project
This project functions as the Device-'Cloud' that subscribes to all relevant MQTT topics and pushes that data into the InfluxDB as is.
- **main.py** contains all the logic for subscribing to the relevant topics on the MQTT-broker and then pushing that data to an InfluxDB instance. This happens without any further data validation.
- **Procfile** contains configuration to turn this into a long-running worker script on Scalingo
- **ca.pem** and **emqsxl-ca.crt** are Root CA certificates necessary for establishing a SSL connection to our InfluxDB instance and EMQX MQTT Broker instance, respectively.

## Authors
- [Jannik Winkelmann](https://github.com/janwin96)
- [Jonas Weichenhain](https://github.com/newjonny)