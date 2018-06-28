# Uplink + Protocol Buffers
[![Build Status](https://travis-ci.org/prkumar/uplink-protobuf.svg?branch=master)](https://travis-ci.org/prkumar/uplink-protobuf)
[![codecov](https://codecov.io/gh/prkumar/uplink-protobuf/branch/master/graph/badge.svg)](https://codecov.io/gh/prkumar/uplink-protobuf)
[![Maintainability](https://api.codeclimate.com/v1/badges/65d2d66958c6e20a3bb0/maintainability)](https://codeclimate.com/github/prkumar/uplink-protobuf/maintainability)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

`uplink-protobuf` makes it easy to send and receive protobuf messages over HTTP.

This library is an [Uplink](https://github.com/prkumar/uplink) plugin.

## Table of Contents

- **[Installation](#installation)**
- **[Basic Usage](#basic-usage)**
    * **[Receiving Protobuf Messages](#receiving-protobuf-messages)**
    * **[Sending Protobuf Messages](#sending-protobuf-messages)**
- **[Communicating with a JSON API](#communicating-with-a-json-api)**
    * **[Converting JSON Responses into Protobuf Messages](#converting-json-responses-into-protobuf-messages)**
    * **[Converting Protobuf Messages into JSON Requests](#converting-protobuf-messages-into-json-requests)**
    * **[JSON Options](#json-options)**
- **[FAQs](#faqs)**

## Installation

```
$ pip install uplink-protobuf
```

## Basic Usage

### Receiving Protobuf Messages

For any `Consumer` method that is expecting a protobuf encoded response,
simply set the appropriate protobuf message type as the method's [return
value annotation](https://www.python.org/dev/peps/pep-3107/#return-values):

```python
from uplink import Consumer, get

# Import Python code generated by Google's protobuf compiler:
from addressbook_pb2.py import Person

class AddressBookClient(Consumer):
    @get("/persons/{person_id}")
    def get_person(self, id) -> Person:
        pass
```

Then when invoked, the annotated method will appropriately decode the
response into the specified message type:

```python
>>> addressbook_client = AddressBookClient(base_url=BASE_URL)
>>> addressbook_client.get_person(1234)
name: "Haley Arganbright"
id: 1234
email: "haley.arganbright@example.com"
phones {
  number: "555-4321"
  type: HOME
}
```

### Sending Protobuf Messages

For a `Consumer` method that needs to send a protobuf encoded request,
simply annotate the appropriate method argument with [`uplink.Body`](https://uplink.readthedocs.io/en/stable/quickstart.html#request-body):

```python
from uplink import Consumer, post, Body

# Import Python code generated by Google's protobuf compiler:
from addressbook_pb2.py import Person

class AddressBookClient(Consumer):
    @post("/persons")
    def create_person(self, person: Body(type=Person)):
        pass
```

Then when the method is invoked, the value of the annotated argument is
automatically encoded:

```python
# Register new person:
person = Person()
person.name = "Susie Morales"
person.id = 5678
person.email = "susie.morales@example.com"

# Send person to API:
addressbook_client = AddressBookClient(base_url=BASE_URL)
addressbook_client.create_person(person)
```

## Communicating with a JSON API

This library also supports converting JSON responses and requests
to and from protobuf messages.

### Converting JSON Responses into Protobuf Messages

`uplink-protobuf` can automatically convert JSON responses into
protobuf messages if the `Consumer` method is annotated with
`returns.from_json`:

```python
from uplink import Consumer, get, returns

# Import Python code generated by Google's protobuf compiler:
from addressbook_pb2.py import Person

class AddressBookClient(Consumer):
    @returns.from_json
    @get("/persons/{person_id}")
    def get_person(self, id) -> Person:
        pass
```

### Converting Protobuf Messages into JSON Requests

`uplink-protobuf` can automatically convert a protobuf message into
JSON request body if the `Consumer` method is annotated with
`uplink.json`:

```python
from uplink import Consumer, post, Body, json

# Import Python code generated by Google's protobuf compiler:
from addressbook_pb2.py import Person

class AddressBookClient(Consumer):
    @json
    @post("/persons")
    def create_person(self, person: Body(type=Person)):
        pass
```

### JSON Options

There are also a few decorators we provide that allows you to control
the conversion. These decorators are available through the
`uplink_protobuf.json_options` submodule.

Here are options that can be used with `@returns.json`, to control
the conversion of JSON objects to protobuf messages:

- `json_options.include_default_value_fields`: This decorator
  indicates that JSON output should include fields with their default
  values.By default, default values are omitted if the field is not set.
- `json_options.preserve_proto_field_names`: This decorator indicates
  that the JSON output should use the proto field name as the JSON name.
  By default, the JSON printer converts the proto field names to
  lowerCamelCase and uses that as the JSON name.
- `json_options.use_integers_for_enums`: This decorator indicates that
  the JSON output should use the numerical value of a proto enum value,
  instead of the name of the enum value. By default, the name of an
  enum value is used in the JSON output.

Next, here are options that can be used with `@json`, to control
the conversion of protobuf messages to JSON objects:

- `json_options.ignore_unknown_fields`: This decorator indicates
  that the JSON parser should ignore unknown fields in parsing.
  By default, the JSON parser raises an error if it encounters
  an unknown field.


```python
from uplink import Consumer, post, Body
from uplink_protobuf import json_options

# Import Python code generated by Google's protobuf compiler:
from addressbook_pb2.py import Person

class AddressBookClient(Consumer):
    @json
    @returns.json
    @json_options.include_default_value_fields
    @json_options.ignore_unknown_fields
    @post("/persons")
    def create_person(self, person: Body(type=Person)):
        pass
```

## FAQs

- **What is Protocol Buffers?**

    Checkout Google's official Protocol Buffers [Developer Guide](https://developers.google.com/protocol-buffers/docs/overview).

- **How do I install Google's protobuf compiler, `protoc`?**

   Checkout [this guide](http://google.github.io/proto-lens/installing-protoc.html) for installation instructions with Mac
   and Linux.

- **How do compile my `.proto` file using `protoc`?**

    Refer to [this section](https://developers.google.com/protocol-buffers/docs/reference/python-generated#invocation)
    in the offical Protocol Buffers Developer Guide.

- **What is Uplink?**

  It's a "Declarative HTTP Client". Checkout the library's [GitHub repo](https://github.com/prkumar/uplink)
  for more.
