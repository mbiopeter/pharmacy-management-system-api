import filter from './filter.js';

/**
 * Filters values from the given array and returns an array excluding the matching items.
 * If all the items match, or if the original array is empty, the original array instance is
 * returned instead of a new reference.
 * @param array array of items to filter
 * @param fn function returing if the item is excluded or not
 */
function reject<T, U extends T>(arr: T[], fn: (value: T, i: number, arr: T[]) => value is U): Array<Exclude<T, U>>;
function reject<T>(array: T[], fn: (value: T, index: number, array: T[]) => boolean): T[];
function reject<T>(array: T[], fn: (value: T, index: number, array: T[]) => boolean): T[] {
  return filter(array, (value, index, arr) => !fn(value, index, arr));
}

export default reject;
