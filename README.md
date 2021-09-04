# PPM/KPM monitoring draft

## Configuring and running

Create Twitch OAuth token [here](https://twitchapps.com/tmi/) and copy it to *docker-compose.yml*. As well as yours Twitch nickname and selected twitch channel using `#channelname` format.

*Example:*

```yaml
...
TWITCH_TOKEN: 'oauth:pogu252454kekw' # Fake token for example
TWITCH_NICKNAME: 'foobar'
TWITCH_CHANNEL: '#lirik'
```

After that you can run the app using this comand:

`docker-compose up` **Requires [docker-compose](https://docs.docker.com/compose/) installed.*

Prometheus now accesible at [localhost:9090](http://localhost:9090).

## Optional configuration

* You can enable Grafana just by uncommenting these rows and accessing [localhost:3000](http://localhost:3000). It is provisioned and have example vusialization and prometheus datasource.
  * ```yaml
        # Uncomment to enable grafana
        # grafana:
        #   image: grafana/grafana
        #   depends_on:
        #     - prometheus
        #   ports:
        #     - 3000:3000
        #   volumes:
        #     - grafana_data:/var/lib/grafana
        #     - ./grafana/provisioning/:/etc/grafana/provisioning/
        #   env_file:
        #     - ./grafana/config.monitoring
        #   networks:
        #     - ppm-mon
        #   restart: always```
  * User and password `admin:foobar`
