## Peer-to-Peer Messager

This is a simple peer-to-peer messager program written in Python. It uses Fernet encryption to protect messages in transit.

### Features

* Send and receive encrypted messages
* Connect to a server or act as a server
* Use a command-line interface to interact with the program

### Getting Started

1. Install Python 3 or later.
2. Clone this repository to your local machine: 
﻿```git clone https://github.com/YourUsername/peer-to-peer-messager.git```

4. Open a terminal window and navigate to the project directory: 
﻿
```
cd peer-to-peer-messager
```

5. Install the required dependencies: 
﻿
```pip install -r requirements.txt```

### Usage

To use the program, you can choose to either listen for incoming connections or connect to a server.

#### Listen Mode

Start the program in listen mode:
﻿
```
python main.py listen
```

This will make your computer listen for incoming connections from other users.

#### Sender Mode

Start the program in sender mode:
﻿
```
python main.py sender
```
﻿
You will need to specify the IP address and port of the server you want to connect to:
﻿
```
python main.py sender --ip 192.168.1.100 --port 6969
```

Once you are connected, you can start sending and receiving messages. Type your message in the terminal window and press Enter to send it.

### Encryption

All messages are encrypted using Fernet encryption. This ensures that messages are protected from eavesdropping.

### License

This project is licensed under the MIT License.
