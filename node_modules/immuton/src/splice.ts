import empty from './empty.js';

/**
 * Changes an array by removing or replacing existing elements and/or adding new elements.
 * Unlike JavaScript's native `splice` method, this returns a new copy and does not mutate
 * the original array. If the splice operation would result in no changes, then the reference
 * to the original array is returned.
 * @param array array to splice
 * @param start starting index
 * @param deleteCount number of items to remove at the index
 * @param items items to add at the index
 */
function splice<T>(array: T[], start: number, deleteCount: number): T[];
function splice<T>(array: T[], start: number, deleteCount: number, ...items: T[]): T[];
function splice<T>(array: T[], start: number, deleteCount: number, ...items: T[]): T[] {
  if (!array.length && !items.length) {
    return array;
  }
  if ((!deleteCount || !array.length) && !items.length) {
    return array;
  }
  const result = array.slice();
  result.splice(start, deleteCount, ...items);
  return result.length ? result : empty;
}

export default splice;
