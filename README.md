# Flight Tracker
## Get flight info from CLI
Get some info of the closest flight that you may see taking off in real time!
###### _Who knows maybe it's the aircraft you've just seen from your window_

This simple CLI application gives you a cool user interface that brings you information about the closest aircraft that is taking off in real time.

## Verbosity levels

Flight tracker supports three levels of verbosity. Each level includes the previous levels data and more.

| Info | Verbosity levels
| ------ | ------ |
| Enormous flight number | Always |
| Destination | Always, <b>adding airport name on -v</b> |
| IATA representation (e.g TLV -> XYZ)| -v |
| Airline company | Always |
| Speed | Always |
| Altitude | -v |
| Flight time | -v |
| Flight distance | -v |
| Github link | -vv
