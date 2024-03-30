import empty from './empty.js';

/**
 * Concatenates the arrays given as the parameters.
 * If only one of the arrays is non-empty, then returns a reference to that array.
 * @param arrays arrays to concatenate
 */
export default function concat<T>(...arrays: T[][]): T[] {
  const { length } = arrays;
  let result: T[] | undefined;
  for (let i = 0; i < length; i += 1) {
    const array = arrays[i];
    if (array.length) {
      if (result != null) {
        // More than one non-empty array.
        // Fall back to native flatten.
        return (empty as T[]).concat(...arrays);
      }
      // First non-empty array
      result = array;
    }
  }
  return result || arrays[0] || empty;
}
