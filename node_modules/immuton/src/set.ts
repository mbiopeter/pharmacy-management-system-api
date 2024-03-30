import hasOwnProperty from './hasOwnProperty.js';

/**
 * Returns a copy of the object with the given property name set to the value.
 * If the object already has that value on that property, then returns the original
 * instance, otherwise a new reference is returned.
 * @param object object to copy and set
 * @param prop property name or symbol
 * @param value value to set
 */
function set<T, K extends keyof T>(object: T, prop: K, value: T[K]): T {
  if (hasOwnProperty(object, prop) && object[prop] === value) {
    return object;
  }
  return { ...object, [prop]: value };
}

export default set;
