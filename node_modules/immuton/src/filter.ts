import empty from './empty.js';

/**
 * Filters values from the given array and returns an array
 * only containing the matching items. If all the items match,
 * or if the original array is empty, the original array instance is
 * returned instead of a new reference.
 * @param array array of items to filter
 * @param fn function returing if the item matches or not
 */
function filter<T, U extends T>(arr: T[], fn: (value: T, i: number, arr: T[]) => value is U): U[];
function filter<T>(array: T[], fn: (value: T, index: number, array: T[]) => boolean): T[];
function filter<T>(array: T[], fn: (value: T, index: number, array: T[]) => boolean): T[] {
  let altered = false;
  const result = array.filter((value, index, arr) => {
    const matches = fn(value, index, arr);
    if (!matches) {
      altered = true;
    }
    return matches;
  });
  if (!altered) {
    return array;
  }
  return result.length ? result : empty;
}

export default filter;
