FROM emscripten/emsdk:3.1.14
LABEL maintainer "github/scottroot"

RUN apt-get update -qq -y
RUN apt-get install -y curl vim make gcc libreadline6-dev libssl-dev zlib1g-dev zip unzip

ENV LUA_VERSION 5.3.4
ENV LUAROCKS_VERSION 3.11.0

# Intall yaml
RUN pip3 install pyyaml

RUN apt-get update -qq -y
RUN apt-get install -y build-essential clang pkg-config libssl-dev libreadline-dev
RUN apt-get update -qq -y

# Install lua runtime
RUN cd / \
  && curl -L http://www.lua.org/ftp/lua-${LUA_VERSION}.tar.gz | tar xzf - \
  && cd /lua-${LUA_VERSION} \
  && make linux test \
  && make install

# Re-compile Lua to Generic WASM
RUN cd /lua-${LUA_VERSION} && \
  make clean && \
  make generic CC="emcc -s WASM=1 -U LUA_32BITS"

# Install luarocks (if using any rocks)
RUN cd / \
  && curl -L https://luarocks.org/releases/luarocks-${LUAROCKS_VERSION}.tar.gz | tar xzf - \
  && cd /luarocks-${LUAROCKS_VERSION} \
  && ./configure --with-lua-include=/lua-${LUA_VERSION}/src \
  && make build \
  && make install

# Install Rust (if compiling Rust mlua -> wasm)
RUN curl https://sh.rustup.rs -sSf | bash -s -- -y
ENV PATH="/root/.cargo/bin:${PATH}"
RUN rustup toolchain add stable
RUN rustup target add wasm32-unknown-emscripten --toolchain stable
RUN rustup target add wasm32-unknown-unknown --toolchain stable
RUN cargo install wasm-bindgen-cli

# Install commands
COPY ./src/emcc-lua /usr/local/bin/emcc-lua
RUN chmod +x /usr/local/bin/emcc-lua
COPY ./src/emcc_lua_lib /usr/local/emcc-lua/emcc_lua_lib
COPY ./src/main.c /opt/main.c
COPY ./src/main.lua /opt/main.lua

RUN mkdir -p /opt/src
COPY ./src/lua-files-to-include/ /opt/src/


ENV CC 'emcc -s WASM=1'
ENV NM 'llvm-nm'
