import isEqual from './isEqual.js';

/**
 * Returns whether or not the given array contains a value equal to the given value.
 * @param array array to search from
 * @param value value to search
 * @param depth maximum recursive comparison depth
 */
function includes<T>(array: T[], value: unknown, depth?: number): value is T;
function includes<T>(array: T[], value: T, depth?: number): boolean {
  if (value != null) {
    const type = typeof value;
    if (type === 'number' || type === 'boolean' || type === 'string' || type === 'symbol') {
      return array.indexOf(value) >= 0;
    }
  }
  return array.some((val) => isEqual(val, value, depth));
}

export default includes;
