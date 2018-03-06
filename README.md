# Simple mock server

This is a simple mock server to provide a server with endpoints configured on a yaml file. Originally built to provide aws endpoints, but can also be used for general purpose.

## Running

### Local

```bash
$ git clone repo
$ sudo pip install pyaml
$ ./src/simple-mock-server.py
```

### Docker

The docker-compose will create the network and the service with the IP `169.254.169.254`. Any docker in the same network will be able to access it without IP/port forwarding. You can still configure the host to forward the IP to the bound port.

```bash
$ docker-compose up
# Without port binding
$ docker-compose -f docker-compose.yml up
```

### Forwarding the ip

To forward the aws ip `169.254.169.254` on linux:

```bash
$ /sbin/ifconfig lo:1 inet 169.254.169.254 netmask 255.255.255.255 up
# Or if host 80 is not available/permited
$ echo 1 > /proc/sys/net/ipv4/ip_forward
$ iptables -t nat -A OUTPUT -p tcp -d 169.254.169.254/32 --dport 80  -j DNAT --to-destination 169.254.169.254:8111
$ service iptables save
```

> Check the script to use on mac.
>
> ```bash
> $ ./config/setup_mac.sh
> ```

## Customization

It comes with AWS ec2 metadata endpoints as sample data. You can create another samples file and set the variable `SAMPLE_PATH`. It will use both samples files replacing the original endpoint contents with your custom file.

> /home/myuser/app/my-sample.yml
```yaml
default:
    /some/endpoint: response data
    /some/other-endpoint:
        content-type: application/json
        content: |
            {
                "key": "value"
            }
```

```bash
$ SAMPLE_PATH=/home/myuser/app/my-sample.yml ./simple-mock-server.py
# With docker compose
$ SAMPLE_PATH=/app/my-sample.yml docker-compose up
```
### Profiles

Use `MOCK_PROFILE` to switch the profiles. You can also use inheritance to reuse the original data and extend/override with your own data.

> /home/myuser/app/my-sample.yml
```yaml
dev: &dev
    <<: *default # To copy all the struct from default samples
    /some/endpoint: dev data
test:
    <<: *dev
    /some/endpoint: test data
```

```bash
MOCK_PROFILE=dev SAMPLE_PATH=/app/my-sample.yml ./simple-mock-server.py
MOCK_PROFILE=test SAMPLE_PATH=/app/my-sample.yml ./simple-mock-server.py
```

> If not defined it will read the first profile even if its name differs from `default` name.

## References

Those references helped me to create this one but are all good solutions. I decide to make my own since one solution is too complicated, and we want something simpler, and another is missing supoort for other endpoints that we need. We also handle better python, so it will be easie to us.

- https://github.com/bpholt/fake-ec2-metadata-service
- https://github.com/NYTimes/mock-ec2-metadata
