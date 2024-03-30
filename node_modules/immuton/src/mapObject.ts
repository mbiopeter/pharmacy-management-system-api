/* eslint-disable no-restricted-syntax */
import empty from './empty.js';
import hasOwnProperty from './hasOwnProperty.js';

/**
 * Converts an object to an array of items by calling the given
 * iterator function for each property name and the corresponding value,
 * constructing an array from the returned values.
 * @param obj Object whose values are mapped
 * @param iterator Function that returns new value for each key
 */
export default function mapObject<T, R>(
  obj: T,
  iterator: (value: T[string & keyof T], key: string & keyof T) => R,
): R[] {
  let result: R[] | undefined;
  for (const key in obj) {
    if (hasOwnProperty(obj, key) && typeof key === 'string') {
      const value = obj[key];
      const item = iterator(value, key);
      if (result) {
        result.push(item);
      } else {
        result = [item];
      }
    }
  }
  return result || empty;
}
