# Create app
FROM grafana/grafana:10.3.3

# Maintainer
LABEL maintainer="Andres Eusse <andeusse@gmail.com>"

# Copy plugins and rewrite defaults.ini file to allow loading unsigned plugins
USER root

COPY ./assets/images /usr/share/grafana/public/img/bg/
COPY ./assets/defaultDashboards /var/lib/grafana/dashboards

# Expose port
EXPOSE 3000
