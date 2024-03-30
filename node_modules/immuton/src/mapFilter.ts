import empty from './empty.js';
import isEqual from './isEqual.js';

/**
 * Transforms every value in the array using the given function and returns an array
 * with the transformed values. If the function does not return a value, or returns
 * undefined, then the value will be omitted from the final array.
 *
 * If every transformed value are the same than the original values and no values
 * were filtered out, or if the original array is empty, the original array instance
 * is returned instead of a new reference.
 * @param array array of values to transform or filter
 * @param fn function to determine the transformed value, or undefined
 */
function mapFilter<T, U>(array: T[], fn: (value: T, index: number) => U | undefined | void): U[] {
  let altered = false;
  let result: U[] | undefined;
  array.forEach((value, index) => {
    const transformed = fn(value, index);
    if (typeof transformed === 'undefined') {
      altered = true;
    } else {
      if (result == null) {
        // First included item
        result = [transformed];
      } else {
        // Latter included item
        result.push(transformed);
      }
      if (!isEqual(transformed, value, 0)) {
        altered = true;
      }
    }
  });
  if (!altered) {
    return array as unknown[] as U[];
  }
  return result || empty;
}

export default mapFilter;
