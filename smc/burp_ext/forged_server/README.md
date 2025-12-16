### What is this?

So back when researching the exploit, our team was debating on two methods: one is setting up a true MITM with a fake client and a fake server, the other is using Burp to redirect all client request to a running server. In the end, the former method was chosen, in order to make client unaware of them being eavesdropped, making an illusion of secure communication. Also, the later method didn't have capability to reply messages in a contexual way like a real server, thus making it quite distinguishable.

However the code for the second method didn't get out-right removed, and after a bit of cleaning up, I was able to set-up a forged server returning response from clients with similar API endpoints.

This code doesn't have much documentation, but if you understand how the flow work, this is no less different than the result of the true MITM.

# Installation

You will need install these libraries:
`pip install pycryptodome
pip install fastapi
pip install pyjwt`

# Running
1. Set up BurpSuite, Frida and AVD as usual. See the README in upper folder for the first method

2. On BurpSuite, inside Proxy setting, edit the proxy you're using. Under "Redirect Handling" tab, add host `127.0.0.1` and port `9999` to redirect address, then click OK. After that, install `replace_host.py` as Python extension on BurpSuite. 

2. Copy `intercept_server.py` and `ec_curve.py` and put them into this folder.

3. Inside forged_server folder, run:
`fastapi run fake_server.py --port 9999`

4. Start up your app using Frida, then proceed as normal.

You will see requests from the client logged onto the FastAPI server console.
