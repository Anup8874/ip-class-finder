from flask import Flask, request, render_template_string
import ipaddress

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">

<title>IP CLASS FINDER</title>

<style>

* {
    box-sizing: border-box;
}

body {
    margin: 0;
    background: #050505;
    color: #00ff88;
    font-family: "Courier New", monospace;
    min-height: 100vh;
}

/* Background grid */

body::before {
    content: "";
    position: fixed;
    inset: 0;
    background:
        linear-gradient(rgba(0,255,136,.04) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0,255,136,.04) 1px, transparent 1px);
    background-size: 35px 35px;
    pointer-events: none;
}

/* Header */

.header {
    border-bottom: 1px solid #00ff88;
    padding: 20px;
    text-align: center;
    box-shadow: 0 0 20px rgba(0,255,136,.15);
}

.logo {
    font-size: 28px;
    font-weight: bold;
    letter-spacing: 4px;
    text-shadow: 0 0 12px #00ff88;
}

.status {
    margin-top: 8px;
    font-size: 13px;
}

.dot {
    display: inline-block;
    width: 8px;
    height: 8px;
    background: #00ff88;
    border-radius: 50%;
    box-shadow: 0 0 10px #00ff88;
}

/* Main */

.container {
    max-width: 900px;
    margin: 45px auto;
    padding: 20px;
}

.panel {
    border: 1px solid #00ff88;
    background: rgba(0, 20, 10, .75);
    padding: 30px;
    box-shadow: 0 0 25px rgba(0,255,136,.12);
}

.title {
    font-size: 18px;
    margin-bottom: 20px;
}

/* Input */

.input-area {
    display: flex;
    gap: 10px;
}

input {
    flex: 1;
    padding: 15px;
    background: #020a06;
    border: 1px solid #00ff88;
    color: #00ff88;
    font-family: inherit;
    font-size: 16px;
    outline: none;
}

input:focus {
    box-shadow: 0 0 15px rgba(0,255,136,.3);
}

button {
    padding: 15px 25px;
    background: #00ff88;
    color: #00150a;
    border: none;
    font-family: inherit;
    font-weight: bold;
    cursor: pointer;
}

button:hover {
    box-shadow: 0 0 20px #00ff88;
}

/* Result */

.result {
    margin-top: 30px;
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 15px;
}

.card {
    border: 1px solid #155c3b;
    background: #07120d;
    padding: 18px;
}

.label {
    color: #777;
    font-size: 12px;
    margin-bottom: 7px;
}

.value {
    color: #00ff88;
    font-size: 17px;
    font-weight: bold;
}

.class-card {
    grid-column: span 2;
    text-align: center;
    border: 1px solid #00ff88;
}

.class-value {
    font-size: 42px;
    font-weight: bold;
    text-shadow: 0 0 20px #00ff88;
}

/* Error */

.error {
    margin-top: 20px;
    border: 1px solid #ff3333;
    color: #ff3333;
    padding: 15px;
}

/* Footer */

.footer {
    text-align: center;
    margin-top: 30px;
    color: #555;
    font-size: 12px;
}

@media(max-width:600px) {

    .input-area {
        flex-direction: column;
    }

    .result {
        grid-template-columns: 1fr;
    }

    .class-card {
        grid-column: span 1;
    }

    .logo {
        font-size: 20px;
    }
}

</style>
</head>

<body>

<div class="header">

    <div class="logo">
        [ IP CLASS FINDER ]
    </div>

    <div class="status">
        <span class="dot"></span>
        SYSTEM ONLINE // NETWORK ANALYZER
    </div>

</div>


<div class="container">

<div class="panel">

<div class="title">
    > ENTER TARGET IPv4
</div>

<form method="GET">

<div class="input-area">

<input
    type="text"
    name="ip"
    placeholder="192.168.1.10"
    value="{{ ip }}"
    autocomplete="off"
>

<button type="submit">
    ANALYZE
</button>

</div>

</form>


{% if result %}

<div class="result">

    <div class="card class-card">

        <div class="label">
            IP CLASS
        </div>

        <div class="class-value">
            CLASS {{ result.cls }}
        </div>

    </div>


    <div class="card">

        <div class="label">
            IP ADDRESS
        </div>

        <div class="value">
            {{ result.ip }}
        </div>

    </div>


    <div class="card">

        <div class="label">
            SUBNET MASK
        </div>

        <div class="value">
            {{ result.mask }}
        </div>

    </div>


    <div class="card">

        <div class="label">
            CIDR
        </div>

        <div class="value">
            {{ result.cidr }}
        </div>

    </div>


    <div class="card">

        <div class="label">
            NETWORK
        </div>

        <div class="value">
            {{ result.network }}
        </div>

    </div>


    <div class="card">

        <div class="label">
            BROADCAST
        </div>

        <div class="value">
            {{ result.broadcast }}
        </div>

    </div>

</div>

{% endif %}


{% if error %}

<div class="error">
    [ERROR] {{ error }}
</div>

{% endif %}

</div>

<div class="footer">
    IP ANALYSIS TERMINAL // RHEL LAB
</div>

</div>

</body>
</html>
"""


@app.route("/")
def home():

    ip = request.args.get("ip", "").strip()

    result = None
    error = None

    if ip:

        try:

            address = ipaddress.IPv4Address(ip)

            first = int(ip.split(".")[0])

            if 1 <= first <= 126:

                cls = "A"
                mask = "255.0.0.0"
                cidr = "/8"

            elif 128 <= first <= 191:

                cls = "B"
                mask = "255.255.0.0"
                cidr = "/16"

            elif 192 <= first <= 223:

                cls = "C"
                mask = "255.255.255.0"
                cidr = "/24"

            elif 224 <= first <= 239:

                cls = "D"
                mask = "N/A"
                cidr = "N/A"

            elif 240 <= first <= 255:

                cls = "E"
                mask = "N/A"
                cidr = "N/A"

            else:

                error = "Reserved IP range"

                return render_template_string(
                    HTML,
                    ip=ip,
                    result=None,
                    error=error
                )

            if cls in ["A", "B", "C"]:

                network = ipaddress.IPv4Network(
                    f"{ip}{cidr}",
                    strict=False
                )

                network_ip = str(network.network_address)
                broadcast_ip = str(network.broadcast_address)

            else:

                network_ip = "N/A"
                broadcast_ip = "N/A"

            result = {
                "ip": str(address),
                "cls": cls,
                "mask": mask,
                "cidr": cidr,
                "network": network_ip,
                "broadcast": broadcast_ip
            }

        except ValueError:

            error = "Invalid IPv4 address"

    return render_template_string(
        HTML,
        ip=ip,
        result=result,
        error=error
    )


app.run(host="0.0.0.0", port=5000)
