#!/bin/bash

# * Redistributions in binary form must reproduce the above copyright
#   notice, this list of conditions and the following disclaimer in the
#   documentation and/or other materials provided with the distribution.
# * Neither the name of the axTLS project nor the names of its
#   contributors may be used to endorse or promote products derived
#   from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED
# TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY
# OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF
# THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

#
# Generate the certificates and keys for testing.
#


PROJECT_NAME="ARTEMIS TLS Project"

# Generate the openssl configuration files.
cat > ca_cert.conf << EOF
[ req ]
distinguished_name     = req_distinguished_name
prompt                 = no

[ req_distinguished_name ]
 O                      = $PROJECT_NAME Dodgy Certificate Authority
EOF

cat > server_cert.conf << EOF
[ req ]
distinguished_name     = req_distinguished_name
prompt                 = no

[ req_distinguished_name ]
 O                      = $PROJECT_NAME
 CN                     = 192.168.123.140
EOF

cat > client_cert.conf << EOF
[ req ]
distinguished_name     = req_distinguished_name
prompt                 = no

[ req_distinguished_name ]
 O                      = $PROJECT_NAME Device Certificate
 CN                     = 127.0.0.1
EOF

rm -f -r ca
rm -f -r server
rm -f -r client
rm -f -r certDER
mkdir ca
mkdir server
mkdir client
mkdir certDER

# private key generation
openssl genrsa -out ca.key 2048
openssl genrsa -out server.key 2048
openssl genrsa -out client.key 2048


# cert requests
openssl req -out ca.req -key ca.key -new \
            -config ./ca_cert.conf
openssl req -out server.req -key server.key -new \
            -config ./server_cert.conf
openssl req -out client.req -key client.key -new \
            -config ./client_cert.conf

# generate the actual certs.
openssl x509 -req -in ca.req -out ca.crt \
            -sha1 -days 180 -signkey ca.key
#openssl x509 -req -in server.req -out server.crt \
#            -sha1 -CAcreateserial -days 180 \
#            -CA ca.crt -CAkey ca.key

openssl x509 -req -in server.req \
        -extfile <(printf "subjectAltName=IP:192.168.123.140") \
        -CA ca.crt \
        -CAkey ca.key \
        -CAcreateserial -out server.crt \
        -days 180

openssl x509 -req -in client.req -out client.crt \
        -extfile <(printf "subjectAltName=IP:192.168.123.140") \
            -sha1 -CAcreateserial -days 180 \
            -CA ca.crt -CAkey ca.key

openssl x509 -in ca.crt -outform DER -out ca.der
openssl x509 -in server.crt -outform DER -out server.der
openssl x509 -in client.crt -outform DER -out client.der

echo generate ca key
openssl pkcs12 -export -inkey server.key -in server.crt -name "server" -CAfile ca.crt -password pass:"Fast123456" -out server.pfx
openssl pkcs12 -export -inkey client.key -in client.crt -name "client" -CAfile ca.crt -password pass:"Slow012345" -out client.pfx

echo step1: input server password
keytool -importkeystore -srckeystore server.pfx -srcstoretype PKCS12 -deststoretype JKS -destkeystore server.jks -storepass Fast123456
echo step2: input client password
keytool -importkeystore -srckeystore client.pfx -srcstoretype PKCS12 -deststoretype JKS -destkeystore client.jks -storepass Slow012345
# 将client证书导入到truststore
echo step3: repeat input servertruststore password, password is Fast123456
keytool -import -v -trustcacerts -alias serversslkey -file server.crt -keystore servertruststore.ts
echo step4: repeat input clienttruststore password, password is Slow12345
keytool -import -v -trustcacerts -alias clientsslkey -file client.crt -keystore clienttruststore.ts

mv ca.crt ca.key ca/
mv server.crt server.key server.jks server.pfx servertruststore.ts  server/
mv client.crt client.key client.jks client.pfx clienttruststore.ts  client/

mv ca.der server.der client.der certDER/

rm *.conf
rm *.req
rm *.srl

