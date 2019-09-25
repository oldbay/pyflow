FROM artifacts.devogip.ru/docker/arm-les/pygdal:latest

# RUN apt-get update
# RUN apt-get install -y nodejs python3-pip curl apt-transport-https
# RUN curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | apt-key add -
# RUN curl -sL https://deb.nodesource.com/setup_10.x | bash -
# RUN echo "deb https://dl.yarnpkg.com/debian/ stable main" | tee /etc/apt/sources.list.d/yarn.list
# RUN apt update && apt install yarn nodejs

RUN apt-get update -qq \
 && apt-get install -y --no-install-recommends build-essential  \
    apt-transport-https curl ca-certificates gnupg2 apt-utils nodejs

# Install node from nodesource
# uncomment the next 2 lines for fix
RUN curl -sL https://deb.nodesource.com/setup_10.x | bash - \
 && apt-get install -y nodejs

# Install yarn
RUN curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | apt-key add - \
 && echo "deb https://dl.yarnpkg.com/debian/ stable main" | tee /etc/apt/sources.list.d/yarn.list \
 && apt-get update -qq \
 && apt-get install -y yarn

WORKDIR /home
COPY src/ pyflow/src/

RUN python3 -m pip install --upgrade pip
RUN pip config --global set global.extra-index-url https://artifacts.devogip.ru/artifactory/api/pypi/geo-pypi/simple
WORKDIR /home/pyflow/src
RUN python3 -m pip install -U flask
WORKDIR /home/pyflow/src/static
RUN yarn install

COPY ./docker/start.sh /home/pyflow
RUN chmod +x /home/pyflow/start.sh

EXPOSE 5000

WORKDIR /home/pyflow
CMD ["./start.sh"]
