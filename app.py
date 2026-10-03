from flask import Flask, request, render_template_string
import ipaddress

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <title>Anup Verma | IP Class Finder</title>

    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            background: #050505;
            color: #00ff41;
            font-family: "Courier New", monospace;
            min-height: 100vh;
            overflow-x: hidden;
        }

        body::before {
            content: "";
            position: fixed;
            inset: 0;
            pointer-events: none;
            background:
                linear-gradient(rgba(0,255,65,0.025) 1px, transparent 1px),
                linear-gradient(90deg, rgba(0,255,65,0.025) 1px, transparent 1px);
            background-size: 35px 35px;
        }

        .container {
            width: 92%;
            max-width: 1000px;
            margin: auto;
            padding: 25px 0 50px;
        }

        .top-header {
            text-align: center;
            padding: 20px 0 18px;
            margin-bottom: 30px;
            border-bottom: 1px solid #00ff41;
            box-shadow: 0 5px 20px rgba(0,255,65,0.08);
        }

        .name {
            font-size: 32px;
            font-weight: bold;
            letter-spacing: 8px;
            color: #00ff41;
            text-shadow:
                0 0 5px #00ff41,
                0 0 15px #00ff41;
        }

        .role {
            margin-top: 8px;
            color: #888;
            font-size: 12px;
            letter-spacing: 4px;
        }

        .title-box {
            text-align: center;
            margin-bottom: 30px;
        }

        .title {
            font-size: 38px;
            font-weight: bold;
            letter-spacing: 5px;
            text-shadow:
                0 0 5px #00ff41,
                0 0 15px #00ff41;
        }

        .status {
            margin-top: 10px;
            color: #00ff41;
            font-size: 13px;
        }

        .dot {
            display: inline-block;
            width: 9px;
            height: 9px;
            background: #00ff41;
            border-radius: 50%;
            margin-right: 7px;
            box-shadow: 0 0 10px #00ff41;
        }

        .card {
            background: rgba(0, 15, 5, 0.92);
            border: 1px solid #00ff41;
            padding: 30px;
            box-shadow:
                0 0 20px rgba(0,255,65,0.08),
                inset 0 0 20px rgba(0,255,65,0.025);
        }

        .terminal-line {
            color: #888;
            margin-bottom: 18px;
            font-size: 14px;
        }

        .prompt {
            color: #00ff41;
        }

        .form {
            display: flex;
            gap: 12px;
        }

        input {
            flex: 1;
            background: #000;
            border: 1px solid #00ff41;
            color: #00ff41;
            padding: 15px;
            font-family: inherit;
            font-size: 16px;
            outline: none;
        }

        input::placeholder {
            color: #386b43;
        }

        input:focus {
            box-shadow: 0 0 15px rgba(0,255,65,0.25);
        }

        button {
            background: #00ff41;
            color: #000;
            border: none;
            padding: 0 28px;
            font-family: inherit;
            font-weight: bold;
            cursor: pointer;
            transition: 0.2s;
        }

        button:hover {
            background: #8aff9f;
            box-shadow: 0 0 20px rgba(0,255,65,0.6);
        }

        .error {
            margin-top: 25px;
            padding: 15px;
            border: 1px solid #ff3333;
            color: #ff5555;
            background: rgba(255,0,0,0.05);
        }

        .result {
            margin-top: 30px;
        }

        .result-title {
            color: #888;
            font-size: 13px;
            margin-bottom: 15px;
            border-bottom: 1px solid #173d20;
            padding-bottom: 10px;
        }

        .grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 12px;
        }

        .item {
            border: 1px solid #174d24;
            background: #020a04;
            padding: 18px;
        }

        .label {
            color: #777;
            font-size: 11px;
            margin-bottom: 8px;
            text-transform: uppercase;
        }

        .value {
            color: #00ff41;
            font-size: 18px;
            font-weight: bold;
            word-break: break-word;
        }

        .class-value {
            font-size: 30px;
            text-shadow: 0 0 10px #00ff41;
        }

        .footer {
            text-align: center;
            margin-top: 35px;
            color: #555;
            font-size: 11px;
            letter-spacing: 2px;
        }

        .footer span {
            color: #00ff41;
        }

        @media (max-width: 650px) {
            .name {
                font-size: 23px;
                letter-spacing: 5px;
            }

            .title {
                font-size: 25px;
            }

            .form {
                flex-direction: column;
            }

            button {
                padding: 15px;
            }

            .grid {
                grid-template-columns: 1fr;
            }

            .card {
                padding: 20px;
            }
        }
    </style>
</head>

<body>

<div class="container">

    <div class="top-header">
        <div class="name">ANUP VERMA</div>
        <div class="role">NETWORK • LINUX • SECURITY</div>
    </div>

    <div class="title-box">
        <div class="title">IP CLASS FINDER</div>

        <div class="status">
            <span class="dot"></span>
            SYSTEM ONLINE // NETWORK ANALYZER
        </div>
    </div>

    <div class="card">

        <div class="terminal-line">
            <span class="prompt">root@anup:~$</span>
            enter IPv4 address for analysis
        </div>

        <form class="form" method="GET">

            <input
                type="text"
                name="ip"
                value="{{ ip }}"
                placeholder="Example: 192.168.1.10"
                autocomplete="off"
                required
            >

            <button type="submit">
                ANALYZE
            </button>

        </form>

        {% if error %}
        <div class="error">
            [ERROR] {{ error }}
        </div>
        {% endif %}

        {% if result %}

        <div class="result">

            <div class="result-title">
                // ANALYSIS RESULT
            </div>

            <div class="grid">

                <div class="item">
                    <div class="label">IP Address</div>
                    <div class="value">{{ result.ip }}</div>
                </div>

                <div class="item">
                    <div class="label">IP Class</div>
                    <div class="value class-value">
                        {{ result.ip_class }}
                    </div>
                </div>

                <div class="item">
                    <div class="label">Subnet Mask</div>
                    <div class="value">
                        {{ result.subnet }}
                    </div>
                </div>

                <div class="item">
                    <div class="label">CIDR</div>
                    <div class="value">
                        {{ result.cidr }}
                    </div>
                </div>

                <div class="item">
                    <div class="label">Network Address</div>
                    <div class="value">
                        {{ result.network }}
                    </div>
                </div>

                <div class="item">
                    <div class="label">Broadcast Address</div>
                    <div class="value">
                        {{ result.broadcast }}
                    </div>
                </div>

            </div>
        </div>

        {% endif %}

    </div>

    <div class="footer">
        DEVELOPED BY <span>ANUP VERMA</span>
        // IP NETWORK ANALYSIS TOOL
    </div>

</div>

</body>
</html>
"""


def analyze_ip(ip_input):

    ip_obj = ipaddress.IPv4Address(ip_input)
    first_octet = int(str(ip_obj).split(".")[0])

    if 1 <= first_octet <= 126:

        ip_class = "CLASS A"
        subnet = "255.0.0.0"
        cidr = "/8"

        network = ipaddress.IPv4Network(
            f"{ip_obj}/8",
            strict=False
        )

    elif first_octet == 127:

        ip_class = "LOOPBACK"
        subnet = "N/A"
        cidr = "127.0.0.0/8"

        network = ipaddress.IPv4Network("127.0.0.0/8")

    elif 128 <= first_octet <= 191:

        ip_class = "CLASS B"
        subnet = "255.255.0.0"
        cidr = "/16"

        network = ipaddress.IPv4Network(
            f"{ip_obj}/16",
            strict=False
        )

    elif 192 <= first_octet <= 223:

        ip_class = "CLASS C"
        subnet = "255.255.255.0"
        cidr = "/24"

        network = ipaddress.IPv4Network(
            f"{ip_obj}/24",
            strict=False
        )

    elif 224 <= first_octet <= 239:

        ip_class = "CLASS D"
        subnet = "N/A"
        cidr = "N/A"
        network = None

    elif 240 <= first_octet <= 255:

        ip_class = "CLASS E"
        subnet = "N/A"
        cidr = "N/A"
        network = None

    else:

        ip_class = "RESERVED"
        subnet = "N/A"
        cidr = "N/A"
        network = None

    if network:
        network_address = str(network.network_address)
        broadcast_address = str(network.broadcast_address)
    else:
        network_address = "N/A"
        broadcast_address = "N/A"

    return {
        "ip": str(ip_obj),
        "ip_class": ip_class,
        "subnet": subnet,
        "cidr": cidr,
        "network": network_address,
        "broadcast": broadcast_address
    }


@app.route("/", methods=["GET"])
def home():

    ip = request.args.get("ip", "").strip()

    result = None
    error = None

    if ip:
        try:
            result = analyze_ip(ip)
        except ValueError:
            error = "Invalid IPv4 address. Example: 192.168.1.10"

    return render_template_string(
        HTML,
        ip=ip,
        result=result,
        error=error
    )


if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000
    )
