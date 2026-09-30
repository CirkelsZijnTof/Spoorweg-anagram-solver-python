# spoorsolver

Read project description. Solves an anagram of a train station name. This is after a game most Dutch people regularly taking public transport will know.
The program GUI is formatted in Dutch, but it should be simple enough to understand for anyone.

Requires the presence of stationnames.csv. Based on this file, it will (re)generate encodednames.csv. This functionality can be turned off in the code by toggling the variable doRedoFiles to False. This makes the code a little lighter to run but is not particularly necessary.

# Add new train station names

It is possible to add new stations to stationnames.csv. To prevent bugs, please use the following format:
Simply append to the end of stationnames.csv the true name of the station you want to add (complete with capital letters and spaces).
At the end, seperate it with a comma and enter the raw name (no capital letters and spaces). Look at how other entries do it if you're unsure. Press enter at the end and save the updated file.

# Previous successful solves
* Noord pela - apeldoorn
* Plann de haanrijen - alphen aan de rijn
* Waan vleesetend - veenendaal west
* Clumsy rental ted - lelystad centrum
* Zere tanda voozan - zandvoort aan zee
* Gal woev - wolvega
* Nul te teer - etten leur
* Los pichor pathir - schiphol airport
* Stil vier giet in buurt - tilburg universiteit
* Treijnmotor lambodder - rotterdam lombardijen
* La tore di mele - almere buiten
* Les enfants de miromek - eygelshoven markt
