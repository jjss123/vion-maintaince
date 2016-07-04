#websocket sdk interfaces

custom websocket protocol used to describe the rule of the message transmitted between server and client.

it will be sent and received by method **on_message()**, of which type is '**json**', and its content must follow the description below.

protocol content description:

	{option: value}
	{option: value}
	...
	{message: value}

***

###protocol option

| option| value content	| Nullable	|
| ------|:-------------:| -------:	|
| msg_type|GET/POST/CONFIRM/LOGIN/LOGOUT		|No	
| seq	|hash string	| No	
| callback|json-like dict| Yes
| message|json-like dict|No

***
###
