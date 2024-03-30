/* eslint-disable no-restricted-syntax */
import hasOwnProperty from './hasOwnProperty.js';
import isEqual from './isEqual.js';

/**
 * Check that the given object has every matching property of the second object,
 * returning true/false accordingly. The first object may contain additional properties.
 * This is useful for simple filtering. By default the equality is checked with
 * recursive deep check. You may provide depth 0 for a simple equality check.
 *
 * @param obj object whose properties are checked
 * @param values the required values
 * @param depth depth of the equality check
 */
export default function hasProperties<T>(obj: T, values: { [key: string]: unknown }, depth?: number): boolean {
  for (const key in values) {
    if (hasOwnProperty(values, key)) {
      if (!hasOwnProperty(obj, key) || !isEqual(values[key], obj[key], depth)) {
        return false;
      }
    }
  }
  return true;
}
