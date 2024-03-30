import set from './set.js';

/**
 * Returns a copy of the object with the given property name set to the value.
 * If the object already has that value on that property, then returns the original
 * instance, otherwise a new reference is returned.
 * @param object object to copy and set
 * @param prop property name or symbol
 * @param value value to set
 */
function editProperty<T, K extends keyof T>(object: T, prop: K, fn: (value: T[K]) => T[K]): T {
  return set(object, prop, fn(object[prop]));
}

export default editProperty;
