import hasOwnProperty from './hasOwnProperty.js';
import type { Propertyless } from './types.js';

function isEmpty(value: unknown[]): value is never[];
function isEmpty(value: { [key: string]: unknown }): value is Propertyless;
function isEmpty(value: unknown[] | { [key: string]: unknown } | Propertyless): boolean;
function isEmpty(value: unknown[] | { [key: string]: unknown } | Propertyless): boolean {
  // eslint-disable-next-line no-restricted-syntax
  for (const prop in value) {
    if (hasOwnProperty(value, prop)) {
      return false;
    }
  }
  return true;
}

export default isEmpty;
