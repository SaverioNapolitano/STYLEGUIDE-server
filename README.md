# STYLEGUIDE-server 

Code for the server of the [STYLEGUIDE](https://github.com/SaverioNapolitano/STYLEGUIDE.git) project. 

## Purpose 

The server stores all the data related to the STYLEGUIDE users in a (currently) SQLite DB and provides them when asked to by a client. It receives the data to store by the [bridge](https://github.com/SaverioNapolitano/STYLEGUIDE-bridge.git). It interacts with a machine learning client, providing it the data needed to perform its predictions. 

## How it works 

All the communications take place using HTTP protocol.

The bridge sends the data to be stored to the server (with [this](https://github.com/SaverioNapolitano/STYLEGUIDE-bridge?tab=readme-ov-file#http) format), then the server provides this data both to the [mobile app](https://github.com/SaverioNapolitano/STYLEGUIDE-app.git) and any generic client to look at.

The server makes this data available to a machine learning client that will output the future consumption data. This predicted data is also provided to the mobile app and the other clients.

> [!NOTE]
> For the sake of simplicity, in this case both the MQTT and the HTTP clients are integrated with the rest server, but it's possible for potentially any client to connect to the server. 

### MQTT Client 

See [here](https://github.com/SaverioNapolitano/STYLEGUIDE-bridge?tab=readme-ov-file#bridge---mobile-app-generic-client)

### HTTP Client 

