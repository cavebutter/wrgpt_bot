# WRGPT BOT  
This application is a set of automation tools for the [WRGPT email poker tournament](http://wrgpt.org). WRGPT is an 
annual email poker tournament with almost 1000 players. It is run as a standard Hold 'Em tournament, but with all action
 occuring asynchronously via email. Users will receive email messages telling them their hole cards. Users act by sending
 email messages back to the dealer. Table status and action history is available on the web as a link in each message 
from the dealer.  
## Base Model  
The base model will run in terminal. It will fetch the most recent email from the dealer and display table status, 
current hand, and allow the user to send instructions to the dealer to call, fold, raise, etc.  
## Enhanced Model  
After verification that the base model works, the enhanced model will offer a webUI for the Base Model along with the 
following enhancements:  
- Probability analysis from Holdem-Sim (../holdem-sim)  
## AI Model  
After validation of the enhanced model, we will build in AI analysis of other players' tendencies and recommendation for 
action. AI will be provided by Ollama on the local machine.