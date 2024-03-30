/**
 * Appends the given values to the array, returning a new copy with the items
 * added at the end of the array. If no item parameters are provided, then the
 * reference to the original array is returned.
 * @param array array to splice
 * @param fn function used to transform each item
 */
export default function append<T>(array: T[], ...items: T[]): T[] {
  return items.length ? array.concat(items) : array;
}
