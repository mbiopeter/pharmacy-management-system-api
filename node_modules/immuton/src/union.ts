import empty from './empty.js';
import includes from './includes.js';

/**
 * Returns an array of unique items in the all of the given arrays.
 * Each distinct value will only occur once in the returned array.
 * If there is only one non-empty array where all the items are already unique,
 * that array reference is returned.
 */
export default function union<T>(arrays: T[][], depth?: number): T[] {
  if (!arrays.length) {
    return arrays as unknown[] as T[];
  }
  let foundSingle: T[] | undefined;
  let result: T[] | undefined;
  let foundDuplicates = false;
  let foundSingleCount = 0;
  arrays.forEach((array) => {
    let pushedEverything = true;
    array.forEach((value) => {
      if (!result) {
        result = [value];
      } else if (!includes(result, value, depth)) {
        result.push(value);
      } else {
        foundDuplicates = true;
        pushedEverything = false;
      }
    });
    if (pushedEverything && array.length) {
      foundSingle = array;
      foundSingleCount += 1;
    }
  });
  if (!foundDuplicates && foundSingle && foundSingleCount === 1) {
    return foundSingle;
  }
  return result || empty;
}
