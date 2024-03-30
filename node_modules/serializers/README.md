# Serializers

This package provides type-safe data validation and serialization.

It's perfect to these kind of use cases:

- Safely validate & deserialize data sent to an API
- Serialize data returned by an API
- Validate data on client-side before sending to a server
- Encode/decode URL parameters with safe validation and type coercion

## Usage

Start by installing the library to your project:

```
npm i serializers
```

You start by defining _serializers_ to your project:

```typescript
import { serializer, fields } from 'serializers';

export const productSerializer = serializers({
  id: fields.uuid(),
  name: fields.string(1, 128, true),
  price: fields.decimal(2),
  status: fields.choice(['in-stock', 'out-of-stock', 'coming-soon']),
  createdAt: fields.datetime(),
  updatedAt: fields.datetime(),
  url: fields.url(),
});
```

### Validation

Validate any input data:

```typescript
import { assertValidationError } from 'serializers';
// ...

try {
  const product = productSerializer.validate({
    /* input data */
  });
  console.log('A valid product:', product);
} catch (error) {
  assertValidationError(error);
  console.error(`Not a valid product: ${error.message}`);
}
```

### Deserialization

Example: deserialize a JSON payload to an API server

```typescript
import { assertValidationError } from 'serializers';
// ...

const payload = JSON.parse(request.body);
try {
  const product = productSerializer.deserialize(payload);
  console.log('Received valid product:', product);
} catch (error) {
  assertValidationError(error);
  console.error(`Not a valid product: ${error.message}`);
}
```

### Serialization

When returning a JSON response you can serialize the data so that it's guaranteed to be JSON-encodeable:

```typescript
const product: productSerializer = loadProductDatabase();
return JSON.stringify(productSerializer.serialize(product));
```

### Data type

You may extract the data type of valid data:

```typescript
import { ValueOf } from 'serializers';
// ...

export type Product = ValueOf<typeof productSerializer>;
```

In the above example, the `Product` type equals to:

```typescript
export interface Product {
  id: string;
  name: string;
  price: string;
  status: 'in-stock' | 'out-of-stock' | 'coming-soon';
  createdAt: Date;
  updatedAt: Date;
  url: string;
}
```
