# STYLEGUIDE-server 

Code for the server of the [STYLEGUIDE](https://github.com/SaverioNapolitano/STYLEGUIDE.git) project. 

## Purpose 

The server stores all the data related to the STYLEGUIDE users in a (currently) SQLite DB and provides them when asked to by a client. Moreover, it also keeps track of the current state of the house. It receives the data to store by the [bridge](https://github.com/SaverioNapolitano/STYLEGUIDE-bridge.git). It interacts with a machine learning client, providing it the data needed to perform its predictions. 

## How it works 

All the communications take place using HTTP protocol.

The bridge sends the data to be stored to the server (with [these](https://github.com/SaverioNapolitano/STYLEGUIDE-bridge?tab=readme-ov-file#http) formats), then the server provides this data both to the [mobile app](https://github.com/SaverioNapolitano/STYLEGUIDE-app.git) and the dashboards.

The server makes this data available to a machine learning client that will output the future consumption data. This predicted data is also provided to the mobile app and the dashboards.

> [!NOTE]
> For the sake of simplicity, in this case the HTTP clients(the dashboards) are integrated with the rest server, but it's possible for potentially any client to connect to the server.  

### HTTP Client (Dashboards)

It asks the server for refined data, including:
- which colors are the most used 
- which methods to turn on the lights are the most used
- the correlation between the power consumption and the electricity bill 
- the past power consumption 
- the future power consumption (AI-based)
- energy saving tips and a numerical estimate of those savings (AI-based)
- the energy savers ranking to see how good one's doing with respect to its neighbours 

In the **user dashboard** only the data related to the user is shown (e.g., only its position in the ranking is displayed), while in the **company dashboard** it's possible to see the full ranking.

## Further improvements 

- [ ] Consider both the methods to turn on the lights and the methods to turn them off in the estimate 
- [ ] Implement the AI-based solution for energy saving tips and numerical estimate 
- [ ] Enhance ranking and gamification features
- [ ] Implement the full admin dashboard to display the overall data (consumption, most used color/methods) for every user

 
