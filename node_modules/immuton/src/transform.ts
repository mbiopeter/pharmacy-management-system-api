/* eslint-disable no-restricted-syntax */
import hasOwnProperty from './hasOwnProperty.js';
import isEqual from './isEqual.js';

/**
 * Maps each value for each property of an object to a new value,
 * as returned by the given function that is called for each property.
 * If no property is changed, then the original object reference is returned.
 * @param obj object whose values are mapped
 * @param iterator function that returns new value for each key
 */
function transform<T, R>(
  obj: T,
  iterator: (value: T[string & keyof T], key: string & keyof T) => R,
): { [P in keyof T]: R } {
  let isAltered = false;
  let result: { [P in keyof T]: R } | undefined;
  for (const key in obj) {
    if (hasOwnProperty(obj, key) && typeof key === 'string') {
      const value = obj[key];
      const newValue = iterator(value, key);
      if (result == null) {
        result = {} as { [P in keyof T]: R };
      }
      result[key] = newValue;
      if (!isEqual(value, newValue, 0)) {
        isAltered = true;
      }
    }
  }
  return isAltered ? (result as { [P in keyof T]: R }) : (obj as unknown as { [P in keyof T]: R });
}

export default transform;
