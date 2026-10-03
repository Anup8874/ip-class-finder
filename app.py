from flask import Flask, request, render_template_string
import ipaddress
import math

app = Flask(__name__)


HTML = """
<!DOCTYPE html>
<html lang="en">

<head>

<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<title>Anup Verma | IPv4 Network Analyzer</title>

<style>

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    background: #030603;
    color: #00ff41;
    font-family: "Courier New", monospace;
    min-height: 100vh;
}

body::before {
    content: "";
    position: fixed;
    inset: 0;
    pointer-events: none;

    background:
        linear-gradient(rgba(0,255,65,.025) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0,255,65,.025) 1px, transparent 1px);

    background-size: 35px 35px;
}

.container {
    width: 94%;
    max-width: 1200px;
    margin: auto;
    padding: 25px 0 60px;
}

.header {
    text-align: center;
    padding: 20px 0;
    border-bottom: 1px solid #00ff41;
    margin-bottom: 30px;
}

.name {
    font-size: 32px;
    font-weight: bold;
    letter-spacing: 8px;
    text-shadow: 0 0 15px #00ff41;
}

.role {
    margin-top: 8px;
    color: #777;
    font-size: 12px;
    letter-spacing: 3px;
}

.title {
    text-align: center;
    font-size: 35px;
    letter-spacing: 5px;
    margin-bottom: 8px;
    text-shadow: 0 0 15px #00ff41;
}

.status {
    text-align: center;
    color: #00ff41;
    font-size: 12px;
    margin-bottom: 30px;
}

.dot {
    display: inline-block;
    width: 8px;
    height: 8px;
    background: #00ff41;
    border-radius: 50%;
    margin-right: 6px;
    box-shadow: 0 0 10px #00ff41;
}

.card {
    background: rgba(0,20,5,.85);
    border: 1px solid #00ff41;
    padding: 25px;
    margin-bottom: 25px;
    box-shadow: 0 0 25px rgba(0,255,65,.08);
}

.card-title {
    font-size: 15px;
    color: #00ff41;
    border-bottom: 1px solid #174d24;
    padding-bottom: 12px;
    margin-bottom: 20px;
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
    padding: 14px;
    font-family: inherit;
    font-size: 15px;
    outline: none;
}

input:focus {
    box-shadow: 0 0 15px rgba(0,255,65,.3);
}

button {
    background: #00ff41;
    color: #000;
    border: none;
    padding: 0 25px;
    font-family: inherit;
    font-weight: bold;
    cursor: pointer;
}

button:hover {
    background: #9affb0;
    box-shadow: 0 0 20px #00ff41;
}

.grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 12px;
}

.item {
    border: 1px solid #174d24;
    background: #020902;
    padding: 17px;
}

.label {
    color: #777;
    font-size: 10px;
    margin-bottom: 8px;
    text-transform: uppercase;
}

.value {
    color: #00ff41;
    font-size: 16px;
    font-weight: bold;
    word-break: break-word;
}

.big {
    font-size: 25px;
    text-shadow: 0 0 10px #00ff41;
}

.definition {
    border-left: 3px solid #00ff41;
    background: #020902;
    padding: 15px;
    margin-top: 15px;
    color: #aaa;
    line-height: 1.6;
}

.definition strong {
    color: #00ff41;
}

.binary {
    word-break: break-all;
    line-height: 1.7;
    font-size: 13px;
}

.error {
    border: 1px solid red;
    color: #ff5555;
    padding: 15px;
    margin-top: 20px;
}

table {
    width: 100%;
    border-collapse: collapse;
}

th, td {
    border: 1px solid #174d24;
    padding: 11px;
    text-align: left;
}

th {
    color: #00ff41;
    background: #031006;
}

td {
    color: #aaa;
}

.info-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 12px;
}

.info {
    background: #020902;
    border: 1px solid #174d24;
    padding: 15px;
    color: #aaa;
    line-height: 1.6;
}

.info strong {
    color: #00ff41;
}

.footer {
    text-align: center;
    color: #555;
    font-size: 11px;
    letter-spacing: 2px;
    margin-top: 30px;
}

.footer span {
    color: #00ff41;
}

@media(max-width: 800px) {

    .grid,
    .info-grid {
        grid-template-columns: 1fr;
    }

    .form {
        flex-direction: column;
    }

    button {
        padding: 15px;
    }

    .title {
        font-size: 25px;
    }

    .name {
        font-size: 23px;
    }
}

</style>

</head>


<body>

<div class="container">


<div class="header">

    <div class="name">
        ANUP VERMA
    </div>

    <div class="role">
        NETWORK • LINUX • SECURITY
    </div>

</div>


<div class="title">
    [ IPv4 NETWORK ANALYZER ]
</div>

<div class="status">
    <span class="dot"></span>
    SYSTEM ONLINE // BEGINNER NETWORK TOOL
</div>


<!-- IP ANALYZER -->

<div class="card">

<div class="card-title">
    &gt; IPv4 ADDRESS ANALYZER
</div>

<form method="GET" class="form">

<input
    type="text"
    name="ip"
    value="{{ ip }}"
    placeholder="Enter IPv4 e.g. 192.168.1.10"
    required
>

<input
    type="text"
    name="prefix"
    value="{{ prefix }}"
    placeholder="CIDR optional e.g. 24"
    style="max-width:180px;"
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

</div>


{% if result %}


<!-- BASIC INFORMATION -->

<div class="card">

<div class="card-title">
    &gt; BASIC IP INFORMATION
</div>

<div class="grid">


<div class="item">
<div class="label">IP Address</div>
<div class="value">{{ result.ip }}</div>
</div>


<div class="item">
<div class="label">IP Class</div>
<div class="value big">{{ result.ip_class }}</div>
</div>


<div class="item">
<div class="label">Type</div>
<div class="value">{{ result.type }}</div>
</div>


<div class="item">
<div class="label">Default Mask</div>
<div class="value">{{ result.default_mask }}</div>
</div>


<div class="item">
<div class="label">CIDR</div>
<div class="value">{{ result.cidr }}</div>
</div>


<div class="item">
<div class="label">Network Mask</div>
<div class="value">{{ result.mask }}</div>
</div>


<div class="item">
<div class="label">Network ID</div>
<div class="value">{{ result.network }}</div>
</div>


<div class="item">
<div class="label">Host ID</div>
<div class="value">{{ result.host_id }}</div>
</div>


<div class="item">
<div class="label">Broadcast</div>
<div class="value">{{ result.broadcast }}</div>
</div>


<div class="item">
<div class="label">First Host</div>
<div class="value">{{ result.first_host }}</div>
</div>


<div class="item">
<div class="label">Last Host</div>
<div class="value">{{ result.last_host }}</div>
</div>


<div class="item">
<div class="label">Total Addresses</div>
<div class="value">{{ result.total }}</div>
</div>


<div class="item">
<div class="label">Usable Hosts</div>
<div class="value">{{ result.usable }}</div>
</div>


<div class="item">
<div class="label">IP Visibility</div>
<div class="value">{{ result.visibility }}</div>
</div>


<div class="item">
<div class="label">IP Range</div>
<div class="value">{{ result.range }}</div>
</div>


</div>


<div class="definition">

<strong>Class Definition:</strong><br>

{{ result.definition }}

</div>


<div class="definition">

<strong>Network ID:</strong>
Identifies the network portion of the IP address.<br><br>

<strong>Host ID:</strong>
Identifies a device/host inside that network.<br><br>

<strong>Broadcast:</strong>
Used to communicate with all hosts in a subnet.<br><br>

<strong>Subnet Mask:</strong>
Separates the network portion from the host portion.

</div>

</div>


<!-- BINARY -->

<div class="card">

<div class="card-title">
    &gt; BINARY REPRESENTATION
</div>

<div class="definition binary">

<strong>IP Binary:</strong><br>
{{ result.binary }}

<br><br>

<strong>Subnet Mask Binary:</strong><br>
{{ result.mask_binary }}

</div>

</div>


{% endif %}


<!-- AUTO SUBNET GENERATOR -->

<div class="card">

<div class="card-title">
    &gt; AUTO SUBNET GENERATOR
</div>

<form method="GET" class="form">

<input
    type="text"
    name="subnet_ip"
    placeholder="Network e.g. 192.168.1.0"
>

<input
    type="text"
    name="subnet_prefix"
    placeholder="Current CIDR e.g. 24"
>

<input
    type="text"
    name="subnet_count"
    placeholder="Number of subnets e.g. 4"
>

<button type="submit">
    GENERATE
</button>

</form>


{% if subnet_error %}

<div class="error">
    [ERROR] {{ subnet_error }}
</div>

{% endif %}


{% if subnets %}

<br>

<div class="definition">

<strong>Auto Generated Subnets:</strong>
{{ subnets|length }} subnet(s) generated automatically.

</div>

<br>

<table>

<tr>

<th>#</th>
<th>Network ID</th>
<th>CIDR</th>
<th>First Host</th>
<th>Last Host</th>
<th>Broadcast</th>
<th>Usable Hosts</th>

</tr>


{% for s in subnets %}

<tr>

<td>{{ loop.index }}</td>

<td>{{ s.network }}</td>

<td>{{ s.cidr }}</td>

<td>{{ s.first }}</td>

<td>{{ s.last }}</td>

<td>{{ s.broadcast }}</td>

<td>{{ s.usable }}</td>

</tr>

{% endfor %}

</table>

{% endif %}

</div>


<!-- BEGINNER GUIDE -->

<div class="card">

<div class="card-title">
    &gt; IPv4 CLASS QUICK GUIDE
</div>


<div class="info-grid">


<div class="info">

<strong>CLASS A</strong><br>

Range: 1.0.0.0 – 126.255.255.255<br>

Default Mask: 255.0.0.0<br>

CIDR: /8<br>

Large networks.

</div>


<div class="info">

<strong>CLASS B</strong><br>

Range: 128.0.0.0 – 191.255.255.255<br>

Default Mask: 255.255.0.0<br>

CIDR: /16<br>

Medium networks.

</div>


<div class="info">

<strong>CLASS C</strong><br>

Range: 192.0.0.0 – 223.255.255.255<br>

Default Mask: 255.255.255.0<br>

CIDR: /24<br>

Small networks.

</div>


<div class="info">

<strong>CLASS D</strong><br>

Range: 224.0.0.0 – 239.255.255.255<br>

Used for multicast communication.<br>

Normal host subnetting is not applied.

</div>


<div class="info">

<strong>CLASS E</strong><br>

Range: 240.0.0.0 – 255.255.255.255<br>

Reserved/experimental range.

</div>


<div class="info">

<strong>LOOPBACK</strong><br>

127.0.0.0/8<br>

Used by a computer to communicate with itself.

</div>


</div>

</div>


<div class="footer">

IPv4 NETWORK ANALYSIS TERMINAL //
DEVELOPED BY <span>ANUP VERMA</span>

</div>


</div>

</body>

</html>
"""


def get_class(first):

    if 1 <= first <= 126:
        return "CLASS A"

    if first == 127:
        return "LOOPBACK"

    if 128 <= first <= 191:
        return "CLASS B"

    if 192 <= first <= 223:
        return "CLASS C"

    if 224 <= first <= 239:
        return "CLASS D"

    if 240 <= first <= 255:
        return "CLASS E"

    return "RESERVED"


def class_details(ip_class):

    data = {

        "CLASS A": {
            "mask": "255.0.0.0",
            "prefix": 8,
            "definition":
                "Class A was designed for very large networks. "
                "The first octet identifies the network and the remaining "
                "three octets are available for hosts."
        },

        "CLASS B": {
            "mask": "255.255.0.0",
            "prefix": 16,
            "definition":
                "Class B was designed for medium-sized networks. "
                "The first two octets identify the network and the last "
                "two octets identify hosts."
        },

        "CLASS C": {
            "mask": "255.255.255.0",
            "prefix": 24,
            "definition":
                "Class C was designed for smaller networks. "
                "The first three octets identify the network and the "
                "last octet identifies hosts."
        },

        "CLASS D": {
            "mask": "N/A",
            "prefix": None,
            "definition":
                "Class D addresses are used for multicast communication."
        },

        "CLASS E": {
            "mask": "N/A",
            "prefix": None,
            "definition":
                "Class E addresses are reserved for experimental or future use."
        },

        "LOOPBACK": {
            "mask": "255.0.0.0",
            "prefix": 8,
            "definition":
                "127.0.0.0/8 is the IPv4 loopback range. "
                "It is used by a computer to communicate with itself."
        }

    }

    return data.get(ip_class, {
        "mask": "N/A",
        "prefix": None,
        "definition": "Reserved IPv4 range."
    })


def make_host_id(ip, prefix):

    ip_int = int(ip)

    host_bits = 32 - prefix

    if host_bits <= 0:
        return "N/A"

    host_mask = (1 << host_bits) - 1

    host_value = ip_int & host_mask

    octets = []

    for shift in [24, 16, 8, 0]:

        value = (host_value >> shift) & 255
        octets.append(str(value))

    return ".".join(octets)


def analyze(ip_text, custom_prefix):

    ip = ipaddress.IPv4Address(ip_text)

    first = int(str(ip).split(".")[0])

    ip_class = get_class(first)

    details = class_details(ip_class)

    if custom_prefix:

        prefix = int(custom_prefix)

        if prefix < 0 or prefix > 32:
            raise ValueError("CIDR prefix must be between 0 and 32.")

    else:

        prefix = details["prefix"]

    if prefix is None:

        return {

            "ip": str(ip),
            "ip_class": ip_class,
            "type": "Multicast / Reserved",
            "default_mask": details["mask"],
            "cidr": "N/A",
            "mask": "N/A",
            "network": "N/A",
            "host_id": "N/A",
            "broadcast": "N/A",
            "first_host": "N/A",
            "last_host": "N/A",
            "total": "N/A",
            "usable": "N/A",
            "visibility": "N/A",
            "range": "N/A",
            "binary": ".".join(
                format(int(x), "08b")
                for x in str(ip).split(".")
            ),
            "mask_binary": "N/A",
            "definition": details["definition"]

        }


    network = ipaddress.IPv4Network(
        f"{ip}/{prefix}",
        strict=False
    )

    mask = network.netmask

    total = network.num_addresses

    if prefix <= 30:

        usable = total - 2

        first_host = network.network_address + 1

        last_host = network.broadcast_address - 1

    else:

        usable = 0

        first_host = "N/A"

        last_host = "N/A"


    if ip.is_private:

        visibility = "PRIVATE"

    elif ip.is_loopback:

        visibility = "LOOPBACK"

    elif ip.is_multicast:

        visibility = "MULTICAST"

    else:

        visibility = "PUBLIC"


    binary_ip = ".".join(
        format(int(x), "08b")
        for x in str(ip).split(".")
    )

    binary_mask = ".".join(
        format(int(x), "08b")
        for x in str(mask).split(".")
    )


    return {

        "ip": str(ip),

        "ip_class": ip_class,

        "type": visibility,

        "default_mask": details["mask"],

        "cidr": f"/{prefix}",

        "mask": str(mask),

        "network": str(network.network_address),

        "host_id": make_host_id(ip, prefix),

        "broadcast": str(network.broadcast_address),

        "first_host": str(first_host),

        "last_host": str(last_host),

        "total": total,

        "usable": usable,

        "visibility": visibility,

        "range":
            f"{network.network_address} - "
            f"{network.broadcast_address}",

        "binary": binary_ip,

        "mask_binary": binary_mask,

        "definition": details["definition"]

    }


def generate_subnets(ip_text, prefix_text, count_text):

    ip = ipaddress.IPv4Address(ip_text)

    prefix = int(prefix_text)

    count = int(count_text)

    if prefix < 0 or prefix > 30:

        raise ValueError(
            "Current CIDR must be between /0 and /30."
        )

    if count < 1:

        raise ValueError(
            "Number of subnets must be at least 1."
        )

    base = ipaddress.IPv4Network(
        f"{ip}/{prefix}",
        strict=False
    )

    required_bits = math.ceil(math.log2(count))

    new_prefix = prefix + required_bits

    if new_prefix > 30:

        raise ValueError(
            "Too many subnets for the selected network."
        )

    all_subnets = list(
        base.subnets(new_prefix=new_prefix)
    )

    selected = all_subnets[:count]

    output = []

    for subnet in selected:

        total = subnet.num_addresses

        usable = total - 2

        first = subnet.network_address + 1

        last = subnet.broadcast_address - 1

        output.append({

            "network":
                str(subnet.network_address),

            "cidr":
                f"/{new_prefix}",

            "first":
                str(first),

            "last":
                str(last),

            "broadcast":
                str(subnet.broadcast_address),

            "usable":
                usable

        })

    return output


@app.route("/", methods=["GET"])
def home():

    ip = request.args.get("ip", "").strip()

    prefix = request.args.get("prefix", "").strip()

    subnet_ip = request.args.get(
        "subnet_ip", ""
    ).strip()

    subnet_prefix = request.args.get(
        "subnet_prefix", ""
    ).strip()

    subnet_count = request.args.get(
        "subnet_count", ""
    ).strip()


    result = None

    error = None

    subnets = None

    subnet_error = None


    # IP ANALYZER

    if ip:

        try:

            result = analyze(
                ip,
                prefix
            )

        except ValueError as e:

            error = str(e)


    # SUBNET GENERATOR

    if subnet_ip and subnet_prefix and subnet_count:

        try:

            subnets = generate_subnets(
                subnet_ip,
                subnet_prefix,
                subnet_count
            )

        except ValueError as e:

            subnet_error = str(e)


    return render_template_string(

        HTML,

        ip=ip,

        prefix=prefix,

        result=result,

        error=error,

        subnets=subnets,

        subnet_error=subnet_error

    )


if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000
    )
